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
    CURL_CMD="curl -s -X POST -H \"Content-Type: application/json\""
    
    if [ -n "$API_KEY" ]; then
        CURL_CMD="$CURL_CMD -H \"Authorization: Bearer $API_KEY\""
    fi
    
    CURL_CMD="$CURL_CMD -d @test_input_${size}.json \"$RUNPOD_URL\""
    
    response=$(eval $CURL_CMD)
    
    # Extract job ID from response
    job_id=$(echo "$response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    
    if [ -z "$job_id" ]; then
        echo "  Status: FAILED - No job ID received"
        echo "  Response: $response"
        echo ""
        continue
    fi
    
    echo "  Job submitted with ID: $job_id"
    
    # Poll for job completion
    poll_count=0
    max_polls=20  # Poll for up to 10 minutes (20 * 30 seconds)
    
    while [ $poll_count -lt $max_polls ]; do
        sleep 30
        poll_count=$((poll_count + 1))
        
        # Build status check command
        # Extract the endpoint ID from the URL
        # URL format: https://api.runpod.ai/v2/{endpoint_id}/run
        if [[ "$RUNPOD_URL" == *"/run"* ]]; then
            # Remove /run from the end to get the base URL
            BASE_URL="${RUNPOD_URL%/run}"
        else
            # Fallback: assume it's already the base URL
            BASE_URL="${RUNPOD_URL%/}"
        fi
        
        STATUS_CMD="curl -s -X GET"
        if [ -n "$API_KEY" ]; then
            STATUS_CMD="$STATUS_CMD -H \"Authorization: Bearer $API_KEY\""
        fi
        STATUS_CMD="$STATUS_CMD \"$BASE_URL/status/$job_id\""
        
        echo "    Status URL: $BASE_URL/status/$job_id"
        status_response=$(eval $STATUS_CMD)
        status=$(echo "$status_response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
        
        echo "    Poll $poll_count: Status = $status"
        
        if [ "$status" = "COMPLETED" ]; then
            end_time=$(date +%s.%N)
            total_time=$(echo "$end_time - $start_time" | bc -l)
            
            echo "  Status: SUCCESS"
            echo "  Total Time: ${total_time}s"
            echo "  Job ID: $job_id"
            break
        elif [ "$status" = "FAILED" ]; then
            error_msg=$(echo "$status_response" | grep -o '"error":"[^"]*"' | cut -d'"' -f4)
            echo "  Status: FAILED - $error_msg"
            echo "  Job ID: $job_id"
            break
        elif [ "$status" = "IN_QUEUE" ] || [ "$status" = "IN_PROGRESS" ]; then
            # Continue polling
            continue
        else
            echo "  Status: UNKNOWN - $status"
            echo "  Job ID: $job_id"
            break
        fi
    done
    
    if [ $poll_count -eq $max_polls ]; then
        echo "  Status: TIMEOUT - Job did not complete within 10 minutes"
        echo "  Job ID: $job_id"
    fi
    
    echo ""
done

echo "Testing complete!" 