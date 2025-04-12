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
                "Python": ["python", "py", "pandas", "numpy"],
                "SQL": ["sql", "mysql", "postgresql", "sqlite"],
                "Excel": ["excel", "vlookup", "pivot tables"],
                "Power BI": ["powerbi", "power bi", "dax", "power query"],
                "Tableau": ["tableau", "tableau desktop"],
                "Statistics": ["statistics", "hypothesis testing", "regression"],
                "R": ["r programming", "r studio"],
                "Data Visualization": ["data viz", "visualization", "matplotlib", "seaborn"],
                "Machine Learning": ["machine learning", "ml", "supervised learning"],
                "Big Data": ["hadoop", "spark", "pyspark"]
            },
            "Web Developer": {
                "HTML": ["html", "html5"],
                "CSS": ["css", "css3", "bootstrap", "tailwind"],
                "JavaScript": ["javascript", "js", "es6", "typescript"],
                "React": ["react", "reactjs", "react.js"],
                "Node.js": ["node", "nodejs", "express.js"],
                "MongoDB": ["mongodb", "nosql"],
                "Git": ["git", "github", "gitlab"],
                "REST APIs": ["rest", "api", "restful"],
                "AWS": ["aws", "amazon web services"],
                "Docker": ["docker", "containerization"]
            },
            "AI/ML Engineer": {
                "Python": ["python", "py", "scikit-learn"],
                "TensorFlow": ["tensorflow", "tf"],
                "PyTorch": ["pytorch"],
                "Deep Learning": ["deep learning", "neural networks", "cnn"],
                "NLP": ["nlp", "natural language processing"],
                "Computer Vision": ["computer vision", "opencv"],
                "Data Preprocessing": ["data cleaning", "feature engineering"],
                "MLOps": ["mlops", "model deployment"],
                "Statistics": ["statistics", "probability"],
                "Cloud AI": ["vertex ai", "sagemaker"]
            },
            # Added 9 more roles with 10 skills each
            "Cloud Engineer": {
                "AWS": ["aws", "ec2", "s3"],
                "Azure": ["azure", "azure cloud"],
                "GCP": ["gcp", "google cloud"],
                "Terraform": ["terraform", "iac"],
                "Kubernetes": ["kubernetes", "k8s"],
                "Docker": ["docker", "containers"],
                "CI/CD": ["ci/cd", "jenkins", "github actions"],
                "Linux": ["linux", "bash", "shell scripting"],
                "Networking": ["networking", "vpc", "subnets"],
                "Security": ["cloud security", "iam"]
            },
            "DevOps Engineer": {
                "Docker": ["docker", "containerization"],
                "Kubernetes": ["kubernetes", "k8s"],
                "AWS": ["aws", "cloudformation"],
                "CI/CD": ["jenkins", "gitlab ci", "circleci"],
                "Terraform": ["terraform", "infrastructure as code"],
                "Linux": ["linux", "bash"],
                "Python": ["python", "scripting"],
                "Monitoring": ["prometheus", "grafana"],
                "Ansible": ["ansible", "configuration management"],
                "Git": ["git", "version control"]
            },
            "Data Scientist": {
                "Python": ["python", "pandas", "numpy"],
                "R": ["r", "rstudio"],
                "SQL": ["sql", "querying"],
                "Machine Learning": ["ml", "scikit-learn"],
                "Statistics": ["stats", "probability"],
                "Data Visualization": ["matplotlib", "seaborn"],
                "Big Data": ["spark", "hadoop"],
                "Deep Learning": ["neural networks", "tensorflow"],
                "Experimental Design": ["a/b testing", "hypothesis testing"],
                "Cloud Platforms": ["aws", "gcp"]
            },
            "UX/UI Designer": {
                "Figma": ["figma", "ui design"],
                "Adobe XD": ["adobe xd", "xd"],
                "Sketch": ["sketch", "sketch app"],
                "User Research": ["user research", "usability testing"],
                "Wireframing": ["wireframes", "prototyping"],
                "UI Principles": ["ui", "user interface"],
                "UX Principles": ["ux", "user experience"],
                "Color Theory": ["color theory", "palettes"],
                "Typography": ["fonts", "typography"],
                "Accessibility": ["a11y", "wcag"]
            },
            "Cybersecurity Analyst": {
                "Network Security": ["network security", "firewalls"],
                "Ethical Hacking": ["ethical hacking", "penetration testing"],
                "SIEM": ["siem", "splunk"],
                "Cryptography": ["crypto", "encryption"],
                "Linux": ["linux", "bash"],
                "Python": ["python", "scripting"],
                "Risk Assessment": ["risk assessment", "vulnerability"],
                "Compliance": ["gdpr", "hipaa"],
                "Incident Response": ["incident response", "ir"],
                "Cloud Security": ["aws security", "azure security"]
            },
            "Product Manager": {
                "Agile": ["agile", "scrum"],
                "JIRA": ["jira", "atlassian"],
                "Roadmapping": ["roadmap", "product strategy"],
                "Market Research": ["market research", "competitive analysis"],
                "User Stories": ["user stories", "requirements"],
                "SQL": ["sql", "data analysis"],
                "Metrics": ["kpis", "okrs"],
                "Prototyping": ["prototyping", "wireframes"],
                "Stakeholder Mgmt": ["stakeholders", "communication"],
                "Prioritization": ["prioritization", "rice"]
            },
            "Digital Marketer": {
                "SEO": ["seo", "search engine optimization"],
                "Google Analytics": ["ga", "google analytics"],
                "Social Media": ["facebook", "instagram", "linkedin"],
                "Content Marketing": ["content", "blogging"],
                "PPC": ["ppc", "google ads"],
                "Email Marketing": ["email", "mailchimp"],
                "Copywriting": ["copy", "copywriting"],
                "Data Analysis": ["analytics", "metrics"],
                "CRM": ["crm", "salesforce"],
                "Growth Hacking": ["growth", "acquisition"]
            },
            "Blockchain Developer": {
                "Solidity": ["solidity", "smart contracts"],
                "Ethereum": ["ethereum", "eth"],
                "Web3": ["web3", "dapps"],
                "Smart Contracts": ["smart contracts", "blockchain"],
                "Cryptography": ["crypto", "encryption"],
                "Node.js": ["node", "javascript"],
                "Truffle": ["truffle", "ganache"],
                "IPFS": ["ipfs", "decentralized storage"],
                "DeFi": ["defi", "decentralized finance"],
                "NFTs": ["nfts", "non fungible"]
            },
            "Game Developer": {
                "Unity": ["unity", "unity3d"],
                "C#": ["c#", "c sharp"],
                "Unreal Engine": ["unreal", "ue4"],
                "3D Modeling": ["3d", "blender"],
                "Game Physics": ["physics", "rigidbody"],
                "AI Programming": ["game ai", "pathfinding"],
                "Multiplayer": ["multiplayer", "networking"],
                "VR/AR": ["vr", "ar", "virtual reality"],
                "Mobile Games": ["mobile", "ios", "android"],
                "Game Design": ["gdd", "mechanics"]
            }
            },
            "learning_resources": {
                "Python": "https://www.learnpython.org/",
            "SQL": "https://www.w3schools.com/sql/",
            "Excel": "https://excel-practice-online.com/",
            "Power BI": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/",
            "Tableau": "https://www.tableau.com/learn/training",
            "R": "https://www.coursera.org/learn/r-programming",
            "Data Visualization": "https://www.datacamp.com/courses/data-visualization",
            "Machine Learning": "https://www.coursera.org/learn/machine-learning",
            "Big Data": "https://www.udacity.com/course/intro-to-hadoop-and-mapreduce--ud617",
            "HTML": "https://www.codecademy.com/learn/learn-html",
            "CSS": "https://web.dev/learn/css/",
            "JavaScript": "https://javascript.info/",
            "React": "https://reactjs.org/docs/getting-started.html",
            "Node.js": "https://nodejs.dev/en/learn/",
            "MongoDB": "https://university.mongodb.com/",
            "Git": "https://git-scm.com/doc",
            "REST APIs": "https://www.restapitutorial.com/",
            "AWS": "https://aws.amazon.com/getting-started/",
            "Docker": "https://docs.docker.com/get-started/",
            "TensorFlow": "https://www.tensorflow.org/learn",
            "PyTorch": "https://pytorch.org/tutorials/",
            "Deep Learning": "https://www.deeplearning.ai/",
            "NLP": "https://www.coursera.org/specializations/natural-language-processing",
            "Computer Vision": "https://www.coursera.org/learn/computer-vision",
            "Data Preprocessing": "https://www.kaggle.com/learn/data-cleaning",
            "MLOps": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops",
            "Statistics": "https://www.khanacademy.org/math/statistics-probability",
            "Cloud AI": "https://cloud.google.com/learn/training",
            "Azure": "https://learn.microsoft.com/en-us/training/azure/",
            "GCP": "https://cloud.google.com/training",
            "Terraform": "https://learn.hashicorp.com/terraform",
            "Kubernetes": "https://kubernetes.io/docs/tutorials/",
            "CI/CD": "https://www.redhat.com/en/topics/devops/what-is-ci-cd",
            "Linux": "https://www.linuxfoundation.org/training/",
            "Networking": "https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/entry/ccna.html",
            "Security": "https://www.coursera.org/professional-certificates/google-cybersecurity",
            "Ansible": "https://www.ansible.com/resources/get-started",
            "Monitoring": "https://grafana.com/learn/",
            "Figma": "https://www.figma.com/resources/learn-design/",
            "Adobe XD": "https://helpx.adobe.com/xd/tutorials.html",
            "Sketch": "https://www.sketch.com/docs/",
            "User Research": "https://www.interaction-design.org/literature/topics/user-research",
            "Wireframing": "https://www.uxdesigninstitute.com/blog/what-is-wireframing/",
            "UI Principles": "https://www.coursera.org/learn/user-interface-design",
            "UX Principles": "https://www.interaction-design.org/literature/topics/ux-design",
            "Color Theory": "https://www.canva.com/learn/color-theory/",
            "Typography": "https://practicaltypography.com/",
            "Accessibility": "https://www.w3.org/WAI/fundamentals/",
            "Network Security": "https://www.coursera.org/learn/network-security",
            "Ethical Hacking": "https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/",
            "SIEM": "https://www.udemy.com/course/splunk-beginner/",
            "Cryptography": "https://www.coursera.org/learn/crypto",
            "Risk Assessment": "https://www.isaca.org/resources/isaca-journal/issues/2021/volume-3/risk-assessment-techniques",
            "Compliance": "https://www.coursera.org/learn/intro-gdpr",
            "Incident Response": "https://www.sans.org/courses/incident-response-handler/",
            "Agile": "https://www.scrum.org/resources/what-is-scrum",
            "JIRA": "https://www.atlassian.com/software/jira/guides",
            "Roadmapping": "https://www.productplan.com/learn/product-roadmap/",
            "Market Research": "https://www.coursera.org/learn/market-research",
            "User Stories": "https://www.agilealliance.org/glossary/user-stories/",
            "Metrics": "https://www.productplan.com/learn/product-metrics/",
            "Prototyping": "https://www.interaction-design.org/literature/topics/prototyping",
            "Stakeholder Mgmt": "https://www.pmi.org/learning/library/stakeholder-management-5890",
            "Prioritization": "https://www.productplan.com/learn/prioritization/",
            "SEO": "https://moz.com/beginners-guide-to-seo",
            "Google Analytics": "https://analytics.google.com/analytics/academy/",
            "Social Media": "https://www.coursera.org/learn/social-media-marketing",
            "Content Marketing": "https://contentmarketinginstitute.com/training/",
            "PPC": "https://www.wordstream.com/learn",
            "Email Marketing": "https://mailchimp.com/resources/email-marketing-guide/",
            "Copywriting": "https://www.udemy.com/course/copywriting-secrets/",
            "CRM": "https://trailhead.salesforce.com/en",
            "Growth Hacking": "https://www.coursera.org/learn/growth-hacking",
            "Solidity": "https://soliditylang.org/",
            "Ethereum": "https://ethereum.org/en/developers/docs/",
            "Web3": "https://web3.university/",
            "Smart Contracts": "https://www.udemy.com/course/ethereum-and-solidity-the-complete-developers-guide/",
            "Truffle": "https://trufflesuite.com/docs/truffle/",
            "IPFS": "https://docs.ipfs.tech/",
            "DeFi": "https://defi-learn.org/",
            "NFTs": "https://ethereum.org/en/nft/",
            "Unity": "https://learn.unity.com/",
            "C#": "https://learn.microsoft.com/en-us/dotnet/csharp/",
            "Unreal Engine": "https://www.unrealengine.com/en-US/learn",
            "3D Modeling": "https://www.blender.org/support/tutorials/",
            "Game Physics": "https://learn.unity.com/course/physics-fundamentals",
            "AI Programming": "https://www.udemy.com/course/artificial-intelligence-in-unity/",
            "Multiplayer": "https://www.photonengine.com/en-US/Photon",
            "VR/AR": "https://learn.unity.com/course/vr-development",
            "Mobile Games": "https://www.udemy.com/course/unitymobilegame/",
            "Game Design": "https://www.coursera.org/learn/game-design"
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
        page_title="Smart
Resume
Analyzer for
Career
Growth", 
        page_icon="🧠", 
        layout="wide"
    )
    
    st.title("🧠 Smart
Resume
Analyzer for
Career
Growth")
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
    st.caption("© 2025 Resume Analyzer | For educational purposes only")

if __name__ == "__main__":
    main()
