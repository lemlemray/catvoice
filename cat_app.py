import streamlit as st

st.set_page_config(page_title="猫翻訳AI", page_icon="🐈")

st.markdown("""
<style>
.block-container { max-width: 500px; padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.title("🐈 猫翻訳AI")
st.markdown("---")
st.write("👇 こちらのリアルタイム版をお使いください")
st.markdown("""
<a href="https://lemlemray.github.io/catvoice/" target="_blank"
style="
    display: block;
    background: #e94560;
    color: white;
    text-align: center;
    padding: 20px;
    border-radius: 15px;
    font-size: 1.5em;
    text-decoration: none;
    margin: 20px 0;
">
🎙 リアルタイム猫翻訳を開く
</a>
""", unsafe_allow_html=True)
