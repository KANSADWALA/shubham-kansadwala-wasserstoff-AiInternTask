# shubham-kansadwala-wasserstoff-AiInternTask

# PDF Summarization & Keyword Extraction System

## Project Overview
This project is designed to automatically summarize PDF documents and extract important keywords. It processes multiple PDFs concurrently, stores results in MongoDB, and includes performance benchmarking to evaluate the system's efficiency.

## Features:
- **Custom Summarization**: Uses frequency-based sentence scoring.
- **Custom Keyword Extraction**: Extracts top keywords based on term frequency.
- **MongoDB Integration**: Stores metadata, summaries, and keywords in MongoDB.
- **Concurrency**: Handles multiple PDFs concurrently to improve performance.

## System Requirements

### Hardware:
- Minimum 4 GB of RAM
- Multi-core processor for concurrent execution

### Software:
- Python 3.9+
- MongoDB (local or remote)

### Python Dependencies:
- `nltk`
- `pdfminer.six`
- `pymongo`
- `concurrent.futures`
- `psutil` (for performance monitoring)

## Setup Instructions

<ol>
    <li><strong>Clone the repository:</strong>
        <pre><code class="bash">
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository 
        </code></pre>
    </li>

<li><strong>Install Python dependencies:</strong>
        <pre><code class="bash">
pip install -r requirements.txt
        </code></pre>
    </li>

<li><strong>Download NLTK Data:</strong>
        <pre><code class="bash">
python -m nltk.downloader punkt stopwords
        </code></pre>
    </li>

<li><strong>Set Up MongoDB:</strong>
       <ul>
  <li>Ensure MongoDB is running either locally or via a remote service (e.g., MongoDB Atlas).</li>
  <li>Update the connection URI in the script.</li>
       </ul>
</li>

<li><strong>Run the System:</strong>
    To run the main pipeline and process PDFs:
<pre><code class="bash">
       python app.py        
       </code></pre>
</li>

</ol>

## Explaination of the full solution

### PDF Summarization:

The TextRank-inspired algorithm for summarization is an extractive summarization technique. It identifies and selects the most important sentences from the document based on the importance of the words they contain. The algorithm relies on word frequency to determine sentence importance, similar to how the PageRank algorithm ranks web pages.

Steps:
<ol>
<li><strong>Tokenization:</strong> The input text is broken down into sentences and individual words using NLTK.</li>
<li><strong>Word Frequency Calculation:</strong> A frequency distribution is created for the words in the document (excluding stopwords).
Words that occur more frequently in the document are considered more important.</li>
<li><strong>Sentence Scoring:</strong>Each sentence is scored based on the sum of the word frequencies of the words it contains. Sentences with higher scores are considered more relevant.</li>
<li><strong>Sentence Ranking:</strong> The sentences are sorted in descending order of their scores.</li>
<li><strong>Summary Generation:</strong> The top N sentences are selected as the summary of the document.</li>
</ol>
