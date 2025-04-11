import streamlit as st
import pdfplumber   # PyMuPDF

# === Expanded Roles and Skills ===
skill_map = {
    "Data Analyst": [
        "Python", "SQL", "Data Analysis", "Excel", "Power BI", "Tableau",
        "Statistics", "Machine Learning", "Pandas", "Communication"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React", "Node.js", "MongoDB",
        "Git", "Responsive Design", "Communication"
    ],
    "AI/ML Engineer": [
        "Python", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "Numpy",
        "Deep Learning", "Model Deployment", "Data Preprocessing", "Communication"
    ],
    "Cloud Engineer": [
        "AWS", "Azure", "Google Cloud", "Linux", "Terraform", "CI/CD",
        "Networking", "Docker", "Kubernetes", "Shell Scripting"
    ],
    "UI/UX Designer": [
        "Figma", "Adobe XD", "User Research", "Wireframing", "Prototyping",
        "Visual Design", "Usability Testing", "Design Thinking", "Communication"
    ],
    "Cybersecurity Analyst": [
        "Network Security", "Firewalls", "Threat Detection", "Linux",
        "Ethical Hacking", "Incident Response", "SIEM", "Risk Assessment", "Communication"
    ]
}

# === Learning Resource Suggestions ===
learning_suggestions = {
    "Machine Learning": "🧠 [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course)",
    "Power BI": "📊 [Microsoft Learn: Power BI](https://learn.microsoft.com/en-us/training/powerplatform/power-bi/)",
    "Statistics": "📈 [Khan Academy: Statistics](https://www.khanacademy.org/math/statistics-probability)",
    "Communication": "🗣️ [Coursera: Communication Skills](https://www.coursera.org/learn/wharton-communication)",
    "JavaScript": "🌐 [FreeCodeCamp: JavaScript](https://www.freecodecamp.org/learn)",
    "React": "⚛️ [Codecademy: React](https://www.codecademy.com/learn/react-101)",
    "TensorFlow": "🧠 [TensorFlow Tutorials](https://www.tensorflow.org/learn)",
    "Git": "🔧 [Git Handbook](https://guides.github.com/introduction/git-handbook/)",
    "MongoDB": "🛢️ [MongoDB University](https://university.mongodb.com/)",
    "Docker": "🐳 [Docker Essentials – Codecademy](https://www.codecademy.com/learn/learn-docker)",
    "Kubernetes": "📦 [Kubernetes – KodeKloud](https://kodekloud.com/courses/kubernetes-for-beginners/)",
    "AWS": "☁️ [AWS Cloud Practitioner](https://explore.skillbuilder.aws/learn/course/134/aws-cloud-practitioner-essentials)",
    "Figma": "🎨 [Figma Tutorial – freeCodeCamp](https://www.youtube.com/watch?v=jwCmIBJ8Jtc)",
    "Cybersecurity": "🛡️ [Cisco: Intro to Cybersecurity](https://skillsforall.com/course/introduction-to-cybersecurity)",
}

# === Extract Text from PDF ===
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# === Skill Analysis ===
def extract_skills(text, skill_list):
    return [skill for skill in skill_list if skill.lower() in text.lower()]

def get_missing_skills(skill_list, detected_skills):
    return [skill for skill in skill_list if skill not in detected_skills]

def recommend_courses(missing_skills):
    return [learning_suggestions.get(skill) for skill in missing_skills if skill in learning_suggestions]

# === Streamlit App ===
st.set_page_config(page_title="Resume Analyzer", page_icon="🧠")
st.title("🧠 Free Resume Analyzer")
st.markdown("Upload your resume and get **personalized skill gaps and learning suggestions** based on your career goal.")

# Select Career Role
selected_role = st.selectbox("🎯 Select your target role:", list(skill_map.keys()))

# Choose Input Method
input_method = st.radio("📥 Choose input method:", ["Upload PDF", "Paste Text"])
resume_text = ""

if input_method == "Upload PDF":
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        st.success("✅ Resume uploaded and extracted.")
elif input_method == "Paste Text":
    resume_text = st.text_area("Paste your resume content here:", height=300)

# Analyze Button
if st.button("🔍 Analyze Resume"):
    if not resume_text.strip():
        st.warning("⚠️ Please upload or paste resume content.")
    else:
        # Detect Skills
        role_skills = skill_map[selected_role]
        detected_skills = extract_skills(resume_text, role_skills)
        missing_skills = get_missing_skills(role_skills, detected_skills)
        course_recommendations = recommend_courses(missing_skills)

        # Output
        st.subheader("✅ Skills Found in Resume")
        st.write(", ".join(detected_skills) if detected_skills else "No relevant skills found.")

        st.subheader("🚧 Missing Skills for Role")
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"- ❌ {skill}")
        else:
            st.success("You're covering all key skills for this role!")

        st.subheader("📚 Learning Recommendations")
        if course_recommendations:
            for rec in course_recommendations:
                st.markdown(f"- {rec}")
        else:
            st.write("🎉 You're already skilled enough. Keep it up!")
