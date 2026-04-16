import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd

from utils.nlp_extractor import extract_skills_from_text
from utils.ml_comparator import calculate_skill_gap
from utils.dataset_loader import load_dataset_skills

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load global dataset defaults if they exist
job_data_cache = None

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume uploaded'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    
    target_role = request.form.get('target_role', 'Data Scientist')
    
    required_skills = load_dataset_skills(target_role)
    
    # Extract directly from memory stream (Vercel Serverless safe)
    candidate_skills = extract_skills_from_text(file.stream, ext=ext)
    
    gap_analysis = calculate_skill_gap(candidate_skills, required_skills)
    
    return jsonify(gap_analysis)

if __name__ == '__main__':
    app.run(debug=True)
