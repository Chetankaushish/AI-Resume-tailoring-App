# =====================================
# app.py
# =====================================

import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# Core Imports
from core.parser import ResumeParser
from core.job_scraper import JobScraper
from core.ats_scorer import ATSScorer
from core.keyword_analyzer import KeywordAnalyzer
from core.cover_letter import generate_cover_letter
from core.interview_questions import generate_questions
from core.pdf_export import export_pdf

# Future Imports
# from core.rag import ResumeRAG
# from core.gemini_chain import get_llm

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Resume Tailor Pro",
    page_icon="📝",
    layout="wide"
)

# =====================================
# LOAD CSS
# =====================================

css_file = Path("assets/style.css")

if css_file.exists():
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# =====================================
# SESSION STATE
# =====================================

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""

if "ats_score" not in st.session_state:
    st.session_state.ats_score = 0

if "missing_keywords" not in st.session_state:
    st.session_state.missing_keywords = []

if "tailored_resume" not in st.session_state:
    st.session_state.tailored_resume = ""

# =====================================
# ATS GAUGE
# =====================================

def ats_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            gauge={
                "axis": {
                    "range": [0, 100]
                }
            }
        )
    )

    fig.update_layout(height=300)

    return fig

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("🚀 AI Resume Tailor")

    menu = st.radio(
        "Navigation",
        [
            "Resume Analysis",
            "Cover Letter",
            "Interview Questions",
            "History"
        ]
    )

    st.markdown("---")

    st.info(
        """
        Powered By

         Gemini 2.5 Flash+
         LangChain+
         FAISS
        """
    )

# =====================================
# RESUME ANALYSIS PAGE
# =====================================

