import streamlit as st
from docx import Document
import os

def fill_resume(template_path, data):
    doc = Document(template_path)
    for para in doc.paragraphs:
        for key, value in data.items():
            placeholder = f"{{{key}}}"
            if placeholder in para.text:
                para.text = para.text.replace(placeholder, value if value else "")
    output_path = f'output/{data["NAME"].replace(" ", "_")}_resume.docx'
    doc.save(output_path)
    return output_path

st.set_page_config(page_title="Pro Resume Builder", layout="centered")
st.title("🧑‍💼 Professional Resume Builder")

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# Collect user data
data = {}
data["NAME"] = st.text_input("Full Name *")
data["EMAIL"] = st.text_input("Email *")

# Optional fields
data["ADDRESS"] = st.text_input("Address")
data["PHONE"] = st.text_input("Phone Number")
data["LINKEDIN"] = st.text_input("LinkedIn Profile URL")
data["GITHUB"] = st.text_input("GitHub Profile URL")
data["OBJECTIVE"] = st.text_area("Career Objective")

st.subheader("💻 Skills")
data["TECHNICAL_SKILLS"] = st.text_area("Technical Skills")
data["SOFT_SKILLS"] = st.text_area("Soft Skills")

st.subheader("💼 Experience")
data["EXP1_ROLE"] = st.text_input("Experience 1: Role")
data["EXP1_COMPANY"] = st.text_input("Experience 1: Company")
data["EXP1_DATE"] = st.text_input("Experience 1: Duration")
data["EXP1_DESC"] = st.text_area("Experience 1: Description")
data["EXP2_ROLE"] = st.text_input("Experience 2: Role")
data["EXP2_COMPANY"] = st.text_input("Experience 2: Company")
data["EXP2_DATE"] = st.text_input("Experience 2: Duration")
data["EXP2_DESC"] = st.text_area("Experience 2: Description")

st.subheader("🎓 Education")
data["EDU_DEGREE"] = st.text_input("Degree")
data["EDU_INSTITUTE"] = st.text_input("Institute")
data["EDU_YEAR"] = st.text_input("Year")

st.subheader("📜 Certifications")
data["CERTIFICATIONS"] = st.text_area("Certifications")

st.subheader("🧠 Projects / Leadership")
data["PROJECTS"] = st.text_area("Projects or Leadership Experience")

st.subheader("🌍 Languages")
data["LANGUAGES"] = st.text_input("Languages Known")

st.subheader("🏆 Awards / Achievements")
data["AWARDS"] = st.text_area("Awards or Accomplishments")

# Generate Resume Button
if st.button("🎯 Generate Resume"):
    if data["NAME"] and data["EMAIL"]:
        try:
            output_file = fill_resume("resume_template.docx", data)
            with open(output_file, "rb") as file:
                st.success("✅ Resume generated successfully!")
                st.download_button("📥 Download Resume", data=file, file_name=os.path.basename(output_file))
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please fill in at least your Name and Email.")
