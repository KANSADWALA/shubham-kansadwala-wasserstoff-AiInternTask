# shubham-kansadwala-wasserstoff-AiInternTask

# Summarization & Keyword Extraction System

## Project Overview
This project is designed to automatically summarize PDF documents and extract important keywords. It processes multiple PDFs concurrently, stores results in MongoDB, and includes performance benchmarking to evaluate the system's efficiency.

### Features:
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

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
