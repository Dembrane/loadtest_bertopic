from typing import Optional, List
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import torch
import runpod

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
    input = event["input"]
    print(input)
    sentences = input["sentences"]
    print(sentences)
    topics, probs, hierarchical_topics = run_topic_model_hierarchical(
        topic_model, sentences)
    print(topics)
    return {"completed": True}

runpod.serverless.start({"handler": handler})