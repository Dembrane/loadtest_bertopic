#!/usr/bin/env python3
"""
Example usage of the load testing tools for RunPod BERTopic handler.

This script demonstrates how to use the load testing tools with different configurations.
"""

import subprocess
import sys
import os

def run_example():
    """Run example load tests with different configurations."""
    
    # Example RunPod URL (replace with your actual endpoint)
    example_url = "https://your-runpod-endpoint.runpod.net"
    
    print("RunPod BERTopic Load Testing Examples")
    print("=" * 50)
    print()
    
    print("1. Generate test files first:")
    print("   python generate_test_files.py")
    print()
    
    print("2. Simple curl test:")
    print(f"   ./test_with_curl.sh '{example_url}'")
    print(f"   ./test_with_curl.sh '{example_url}' 'your-api-key-here'")
    print()
    
    print("3. Python load test with default settings:")
    print(f"   python load_test.py --url '{example_url}'")
    print(f"   python load_test.py --url '{example_url}' --api-key 'your-api-key-here'")
    print()
    
    print("4. Python load test with custom settings:")
    print(f"   python load_test.py --url '{example_url}' --sizes 100 1000 --requests 5 --concurrent 2")
    print(f"   python load_test.py --url '{example_url}' --api-key 'your-api-key-here' --sizes 100 1000 --requests 5 --concurrent 2")
    print()
    
    print("5. Test with larger dataset (be careful with timeouts):")
    print(f"   python load_test.py --url '{example_url}' --sizes 100 1000 10000 --requests 3 --concurrent 1")
    print()
    
    print("6. Manual curl test with specific file:")
    print(f"   curl -X POST -H 'Content-Type: application/json' -d @test_input_1000.json '{example_url}'")
    print(f"   curl -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer your-api-key-here' -d @test_input_1000.json '{example_url}'")
    print()
    
    print("Expected Performance:")
    print("- 100 documents: ~30-90 seconds (including polling)")
    print("- 1,000 documents: ~2-5 minutes (including polling)")
    print("- 10,000 documents: ~5-15 minutes (including polling)")
    print("- 100,000 documents: ~15-60 minutes (including polling)")
    print()
    
    print("Input Format:")
    print("- num_docs: Number of documents to process")
    print("- num_topics: Number of topics to reduce to (default: 10)")
    print("- random_seed: Random seed for reproducibility (default: 42)")
    print()
    
    print("Async API Notes:")
    print("- Jobs are submitted immediately and return a job ID")
    print("- Status is polled every 30 seconds until completion")
    print("- Dataset is downloaded within the handler to avoid payload limits")
    print("- Larger datasets may take longer due to processing time")
    print()
    
    print("Tips:")
    print("- Start with smaller sizes to test connectivity")
    print("- Monitor your RunPod instance resources during testing")
    print("- Check the generated JSON files before sending large requests")
    print("- Use the --output flag to save results for analysis")
    print("- Increase timeout for larger datasets")
    print("- Jobs may queue if multiple requests are sent simultaneously")

if __name__ == "__main__":
    run_example() 