import streamlit as st
import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Scenario prompts 
SCENARIOS = {
    "👥 Citizens": {
        "instruction": "Rewrite the summary focusing on how this policy impacts everyday citizens, emphasizing accessibility, fairness, and public benefits.",
        "color": "#f0f4f8"  
    },
    "💼 Businesses": {
        "instruction": "Rewrite the summary focusing on how this policy affects businesses, highlighting compliance, opportunities, and economic growth.",
        "color": "#e8eaf6"  
    },
    "🏛️ Government": {
        "instruction": "Rewrite the summary focusing on government priorities, emphasizing regulation, governance, and national development.",
        "color": "#e3f2fd"  
    },
    "👷 Sector Workforce": {
        "instruction": "Rewrite the summary focusing on the workforce in the sector, highlighting training, employment opportunities, and skill development.",
        "color": "#fffde7"  
    }
}

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

def generate_summary(text, sentences_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, sentences_count)
    return " ".join([str(sentence) for sentence in summary_sentences])

def adapt_summary(summary, scenario_instruction):
    return f"{scenario_instruction}\n\n{summary}"

# Streamlit 
st.set_page_config(page_title="📑 AI Policy Summarizer & Scenario Generator", layout="wide")

#  background 
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f9f9fb; /* clean light gray background */
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
h1, h2, h3, h4 {
    font-family: 'Segoe UI', sans-serif;
    color: #2c3e50;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("📑 AI Policy Summarizer & Scenario Generator")
st.markdown("Upload a policy document and generate summaries tailored for different audiences.")

uploaded_file = st.file_uploader("📂 Upload Policy PDF", type=["pdf"])
input_text = st.text_area("✍️ Or paste policy text here:")

if uploaded_file or input_text:
    if uploaded_file:
        policy_text = extract_text_from_pdf(uploaded_file)
    else:
        policy_text = input_text

    st.subheader("🔍 Policy Summary 📜")
    summary = generate_summary(policy_text)
    st.success(summary)

    st.subheader("🎯 Scenario-Based Drafts")
    scenario_choice = st.selectbox("👉 Choose a scenario:", list(SCENARIOS.keys()))

    if scenario_choice:
        data = SCENARIOS[scenario_choice]
        adapted = adapt_summary(summary, data["instruction"])
        st.markdown(
            f"<div style='background-color:{data['color']};padding:15px;border-radius:8px;border:1px solid #dcdcdc'>"
            f"<h4>{scenario_choice}</h4><p>{adapted}</p></div>",
            unsafe_allow_html=True
        )
