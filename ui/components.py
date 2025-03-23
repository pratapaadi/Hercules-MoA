import streamlit as st
import markdown

def render_sidebar():
    st.sidebar.title("🤖 Advanced MoA System")
    st.sidebar.info("""
    Specialized Agents:
    
    1. 🏗️ System Architect
       - Architecture Design
       - System Integration
       - API Design
    
    2. 💻 Technical Implementation
       - Code Quality
       - Performance
       - Security
    
    3. 📊 Business Analysis
       - Requirements
       - Risk Assessment
       - Market Analysis
    
    4. 🔄 DevOps Specialist
       - CI/CD
       - Infrastructure
       - Deployment
    """)

def render_chat_history():
    if st.sidebar.checkbox("Show Chat History"):
        st.sidebar.subheader("💬 Previous Analyses")
        for idx, chat in enumerate(st.session_state.chat_history):
            with st.sidebar.expander(f"Analysis {idx + 1}"):
                st.write("**Query:**", chat["prompt"])
                st.write("**Summary:**", chat["response"]["aggregated_response"][:200] + "...")

def render_agent_responses(result):
    st.subheader("🔍 Expert Analysis")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Individual Analyses", "Synthesized Solution"])
    
    with tab1:
        cols = st.columns(2)
        for idx, (agent, response) in enumerate(result["individual_responses"].items()):
            with cols[idx % 2]:
                with st.expander(f"📋 {agent}", expanded=True):
                    # Convert markdown to HTML for better formatting
                    st.markdown(response)
    
    with tab2:
        st.markdown("## 🔄 Comprehensive Solution")
        st.markdown(result["aggregated_response"])