if menu == "Resume Analysis":

    st.title("🚀 AI Resume Tailor Pro")

    st.caption(
        "ATS Optimization using Gemini + LangChain + FAISS"
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        resume_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx", "txt"]
        )

    with col2:

        job_url = st.text_input(
            "Job URL",
            placeholder="Paste LinkedIn / Indeed / Naukri URL / Company Career Page "
        )

    job_description = st.text_area(
        "Or Paste Job Description",
        height=250
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    analyze_btn = c1.button(
    "Analyze Resume",
    use_container_width=True
    )

    tailor_btn = c2.button(
    "Tailor Resume",
    use_container_width=True
    )

    pdf_btn = c3.button(
    "PDF",
    use_container_width=True
    )

    docx_btn = c4.button(
    "DOCX",
    use_container_width=True
    )

    txt_btn = c5.button(
    "TXT",
    use_container_width=True
    )

    clear_btn = c6.button(
    "Clear",
    use_container_width=True
    )

    # =====================================
    # CLEAR BUTTON
    # =====================================

    if clear_btn:

        st.session_state.resume_text = ""
        st.session_state.job_description = ""
        st.session_state.analysis_result = ""
        st.session_state.ats_score = 0
        st.session_state.missing_keywords = []

        st.rerun()

    # =====================================
    # ANALYZE BUTTON
    # =====================================

    if analyze_btn:

        if resume_file is None:

            st.error(
                "Please Upload Resume"
            )

        else:

            try:

                with st.spinner(
                    "Reading Resume..."
                ):

                    resume_text = (
                        ResumeParser.extract_text(
                            resume_file
                        )
                    )

                if job_url.strip():

                    with st.spinner(
                        "Extracting Job Description..."
                    ):

                        job_description = (
                            JobScraper
                            .extract_job_description(
                                job_url
                            )
                        )

                st.session_state.resume_text = (
                    resume_text
                )

                st.session_state.job_description = (
                    job_description
                )

                score = (
                    ATSScorer.calculate_score(
                        resume_text,
                        job_description
                    )
                )

                missing_keywords = (
                    KeywordAnalyzer
                    .missing_keywords(
                        resume_text,
                        job_description
                    )
                )

                st.session_state.ats_score = score

                st.session_state.missing_keywords = (
                    missing_keywords
                )

                st.success(
                    "Analysis Completed"
                )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )
                

    # =====================================
    # DISPLAY RESULTS
    # =====================================

    if st.session_state.ats_score > 0:

        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "ATS Score",
                f"{st.session_state.ats_score}%"
            )

        with col2:

            st.metric(
                "Missing Keywords",
                len(
                    st.session_state
                    .missing_keywords
                )
            )

        with col3:

            st.metric(
                "Resume Status",
                "Analyzed"
            )

        st.plotly_chart(
            ats_gauge(
                st.session_state.ats_score
            ),
            use_container_width=True
        )

        st.subheader(
            "Missing Keywords"
        )

        st.write(
            ", ".join(
                st.session_state
                .missing_keywords[:30]
            )
        )

        st.subheader(
            "Resume Preview"
        )

        st.text_area(
            "",
            st.session_state.resume_text[:5000],
            height=250
        )

    # =====================================
    # TAILOR BUTTON
    # =====================================

    if tailor_btn:

        if (
            st.session_state.resume_text == ""
        ):

            st.warning(
                "Analyze Resume First"
            )

        else:
            with st.spinner(
                "Generating Tailored Resume..."
            ):
                
                tailored_resume = f"""
                TAILORED RESUME
                
                {st.session_state.resume_text}
                
                Optimized For Job Description
                
                {st.session_state.job_description}
                """
                
                
                st.session_state.tailored_resume = (
                    tailored_resume
                )
                st.session_state.history.append(
                    {
                        "date": str(datetime.now()),
                        "score": st.session_state.ats_score
                    }
                )
                
                st.success(
                    "Tailored Resume Generated"
                )
                
                st.text_area(
                    "Tailored Resume",
                    st.session_state.tailored_resume,
                    height=500
                )
                
                st.markdown("---")
                
                st.subheader(
                    "Download Tailored Resume"
                )
                
                st.download_button(
                    "Download TXT",
                    st.session_state.tailored_resume,
                    file_name="tailored_resume.txt",
                    mime="text/plain"
                )
            # Future Code

            # rag = ResumeRAG()
            # vector_store = rag.build_vector_store(
            #     st.session_state.resume_text
            # )
            #
            # context = rag.retrieve(
            #     vector_store,
            #     st.session_state.job_description
            # )
            #
            # llm = get_llm()
            # response = llm.invoke(...)

# =====================================
# COVER LETTER PAGE
# =====================================

elif menu == "Cover Letter":

    st.title(
        "Cover Letter Generator"
    )

    if st.button(
        "Generate Cover Letter"
    ):

        if (
            st.session_state.resume_text == ""
        ):

            st.warning(
                "Analyze Resume First"
            )

        else:

            result = (
                generate_cover_letter(
                    st.session_state.resume_text,
                    st.session_state.job_description
                )
            )

            st.write(result)

# =====================================
# INTERVIEW QUESTIONS PAGE
# =====================================

elif menu == "Interview Questions":

    st.title(
        "Interview Questions"
    )

    if st.button(
        "Generate Questions"
    ):

        if (
            st.session_state.job_description == ""
        ):

            st.warning(
                "Analyze Resume First"
            )

        else:

            result = (
                generate_questions(
                    st.session_state.job_description
                )
            )

            st.write(result)

# =====================================
# HISTORY PAGE
# =====================================

elif menu == "History":

    st.title(
        "Analysis History"
    )

    if len(
        st.session_state.history
    ) == 0:

        st.info(
            "No History Available"
        )

    else:

        for item in (
            st.session_state.history
        ):

            st.write(item)

            st.divider()

# =====================================
# PDF EXPORT SECTION
# =====================================

# Use after Gemini Tailored Resume Output

# pdf_path = export_pdf(
#     output,
#     "tailored_resume.pdf"
# )
#
# with open(pdf_path, "rb") as f:
#
#     st.download_button(
#         "Download PDF",
#         f,
#         file_name="tailored_resume.pdf"
#     )
