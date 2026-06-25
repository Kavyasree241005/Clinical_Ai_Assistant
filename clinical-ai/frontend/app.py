import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import process_audio_file, enroll_new_doctor

st.set_page_config(page_title="ClinicalAI", page_icon="🏥", layout="wide")
st.title("🏥 Clinical Conversation AI")

tab1, tab2 = st.tabs(["Process Consultation", "Enroll Doctor"])

with tab1:
    st.subheader("Upload consultation audio")
    uploaded_file = st.file_uploader("Upload .wav file", type=['wav'])
    
    if uploaded_file and st.button("Analyze Consultation"):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        
        with st.spinner("Processing..."):
            result = process_audio_file(tmp_path)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Transcript")
            for turn in result["conversation"]:
                color = "blue" if "Dr" in turn["speaker"] else "green"
                st.markdown(f"**:{color}[{turn['speaker']}]:** {turn['text']}")
        
        with col2:
            st.subheader("Clinical Summary")
            entities = result["entities"]
            st.write(f"**Symptoms:** {', '.join(entities['symptoms'])}")
            st.write(f"**Duration:** {entities['duration']}")
            st.write(f"**Severity:** {entities['severity']}")
            
            st.subheader("Differential Diagnoses")
            for diag in result["clinical_output"]["diagnoses"]:
                with st.expander(f"{diag['condition']} — {diag['confidence']}"):
                    st.write(f"**Tests:** {', '.join(diag['recommended_tests'])}")
                    st.write(f"**Management:** {diag['management']}")
                    if diag.get("referral"):
                        st.warning(f"Referral: {diag['referral']}")
        
        st.success(f"Report generated: `{result['report_path']}`")
        os.unlink(tmp_path)

with tab2:
    st.subheader("Enroll a new doctor")
    doctor_name = st.text_input("Doctor name (e.g. Dr. Ravi Kumar)")
    samples = st.file_uploader("Upload 3-5 voice samples (10-20s each)", 
                                type=['wav'], accept_multiple_files=True)
    
    if doctor_name and samples and len(samples) >= 3:
        if st.button("Enroll Doctor"):
            import tempfile
            paths = []
            for s in samples:
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                    tmp.write(s.read())
                    paths.append(tmp.name)
            
            with st.spinner("Enrolling..."):
                enroll_new_doctor(doctor_name, paths)
            
            for p in paths:
                os.unlink(p)
            
            st.success(f"✅ {doctor_name} enrolled successfully!")