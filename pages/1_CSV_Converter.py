import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from io import BytesIO

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

st.title("📄 CSV/Text File Converter")
st.markdown("**Advanced CSV/TSV/TXT conversion with custom delimiter support**")

# ---- Session state init ----
if "conversion_history" not in st.session_state:
    st.session_state.conversion_history = []

if "file_bytes" not in st.session_state:
    st.session_state.file_bytes = None

if "current_df" not in st.session_state:
    st.session_state.current_df = None

if "preview_df" not in st.session_state:
    st.session_state.preview_df = None

if "file_info" not in st.session_state:
    st.session_state.file_info = {}

# File upload
uploaded_file = st.file_uploader(
    "Upload CSV, TSV, or text file",
    type=["csv", "txt", "tsv", "dat"],
    help="Supports CSV, TSV, delimited text files",
)

# Persist uploaded file bytes so reruns still have full content
if uploaded_file is not None:
    st.session_state.file_bytes = uploaded_file.getvalue()
    st.session_state.file_info["name"] = uploaded_file.name

if st.session_state.file_bytes is not None:
    # Recreate a file-like object from bytes for each read
    file_buffer = BytesIO(st.session_state.file_bytes)
    file_size = len(st.session_state.file_bytes)
    st.info(
        f"📁 File: **{st.session_state.file_info.get('name', 'uploaded_file')}** | "
        f"Size: **{file_size/1024:.1f} KB**"
    )

    # Configuration - 3 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        # Delimiter with manual input
        delimiter_type = st.radio(
            "Delimiter Type",
            ["Common", "Custom"],
            horizontal=True,
        )

        if delimiter_type == "Common":
            delimiter = st.selectbox(
                "Select delimiter",
                [",", "\t", ";", "|", ":", " ", "\\n"],
                index=0,
                format_func=lambda x: f"{x} ({'tab' if x == '\t' else x})",
            )
            if delimiter == "\\n":
                delimiter = "\n"
            manual_delimiter = None
        else:
            manual_delimiter = st.text_input(
                "Enter custom delimiter (single character)",
                placeholder="e.g. ~, #, ^",
                max_chars=1,
                help="Enter exactly one character",
            )
            delimiter = manual_delimiter if manual_delimiter else ","

    with col2:
        encoding = st.selectbox(
            "Encoding",
            ["utf-8", "latin-1", "iso-8859-1", "cp1252", "utf-16"],
            index=0,
        )

        header_option = st.radio(
            "Header",
            ["First row", "No header", "Row number"],
            horizontal=True,
            key="header_radio",
        )

        if header_option == "First row":
            header = 0
        elif header_option == "No header":
            header = None
        else:  # "Row number"
            header = 0  # keep as header row; use index later if needed

    with col3:
        skip_rows = st.number_input(
            "Skip first rows", min_value=0, value=0, step=1
        )
        preview_rows = st.number_input(
            "Preview rows", min_value=1, max_value=50, value=10, step=1
        )

    # Advanced options expander
    with st.expander("⚙️ Advanced Options", expanded=False):
        col1_adv, col2_adv, col3_adv = st.columns(3)

        with col1_adv:
            na_values = st.text_area(
                "Missing values to treat as NA",
                value="NA,N/A,Null,Empty,-",
                height=60,
                help="Comma-separated values",
            ).split(",")

        with col2_adv:
            dtype_str = st.text_area(
                "Column data types (col:type)",
                value="",
                height=60,
                placeholder="id:int64\ndate:datetime64[ns]",
                help="Format: column_name:data_type",
            )

        with col3_adv:
            thousands_sep = st.checkbox("Thousands separator", value=False)
            decimal_sep = st.text_input(
                "Decimal separator", value=".", max_chars=1
            )

    # Convert options to parameters
    try:
        na_values = [v.strip() for v in na_values if v.strip()]
        dtype_dict = {}
        if dtype_str:
            for line in dtype_str.strip().split("\n"):
                if ":" in line:
                    col_name, dtype = line.split(":", 1)
                    dtype_dict[col_name.strip()] = dtype.strip()
    except Exception:
        dtype_dict = None

    # ---------- PREVIEW (top section) ----------
    if st.button("👁️ Preview Data", type="primary"):
        with st.spinner("Reading file for preview..."):
            try:
                file_buffer.seek(0)
                df_preview = pd.read_csv(
                    file_buffer,
                    sep=delimiter,
                    encoding=encoding,
                    header=header,
                    skiprows=skip_rows,
                    na_values=na_values,
                    dtype=dtype_dict or None,
                    nrows=int(preview_rows) + 5,  # only for preview
                    thousands="," if thousands_sep else None,
                    decimal=decimal_sep,
                )

                st.session_state.preview_df = df_preview
                st.session_state.file_info.update(
                    {
                        "rows": len(df_preview),
                        "cols": len(df_preview.columns),
                        "delimiter": delimiter,
                        "encoding": encoding,
                    }
                )

                st.success(
                    f"✅ Preview loaded: {len(df_preview)} rows × {len(df_preview.columns)} columns"
                )
                st.dataframe(
                    df_preview.head(int(preview_rows)), use_container_width=True
                )

                col1_m, col2_m, col3_m, col4_m = st.columns(4)
                col1_m.metric("Preview rows", len(df_preview))
                col2_m.metric("Columns", len(df_preview.columns))
                col3_m.metric(
                    "Memory",
                    f"{df_preview.memory_usage(deep=True).sum() / 1024:.1f} KB",
                )
                col4_m.metric("Non-null", f"{df_preview.count().sum()}")

            except Exception as e:
                st.error(f"❌ Error reading file: **{str(e)}**")
                st.info(
                    "💡 Try different delimiter, encoding, or check advanced options"
                )

    # ---------- CONVERSION & PREVIEW ----------
    st.markdown("---")
    st.subheader("📥 Convert & Download")

    col1_conv, col2_conv = st.columns([1, 2])

    with col1_conv:
        output_format = st.selectbox(
            "Output format",
            ["csv", "excel", "json", "parquet"],
            help="Parquet requires pyarrow/fastparquet",
        )

    with col2_conv:
        csv_options = st.expander("CSV Options", expanded=False)
        with csv_options:
            csv_delimiter = st.selectbox(
                "CSV delimiter", [",", ";", "\t", "|"]
            )
            csv_encoding = st.selectbox(
                "CSV encoding", ["utf-8", "latin-1"]
            )

    if st.button("🚀 Convert & Download", type="primary", use_container_width=True):
        try:
            # Always read FULL dataset for conversion (no nrows)
            full_buffer = BytesIO(st.session_state.file_bytes)
            full_buffer.seek(0)

            df_full = pd.read_csv(
                full_buffer,
                sep=delimiter,
                encoding=encoding,
                header=header,
                skiprows=skip_rows,
                na_values=na_values,
                dtype=dtype_dict or None,
                thousands="," if thousands_sep else None,
                decimal=decimal_sep,
            )

            st.session_state.current_df = df_full
            st.session_state.file_info.update(
                {
                    "rows": len(df_full),
                    "cols": len(df_full.columns),
                    "delimiter": delimiter,
                    "encoding": encoding,
                }
            )

            # --- Preview in Convert section ---
            st.success(
                f"✅ Full data loaded: {len(df_full)} rows × {len(df_full.columns)} columns"
            )
            st.markdown("**Preview of converted data:**")
            st.dataframe(
                df_full.head(int(preview_rows)), use_container_width=True
            )

            col1_c, col2_c, col3_c, col4_c = st.columns(4)
            col1_c.metric("Total rows", len(df_full))
            col2_c.metric("Columns", len(df_full.columns))
            col3_c.metric(
                "Memory",
                f"{df_full.memory_usage(deep=True).sum() / 1024:.1f} KB",
            )
            col4_c.metric("Non-null", f"{df_full.count().sum()}")

            # --- Build output for download ---
            output = BytesIO()

            if output_format == "csv":
                df_full.to_csv(
                    output,
                    index=False,
                    sep=csv_delimiter,
                    encoding=csv_encoding,
                )
                filename = (
                    st.session_state.file_info["name"].rsplit(".", 1)[0]
                    + "_converted.csv"
                )

            elif output_format == "excel":
                df_full.to_excel(output, index=False, engine="openpyxl")
                filename = (
                    st.session_state.file_info["name"].rsplit(".", 1)[0]
                    + "_converted.xlsx"
                )

            elif output_format == "json":
                df_full.to_json(output, orient="records", indent=2)
                filename = (
                    st.session_state.file_info["name"].rsplit(".", 1)[0]
                    + "_converted.json"
                )

            elif output_format == "parquet":
                df_full.to_parquet(output, index=False)
                filename = (
                    st.session_state.file_info["name"].rsplit(".", 1)[0]
                    + "_converted.parquet"
                )

            output.seek(0)
            st.download_button(
                label="📥 Download Converted File",
                data=output.getvalue(),
                file_name=filename,
                mime="application/octet-stream",
            )

            st.session_state.conversion_history.append(
                {
                    "input": st.session_state.file_info["name"],
                    "output": filename,
                    "rows": len(df_full),
                    "timestamp": pd.Timestamp.now().strftime("%H:%M:%S"),
                }
            )

            st.success(
                f"🎉 Converted **{st.session_state.file_info['name']}** "
                f"→ **{filename}** with {len(df_full)} rows"
            )

        except Exception as e:
            st.error(f"❌ Conversion error: **{str(e)}**")

    # Help tips
    with st.expander("💡 Common Issues & Solutions"):
        st.markdown(
            """
**Delimiter not working?**
- Use "Custom" and enter exact character (e.g. `~`, `#`).
- Check first few lines of your file.
- Try different encodings.

**Unicode errors?**
- Try `latin-1` or `cp1252` encoding.
- Use "Advanced Options" for specific columns.

**Wrong columns?**
- Adjust "Skip rows" or "Header" settings.
- Check delimiter matches your file.
"""
        )
else:
    st.info("👆 Upload a CSV/TXT/TSV file to begin.")
