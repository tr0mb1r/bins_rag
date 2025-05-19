from typing import List, Dict, Any, Optional
from llama_index.core import VectorStoreIndex, Document
from rag_base import BaseRAG

class GTFOBinsRAG(BaseRAG):
    """RAG system for GTFOBins (Unix binaries that can be exploited) data."""
    
    def __init__(self):
        """Initialize the GTFOBins RAG system."""
        super().__init__(
            data_url="https://gtfobins.github.io/gtfobins.json",
            cache_file="gtfobins_data.json"
        )
    
    def _create_index(self) -> None:
        """Create vector index from GTFOBins data."""
        if not self.data:
            raise ValueError("No data available to index")
        
        documents = []
        
        # Process each entry in the GTFOBins data
        # GTFOBins structure is different from LOLBAS
        for binary_name, binary_data in self.data.items():
            # Process each function category
            for function_name, function_examples in binary_data.get("functions", {}).items():
                for example in function_examples:
                    description = example.get("description", "")
                    code = example.get("code", "")
                    
                    # Create a structured document with all relevant information
                    content = f"""
                    Source: GTFOBins (Unix/Linux)
                    Binary: {binary_name}
                    Function: {function_name}
                    Description: {description}
                    Code Sample: {code}
                    """
                    
                    doc = Document(text=content)
                    documents.append(doc)
        
        # Create vector store index
        self.index = VectorStoreIndex.from_documents(documents)
    
    def get_all_entries(self) -> List[str]:
        """Get a list of all binaries in the GTFOBins database.
        
        Returns:
            List of binary names
        """
        if not self.data:
            return []
        
        return list(self.data.keys())
    
    def get_entry_details(self, entry_name: str) -> Optional[Dict[str, Any]]:
        """Get details for a specific binary.
        
        Args:
            entry_name: Name of the binary
            
        Returns:
            Dictionary with binary details or None if not found
        """
        if not self.data:
            return None
        
        return self.data.get(entry_name)
    
    def get_functions_for_binary(self, binary_name: str) -> List[str]:
        """Get a list of available functions for a specific binary.
        
        Args:
            binary_name: Name of the binary
            
        Returns:
            List of function names
        """
        if not self.data or binary_name not in self.data:
            return []
        
        return list(self.data[binary_name].get("functions", {}).keys())