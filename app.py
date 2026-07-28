"""Streamlit interface for SignalForge AI."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from agent.orchestrator import analyze_opportunity, get_provider
from config.settings import settings
from tools.artifact_writer import analysis_to_docx, analysis_to_json, analysis_to_markdown
from tools.document_parser import parse_documents


ROOT = Path(__file__).resolve().parent
DEMO_FILES = [
    ROOT / "sample_data" / "meridian_discovery_notes.txt",
    ROOT / "sample_data" / "meridian_requirements.csv",
]

st.set_page_config(page_title="SignalForge AI", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1280px;}
.sf-hero {padding: 1.5rem 1.75rem; border: 1px solid #dbe3ee; border-radius: 18px; background: linear-gradient(135deg,#f8fafc,#eef4ff);}
.sf-kicker {font-size: .78rem; letter-spacing: .12em; font-weight: 700; color: #475569; text-transform: uppercase;}
.sf-sub {color:#475569; max-width:760px; margin-top:.4rem;}
</style>
""", unsafe_allow_html=True)

st.markdown(
    """<div class="sf-hero"><div class="sf-kicker">Agentic opportunity intelligence</div>
    <h1 style="margin:.25rem 0 0">SignalForge AI</h1>
    <div class="sf-sub">Turns unstructured customer material into evidence-backed discovery gaps, risks, solution direction, and an AE-to-SE handoff.</div></div>""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Runtime")
    st.info(f"Mode: **{settings.app_mode.upper()}**")
    st.caption(f"Model: {settings.model_name}")
    st.caption("Synthetic demo data only. No customer information is stored.")
    if st.button("Reset opportunity", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.subheader("1. Add customer material")
left, right = st.columns([1, 1])
with left:
    uploaded = st.file_uploader(
        "Upload meeting notes or requirements",
        type=["txt", "md", "csv", "docx"],
        accept_multiple_files=True,
    )
with right:
    st.write("Use the validated synthetic opportunity for a reliable two-minute demo.")
    use_demo = st.toggle("Load Meridian Hospitality demo", value=not uploaded)

analyze = st.button("Analyze opportunity", type="primary", use_container_width=True)

if analyze:
    try:
        if use_demo:
            file_payloads = [(path.name, path.read_bytes()) for path in DEMO_FILES]
        else:
            file_payloads = [(item.name, item.getvalue()) for item in uploaded]
        with st.status("Running the opportunity agent...", expanded=True) as status:
            documents = parse_documents(file_payloads)
            st.write(f"✓ Parsed {len(documents)} document(s)")
            result = analyze_opportunity(documents, get_provider(settings))
            for step in result.execution_trace[1:]:
                st.write(f"✓ {step}")
            status.update(label="Opportunity analysis complete", state="complete")
        st.session_state["analysis"] = result
    except Exception as exc:
        st.error(f"Analysis failed: {exc}")

result = st.session_state.get("analysis")
if result:
    st.subheader("2. Opportunity workspace")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Discovery coverage", f"{result.coverage.score}%")
    m2.metric("Readiness", f"{result.readiness_score}%")
    m3.metric("Open gaps", len(result.gaps))
    m4.metric("High risks", sum(risk.severity == "high" for risk in result.risks))

    tabs = st.tabs(["Overview", "Requirements", "Discovery gaps", "Risks", "Solution", "Handoff"])
    with tabs[0]:
        st.markdown(f"### {result.profile.customer_name}")
        st.write(result.profile.use_case)
        st.markdown(f"**Recommended action:** {result.decision.recommendation}")
        st.write(result.decision.reason)
        st.markdown("#### Stakeholders")
        st.dataframe([item.model_dump() for item in result.profile.stakeholders], use_container_width=True, hide_index=True)

    with tabs[1]:
        st.dataframe([
            {
                "Category": item.category.title(),
                "Requirement": item.requirement,
                "Status": item.status.title(),
                "Source": item.evidence.source if item.evidence else "Missing",
                "Confidence": item.evidence.confidence if item.evidence else None,
            }
            for item in result.profile.requirements
        ], use_container_width=True, hide_index=True)

    with tabs[2]:
        for gap in result.gaps:
            with st.container(border=True):
                st.markdown(f"**{gap.priority.upper()} · {gap.dimension.title()}**")
                st.write(gap.question)
                st.caption(gap.rationale)

    with tabs[3]:
        st.dataframe([risk.model_dump() for risk in result.risks], use_container_width=True, hide_index=True)

    with tabs[4]:
        st.graphviz_chart(result.architecture_dot, use_container_width=True)
        for component in result.solution_direction:
            with st.container(border=True):
                st.markdown(f"**{component.service}** · {component.capability}")
                st.write(component.rationale)
                st.caption(f"Direction confidence: {component.confidence}")
        st.caption("Initial direction only. Final architecture requires customer validation and sizing.")

    with tabs[5]:
        markdown = analysis_to_markdown(result)
        st.markdown(markdown)
        c1, c2, c3 = st.columns(3)
        c1.download_button("Download Markdown", markdown, "signalforge-opportunity-brief.md", "text/markdown", use_container_width=True)
        c2.download_button("Download JSON", analysis_to_json(result), "signalforge-analysis.json", "application/json", use_container_width=True)
        c3.download_button("Download DOCX", analysis_to_docx(result), "signalforge-ae-se-handoff.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
