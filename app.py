import streamlit as st
from docx import Document
import os
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

# Set up Streamlit UI
st.set_page_config(page_title="AI Resume Assistant", layout="wide")
st.title("🧑‍💼 AI Resume Assistant")

# Tabs
resume_tab, chatbot_tab = st.tabs(["📄 Resume Builder", "🤖 Career Chatbot"])

# ------------------------ Resume Builder --------------------------
with resume_tab:
    # Load Hugging Face text generation model
    @st.cache_resource
    def load_generator():
        return pipeline("text-generation", model="gpt2")

    generator = load_generator()

    # Fill resume template
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

    # Create output directory
    os.makedirs("output", exist_ok=True)

    st.header("Build Your Resume")

    data = {}
    data["NAME"] = st.text_input("Full Name *")
    data["EMAIL"] = st.text_input("Email *")
    data["ADDRESS"] = st.text_input("Address")
    data["PHONE"] = st.text_input("Phone Number")
    data["LINKEDIN"] = st.text_input("LinkedIn Profile URL")
    data["GITHUB"] = st.text_input("GitHub Profile URL")

    st.subheader("🎯 Career Objective")
    job_title = st.text_input("Job Title for Objective (e.g., Data Analyst)")
    if job_title:
        with st.spinner("Generating objective..."):
            result = generator(f"Write a professional resume objective for a {job_title}.",
                               max_length=60, num_return_sequences=1)
            data["OBJECTIVE"] = result[0]["generated_text"]
            st.text_area("Generated Objective", value=data["OBJECTIVE"])
    else:
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

    # Generate Button
    if st.button("📄 Generate Resume"):
        if data["NAME"] and data["EMAIL"]:
            try:
                output_file = fill_resume("resume_template.docx", data)
                with open(output_file, "rb") as file:
                    st.success("✅ Resume generated successfully!")
                    st.download_button("📥 Download Resume", data=file, file_name=os.path.basename(output_file))
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Please enter both Name and Email.")

# ------------------------ Chatbot Tab --------------------------
with chatbot_tab:
    st.header("💬 Career Guidance Chatbot")

    @st.cache_resource
    def load_chat_model():
        tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        return tokenizer, model

    tokenizer, model = load_chat_model()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("You:", key="chat_input")

    if st.button("Send"):
        if user_input:
            # Encode input and append to history
            new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

            bot_input_ids = torch.cat([
                tokenizer.encode(msg + tokenizer.eos_token, return_tensors='pt')
                for _, msg in st.session_state.chat_history[-5:]
            ] + [new_input_ids], dim=-1)

            response_ids = model.generate(
                bot_input_ids,
                max_length=1000,
                pad_token_id=tokenizer.eos_token_id,
                top_k=50,
                top_p=0.95,
                temperature=0.7,
                do_sample=True
            )

            response = tokenizer.decode(response_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", response))

    for speaker, msg in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {msg}")
