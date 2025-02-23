import streamlit as st
import pandas as pd
from utils import read_file, convert_df, clean_data, generate_visualizations, generate_ai_suggestions
import json
from streamlit_lottie import st_lottie
import requests

# Page config
st.set_page_config(
    page_title="Growth Mindset File Transformer",
    page_icon="🔄",
    layout="wide"
)

# Load custom CSS
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Load animations
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

transform_animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jtbfg2nb.json")
analyze_animation = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_qp1q7mct.json")

# App header
st.markdown('<h1 class="gradient-text">Growth Mindset File Transformer</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<h2 class="gradient-text">Settings</h2>', unsafe_allow_html=True)
    st_lottie(transform_animation, height=200)

    output_format = st.selectbox(
        "Select output format",
        ["csv", "xlsx", "json"]
    )

    cleaning_options = st.multiselect(
        "Select cleaning options",
        ["remove_duplicates", "drop_na", "fill_na"],
        default=[]
    )

    # Show message history in sidebar
    st.markdown('<h3 class="gradient-text">Message History</h3>', unsafe_allow_html=True)
    if st.session_state.messages:
        for msg in st.session_state.messages:
            st.text(msg)
    else:
        st.text("No previous messages")

    # Creator links and name at bottom of sidebar
    st.markdown("""
    <div class="creator-links">
        <a href="https://www.linkedin.com/in/syeda-farheen-zehra-648459268/" target="_blank" class="creator-link">LinkedIn Profile</a>
        <a href="mailto:farheen11099@gmail.com" class="creator-link">Email Me</a>
        <div>
            <span class="made-by-text">Made by:</span>
            <span class="creator-name">Syeda Farheen Zehra</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content
uploaded_file = st.file_uploader("Upload your file (CSV, Excel, or JSON)", 
                                type=['csv', 'xlsx', 'xls', 'json'])

if uploaded_file is not None:
    try:
        with st.spinner('Reading file...'):
            df = read_file(uploaded_file)
            # Add message to history
            st.session_state.messages.append(f"Uploaded file: {uploaded_file.name}")

        st.success('File uploaded successfully!')

        # Data preview
        st.markdown('<h3 class="gradient-text">Data Preview</h3>', unsafe_allow_html=True)
        st.dataframe(df.head())

        # Data cleaning
        if cleaning_options:
            with st.spinner('Cleaning data...'):
                df = clean_data(df, cleaning_options)
                # Add message to history
                st.session_state.messages.append(f"Applied cleaning options: {', '.join(cleaning_options)}")
            st.success('Data cleaned successfully!')

        # Visualizations
        st.markdown('<h3 class="gradient-text">Data Visualization</h3>', unsafe_allow_html=True)
        st_lottie(analyze_animation, height=200)

        visualizations = generate_visualizations(df)
        for viz_name, fig in visualizations.items():
            st.plotly_chart(fig, use_container_width=True)

        # AI Suggestions
        st.markdown('<h3 class="gradient-text">AI Suggestions</h3>', unsafe_allow_html=True)
        suggestions = generate_ai_suggestions(df)
        for suggestion in suggestions:
            st.info(suggestion)

        # File conversion and download
        st.markdown('<h3 class="gradient-text">Download Transformed File</h3>', unsafe_allow_html=True)

        converted_file = convert_df(df, output_format)

        if output_format == 'csv':
            st.download_button(
                "Download CSV",
                converted_file,
                f"transformed_file.csv",
                "text/csv",
                key='download-csv'
            )
        elif output_format == 'xlsx':
            st.download_button(
                "Download Excel",
                converted_file,
                f"transformed_file.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key='download-excel'
            )
        else:
            st.download_button(
                "Download JSON",
                converted_file,
                f"transformed_file.json",
                "application/json",
                key='download-json'
            )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # Add error message to history
        st.session_state.messages.append(f"Error: {str(e)}")

else:
    st.info("Please upload a file to begin transformation")