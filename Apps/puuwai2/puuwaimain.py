import streamlit as st
import logging

def initialize_factors():
    logging.info(f"(Re)Initializing Factors, Current ones {st.session_state} ")
    st.session_state.bmi=24
    st.session_state.age=30
    st.session_state.gender=1
    st.session_state.nicotine=2
    st.session_state.mepa=95
    st.session_state.sleep=7
    st.session_state.lipids=100
    st.session_state.pa=150
    st.session_state.glucose=80
    st.session_state.sbp=110
    st.session_state.dbp=75
    st.session_state.messages=[]

if __name__ == '__main__':
    st.set_page_config(
    page_title="Welcome to your heart!",
    page_icon="👋",
)
    st.write("# Welcome to Puuwai! 👋")

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info(f"Session Variables {st.session_state}")
    if ((len(st.session_state)==0) | st.button("Reset Values")):
        initialize_factors()
    
    st.sidebar.success("Select the page.")
    
