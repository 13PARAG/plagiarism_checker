"""
Training data preparation script
Module: plagiarism_checker/backend_api/data_prep.py

This script creates a synthetic training dataset with similarity scores
for training the machine learning plagiarism detection model.
"""

import pandas as pd
import numpy as np
from utils import calculate_cosine_similarity
import os


def create_training_data(output_file="plagiarism_dataset.csv"):
    """
    Create synthetic training dataset with similarity scores and labels
    
    This function generates 20 pairs of text documents with computed
    similarity scores and plagiarism labels.
    
    Returns:
        pd.DataFrame: Training dataset with columns:
                     - Original: Original text
                     - Submission: Submission text
                     - Similarity: Computed cosine similarity score
                     - Label: 1 for plagiarized, 0 for original
    """
    
    # Comprehensive training data
    # Format: (original_text, submission_text, label)
    # Label: 1 = plagiarized (similar), 0 = original (different)
    
    data = [
        # HIGH SIMILARITY (Plagiarized) - Label 1
        (
            "Machine learning is a subset of artificial intelligence.",
            "Machine learning is a subset of artificial intelligence.",
            1
        ),
        (
            "The sky is blue and beautiful.",
            "The sky is blue and beautiful.",
            1
        ),
        (
            "Machine learning is fascinating and complex.",
            "Machine learning is fascinating and quite complex.",
            1
        ),
        (
            "Python is a great programming language for data science.",
            "Python is an amazing language for data science programming.",
            1
        ),
        (
            "Data science involves statistics and machine learning.",
            "Data science requires statistics and machine learning knowledge.",
            1
        ),
        (
            "The quick brown fox jumps over the fence.",
            "The rapid brown fox leaps over the fence.",
            1
        ),
        (
            "Artificial intelligence is evolving rapidly.",
            "AI technology is advancing very rapidly.",
            1
        ),
        (
            "Deep learning uses neural networks.",
            "Neural networks are used in deep learning.",
            1
        ),
        (
            "Natural language processing is a complex field.",
            "NLP is a very complex field of study.",
            1
        ),
        (
            "Computer vision analyzes and processes images.",
            "Image analysis uses computer vision techniques.",
            1
        ),
        (
            "Algorithms are fundamental to computer science.",
            "Algorithms are fundamental to computing.",
            1
        ),
        (
            "Big data requires advanced processing techniques.",
            "Big data needs advanced processing methods.",
            1
        ),
        (
            "Cloud computing provides scalable infrastructure.",
            "Cloud computing offers scalable solutions.",
            1
        ),
        (
            "Cybersecurity protects against digital attacks.",
            "Cybersecurity defends against digital threats.",
            1
        ),
        (
            "Blockchain technology enables secure transactions.",
            "Blockchain enables transactions that are secure.",
            1
        ),
        
        # LOW SIMILARITY (Original) - Label 0
        (
            "Machine learning is fun.",
            "I like eating pizza for dinner.",
            0
        ),
        (
            "Python is cool.",
            "Java is another programming language.",
            0
        ),
        (
            "Weather is nice today.",
            "Apples are very tasty fruits.",
            0
        ),
        (
            "I enjoy reading books.",
            "The car needs an oil change.",
            0
        ),
        (
            "Coffee tastes great.",
            "Mountains are very high.",
            0
        ),
        (
            "Music is relaxing.",
            "Cooking requires practice and patience.",
            0
        ),
        (
            "Exercise is healthy.",
            "Painting walls takes time and effort.",
            0
        ),
        (
            "Trees provide oxygen.",
            "Mathematics involves numbers and equations.",
            0
        ),
        (
            "Ocean waves are powerful.",
            "Basketball is a popular sport.",
            0
        ),
        (
            "Stars shine at night.",
            "Gardening needs water and sunlight.",
            0
        ),
    ]
    
    print("🚀 Creating training dataset...")
    print(f"   Processing {len(data)} text pairs...")
    
    rows = []
    for idx, (original, submission, label) in enumerate(data):
        try:
            # Calculate cosine similarity
            similarity = calculate_cosine_similarity(original, submission)
            rows.append([original, submission, similarity, label])
            print(f"   ✓ Pair {idx+1}: similarity={similarity:.4f}, label={label}")
        except Exception as e:
            print(f"   ✗ Pair {idx+1}: Error - {str(e)}")
            continue
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=["Original", "Submission", "Similarity", "Label"])
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    
    # Print statistics
    print(f"\n✅ Training dataset created successfully!")
    print(f"   Total samples: {len(df)}")
    print(f"   Plagiarized samples: {df['Label'].sum()}")
    print(f"   Original samples: {len(df) - df['Label'].sum()}")
    print(f"   Mean similarity: {df['Similarity'].mean():.4f}")
    print(f"   Min similarity: {df['Similarity'].min():.4f}")
    print(f"   Max similarity: {df['Similarity'].max():.4f}")
    print(f"   Std deviation: {df['Similarity'].std():.4f}")
    print(f"\n💾 Dataset saved to: {output_file}")
    
    return df


if __name__ == "__main__":
    # Change to backend directory if needed
    if os.path.exists("utils.py"):
        create_training_data()
    else:
        print("❌ Error: Make sure you're in the backend_api directory")
        print("   Run: cd backend_api && python data_prep.py")