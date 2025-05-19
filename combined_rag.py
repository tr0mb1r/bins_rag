from typing import List, Dict, Any, Optional, Tuple
from llama_index.core import VectorStoreIndex, Document
from rag import LolbasRAG
from gtfobins_rag import GTFOBinsRAG

class CombinedRAG:
    """Combined RAG system that uses both LOLBAS and GTFOBins data."""
    
    def __init__(self):
        """Initialize the combined RAG system."""
        self.lolbas_rag = LolbasRAG()
        self.gtfobins_rag = GTFOBinsRAG()
    
    def query(self, query_text: str) -> Dict[str, Any]:
        """Query both knowledge bases and combine results.
        
        Args:
            query_text: The query text
            
        Returns:
            Dict containing response and source information
        """
        # Query both systems
        lolbas_result = self.lolbas_rag.query(query_text)
        gtfobins_result = self.gtfobins_rag.query(query_text)
        
        # Combine responses
        combined_response = f"""
        Results from Windows (LOLBAS):
        {lolbas_result['response']}
        
        Results from Unix/Linux (GTFOBins):
        {gtfobins_result['response']}
        """
        
        # Combine sources
        combined_sources = lolbas_result['sources'] + gtfobins_result['sources']
        
        return {
            """response""": combined_response,
            """sources""": combined_sources
        }
    
    def get_all_entries(self, source: str = """all""") -> Dict[str, List[str]]:
        """Get a list of all entries from specified source(s).
        
        Args:
            source: 'lolbas', 'gtfobins', or 'all'
            
        Returns:
            Dictionary with source names as keys and lists of entries as values
        """
        result = {}
        
        if source.lower() in ["""lolbas""", """all"""]:
            result["""lolbas"""] = self.lolbas_rag.get_all_entries()
        
        if source.lower() in ["""gtfobins""", """all"""]:
            result["""gtfobins"""] = self.gtfobins_rag.get_all_entries()
        
        return result
    
    def get_entry_details(self, entry_name: str, source: str) -> Optional[Dict[str, Any]]:
        """Get details for a specific entry from a specific source.
        
        Args:
            entry_name: Name of the entry
            source: 'lolbas' or 'gtfobins'
            
        Returns:
            Dictionary with entry details or None if not found
        """
        if source.lower() == """lolbas""":
            return self.lolbas_rag.get_entry_details(entry_name)
        elif source.lower() == """gtfobins""":
            return self.gtfobins_rag.get_entry_details(entry_name)
        else:
            return None