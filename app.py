import streamlit as st
from agent.generator import generate_pipeline

st.set_page_config(page_title="Agentic Data Builder", layout="wide")

st.title("🚀 Agentic Data Builder")
st.markdown("Generate governed data pipelines using AI")

# Input
prompt = st.text_area(
    "Describe your pipeline",
    placeholder="Create a pipeline that ingests data from API and builds bronze and silver layers"
)

# Botão
if st.button("Generate Pipeline"):
    if prompt:
        with st.spinner("Generating pipeline..."):
            code = generate_pipeline(prompt)

        st.success("Pipeline generated!")

        # Mostrar código
        st.subheader("Generated Code")
        st.code(code, language="python")

        # Salvar arquivo
        with open("generated_pipeline.py", "w") as f:
            f.write(code)

        st.info("Saved as generated_pipeline.py")

    else:
        st.warning("Please enter a prompt")

# Rodapé
st.markdown("---")
st.caption("AI-powered Data Engineering Agent")