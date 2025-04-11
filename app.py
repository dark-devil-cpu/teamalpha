import streamlit as st
import pdfplumber  # More accurate than PyPDF2
import docx
import io
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

# ========== CONFIGURATION ==========
@st.cache_data
def load_config():
    """Load skills configuration from JSON file"""
    config_path = Path("skills_config.json")
    if not config_path.exists():
        # Default configuration if file doesn't exist
        return {
            "role_skills": {
                "Data Analyst": {
                    "Python": ["python", "py"],
                    "SQL": ["sql", "mysql"],
                    "Excel": ["excel"],
                    "Power BI": ["powerbi", "power bi"],
                    "Tableau": ["tableau"]
                },
                "Web Developer": {
                    "HTML": ["html"],
                    "CSS": ["css"],
                    "JavaScript": ["javascript", "js"]
                }
            },
            "learning_resources": {
                "Python": "https://learnpython.org",
                "SQL": "https://www.w3schools.com/sql/"
            }
        }
    with open(config_path) as f:
        return json.load(f)

CONFIG = load_config()
ROLE_SKILLS = CONFIG["role_skills"]
LEARNING_RESOURCES = CONFIG["learning_resources"]

# ========== FILE PROCESSING ==========
def extract_text_from_file(uploaded_file) -> str:
    """Universal text extractor for PDF, DOCX, and TXT files"""
    try:
        file_type = uploaded_file.type
        
        if file_type == "application/pdf":
            with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            return "\n".join(para.text for para in doc.paragraphs if para.text)
        
        else:  # Plain text
            return uploaded_file.read().decode("utf-8")
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return ""

# ========== SKILL ANALYSIS ==========
def analyze_skills(text: str, role: str) -> Tuple[List[str], List[str]]:
    """Analyze text for skills with synonym support"""
    if role not in ROLE_SKILLS:
        return [], []
    
    found_skills = []
    required_skills = ROLE_SKILLS[role]
    
    for skill_name, skill_variants in required_skills.items():
        if any(re.search(rf"\b{re.escape(variant)}\b", text, re.IGNORECASE) 
               for variant in skill_variants):
            found_skills.append(skill_name)
    
    missing_skills = [s for s in required_skills if s not in found_skills]
    return found_skills, missing_skills

# ========== STREAMLIT UI ==========
def main():
    st.set_page_config(
        page_title="Ultimate Resume Analyzer", 
        page_icon="🧠", 
        layout="wide"
    )
    
    st.title("🧠 Ultimate Resume Analyzer")
    st.markdown("Upload your resume to identify skill gaps and learning resources")
    
    # Sidebar controls
    with st.sidebar:
        st.header("Settings")
        selected_role = st.selectbox(
            "Select Target Role",
            options=sorted(ROLE_SKILLS.keys()),
            index=0
        )
        
        st.header("Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose file",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=False,
            help="Supports PDF, Word, and Text files"
        )
    
    # Main analysis workflow
    if uploaded_file and st.button("Analyze Resume"):
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_file(uploaded_file)
            
            if not resume_text.strip():
                st.warning("The uploaded file appears to be empty")
                return
                
            found_skills, missing_skills = analyze_skills(resume_text, selected_role)
            
            # Display results in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("✅ Your Current Skills")
                if found_skills:
                    for skill in found_skills:
                        st.success(f"✔️ {skill}")
                else:
                    st.warning("No matching skills found in your resume")
            
            with col2:
                st.subheader("⚠️ Recommended Skills to Learn")
                if missing_skills:
                    for skill in missing_skills:
                        st.error(f"❌ {skill}")
                        if skill in LEARNING_RESOURCES:
                            st.markdown(
                                f"📚 [Learn {skill}]({LEARNING_RESOURCES[skill]})",
                                help=f"Resource for {skill}"
                            )
                else:
                    st.success("🎉 You have all required skills for this role!")
    
    # Footer
    st.markdown("---")
    st.caption("© 2023 Resume Analyzer | For educational purposes only")

if __name__ == "__main__":
    main()
