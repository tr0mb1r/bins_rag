import json
import os
from typing import List, Dict, Any, Optional

import requests
from llama_index.core import VectorStoreIndex, Document
from rag_base import BaseRAG
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LolbasRAG(BaseRAG):
    """RAG system for LOLBAS (Living Off The Land Binaries, Scripts and Libraries) data."""
    
    def __init__(self):
        """Initialize the LOLBAS RAG system."""
        super().__init__(
            data_url="https://lolbas-project.github.io/api/lolbas.json",
            cache_file="lolbas_data.json"
        )
    
    def _create_index(self) -> None:
        """Create vector index from LOLBAS data."""
        if not self.data:
            raise ValueError("No data available to index")
        
        documents = []
        
        # Process each entry in the LOLBAS data
        for entry in self.data:
            # Create a document for each command with its details
            name = entry.get("Name", "")
            description = entry.get("Description", "")
            
            # Process each command
            for command in entry.get("Commands", []):
                command_name = command.get("Command", "")
                command_description = command.get("Description", "")
                command_code = command.get("Command", "")
                execution = command.get("Usecase", "")
                mitre = command.get("MitreID", "")
                
                # Create a structured document with all relevant information
                content = f"""
                Source: LOLBAS (Windows)
                Binary/Script: {name}
                Description: {description}
                Command: {command_name}
                Command Description: {command_description}
                Execution: {execution}
                MITRE ATT&amp;CK Technique ID: {mitre}
                Code Sample: {command_code}
                """
                
                doc = Document(text=content)
                documents.append(doc)
        
        # Create vector store index
        self.index = VectorStoreIndex.from_documents(documents)
    
    def get_all_entries(self) -> List[str]:
        """Get a list of all binaries/scripts in the LOLBAS database.
        
        Returns:
            List of binary/script names
        """
        if not self.data:
            return []
        
        return [entry.get("Name", "") for entry in self.data]
    
    def get_entry_details(self, entry_name: str) -> Optional[Dict[str, Any]]:
        """Get details for a specific binary/script.
        
        Args:
            entry_name: Name of the binary/script
            
        Returns:
            Dictionary with binary details or None if not found
        """
        if not self.data:
            return None
        
        for entry in self.data:
            if entry.get("Name", "").lower() == entry_name.lower():
                return entry
        
        return None
    
    # Alias methods for backward compatibility
    def get_all_binaries(self) -> List[str]:
        return self.get_all_entries()
    
    def get_binary_details(self, binary_name: str) -> Optional[Dict[str, Any]]:
        return self.get_entry_details(binary_name)