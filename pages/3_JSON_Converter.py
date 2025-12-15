import streamlit as st
import json

st.title("📋 JSON Converter")

st.write("""
Convert JSON files with multiple format options:
- Records orientation
- Split orientation
- Index orientation
- Nested JSON flattening
- Date parsing
""")

uploaded_file = st.file_uploader("Upload JSON file", type=['json', 'jsonl'])

if uploaded_file:
    try:
        import pandas as pd
        
        orient = st.selectbox("JSON Orientation", ['records', 'split', 'index', 'columns', 'values'])
        
        df = pd.read_json(uploaded_file,keep_default_na=False)
        
        st.subheader("📊 Data Preview")
        st.dataframe(df.head())
        
        st.subheader("📈 Data Info")
        st.write(f"Rows: {len(df)}, Columns: {len(df.columns)}")
        
        st.subheader("💾 Download Converted File")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = df.to_csv(index=False)
            st.download_button("📥 CSV", csv_data, "output.csv")
        
        with col2:
            excel_data = df.to_excel(index=False)
            st.download_button("📥 Excel", excel_data, "output.xlsx")
        
        with col3:
            try:
                parquet_data = df.to_parquet()
                st.download_button("📥 Parquet", parquet_data, "output.parquet")
            except:
                st.write("Parquet not available")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
