from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_skill_gap(candidate_skills, required_skills):
    """
    Compares candidate skills against required skills using Scikit-learn
    Calculates match percentage, missing skills, and recommendations.
    """
    if not required_skills:
        # If no required skills defined, return an empty profile or prompt.
        return {
            "match_percentage": 0,
            "missing_skills": [],
            "present_skills": candidate_skills,
            "recommendations": []
        }
        
    candidate_skills = [s.lower() for s in candidate_skills]
    required_skills = [s.lower() for s in required_skills]
    
    # Identify overlaps and gaps
    present_set = set(candidate_skills).intersection(set(required_skills))
    missing_set = set(required_skills).difference(set(candidate_skills))
    
    # Remove penalty for extra skills that the candidate has but the job doesn't require
    filtered_candidate_skills = [s for s in candidate_skills if s in set(required_skills)]
    
    if not filtered_candidate_skills:
        match_percentage = 0.0
    else:
        # Calculate base proportion match
        base_match = (len(present_set) / len(required_skills)) * 100
        
        # Calculate ML weighted match (TF-IDF emphasizes rarer/more important job skills)
        filtered_candidate_doc = " ".join(filtered_candidate_skills)
        required_doc = " ".join(required_skills)
        
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([required_doc, filtered_candidate_doc])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        ml_match = sim * 100
        
        # Blend the standard HR fraction (40%) with ML weighted importance (60%)
        # This yields a much more accurate percentage representation.
        match_percentage = round((base_match * 0.4) + (ml_match * 0.6), 2)
        
        # Ensure we don't go over 100% just in case of float rounding quirks
        match_percentage = min(match_percentage, 100.0)
        
    # Generate upskill recommendations (top missing skills)
    # In a real app, you could weight this by frequency/importance in the job dataset
    recommendations = list(missing_set)[:5] 

    return {
        "match_percentage": match_percentage,
        "present_skills": list(present_set),
        "missing_skills": list(missing_set),
        "recommendations": recommendations,
        "candidate_skills_extracted": candidate_skills
    }
