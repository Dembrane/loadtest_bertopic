#!/usr/bin/env python3
"""
Debug script to test RunPod API URL formats.
"""

import requests
import json
import sys

def test_url_formats(endpoint_url, api_key=None):
    """Test different URL formats to find the correct one."""
    
    print(f"Testing endpoint: {endpoint_url}")
    print(f"API Key provided: {'Yes' if api_key else 'No'}")
    print("=" * 60)
    
    # Extract different possible base URLs
    possible_urls = []
    
    if "/run" in endpoint_url:
        # Format: https://api.runpod.ai/v2/{endpoint_id}/run
        base_url = endpoint_url.replace("/run", "")
        possible_urls.append(("Base URL (remove /run)", base_url))
        possible_urls.append(("API v2 format", f"https://api.runpod.ai/v2/{endpoint_url.split('/')[-2]}"))
    else:
        possible_urls.append(("Original URL", endpoint_url.rstrip("/")))
    
    # Test each URL format
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    for name, url in possible_urls:
        print(f"\nTesting {name}: {url}")
        
        # Test a simple GET request to see if the endpoint exists
        try:
            response = requests.get(f"{url}/status/test", headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            if response.status_code == 404:
                print(f"  Response: {response.text[:200]}...")
            elif response.status_code == 401:
                print("  Response: Unauthorized (check API key)")
            elif response.status_code == 200:
                print("  Response: Success!")
            else:
                print(f"  Response: {response.text[:200]}...")
        except Exception as e:
            print(f"  Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Recommendations:")
    print("1. If you see 401 errors, check your API key")
    print("2. If you see 404 errors, the URL format might be wrong")
    print("3. If you see 200 responses, that URL format works")
    print("4. Check the RunPod documentation for the correct API format")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_url.py <endpoint_url> [api_key]")
        print("Example: python debug_url.py https://api.runpod.ai/v2/abc123/run your-api-key")
        sys.exit(1)
    
    endpoint_url = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else None
    
    test_url_formats(endpoint_url, api_key) 