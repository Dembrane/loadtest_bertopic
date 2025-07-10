# RunPod BERTopic Load Testing

This repository contains tools to load test your RunPod BERTopic handler with different document sizes.

## Files

- `load_test.py` - Comprehensive Python load testing script
- `generate_test_files.py` - Generate individual JSON test files
- `test_with_curl.sh` - Simple bash script using curl
- `create_test_inpot.py` - Original test file generator (fixed)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Generate test files:
```bash
python generate_test_files.py
```

This will create:
- `test_input_100.json` - 100 documents
- `test_input_1000.json` - 1,000 documents  
- `test_input_10000.json` - 10,000 documents
- `test_input_100000.json` - 100,000 documents

## Usage

### 1. Python Load Testing Script

The most comprehensive option with detailed statistics:

```bash
python load_test.py --url "https://api.runpod.ai/v2/your-endpoint-id/run" --sizes 100 1000 10000 --requests 5 --concurrent 2
```

With API key authentication:

```bash
python load_test.py --url "https://api.runpod.ai/v2/your-endpoint-id/run" --api-key "your-api-key-here" --sizes 100 1000 10000 --requests 5 --concurrent 2
```

Options:
- `--url`: Your RunPod endpoint URL (required)
- `--api-key`: RunPod API key for authentication (optional)
- `--sizes`: Document sizes to test (default: 100 1000 10000)
- `--requests`: Number of requests per size (default: 3)
- `--concurrent`: Number of concurrent requests (default: 1)
- `--output`: Output file for results (default: load_test_results.json)

Example output:
```
Testing with 100 documents
==================================================
Data size: 45678 bytes
Running load test: 3 requests, 1 concurrent
Request 1/3
Request 2/3
Request 3/3

Results for 100 documents:
  Success Rate: 100.00%
  Avg Response Time: 12.34s
  Min Response Time: 11.89s
  Max Response Time: 13.01s
  Median Response Time: 12.45s
  Std Response Time: 0.56s
  Avg Response Size: 12345 bytes
```

### 2. Curl-based Testing

Simple testing with curl:

```bash
./test_with_curl.sh "https://api.runpod.ai/v2/your-endpoint-id/run"
```

With API key authentication:

```bash
./test_with_curl.sh "https://api.runpod.ai/v2/your-endpoint-id/run" "your-api-key-here"
```

This will test with 100, 1000, and 10000 documents sequentially.

### 3. Manual Testing

You can also test manually using the generated JSON files:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d @test_input_1000.json \
  "https://api.runpod.ai/v2/your-endpoint-id/run"
```

With API key authentication:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key-here" \
  -d @test_input_1000.json \
  "https://api.runpod.ai/v2/your-endpoint-id/run"
```

## Expected Performance

Based on typical BERTopic performance:

- **100 documents**: ~30-90 seconds (including polling)
- **1,000 documents**: ~2-5 minutes (including polling)
- **10,000 documents**: ~5-15 minutes (including polling)
- **100,000 documents**: ~15-60 minutes (including polling)

**Note**: RunPod uses an asynchronous API. The load testing tools:
1. Submit the job and receive a job ID immediately
2. Poll the status endpoint every 30 seconds
3. Report completion when the job finishes

**Input Format**: The handler now accepts:
- `num_docs`: Number of documents to process
- `num_topics`: Number of topics to reduce to (default: 10)
- `random_seed`: Random seed for reproducibility (default: 42)

The dataset is downloaded and processed within the handler to avoid payload size limits.

Performance depends on:
- GPU availability and type
- Model complexity
- Network latency
- RunPod instance specifications
- Queue position (if other jobs are running)

## Troubleshooting

1. **Timeout errors**: Increase the timeout in `load_test.py` (default: 300s)
2. **Memory errors**: Reduce document size or use smaller batches
3. **Network errors**: Check your RunPod endpoint URL and connectivity

## Results Analysis

The Python script saves detailed results to a JSON file with:
- Success/failure rates
- Response time statistics (min, max, mean, median, std)
- Response sizes
- Error messages

Use this data to:
- Identify performance bottlenecks
- Determine optimal batch sizes
- Plan capacity requirements
- Monitor performance over time 