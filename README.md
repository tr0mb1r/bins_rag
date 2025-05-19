# Binary Exploitation Explorer

A Retrieval-Augmented Generation (RAG) powered application for exploring binary exploitation techniques across Windows (LOLBAS) and Unix/Linux (GTFOBins) systems using natural language queries.

## Overview

Binary Exploitation Explorer combines two powerful security resources:

1. **LOLBAS (Living Off The Land Binaries, Scripts and Libraries)** - A collection of Windows binaries that can be abused for various purposes
2. **GTFOBins (Unix Binaries)** - A curated list of Unix binaries that can be exploited in misconfigured systems

The application uses RAG technology to allow security professionals, penetration testers, and defenders to query these knowledge bases using natural language, making it easier to discover potential attack vectors and defense strategies.

## Features

- **Natural Language Queries**: Ask questions about binary exploitation techniques in plain English
- **Dual Knowledge Base**: Query both Windows (LOLBAS) and Unix/Linux (GTFOBins) resources simultaneously or individually
- **Interactive Browsing**: Browse and explore all available binaries and their exploitation techniques
- **Detailed Information**: View comprehensive details about each binary, including:
  - Command examples
  - MITRE ATT&CK mappings (for LOLBAS)
  - Function categories (for GTFOBins)
  - Code samples
- **Source Attribution**: All responses include references to the original source data

## Technical Architecture

The application is built using:

- **LlamaIndex**: For creating and querying vector indexes of the knowledge bases
- **OpenAI Embeddings**: For converting text into vector representations
- **Streamlit**: For the web interface
- **Docker**: For containerization and easy deployment

The RAG system follows a modular architecture:

1. **BaseRAG**: Abstract base class defining the common RAG functionality
2. **LolbasRAG**: Implementation for the LOLBAS knowledge base
3. **GTFOBinsRAG**: Implementation for the GTFOBins knowledge base
4. **CombinedRAG**: Orchestrator that can query both knowledge bases

## Running with Docker

### Prerequisites

- Docker installed
- OpenAI API key

### Building and Running the Docker Container

1. Clone this repository

2. Build the Docker image:
```bash
docker build -t binary-explorer .
```
3. Run the Docker container, providing your OpenAI API key:
```bash
docker run -p 8501:8501 -e OPENAI_API_KEY=your_openai_api_key_here binary-explorer
```
The application will be available at http://localhost:8501

### Stopping the container
To stop the running container:
```bash
docker ps  # Find the container ID
docker stop <container_id>
```

## Usage Examples

### Querying the Knowledge Base
You can ask questions like:
- "How can I use certutil for downloading files?"
- "What Windows binaries can be used for privilege escalation?"
- "Show me ways to execute code with Python in Unix systems"
- "Which binaries can be used for data exfiltration?"

### Browsing Binaries
The application allows you to browse all available binaries in both LOLBAS and GTFOBins, and view detailed information about each one, including:
- Description
- Available commands/functions
- Code examples
- MITRE ATT&CK techniques (for LOLBAS)

## Data Sources
- LOLBAS Project: https://lolbas-project.github.io/api/lolbas.json
- GTFOBins Project: https://gtfobins.github.io/gtfobins.json

## Project Structure
```
lolbas_rag/
├── main.py                # Streamlit application entry point
├── rag_base.py            # Base RAG class with common functionality
├── rag.py                 # LOLBAS RAG implementation
├── gtfobins_rag.py        # GTFOBins RAG implementation
├── combined_rag.py        # Combined RAG system
├── Dockerfile             # Docker configuration
├── pyproject.toml         # Project dependencies
└── uv.lock                # UV lock file for dependency management
```
