import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add utils to path for imports
sys.path.append(str(Path(__file__).parent))

# Initialize session state
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []
if 'user_settings' not in st.session_state:
    st.session_state.user_settings = {
        'default_encoding': 'utf-8',
        'default_delimiter': ',',
        'preview_rows': 5
    }

# Page configuration
st.set_page_config(
    page_title="File Format Converter",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("📊 File Converter")
st.sidebar.markdown("""
**Supported Formats:**
• CSV, TSV, TXT
• Excel (.xlsx, .xls)
• JSON (all orientations)
• Parquet, Feather
• HDF5, Pickle
• SQL Databases

**Features:**
• Auto encoding detection
• Batch conversion
• Data preview
• Conversion history
""")

# Main page
st.title("🐼 File Format Converter")
st.markdown("""
Convert files between multiple formats with advanced options:
- **CSV/Text** ↔ Excel ↔ JSON ↔ Parquet ↔ Feather ↔ SQL
- Auto encoding detection
- Batch processing  
- Data preview & validation
""")

# Show conversion history
if st.session_state.conversion_history:
    st.sidebar.subheader("📈 Conversion History")
    for i, conv in enumerate(reversed(st.session_state.conversion_history[-5:]), 1):
        st.sidebar.markdown(f"**{i}.** {conv['input']} → {conv['output']} ({conv.get('rows', 0)} rows)")

# Navigation
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📁 Quick Start", "🚀 Features"])

with tab1:
    st.header("Get Started in 3 Steps")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **1. Upload File**
        - Drag & drop or click
        - Supports 20+ formats
        - Auto-detects encoding
        """)
    
    with col2:
        st.markdown("""
        **2. Configure Options**
        - Delimiter, encoding
        - Data types, headers
        - Preview first 5 rows
        """)
    
    with col3:
        st.markdown("""
        **3. Convert & Download**
        - One-click conversion
        - Multiple output formats
        - Track in history
        """)

with tab2:
    st.header("Production-Ready Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Input Handling
        - ✅ Auto encoding detection
        - ✅ Multiple delimiters
        - ✅ Skip rows/headers
        - ✅ Data type mapping
        - ✅ Missing value handling
        """)
    
    with col2:
        st.markdown("""
        ### Output Options
        - ✅ CSV, Excel, JSON
        - ✅ Parquet, Feather, HDF5
        - ✅ SQL databases
        - ✅ Batch processing
        - ✅ Compression options
        """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        🐼 Production-ready file converter | 
        <a href='https://share.streamlit.io'>Deployed on Streamlit Cloud</a>
    </div>
    """, 
    unsafe_allow_html=True
)
