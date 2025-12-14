import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from io import BytesIO

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

st.title("📄 CSV/Text File Converter")
st.markdown("**Advanced CSV/TSV/TXT conversion with custom delimiter support**")

# File upload
uploaded_file = st.file_uploader(
    "Upload CSV, TSV, or text file",
    type=['csv', 'txt', 'tsv', 'dat'],
    help="Supports CSV, TSV, delimited text files"
)

if uploaded_file is not None:
    # File info
    file_size = len(uploaded_file.getvalue())
    st.info(f"📁 File: **{uploaded_file.name}** | Size: **{file_size/1024:.1f} KB**")
    
    # Configuration - 2 rows for better layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Delimiter with manual input
        delimiter_type = st.radio(
            "Delimiter Type",
            ["Common", "Custom"],
            horizontal=True
        )
        
        if delimiter_type == "Common":
            delimiter = st.selectbox(
                "Select delimiter",
                [",", "\t", ";", "|", ":", " ", "\\n"],
                index=0,
                format_func=lambda x: f"{x} ({'tab' if x=='\t' else x})"
            )
            manual_delimiter = None
        else:
            manual_delimiter = st.text_input(
                "Enter custom delimiter (single character)",
                placeholder="e.g. ~, #, ^",
                max_chars=1,
                help="Enter exactly one character"
            )
            delimiter = manual_delimiter if manual_delimiter else ","
    
    with col2:
        encoding = st.selectbox(
            "Encoding",
            ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-16'],
            index=0
        )
        
        header_option = st.radio(
            "Header",
            ["First row", "No header", "Row number"],
            horizontal=True,
            key="header_radio"
        )
        header = 0 if header_option == "First row" else None
    
    with col3:
        skip_rows = st.number_input("Skip first rows", min_value=0, value=0, step=1)
        preview_rows = st.number_input("Preview rows", min_value=1, max_value=50, value=10, step=1)
    
    # Advanced options expander
    with st.expander("⚙️ Advanced Options", expanded=False):
        col1_adv, col2_adv, col3_adv = st.columns(3)
        
        with col1_adv:
            na_values = st.text_area(
                "Missing values to treat as NA",
                value="NA,N/A,Null,Empty,-",
                height=60,
                help="Comma-separated values"
            ).split(",")
            
        with col2_adv:
            dtype_str = st.text_area(
                "Column data types (col:type)",
                value="",
                height=60,
                placeholder="id:int64,date:datetime64[ns]",
                help="Format: column_name:data_type"
            )
            
        with col3_adv:
            thousands_sep = st.checkbox("Thousands separator", value=False)
            decimal_sep = st.text_input("Decimal separator", value=".", max_chars=1)
    
    # Convert options to parameters
    try:
        na_values = [v.strip() for v in na_values if v.strip()]
        dtype_dict = {}
        if dtype_str:
            for line in dtype_str.strip().split("\n"):
                if ":" in line:
                    col, dtype = line.split(":", 1)
                    dtype_dict[col.strip()] = dtype.strip()
    except:
        dtype_dict = None
    
    # Preview button
    if st.button("👁️ Preview Data", type="primary"):
        with st.spinner("Reading file..."):
            try:
                # Reset file pointer
                uploaded_file.seek(0)
                
                df = pd.read_csv(
                    uploaded_file,
                    sep=delimiter,
                    encoding=encoding,
                    header=header,
                    skiprows=skip_rows,
                    na_values=na_values,
                    dtype=dtype_dict,
                    nrows=preview_rows + 5,  # Extra rows for validation
                    thousands=',' if thousands_sep else None,
                    decimal=decimal_sep
                )
                
                st.session_state.current_df = df
                st.session_state.file_info = {
                    'name': uploaded_file.name,
                    'rows': len(df),
                    'cols': len(df.columns),
                    'delimiter': delimiter,
                    'encoding': encoding
                }
                
                st.success(f"✅ Loaded **{len(df)} rows × {len(df.columns)} columns**")
                st.dataframe(df.head(preview_rows), use_container_width=True)
                
                # Data summary
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Rows", len(df))
                col2.metric("Columns", len(df.columns))
                col3.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                col4.metric("Non-null", f"{df.count().sum()}")
                
            except Exception as e:
                st.error(f"❌ Error reading file: **{str(e)}**")
                st.info("💡 Try different delimiter, encoding, or check advanced options")
    
    # Conversion section (if data loaded)
    if 'current_df' in st.session_state:
        st.markdown("---")
        st.subheader("📥 Convert & Download")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            output_format = st.selectbox(
                "Output format",
                ["csv", "excel", "json", "parquet"],
                help="Parquet requires pyarrow/fastparquet"
            )
        
        with col2:
            csv_options = st.expander("CSV Options", expanded=False)
            with csv_options:
                csv_delimiter = st.selectbox("CSV delimiter", [",", ";", "\t", "|"])
                csv_encoding = st.selectbox("CSV encoding", ['utf-8', 'latin-1'])
        
        if st.button("🚀 Convert & Download", type="primary", use_container_width=True):
            try:
                output = BytesIO()
                
                if output_format == "csv":
                    st.session_state.current_df.to_csv(
                        output, 
                        index=False,
                        sep=csv_delimiter,
                        encoding=csv_encoding
                    )
                    filename = st.session_state.file_info['name'].rsplit('.', 1)[0] + '_converted.csv'
                
                elif output_format == "excel":
                    st.session_state.current_df.to_excel(output, index=False, engine='openpyxl')
                    filename = st.session_state.file_info['name'].rsplit('.', 1)[0] + '_converted.xlsx'
                
                elif output_format == "json":
                    st.session_state.current_df.to_json(output, orient='records', indent=2)
                    filename = st.session_state.file_info['name'].rsplit('.', 1)[0] + '_converted.json'
                
                elif output_format == "parquet":
                    st.session_state.current_df.to_parquet(output, index=False)
                    filename = st.session_state.file_info['name'].rsplit('.', 1)[0] + '_converted.parquet'
                
                output.seek(0)
                st.download_button(
                    label="📥 Download Converted File",
                    data=output.getvalue(),
                    file_name=filename,
                    mime="application/octet-stream"
                )
                
                # Add to history
                st.session_state.conversion_history.append({
                    'input': st.session_state.file_info['name'],
                    'output': filename,
                    'rows': len(st.session_state.current_df),
                    'timestamp': pd.Timestamp.now().strftime('%H:%M:%S')
                })
                
                st.success(f"🎉 Converted **{st.session_state.file_info['name']}** → **{filename}**")
                
            except Exception as e:
                st.error(f"❌ Conversion error: **{str(e)}**")
    
    # Help tips
    with st.expander("💡 Common Issues & Solutions"):
        st.markdown("""
        **Delimiter not working?**
        - Use "Custom" and enter exact character (e.g. `~`, `#`)
        - Check first few lines of your file
        - Try different encodings
        
        **Unicode errors?**
        - Try `latin-1` or `cp1252` encoding
        - Use "Advanced Options" for specific columns
        
        **Wrong columns?**
        - Adjust "Skip rows" or "Header" settings
        - Check delimiter matches your file
        """)
