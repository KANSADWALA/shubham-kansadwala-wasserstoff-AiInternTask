# shubham-kansadwala-wasserstoff-AiInternTask

# Domain-Specific PDF Summarization & Keyword Extraction Pipeline

## Project Overview
This project is designed to automatically summarize PDF documents and extract important keywords. It processes multiple PDFs concurrently, stores results in MongoDB, and includes performance benchmarking to evaluate the system's efficiency.

## Features:
- **Custom Summarization**: TextRank-inspired algorithm is used.
- **Custom Keyword Extraction**: TF-IDF (Term Frequency-Inverse Document Frequency) is used.
- **MongoDB Integration**: Stores metadata, summaries, and keywords in MongoDB.
- **Concurrency**: Handles multiple PDFs concurrently to improve performance.

## Dependencies Used

- **nltk**: Natural Language Toolkit for tokenization and stopwords.
- **pdfminer.six**: For extracting text from PDF files.
- **requests**: For handling HTTP requests to download PDF files.
- **concurrent.futures**: For managing parallel processing.
- **scikit-learn**: Provides TfidfVectorizer and cosine_similarity for keyword extraction and sentence ranking.
- **numpy**: For numerical operations used in vectorization.
- **pymongo**: MongoDB client for storing results.
- **psutil**: For tracking system resource usage (CPU, memory).

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

### - PDF Summarization:

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

### - Keywords Extraction:

TF-IDF (Term Frequency-Inverse Document Frequency) is a statistical measure used to evaluate the importance of a word in a document relative to a collection of documents. In your system, TF-IDF is used to extract the most relevant keywords from each document.

### - Why These Techniques (TextRank-inspired algorithm & TF-IDF) Were Chosen:

- **Efficiency**: Both algorithms are computationally efficient, avoiding the need for heavy pre-trained models or external libraries. This makes them suitable for batch processing of multiple PDFs.
- **Scalability**: The TextRank-inspired summarization and TF-IDF keyword extraction are scalable to handle large documents and concurrent processing.
- **Interpretability**: The results (summaries and keywords) are easy to understand and trace back to specific words or sentences in the original text, which makes these methods transparent and explainable.


### - MongoDB Integration:
After processing, the system stores the filename, summary, keywords, and other metadata in MongoDB.

### - Concurrency:
The system uses Python's `concurrent.futures.ThreadPoolExecutor` to handle multiple PDFs concurrently, improving processing speed.

### - Error Handling:

<ol>
<li><strong>Download PDF Errors:</strong> The function `download_pdf` handles errors that may occur during the download of PDFs, such as an invalid URL or a failed HTTP request.
    <ul>
<li>**Invalid URL**: If the URL is invalid or the server is down, the error is caught and logged.</li>
<li>**Connection errors**: If the request to the server fails, the error is logged, and processing continues without terminating the entire pipeline.</li>
<li>**Error Logging**: If an error occurs, it prints a detailed error message but continues to process other files.</li>
    </ul>

</li>

<br>

<li><strong>PDF Processing Errors:</strong> The `parse_pdf` function processes each PDF, and errors may arise during text extraction (e.g., corrupted PDFs).

<ul>
<li>**Corrupted PDFs:** If a PDF is corrupted or unreadable by pdfminer.six, the error is caught, and the system skips the problematic file.</li>
<li>**Empty PDFs:** If a PDF contains no text, the error can be logged, and the file is skipped.</li>
<li>**Empty PDF Handling:** If no text is found, it raises a ValueError and logs the issue.</li>
<li>**General Errors:** A general Exception is caught to handle any unforeseen errors during text extraction or MongoDB updates.</li>
</ul>

</li>

<br>

<li><strong>MongoDB Connection and Insertion Errors:</strong> MongoDB operations, such as inserting document summaries and keywords, may fail if the database is not reachable or there is a data format issue.

<ul>
<li>**Connection errors:** If MongoDB is down or unreachable, the error will be caught, logged, and the program will continue processing other PDFs.</li>
<li>**Data insertion errors:** If there is an issue with inserting the document metadata into MongoDB, the error will be logged without terminating the entire pipeline.</li>
<li>**Error Logging:** Errors related to MongoDB connectivity or data insertion will be logged without stopping the processing of other documents.</li>
</ul>

</li>

<br>

<li><strong>Performance Monitoring Errors:</strong> When monitoring system performance (CPU, memory), the `psutil` library is used. If the monitoring fails due to system limitations, the error is logged.

<ul>
<li>**Handling Missing Permissions:** If `psutil` cannot access system metrics due to missing permissions, the error is caught and logged.</li>
</ul>
 
</li>


</ol>


### - Performance Metrics
The system tracks:

- Total time taken to process all PDFs.
- Resource usage (CPU, memory) using the `psutil` library.




