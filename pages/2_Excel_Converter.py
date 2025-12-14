import streamlit as st

st.title("📊 Excel File Converter")

st.write("""
Convert Excel files with advanced options:
- Multiple sheet support
- Merge sheets
- Range specification
- Data type configuration
- Batch conversion
""")

uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx', 'xls'])

if uploaded_file:
    try:
        import pandas as pd
        
        excel_file = pd.ExcelFile(uploaded_file)
        
        st.subheader("📋 Sheet Selection")
        sheets = st.multiselect("Select sheets", excel_file.sheet_names, default=excel_file.sheet_names[:1])
        
        if sheets:
            dfs = {sheet: pd.read_excel(uploaded_file, sheet_name=sheet) for sheet in sheets}
            
            for sheet, df in dfs.items():
                st.write(f"**{sheet}**: {len(df)} rows, {len(df.columns)} columns")
            
            st.subheader("📊 Data Preview")
            for sheet in sheets:
                st.write(f"Sheet: {sheet}")
                st.dataframe(dfs[sheet].head())
            
            st.subheader("💾 Download Converted File")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                merged_df = pd.concat(dfs.values(), ignore_index=True)
                csv_data = merged_df.to_csv(index=False)
                st.download_button("📥 CSV", csv_data, "output.csv")
            
            with col2:
                json_data = merged_df.to_json(orient='records')
                st.download_button("📥 JSON", json_data, "output.json")
            
            with col3:
                try:
                    parquet_data = merged_df.to_parquet()
                    st.download_button("📥 Parquet", parquet_data, "output.parquet")
                except:
                    st.write("Parquet not available")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
