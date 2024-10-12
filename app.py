
# Importing Dependencies
import time
import os
import json
import requests
from pdfminer.high_level import extract_text
import concurrent.futures
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import numpy as np
import re
from pymongo import MongoClient
import urllib.parse
import psutil

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# Extract username and password
username = "shubhamkansadwala"
password = "Shubham@123"

# URL encode username and password
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

# Build the corrected URI
uri = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.szzfc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(uri)

db = client['pdf_summary_and_extract_keywords']
collection = db['documents']

import json

# Load the Dataset.json file
def load_json(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

json_file_path = 'C:/Users/Admin/Downloads/PDF Summarize & Keywords Extract/Dataset.json'
json_data = load_json(json_file_path)

Insert_data = collection.insert_one(json_data)

print(f"Inserted Data ID : {Insert_data.inserted_id}")


# Preprocessing: Tokenizing, removing stopwords
def preprocess_text(text):
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))

    def clean_sentence(sentence):
        sentence = re.sub(r'\W+', ' ', sentence).lower()
        words = word_tokenize(sentence)
        return [word for word in words if word not in stop_words]

    cleaned_sentences = [clean_sentence(sentence) for sentence in sentences]
    return sentences, cleaned_sentences

# Create sentence vectors for similarity comparison
def sentence_vector(sentence, vocab):
    vector = np.zeros(len(vocab))
    word_count = Counter(sentence)
    for word in sentence:
        if word in vocab:
            vector[vocab[word]] = word_count[word]
    return vector

# Compute cosine similarity between sentence vectors
def build_similarity_matrix(sentences, vocab):
    sentence_vectors = [sentence_vector(sentence, vocab) for sentence in sentences]
    similarity_matrix = cosine_similarity(sentence_vectors)
    return similarity_matrix

# Keyword extraction using TF-IDF
def extract_keywords(text, top_n=5):
    stop_words = set(stopwords.words('english'))  # List of stop words
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)  # Use 'english' as a string

    # Tokenizing and vectorizing the text
    vectors = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    dense = vectors.todense().tolist()

    # Get the top-n keywords
    keywords = [feature_names[idx] for idx in np.argsort(dense[0])[::-1][:top_n]]
    return keywords

# Summarize text based on TextRank-inspired algorithm
def summarize_text(text, top_n=5):
    sentences, cleaned_sentences = preprocess_text(text)

    # Build the vocabulary (all unique words)
    vocab = {word: i for i, word in enumerate(set([word for sentence in cleaned_sentences for word in sentence]))}

    # Build the sentence similarity matrix
    similarity_matrix = build_similarity_matrix(cleaned_sentences, vocab)

    # Rank sentences by summing up similarity scores
    sentence_ranks = similarity_matrix.sum(axis=1)

    # Get indices of top-ranked sentences
    ranked_sentence_indices = sentence_ranks.argsort()[-top_n:][::-1]

    # Select top-n ranked sentences for the summary
    summary_sentences = [sentences[i] for i in sorted(ranked_sentence_indices)]

    return " ".join(summary_sentences)

# Download PDF from URL and save it to the local directory
def download_pdf(pdf_url, output_dir, pdf_name):
    try:
        response = requests.get(pdf_url)
        pdf_path = os.path.join(output_dir, f"{pdf_name}.pdf")
        with open(pdf_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")
        return None

# Parse the downloaded PDF, extract summary, keywords, and store metadata in MongoDB
def parse_pdf(file_path):
    try:
        text = extract_text(file_path)
        file_size = os.path.getsize(file_path)
        summary = summarize_text(text)
        keywords = extract_keywords(text)

        # Save document metadata and content (summary, keywords) to MongoDB
        doc_metadata = {
            'filename': os.path.basename(file_path),
            'path': file_path,
            'size': file_size,
            'summary': summary,
            'keywords': keywords,
            'status': 'completed'
        }
        collection.insert_one(doc_metadata)
        print(f"Processed: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Measure performance: Track time for concurrent processing
def process_pdfs_concurrently(json_data, output_dir):
    start_time = time.time()  # Start timer

    pdf_files = []

    # Download PDFs in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for pdf_name, pdf_url in json_data.items():
            futures.append(executor.submit(download_pdf, pdf_url, output_dir, pdf_name))
        for future in concurrent.futures.as_completed(futures):
            pdf_path = future.result()
            if pdf_path:
                pdf_files.append(pdf_path)

    # Process PDFs concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(parse_pdf, pdf_files)

    print("All PDFs processed.")

    # End timer
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time to process all PDFs: {elapsed_time:.2f} seconds")
    return elapsed_time


# Main pipeline function
def main_pipeline(json_file_path, output_dir):
    json_data = load_json(json_file_path)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    elapsed_time = process_pdfs_concurrently(json_data, output_dir)
    return elapsed_time

# Measure performance and print metrics
def measure_performance(json_file_path, output_dir):
    elapsed_time = main_pipeline(json_file_path, output_dir)
    print(f"\nPerformance Metrics:\nTotal Time: {elapsed_time:.2f} seconds")
    print(f"CPU usage: {psutil.cpu_percent()}%")
    print(f"Memory usage: {psutil.virtual_memory().percent}%")

if __name__ == "__main__":
    json_file_path = 'C:/Users/Admin/Downloads/PDF Summarize & Keywords Extract/Dataset.json'
    output_dir = 'C:/Users/Admin/Downloads/PDF Summarize & Keywords Extract/All PDFs'

    # Run the performance measurement
    measure_performance(json_file_path, output_dir)
