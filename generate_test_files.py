from sklearn.datasets import fetch_20newsgroups
import json

def generate_test_files():
    """Generate test files for different document sizes."""
    print("Loading 20 newsgroups dataset...")
    newsgroups = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))
    docs = newsgroups.data
    
    sizes = [100, 1000, 10000, 100000]
    
    for size in sizes:
        # Take the first 'size' documents, or all if size is larger than available
        sample_docs = docs[:min(size, len(docs))]
        
        test_data = {
            "input": {
                "sentences": sample_docs
            }
        }
        
        filename = f"test_input_{size}.json"
        with open(filename, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        print(f"Generated {filename} with {len(sample_docs)} documents")
        print(f"  File size: {len(json.dumps(test_data))} bytes")

if __name__ == "__main__":
    generate_test_files() 