import os
import spacy
from PyPDF2 import PdfReader

# Load Spacy model safely
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading en_core_web_sm...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# A sample vocabulary of common HR / Tech skills to look out for
# This will be enhanced by the dataset loader if needed.
COMMON_SKILLS = [
    "python", "java", "c++", "c#", "javascript", "react", "angular", "vue", "node.js",
    "html", "css", "sql", "nosql", "mongodb", "postgresql", "mysql", "machine learning",
    "artificial intelligence", "deep learning", "nlp", "computer vision", "scikit-learn",
    "tensorflow", "pytorch", "keras", "pandas", "numpy", "matplotlib", "seaborn",
    "data analysis", "data visualization", "statistics", "data mining", "big data",
    "hadoop", "spark", "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
    "git", "github", "gitlab", "agile", "scrum", "project management", "leadership",
    "communication", "problem solving", "teamwork", "time management", "flask", "django"
]

def extract_text_from_file(filepath):
    """Extracts raw text from pdf or txt files."""
    ext = os.path.splitext(filepath)[1].lower()
    text = ""
    if ext == ".pdf":
        reader = PdfReader(filepath)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + " "
    elif ext == ".txt":
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        print(f"Unsupported file format: {ext}")
    return text

def extract_skills_from_text(filepath):
    """Reads the file and extracts skills using SpaCy based NLP rules."""
    text = extract_text_from_file(filepath)
    if not text:
        return []
    
    # Process text
    doc = nlp(text.lower())
    
    extracted_skills = set()
    
    # Basic token matching based on vocabulary
    # Also extract noun chunks that might represent skills
    for token in doc:
        # Check against common skill dictionary
        word = token.text.strip()
        if word in COMMON_SKILLS:
            extracted_skills.add(word)
            
    # Also check full noun chunks for multi-word skills like "machine learning"
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.strip()
        if chunk_text in COMMON_SKILLS:
            extracted_skills.add(chunk_text)
            
    return list(extracted_skills)
