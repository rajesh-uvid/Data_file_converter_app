import streamlit as st

st.title("🔄 Batch Conversion")

st.write("""
Convert multiple files at once:
- Drag and drop support
- Same parameters for all files
- Parallel processing
- Batch summary
- Error reporting
""")

uploaded_files = st.file_uploader("Upload multiple files", accept_multiple_files=True)

if uploaded_files:
    st.subheader("📁 Files to Convert")
    for file in uploaded_files:
        st.write(f"• {file.name}")
    
    output_format = st.selectbox("Output Format", ['CSV', 'Excel', 'JSON', 'Parquet'])
    
    if st.button("Convert All"):
        try:
            import pandas as pd
            
            for file in uploaded_files:
                df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
                
                if output_format == 'CSV':
                    output = df.to_csv(index=False)
                    st.download_button(f"📥 {file.name.split('.')[0]}.csv", output, f"{file.name.split('.')[0]}.csv")
                elif output_format == 'JSON':
                    output = df.to_json(orient='records')
                    st.download_button(f"📥 {file.name.split('.')[0]}.json", output, f"{file.name.split('.')[0]}.json")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
