# ATS-Resume

ATS-Resume is a Streamlit-based web application that helps users optimize their resumes for Applicant Tracking Systems (ATS). The application analyzes resumes against job descriptions and provides feedback on matching percentages, missing keywords, profile summaries, and suggested changes.

## Features

- Upload PDF resumes for analysis
- Input job descriptions for comparison
- Get detailed feedback on resume matching
- View missing keywords, profile summaries, and suggested changes
- Download updated resume as a PDF

## Requirements

- Docker
- Python 3.11
- Streamlit 1.20.0
- google-generativeai 0.4.0
- PyPDF2 3.0.0
- python-dotenv 1.0.0
- fpdf 1.7.2

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/ATS-Resume.git
   cd ATS-Resume
   ```

2. Create a file with your Google API key:
   ```env
   GOOGLE_API_KEY="your_google_api_key"
   ```

## Usage

### Using Docker

1. Build the Docker image:

   ```sh
   docker build -t ats-resume .
   ```

2. Run the Docker container:

   ```sh
   docker run -p 8501:8501 --env-file .env ats-resume
   ```

3. Open your web browser and go to `http://localhost:8501` to access the application.

### Without Docker

1. Install the required Python packages:

   ```sh
   pip install -r requirment.txt
   pip install numpy==1.23.5 pandas==1.5.3
   ```

2. Run the Streamlit application:

   ```sh
   streamlit run app.py
   ```

3. Open your web browser and go to `http://localhost:8501` to access the application.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- Developed with 💻 by Harshit Jain 🚀🚀🚀🚀
