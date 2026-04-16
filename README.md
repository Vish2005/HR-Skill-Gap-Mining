# 🧠 HR Skill Gap Mining for 2026

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-API-black?logo=flask)
![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange)
![Spacy](https://img.shields.io/badge/NLP-SpaCy-green)
![Tailwind](https://img.shields.io/badge/CSS-Tailwind-38B2AC?logo=tailwind-css)

An Intelligent Human Resources Dashboard equipped with **Natural Language Processing (NLP)** and **Machine Learning (ML)** to automatically analyze candidate resumes, extract professional skills, and compute dynamic skill gaps against target job requirements. 

Built with a stunning glassmorphism user interface designed for 2026.

🚀 **Live Demo:** [https://hr-skill-gap-mining.vercel.app](https://hr-skill-gap-mining.vercel.app)

---

## ✨ Key Features

- **Automated Resume Parsing:** Upload `.pdf` or `.txt` resumes. The backend utilizes `PyPDF2` to read raw data.
- **Intelligent NLP Extraction:** Employs `spaCy` to dynamically extract hard and soft skills based on an internal terminology system.
- **Accurate ML Skill Matching:** Avoids standard TF-IDF pitfalls by stripping unrelated hobbies and utilizing a hybrid scoring mechanism (Exact HR Proportion + ML Weighted TF-IDF Cosine Similarity) to ensure extremely accurate fit calculations.
- **"Upskilling Path" Generation:** Directly prescribes missing skills that the candidate must learn to be competitive for the target role.
- **Premium Glassmorphism Dashboard:** Responsive UI built with pure Tailwind CSS and dynamic asynchronous feedback loops via JavaScript.
- **24 Test Candidates Included:** Comes equipped with "Good" and "Poor" mock candidates across 12 distinct job roles to instantly test the Machine Learning algorithms without external data!

---

## 🛠️ Technology Stack

| Architecture Layer | Tools Utilized |
| :--- | :--- |
| **Backend Framework** | Python, Flask |
| **NLP & AI Engine** | SpaCy (`en_core_web_sm`) |
| **Machine Learning** | Scikit-Learn (`TfidfVectorizer`, `cosine_similarity`) |
| **Data Processing** | Pandas, PyPDF2 |
| **Frontend UI** | HTML5, Tailwind CSS, JavaScript |
| **Visualizations** | Chart.js (Doughnut Distributions) |

---

## 🚀 Quick Setup Guide

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/HR-Skill-Gap-Mining.git
   cd HR-Skill-Gap-Mining
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```

5. **Access the Dashboard:**
   Open your browser and navigate to `http://127.0.0.1:5000`

---

## 🗂️ Incorporating Kaggle Datasets
This tool is designed to utilize real-world job posting data from **Kaggle**. 
* If you have downloaded the **"Job Descriptions / Job Skills Dataset"**, simply place the CSV file into the `data/` directory named exactly as `Job Descriptions.csv`.
* If no dataset is found, the application intelligently falls back to an internal skills dictionary to ensure uninterrupted operation!

---

## 📸 Usage

To test the ML logic instantly, launch the app and upload any of the 24 text files generated inside the `sample_resumes/` folder!
