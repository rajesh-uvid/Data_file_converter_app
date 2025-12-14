import streamlit as st

st.title("⚙️ Settings & Preferences")

st.subheader("📊 Default Options")

col1, col2, col3 = st.columns(3)

with col1:
    encoding = st.selectbox("Default Encoding", ['utf-8', 'latin-1', 'iso-8859-1'])
    st.session_state.user_settings['default_encoding'] = encoding

with col2:
    delimiter = st.selectbox("Default Delimiter", [',', '\t', '|', ';'])
    st.session_state.user_settings['default_delimiter'] = delimiter

with col3:
    preview_rows = st.number_input("Preview Rows", min_value=1, max_value=100, value=5)
    st.session_state.user_settings['preview_rows'] = preview_rows

st.subheader("📁 File Settings")

max_size = st.slider("Max Upload Size (MB)", min_value=10, max_value=500, value=500)

st.subheader("🎨 Display Options")

col1, col2 = st.columns(2)

with col1:
    wide_mode = st.checkbox("Wide Layout", value=True)

with col2:
    show_stats = st.checkbox("Show Statistics", value=True)

if st.button("Save Settings"):
    st.success("Settings saved!")
