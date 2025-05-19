import streamlit as st
from combined_rag import CombinedRAG

# Set up the Streamlit app - this must be the first Streamlit command
st.set_page_config(
    page_title="Binary Exploitation Explorer",
    page_icon="🔍",
    layout="wide"
)

# Initialize the RAG system
@st.cache_resource
def get_rag_system():
    return CombinedRAG()

rag = get_rag_system()

st.title("🔍 Binary Exploitation Explorer")
st.markdown("""
This application helps you explore techniques for exploiting binaries across Windows and Unix/Linux systems.
You can search for specific techniques, binaries, or ask general questions about binaries that can be 
used for various purposes.
""")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Query Knowledge Base", "Browse Binaries", "About"])

with tab1:
    st.header("Query the Knowledge Base")
    
    # Add source selection
    query_source = st.radio(
        "Select source to query:",
        ["Both (Windows & Unix/Linux)", "LOLBAS (Windows only)", "GTFOBins (Unix/Linux only)"],
        horizontal=True
    )
    
    # Map the selection to source parameter
    source_map = {
        "Both (Windows & Unix/Linux)": "all",
        "LOLBAS (Windows only)": "lolbas",
        "GTFOBins (Unix/Linux only)": "gtfobins"
    }
    
    query = st.text_input("Enter your query:", 
                         placeholder="Example: How can I use certutil for downloading files?")
    
    if st.button("Submit Query"):
        if query:
            with st.spinner(f"Processing your query against {query_source}..."):
                selected_source = source_map[query_source]
                
                if selected_source == "all":
                    # Query both systems
                    result = rag.query(query)
                elif selected_source == "lolbas":
                    # Query only LOLBAS
                    result = rag.lolbas_rag.query(query)
                else:
                    # Query only GTFOBins
                    result = rag.gtfobins_rag.query(query)
                
                st.markdown("### Answer")
                st.write(result["response"])
                
                st.markdown("### Sources")
                for i, source in enumerate(result["sources"]):
                    with st.expander(f"Source {i+1}"):
                        st.text(source)
        else:
            st.warning("Please enter a query.")

with tab2:
    st.header("Browse Binaries")
    
    # Create tabs for LOLBAS and GTFOBins
    tab2_1, tab2_2 = st.tabs(["LOLBAS (Windows)", "GTFOBins (Unix/Linux)"])
    
    with tab2_1:
        st.subheader("Browse LOLBAS Binaries and Scripts")
        
        # Get all binaries from LOLBAS
        all_entries = rag.get_all_entries("lolbas")
        all_lolbas_binaries = all_entries.get("lolbas", [])
        
        # Create a selectbox to choose a binary
        selected_binary = st.selectbox("Select a binary or script:", [""] + all_lolbas_binaries, key="lolbas_select")
        
        if selected_binary:
            binary_details = rag.get_entry_details(selected_binary, "lolbas")
            
            if binary_details:
                st.markdown(f"## {binary_details.get('Name')}")
                st.markdown(f"**Description:** {binary_details.get('Description', 'No description available')}")
                
                st.markdown("### Commands")
                for i, command in enumerate(binary_details.get("Commands", [])):
                    with st.expander(f"Command {i+1}: {command.get('Usecase', 'N/A')}"):
                        st.markdown(f"**Description:** {command.get('Description', 'No description')}")
                        st.markdown(f"**MITRE ATT&CK:** {command.get('MitreID', 'N/A')}")
                        st.code(command.get("Command", ""), language="bash")
            else:
                st.warning("Binary details not found.")
    
    with tab2_2:
        st.subheader("Browse GTFOBins")
        
        # Get all binaries from GTFOBins
        all_entries = rag.get_all_entries("gtfobins")
        all_gtfo_binaries = all_entries.get("gtfobins", [])
        
        # Create a selectbox to choose a binary
        selected_binary = st.selectbox("Select a binary:", [""] + all_gtfo_binaries, key="gtfo_select")
        
        if selected_binary:
            binary_details = rag.get_entry_details(selected_binary, "gtfobins")
            
            if binary_details:
                st.markdown(f"## {selected_binary}")
                
                # Get functions for this binary
                functions = binary_details.get("functions", {})
                
                if functions:
                    st.markdown("### Available Functions")
                    
                    for function_name, examples in functions.items():
                        with st.expander(f"Function: {function_name}"):
                            for i, example in enumerate(examples):
                                st.markdown(f"**Example {i+1}:**")
                                if "description" in example:
                                    st.markdown(f"*{example['description']}*")
                                st.code(example.get("code", ""), language="bash")
                else:
                    st.info("No functions available for this binary.")
            else:
                st.warning("Binary details not found.")

with tab3:
    st.header("About Binary Exploitation Projects")
    
    st.subheader("LOLBAS Project (Windows)")
    st.markdown("""
    The LOLBAS project documents binaries, scripts, and libraries that can be used for "Living Off The Land" techniques.
    
    These binaries may be used by threat actors for various purposes during different phases of the attack lifecycle:
    
    - Download and execute payloads
    - Load and execute code
    - Bypass User Account Control (UAC)
    - Compile code
    - Credential theft
    - And more...
    
    For more information, visit the [LOLBAS Project on GitHub](https://github.com/LOLBAS-Project/LOLBAS).
    """)
    
    st.subheader("GTFOBins Project (Unix/Linux)")
    st.markdown("""
    GTFOBins is a curated list of Unix binaries that can be used to bypass local security restrictions in misconfigured systems.
    
    The project collects legitimate functions of Unix binaries that can be abused to:
    
    - Get a shell
    - Execute commands
    - Transfer files
    - Perform privilege escalation
    - And more...
    
    For more information, visit the [GTFOBins Project on GitHub](https://github.com/GTFOBins/GTFOBins.github.io).
    """)
    
    st.markdown("### Data Sources")
    st.markdown("""
    - LOLBAS API: https://lolbas-project.github.io/api/lolbas.json
    - GTFOBins API: https://gtfobins.github.io/gtfobins.json
    """)

# Add footer
st.markdown("---")
st.markdown("Built with Streamlit and LlamaIndex")
