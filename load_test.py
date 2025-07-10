import json
import time
import requests
import concurrent.futures
from typing import List, Dict, Any, Optional
import statistics
from sklearn.datasets import fetch_20newsgroups
import argparse

def generate_test_data(sizes: List[int]) -> Dict[int, Dict[str, Any]]:
    """
    Generate test data of different sizes for load testing.
    
    Args:
        sizes: List of document counts to generate
        
    Returns:
        Dictionary mapping size to test data
    """
    print("Loading 20 newsgroups dataset...")
    newsgroups = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))
    docs = newsgroups.data
    
    test_data = {}
    
    for size in sizes:
        # Take the first 'size' documents, or all if size is larger than available
        sample_docs = docs[:min(size, len(docs))]
        test_data[size] = {
            "input": {
                "sentences": sample_docs
            }
        }
        print(f"Generated test data with {len(sample_docs)} documents")
    
    return test_data

def send_request(url: str, data: Dict[str, Any], api_key: Optional[str] = None, timeout: int = 300) -> Dict[str, Any]:
    """
    Send a single request to the RunPod handler.
    
    Args:
        url: RunPod endpoint URL
        data: Request payload
        api_key: RunPod API key for authentication
        timeout: Request timeout in seconds
        
    Returns:
        Response data and timing information
    """
    start_time = time.time()
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=timeout)
        end_time = time.time()
        
        return {
            "status_code": response.status_code,
            "response_time": end_time - start_time,
            "success": response.status_code == 200,
            "response_size": len(response.content) if response.content else 0,
            "error": None
        }
    except requests.exceptions.Timeout:
        return {
            "status_code": None,
            "response_time": timeout,
            "success": False,
            "response_size": 0,
            "error": "Timeout"
        }
    except Exception as e:
        return {
            "status_code": None,
            "response_time": time.time() - start_time,
            "success": False,
            "response_size": 0,
            "error": str(e)
        }

def run_load_test(url: str, data: Dict[str, Any], api_key: Optional[str] = None, num_requests: int = 1, concurrent: int = 1) -> Dict[str, Any]:
    """
    Run load test with specified parameters.
    
    Args:
        url: RunPod endpoint URL
        data: Test data to send
        api_key: RunPod API key for authentication
        num_requests: Number of requests to send
        concurrent: Number of concurrent requests
        
    Returns:
        Test results with timing statistics
    """
    print(f"Running load test: {num_requests} requests, {concurrent} concurrent")
    
    results = []
    
    if concurrent == 1:
        # Sequential requests
        for i in range(num_requests):
            print(f"Request {i+1}/{num_requests}")
            result = send_request(url, data, api_key)
            results.append(result)
    else:
        # Concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent) as executor:
            futures = [executor.submit(send_request, url, data, api_key) for _ in range(num_requests)]
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                print(f"Completed request {i+1}/{num_requests}")
                results.append(future.result())
    
    # Calculate statistics
    successful_requests = [r for r in results if r["success"]]
    failed_requests = [r for r in results if not r["success"]]
    
    if successful_requests:
        response_times = [r["response_time"] for r in successful_requests]
        stats = {
            "total_requests": len(results),
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate": len(successful_requests) / len(results),
            "avg_response_time": statistics.mean(response_times),
            "min_response_time": min(response_times),
            "max_response_time": max(response_times),
            "median_response_time": statistics.median(response_times),
            "std_response_time": statistics.stdev(response_times) if len(response_times) > 1 else 0,
            "avg_response_size": statistics.mean([r["response_size"] for r in successful_requests]),
            "errors": [r["error"] for r in failed_requests if r["error"]]
        }
    else:
        stats = {
            "total_requests": len(results),
            "successful_requests": 0,
            "failed_requests": len(results),
            "success_rate": 0,
            "avg_response_time": 0,
            "min_response_time": 0,
            "max_response_time": 0,
            "median_response_time": 0,
            "std_response_time": 0,
            "avg_response_size": 0,
            "errors": [r["error"] for r in failed_requests if r["error"]]
        }
    
    return stats

def main():
    parser = argparse.ArgumentParser(description='Load test RunPod BERTopic handler')
    parser.add_argument('--url', required=True, help='RunPod endpoint URL')
    parser.add_argument('--api-key', help='RunPod API key for authentication')
    parser.add_argument('--sizes', nargs='+', type=int, default=[100, 1000, 10000], 
                       help='Document sizes to test')
    parser.add_argument('--requests', type=int, default=3, help='Number of requests per size')
    parser.add_argument('--concurrent', type=int, default=1, help='Number of concurrent requests')
    parser.add_argument('--output', default='load_test_results.json', help='Output file for results')
    
    args = parser.parse_args()
    
    print("Generating test data...")
    test_data = generate_test_data(args.sizes)
    
    all_results = {}
    
    for size in args.sizes:
        print(f"\n{'='*50}")
        print(f"Testing with {size} documents")
        print(f"{'='*50}")
        
        data = test_data[size]
        print(f"Data size: {len(json.dumps(data))} bytes")
        
        results = run_load_test(args.url, data, args.api_key, args.requests, args.concurrent)
        all_results[size] = results
        
        print(f"\nResults for {size} documents:")
        print(f"  Success Rate: {results['success_rate']:.2%}")
        print(f"  Avg Response Time: {results['avg_response_time']:.2f}s")
        print(f"  Min Response Time: {results['min_response_time']:.2f}s")
        print(f"  Max Response Time: {results['max_response_time']:.2f}s")
        print(f"  Median Response Time: {results['median_response_time']:.2f}s")
        print(f"  Std Response Time: {results['std_response_time']:.2f}s")
        print(f"  Avg Response Size: {results['avg_response_size']:.0f} bytes")
        
        if results['errors']:
            print(f"  Errors: {results['errors']}")
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nResults saved to {args.output}")
    
    # Print summary
    print(f"\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")
    for size, results in all_results.items():
        print(f"{size} docs: {results['success_rate']:.2%} success, "
              f"{results['avg_response_time']:.2f}s avg, "
              f"{results['max_response_time']:.2f}s max")

if __name__ == "__main__":
    main() 