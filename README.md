# 🐼 Streamlit File Format Converter

A production-ready multi-page Streamlit application for converting between 20+ file formats.

## 🚀 Features

- **8 Conversion Modules**: CSV, Excel, JSON, Parquet, SQL, Batch, Settings, Help
- **20+ Format Support**: CSV, Excel, JSON, Parquet, Feather, HDF5, Pickle, SQL
- **Advanced Options**: Custom delimiters, encoding detection, data preview, batch processing
- **Production Ready**: Error handling, session state, caching, Docker support

## 📦 Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📚 Project Structure

```
file_converter_app/
├── app.py                    # Main entry point
├── requirements.txt          # Dependencies
├── .streamlit/config.toml   # Configuration
├── pages/                    # Converter pages
│   ├── 1_CSV_Converter.py
│   ├── 2_Excel_Converter.py
│   ├── 3_JSON_Converter.py
│   ├── 4_Parquet_Feather.py
│   ├── 5_SQL_Converter.py
│   ├── 6_Batch_Conversion.py
│   ├── 7_Settings.py
│   └── 8_Help_Reference.py
└── utils/                    # Utility modules
    ├── conversion_utils.py
    ├── format_handlers.py
    ├── encoding_detector.py
    ├── error_handler.py
    └── file_manager.py
```

## 🔄 Converters

### 1. CSV/Text Converter
- Multiple delimiter support
- Encoding selection
- Skip rows, header configuration
- Data type specification

### 2. Excel Converter
- Multiple sheet support
- Merge sheets option
- Range specification
- Batch conversion

### 3. JSON Converter
- Multiple orientations (records, split, index)
- Nested JSON flattening
- JSONL handling
- Date parsing

### 4. Parquet/Feather
- Engine selection (PyArrow/fastparquet)
- Compression options (snappy, gzip, brotli)
- Performance comparison
- Memory tracking

### 5. SQL Converter
- Database support (SQLite, PostgreSQL, MySQL)
- Custom SQL queries
- Connection testing
- Chunk processing

### 6. Batch Conversion
- Multiple file upload
- Parallel processing
- Zip archive output
- Error reporting

## ⚙️ Configuration

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Font settings
- Upload size limits
- Logger level

## 🌐 Deployment

### Streamlit Cloud (Free)
1. Push to GitHub
2. Sign up at streamlit.io
3. Connect repository
4. Deploy!

### Docker
```bash
docker build -t file-converter .
docker run -p 8501:8501 file-converter
```

## 📖 Usage

1. Select a converter from the sidebar
2. Upload your file
3. Configure conversion options
4. Preview data
5. Download converted file

## 🔧 Troubleshooting

- **Port already in use**: `streamlit run app.py --server.port 8502`
- **Encoding errors**: Use auto-detect or select correct encoding
- **Large files**: Use batch processing for multiple files

## 📄 License

MIT License - feel free to use and modify!

## 🎉 Happy Converting!
