import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
from fpdf import FPDF
import logging

# Load environment variables from .env file
load_dotenv()

# Configure Google Gemini API with the API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Ensure API key is loaded
if not os.getenv("GOOGLE_API_KEY"):
    st.error("API Key is missing. Please set it in your environment variables.")

# Logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Function to fetch Gemini response using gemini-2.0 Flash model
def get_gemini_response(input):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # Use gemini-2.0 Flash model
        response = model.generate_content(input)
        logging.debug(f"API Response: {response}")
        return response.text
    except Exception as e:
        logging.error(f"Error during API call: {e}")
        st.error("Failed to fetch response from the Gemini API.")
        return None

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template for ATS analysis
input_prompt = """
Act like a highly skilled ATS (Application Tracking System) expert specializing in analyzing resumes.
Consider the job market to be highly competitive and evaluate the resume based on the given job description.
Provide:
- JD Match Percentage
- Missing Keywords
- Profile Summary
- Changes Needed

Input Data:
Resume: {text}
Job Description: {jd}

Expected Output Format:
{
    "JD Match": "% match",
    "MissingKeywords": ["keywords"],
    "Profile Summary": "summary",
    "ChangesNeeded": "changes"
}
"""

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #1e1e2f; /* Dark background */
        color: #ffffff; /* White text color */
    }
    .stApp {
        background-color: #1e1e2f; /* Dark background for the app */
        color: #ffffff; /* White text color */
    }
    .stTextInput, .stTextArea, .stFileUploader {
        border-radius: 10px; /* Rounded corners */
        padding: 15px; /* Add padding */
        border: 1px solid #ccc; /* Light border color */
        background-color: #2e2e4f; /* Slightly lighter background */
        color: #ffffff; /* White text color */
    }
    .stButton button {
        background-color: #00c9a7; /* Teal background */
        color: #fff; /* White text */
        border-radius: 25px; /* Rounded corners */
        padding: 10px 15px; /* Padding around text */
        transition: all 0.3s ease; /* Smooth transition for hover effect */
        font-size: 16px; /* Text size */
    }
    .stButton button:hover {
        background-color: #009b82; /* Darker teal on hover */
        transform: scale(1.05); /* Slight zoom effect on hover */
    }
    .response-card {
        background-color: #32324c; /* Dark card background */
        padding: 15px; /* Padding inside the card */
        border-radius: 10px; /* Rounded corners */
        margin-bottom: 10px; /* Space between cards */
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.5); /* Card shadow */
    }
    h1 {
        color: #00c9a7; /* Teal color for titles */
        text-align: center; /* Center-align title */
    }
    .footer {
        text-align: center; /* Center-align footer text */
        font-size: 12px; /* Small font size */
        margin-top: 20px; /* Space above footer */
        color: #aaa; /* Light gray text */
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app
st.title("🚀 Smart ATS: Boost Your Resume 🚀")
st.write("Optimize your resume for ATS and maximize your chances of landing your dream job!")

# Input area for Job Description
jd = st.text_area("📋 Paste the Job Description:", placeholder="Enter the job description here...", height=150)

# Upload PDF Resume
uploaded_file = st.file_uploader("📎 Upload Your Resume (PDF only):", type="pdf")

# Load stored session data
if 'response_data' not in st.session_state:
    st.session_state.response_data = None

# Button to evaluate
submit = st.button("🔍 Analyze Resume")

if submit:
    if uploaded_file is not None:
        # Extract text and get response
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        st.session_state.response_data = json.loads(response)  # Store response in session state

# Display content based on button clicks
if st.session_state.response_data:
    response_data = st.session_state.response_data

    # Show JD Match
    st.markdown(f"<div class='response-card'><h3>✅ JD Match: {response_data['JD Match']}</h3></div>", unsafe_allow_html=True)

    # Show Missing Keywords
    if st.button("🔑 Show Missing Keywords"):
        if response_data["MissingKeywords"]:
            missing_keywords = ", ".join(response_data["MissingKeywords"])
            st.markdown(f"<div class='response-card'>{missing_keywords}</div>", unsafe_allow_html=True)
        else:
            st.success("No missing keywords found. 🎉")

    # Show Profile Summary
    if st.button("📝 Show Profile Summary"):
        st.markdown(f"<div class='response-card'>{response_data['Profile Summary']}</div>", unsafe_allow_html=True)

    # Show Changes Needed (as bullet points)
    if st.button("⚙️ What Changes Needed"):
        changes_needed = response_data["ChangesNeeded"]
        if isinstance(changes_needed, list):
            # Convert changes into bullet points
            bullet_points = "\n".join([f"• {change}" for change in changes_needed])
            st.markdown(f"<div class='response-card'>{bullet_points}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='response-card'>{changes_needed}</div>", unsafe_allow_html=True)

    # Download Updated Resume as PDF
    if uploaded_file:
        st.markdown("### 📥 Download Updated Resume:")

        # Ensure ChangesNeeded is a string, convert if necessary
        changes_needed = response_data["ChangesNeeded"]
        if isinstance(changes_needed, list):
            changes_needed = "\n".join([f"• {change}" for change in changes_needed])  # Join list items with bullet points

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, changes_needed)
        pdf_output = pdf.output(dest='S').encode('latin1')
        
        st.download_button(
            label="Download Updated Resume PDF",
            data=pdf_output,
            file_name="updated_resume.pdf",
            mime="application/pdf"
        )

# Footer
st.markdown("<div class='footer'>Developed with 💻 by Harshit Jain 🚀🚀🚀🚀</div>", unsafe_allow_html=True)
