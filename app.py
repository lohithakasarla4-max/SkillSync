import streamlit as st
import pandas as pd
import re

# Page Configuration
st.set_page_config(
    page_title="SkillSync - Smart Resume & Job Matcher",
    page_icon="🎯",
    layout="wide"
)

# Title & Header
st.title("🎯 SkillSync")
st.subheader("AI-Powered Resume & Job Description Skill Matcher")
st.write("Compare your resume against job postings to calculate match score, identify missing skills, and boost your hiring potential.")

st.divider()

# Layout Columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Paste Your Resume Text")
    resume_text = st.text_area(
        "Enter your background, projects, or resume summary:",
        height=250,
        placeholder="e.g. Computer Science student skilled in Python, Flask, HTML, CSS, MySQL, Git, Data Analysis..."
    )

with col2:
    st.markdown("### 💼 Paste Target Job Description")
    job_text = st.text_area(
        "Enter the job requirements or description:",
        height=250,
        placeholder="e.g. Looking for a Python Developer proficient in Flask, SQL, Cloud deployment, REST APIs, and Git..."
    )

def extract_keywords(text):
    """Extract clean words and skills from input text."""
    words = re.findall(r'\b[A-Za-z0-9+#.-]+\b', text.lower())
    # Filter out common stop words
    stop_words = {'and', 'the', 'is', 'in', 'to', 'of', 'for', 'with', 'a', 'an', 'on', 'at', 'by', 'this', 'or', 'be', 'are', 'you', 'your', 'we', 'our', 'looking', 'required', 'skills', 'experience'}
    return set([w for w in words if w not in stop_words and len(w) > 1])

# Action Button
if st.button("🚀 Analyze Match", type="primary", use_container_width=True):
    if not resume_text.strip() or not job_text.strip():
        st.error("Please paste both your resume text and the job description to run the analysis.")
    else:
        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_text)
        
        matching_skills = resume_keywords.intersection(job_keywords)
        missing_skills = job_keywords.difference(resume_keywords)
        
        if len(job_keywords) > 0:
            match_percentage = int((len(matching_skills) / len(job_keywords)) * 100)
        else:
            match_percentage = 0
            
        st.divider()
        st.header("📊 Match Analysis Results")
        
        # Display Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Overall Match Score", f"{match_percentage}%")
        m2.metric("Matching Skill Keywords", len(matching_skills))
        m3.metric("Missing Key Terms", len(missing_skills))
        
        # Progress Bar
        st.progress(match_percentage / 100)
        
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.success("✅ **Matching Skills Found:**")
            if matching_skills:
                st.write(", ".join([f"`{skill.title()}`" for skill in sorted(matching_skills)]))
            else:
                st.write("No direct matching keywords found.")
                
        with res_col2:
            st.warning("⚠️ **Skills/Keywords to Add to Your Resume:**")
            if missing_skills:
                st.write(", ".join([f"`{skill.title()}`" for skill in sorted(missing_skills)]))
            else:
                st.write("Great job! Your resume covers all key terms from the job description.")
                
        st.divider()
        st.markdown("### 💡 Quick Recommendations")
        if match_percentage >= 75:
            st.balloons()
            st.write("🔥 **Strong Alignment!** Your profile matches the target job keywords very well.")
        elif match_percentage >= 45:
            st.write("⚡ **Good Potential!** Highlight the missing keywords in your project bullet points to pass ATS filters.")
        else:
            st.write("📌 **Action Needed:** Tailor your project descriptions to emphasize core technical requirements listed under missing terms.")