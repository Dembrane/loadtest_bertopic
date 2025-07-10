from typing import Optional, List
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import torch
import runpod
from sklearn.datasets import fetch_20newsgroups
import random

def run_topic_model_hierarchical(
    topic_model, 
    docs, 
    topics: Optional[List[str]] = None, 
    nr_topics: Optional[int] = None
):
    """
    Run hierarchical topic modeling on the provided documents.

    Args:
        topic_model: Initialized BERTopic model
        docs: List of documents to process
        topics: Optional list of predefined topics
        nr_topics: Optional number of topics to reduce to after fitting

    Returns:
        tuple: Contains:
            - topics: List of identified topics
            - probs: Topic probabilities for each document
            - hierarchical_topics: Hierarchical structure of topics
    """
    # First fit the model normally
    topics, probs = topic_model.fit_transform(docs)

    # If nr_topics is specified, reduce the topics
    if nr_topics is not None:
        topic_model.reduce_topics(docs, nr_topics=nr_topics)
        topics = topic_model.topics_
        probs = topic_model.probabilities_

    hierarchical_topics = topic_model.hierarchical_topics(docs)
    return topics, probs, hierarchical_topics

device = "cuda" if torch.cuda.is_available() else "cpu"
topic_model = BERTopic(embedding_model=SentenceTransformer("all-MiniLM-L6-v2",      
device=device))


def handler(event):
    try: 
        input = event["input"]
        print("Received input:", input)
        
        # Extract parameters
        num_docs = input.get("num_docs", 100)  # Number of documents to process
        num_topics = input.get("num_topics", 10)  # Number of topics to reduce to
        random_seed = input.get("random_seed", 42)  # Random seed for reproducibility
        
        print(f"Processing {num_docs} documents with {num_topics} topics")
        
        # Download and prepare the dataset
        print("Loading 20 newsgroups dataset...")
        newsgroups = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))
        docs = newsgroups.data
        
        # Set random seed for reproducibility
        random.seed(random_seed)
        
        # Sample the requested number of documents
        if num_docs <= len(docs):
            sample_docs = random.sample(docs, num_docs)
        else:
            # If requested more than available, use all and repeat
            sample_docs = random.choices(docs, k=num_docs)
        
        print(f"Selected {len(sample_docs)} documents for processing")
        
        # Run topic modeling
        topics, probs, hierarchical_topics = run_topic_model_hierarchical(
            topic_model, sample_docs, nr_topics=num_topics)
        
        print(f"Completed topic modeling. Found {len(set(topics))} unique topics")
  
        return {"completed": True}
    except Exception as e:
        print(f"Error: {e}")
        raise e

runpod.serverless.start({"handler": handler})