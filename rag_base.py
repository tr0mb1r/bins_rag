import json
import os
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

import requests
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseRAG(ABC):
    """Base class for RAG systems."""
    
    def __init__(self, data_url: str, cache_file: str):
        """Initialize the RAG system.
        
        Args:
            data_url: URL to the JSON data
            cache_file: Local file to cache the data
        """
        self.data_url = data_url
        self.cache_file = cache_file
        self.data = None
        self.index = None
        
        # Configure LlamaIndex
        Settings.llm = OpenAI(model="gpt-3.5-turbo")
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
        
        # Load and index data
        self._load_data()
        self._create_index()
    
    def _load_data(self) -> None:
        """Load data from URL or local cache."""
        try:
            response = requests.get(self.data_url)
            response.raise_for_status()
            self.data = response.json()
            
            # Save to local cache for future use
            with open(self.cache_file, "w") as f:
                json.dump(self.data, f)
        except Exception as e:
            print(f"Error fetching data from URL: {e}")
            # Try to load from local cache if available
            try:
                with open(self.cache_file, "r") as f:
                    self.data = json.load(f)
                print(f"Loaded data from local cache: {self.cache_file}")
            except FileNotFoundError:
                raise Exception(f"Failed to load data from URL and no local cache found: {self.cache_file}")
    
    @abstractmethod
    def _create_index(self) -> None:
        """Create vector index from data. To be implemented by subclasses."""
        pass
    
    def query(self, query_text: str) -> Dict[str, Any]:
        """Query the knowledge base.
        
        Args:
            query_text: The query text
            
        Returns:
            Dict containing response and source information
        """
        if not self.index:
            raise ValueError("Index not initialized")
        
        query_engine = self.index.as_query_engine()
        response = query_engine.query(query_text)
        
        return {
            "response": response.response,
            "sources": [node.get_content() for node in response.source_nodes]
        }
    
    @abstractmethod
    def get_all_entries(self) -> List[str]:
        """Get a list of all entries in the database. To be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_entry_details(self, entry_name: str) -> Optional[Dict[str, Any]]:
        """Get details for a specific entry. To be implemented by subclasses."""
        pass