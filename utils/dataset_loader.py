import os
import pandas as pd

from utils.nlp_extractor import COMMON_SKILLS

# Define a fallback dictionary for required skills per job
# This acts as the baseline before the csv datasets are uploaded.
FALLBACK_JOB_SKILLS = {
    "Data Scientist": ["python", "machine learning", "statistics", "sql", "data visualization", "pandas", "numpy", "scikit-learn"],
    "Software Engineer": ["python", "java", "c++", "javascript", "git", "problem solving", "agile", "sql"],
    "Web Developer": ["html", "css", "javascript", "react", "node.js", "git", "mongodb"],
    "HR Manager": ["communication", "leadership", "time management", "problem solving", "project management"],
    "Product Manager": ["agile", "scrum", "project management", "leadership", "communication", "problem solving", "data analysis"],
    "Marketing Specialist": ["communication", "data analysis", "html", "css", "data visualization", "time management"],
    "Financial Analyst": ["sql", "pandas", "numpy", "statistics", "data analysis", "problem solving", "communication"],
    "Cybersecurity Analyst": ["python", "sql", "problem solving", "communication", "time management", "linux", "networking"],
    "Cloud Engineer": ["aws", "azure", "gcp", "docker", "kubernetes", "python", "linux", "problem solving"],
    "UI/UX Designer": ["html", "css", "javascript", "communication", "data visualization", "problem solving", "figma", "sketch"],
    "DevOps Engineer": ["aws", "docker", "kubernetes", "jenkins", "git", "gitlab", "python", "linux", "agile"],
    "Data Analyst": ["sql", "python", "data visualization", "statistics", "pandas", "communication", "problem solving"]
}

def load_dataset_skills(target_role):
    """
    Attempts to load required skills from the 'Job Descriptions' dataset.
    If the dataset is unavailable, it falls back to a predefined dictionary.
    """
    dataset_path = os.path.join('data', 'Job Descriptions.csv')
    
    if os.path.exists(dataset_path):
        try:
            df = pd.read_csv(dataset_path)
            # In Kaggle's Job Descriptions dataset, there are columns for Job Title, Skills, etc.
            # Assuming columns like 'Job Title' and 'skills' exist
            # Note: you might need to adjust column names based on the exact CSV structure
            role_regex = f"(?i){target_role}"
            role_data = df[df['Job Title'].str.contains(role_regex, na=False)]
            
            if not role_data.empty:
                # Concatenate all skills listed for this role
                # For simplicity, if we find matching rows, we combine their skills
                all_skills_text = " ".join(role_data['skills'].dropna().astype(str).tolist())
                all_skills_text = all_skills_text.lower()
                
                # Intersect with our known vocabulary
                extracted_skills = set()
                for skill in COMMON_SKILLS:
                    if skill in all_skills_text:
                        extracted_skills.add(skill)
                        
                if extracted_skills:
                    return list(extracted_skills)
        except Exception as e:
            print(f"Error reading dataset: {e}. Falling back to defaults.")
            
    # Fallback if csv read fails or file doesn't exist
    # If the exact role isn't found, find the closest one or return generic tech skills
    for key in FALLBACK_JOB_SKILLS:
        if key.lower() in target_role.lower() or target_role.lower() in key.lower():
            return FALLBACK_JOB_SKILLS[key]
            
    # Absolute fallback
    return ["communication", "problem solving"]
