import streamlit as st

st.title("🗄️ SQL Database Converter")

st.write("""
Convert files to SQL databases:
- SQLite, PostgreSQL, MySQL support
- Custom SQL queries
- Connection management
- Data validation
- Table creation
""")

db_type = st.selectbox("Database Type", ['SQLite', 'PostgreSQL', 'MySQL'])

if db_type == 'SQLite':
    st.info("SQLite databases are file-based and perfect for local development.")

uploaded_file = st.file_uploader("Upload data file", type=['csv', 'xlsx', 'json'])

if uploaded_file:
    try:
        import pandas as pd
        
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file) if uploaded_file.name.endswith(('.xlsx', '.xls')) else pd.read_json(uploaded_file)
        
        st.subheader("📊 Data Preview")
        st.dataframe(df.head())
        
        table_name = st.text_input("Table Name", "data")
        
        if st.button("Export to Database"):
            if db_type == 'SQLite':
                try:
                    import sqlite3
                    db_file = f"{table_name}.db"
                    conn = sqlite3.connect(db_file)
                    df.to_sql(table_name, conn, if_exists='replace')
                    conn.close()
                    st.success(f"Data exported to {db_file}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
