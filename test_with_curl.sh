#!/bin/bash

# Test script for RunPod BERTopic handler using curl
# Usage: ./test_with_curl.sh <RUNPOD_URL> [API_KEY]

if [ $# -eq 0 ]; then
    echo "Usage: $0 <RUNPOD_URL> [API_KEY]"
    echo "Example: $0 https://your-runpod-endpoint.runpod.net"
    echo "Example: $0 https://your-runpod-endpoint.runpod.net your-api-key-here"
    exit 1
fi

RUNPOD_URL="$1"
API_KEY="$2"

echo "Testing RunPod endpoint: $RUNPOD_URL"
echo "=================================="

# Test with different document sizes
for size in 100 1000 10000; do
    echo ""
    echo "Testing with $size documents..."
    echo "--------------------------------"
    
    if [ ! -f "test_input_${size}.json" ]; then
        echo "Generating test_input_${size}.json..."
        python generate_test_files.py
    fi
    
    echo "Sending request..."
    start_time=$(date +%s.%N)
    
    # Build curl command with optional API key
    CURL_CMD="curl -s -w \"\nHTTP_CODE:%{http_code}\nTIME:%{time_total}\nSIZE:%{size_download}\n\" -X POST -H \"Content-Type: application/json\""
    
    if [ -n "$API_KEY" ]; then
        CURL_CMD="$CURL_CMD -H \"Authorization: Bearer $API_KEY\""
    fi
    
    CURL_CMD="$CURL_CMD -d @test_input_${size}.json \"$RUNPOD_URL\""
    
    response=$(eval $CURL_CMD)
    
    end_time=$(date +%s.%N)
    
    # Extract timing info
    http_code=$(echo "$response" | grep "HTTP_CODE:" | cut -d: -f2)
    curl_time=$(echo "$response" | grep "TIME:" | cut -d: -f2)
    response_size=$(echo "$response" | grep "SIZE:" | cut -d: -f2)
    
    # Calculate total time
    total_time=$(echo "$end_time - $start_time" | bc -l)
    
    echo "Results:"
    echo "  HTTP Code: $http_code"
    echo "  Curl Time: ${curl_time}s"
    echo "  Total Time: ${total_time}s"
    echo "  Response Size: ${response_size} bytes"
    
    if [ "$http_code" = "200" ]; then
        echo "  Status: SUCCESS"
    else
        echo "  Status: FAILED"
        echo "  Response: $(echo "$response" | head -n -3)"
    fi
    
    echo ""
done

echo "Testing complete!" 