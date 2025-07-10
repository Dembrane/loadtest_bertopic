from sklearn.datasets import fetch_20newsgroups
import json

def generate_test_files():
    """Generate test files for different document sizes."""
    sizes = [100, 1000, 10000, 100000]
    
    for size in sizes:
        # Create test data with the new format
        test_data = {
            "input": {
                "num_docs": size,
                "num_topics": 10,  # Default number of topics
                "random_seed": 42   # For reproducibility
            }
        }
        
        filename = f"test_input_{size}.json"
        with open(filename, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        print(f"Generated {filename} for {size} documents")
        print(f"  File size: {len(json.dumps(test_data))} bytes")

if __name__ == "__main__":
    generate_test_files() 