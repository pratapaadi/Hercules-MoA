import streamlit as st
import asyncio
from config import configure_page, init_session_state, get_api_key
from agents.mixture import MixtureOfAgents
from ui.components import render_sidebar, render_chat_history, render_agent_responses

def main():
    configure_page()
    init_session_state()
    st.markdown("<h1 class='title'>🧠 Hercules</h1>", unsafe_allow_html=True)
    st.markdown("""
    This enhanced system combines specialized AI agents to provide comprehensive solutions 
    with technical implementation, business analysis, and practical guidance.
    """)
    
    api_key = get_api_key()
    
    if not api_key:
        st.error("⚠️ API key not found in .env file. Please add your Gemini API Key to continue.")
        return
    
    render_sidebar()
    
    moa = MixtureOfAgents(api_key)
    
    st.subheader("🔍 Analysis Query")
    user_prompt = st.text_area(
        "Enter your question, problem, or request for analysis:",
        height=100,
        help="You can ask about technical implementation, business analysis, or request specific guidance."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button(
            "🚀 Analyze",
            help="Process with all specialized agents",
            use_container_width=True
        )
    
    if analyze_button:
        if not user_prompt.strip():
            st.warning("Please enter a query to analyze.")
            return
            
        with st.spinner("🔄 Processing with specialized agents..."):
            progress_bar = st.progress(0)
            
            result = asyncio.run(moa.process_prompt(user_prompt))
            
            progress_bar.progress(100)
            
            render_agent_responses(result)
            
            st.session_state.chat_history.append({
                "prompt": user_prompt,
                "response": result
            })
    
    render_chat_history()

if __name__ == "__main__":
    main()