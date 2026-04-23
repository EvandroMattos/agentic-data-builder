import streamlit as st
from agent.generator import generate_pipeline
from github_integration.pr_creator import create_pr

st.set_page_config(page_title="Agentic Data Builder", layout="wide")

st.title("🚀 Agentic Data Builder")
st.markdown("Generate production-ready data pipelines using AI")

prompt = st.text_area(
    "Describe your pipeline",
    placeholder="Create a pipeline that ingests data from API and builds bronze and silver layers"
)

if st.button("Generate Pipeline"):
    if prompt:
        with st.spinner("Generating pipeline..."):
            code = generate_pipeline(prompt)

        st.success("Pipeline generated!")

        st.code(code, language="python")

        st.session_state["code"] = code
    else:
        st.warning("Please enter a prompt")

# Ações após geração
if "code" in st.session_state:

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Create PR on GitHub"):
            with st.spinner("Creating PR..."):
                pr_url = create_pr(st.session_state["code"])

            st.success("PR created successfully!")
            st.markdown(f"[👉 View PR]({pr_url})")

    with col2:
        st.download_button(
            label="Download Pipeline",
            data=st.session_state["code"],
            file_name="pipeline.py",
            mime="text/plain"
        )

st.markdown("---")
st.caption("AI-powered Data Engineering Agent")

from github_integration.databricks_client import get_latest_run
import time

if st.button("Check Pipeline Status"):
    with st.spinner("Checking Databricks job..."):
        run = get_latest_run()

    if run:
        state = run["state"]["life_cycle_state"]

        if state == "RUNNING":
            st.warning("🟡 Pipeline running...")

        elif state == "TERMINATED":
            result = run["state"].get("result_state")

            if result == "SUCCESS":
                st.success("🟢 Pipeline succeeded!")

            else:
                st.error("🔴 Pipeline failed!")

        else:
            st.info(f"Status: {state}")
    else:
        st.error("No runs found")