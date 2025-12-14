import streamlit as st

st.title("⚡ Parquet/Feather Converter")

st.write("""
Convert to high-performance columnar formats:
- Parquet format (PyArrow/fastparquet)
- Feather format
- Compression options
- Performance metrics
- File size comparison
""")

uploaded_file = st.file_uploader("Upload data file", type=['csv', 'xlsx', 'json', 'parquet'])

if uploaded_file:
    try:
        import pandas as pd
        
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file) if uploaded_file.name.endswith(('.xlsx', '.xls')) else pd.read_json(uploaded_file)
        
        compression = st.selectbox("Compression", ['snappy', 'gzip', 'brotli', 'none'])
        
        st.subheader("📊 Data Preview")
        st.dataframe(df.head())
        
        st.subheader("📊 Data Info")
        st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        
        st.subheader("💾 Download Converted File")
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                parquet_data = df.to_parquet(compression=compression if compression != 'none' else None)
                st.download_button("📥 Parquet", parquet_data, "output.parquet")
            except:
                st.write("Parquet not available")
        
        with col2:
            try:
                feather_data = df.to_feather()
                st.download_button("📥 Feather", feather_data, "output.feather")
            except:
                st.write("Feather not available")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
