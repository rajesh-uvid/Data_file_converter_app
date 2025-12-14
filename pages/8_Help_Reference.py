import streamlit as st

st.title("❓ Help & Reference")

st.subheader("🚀 Getting Started")

st.write("""
1. **Select a Converter**: Choose from 6 different converters in the sidebar
2. **Upload a File**: Click the upload button and select your file
3. **Configure Options**: Customize conversion settings (optional)
4. **Preview Data**: Review your data before conversion
5. **Download**: Click the download button for your desired format
""")

st.subheader("📚 Format Guide")

formats = {
    'CSV': 'Comma-separated values, universal format, text-based',
    'Excel': 'Microsoft Excel workbooks, multiple sheets, rich formatting',
    'JSON': 'JavaScript Object Notation, web-friendly, structured data',
    'Parquet': 'Columnar format, high performance, compression support',
    'Feather': 'Binary format, very fast I/O, cross-language support',
    'SQL': 'Database format, structured queries, production use',
}

for fmt, desc in formats.items():
    st.write(f"**{fmt}**: {desc}")

st.subheader("❓ FAQ")

with st.expander("What file size limit is there?"):
    st.write("Default limit is 500 MB. You can adjust this in Settings.")

with st.expander("What encodings are supported?"):
    st.write("UTF-8, Latin-1, ISO-8859-1, and auto-detection")

with st.expander("Can I convert multiple files?"):
    st.write("Yes! Use the Batch Conversion page to convert multiple files at once.")

with st.expander("Is my data secure?"):
    st.write("All conversions happen locally. No data is sent to external servers.")

st.subheader("🔗 Resources")

st.write("""
- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas Documentation](https://pandas.pydata.org/docs)
- [Apache Parquet](https://parquet.apache.org)
""")
