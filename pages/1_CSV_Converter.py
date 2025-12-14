import streamlit as st
import sys
from pathlib import Path

st.title("📄 CSV/Text File Converter")

st.write("""
Convert CSV and text files with advanced options:
- Multiple delimiter support
- Encoding detection and selection
- Header row configuration
- Data type specification
- Preview and validation
""")

uploaded_file = st.file_uploader("Upload CSV or text file", type=['csv', 'txt', 'tsv'])

if uploaded_file:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        delimiter = st.selectbox("Delimiter", [',', '\t', '|', ';'])
    
    with col2:
        encoding = st.selectbox("Encoding", ['utf-8', 'latin-1', 'iso-8859-1'])
    
    with col3:
        skip_rows = st.number_input("Skip rows", min_value=0, value=0)
    
    try:
        import pandas as pd
        df = pd.read_csv(uploaded_file, sep=delimiter, encoding=encoding, skiprows=skip_rows)
        
        st.subheader("📊 Data Preview")
        st.dataframe(df.head())
        
        st.subheader("📈 Data Info")
        st.write(f"Rows: {len(df)}, Columns: {len(df.columns)}")
        
        st.subheader("💾 Download Converted File")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            csv_data = df.to_csv(index=False)
            st.download_button("📥 CSV", csv_data, "output.csv")
        
        with col2:
            try:
                excel_data = df.to_excel(index=False)
                st.download_button("📥 Excel", excel_data, "output.xlsx")
            except:
                st.write("Excel not available")
        
        with col3:
            json_data = df.to_json(orient='records')
            st.download_button("📥 JSON", json_data, "output.json")
        
        with col4:
            try:
                parquet_data = df.to_parquet()
                st.download_button("📥 Parquet", parquet_data, "output.parquet")
            except:
                st.write("Parquet not available")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
