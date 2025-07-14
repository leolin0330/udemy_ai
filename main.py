import streamlit as st
from utils import generate_script

if "font_size" not in st.session_state:
    st.session_state.font_size = "中"

font_size_map = {
    "小": "12px",
    "中": "16px",
    "大": "25px"
}

font_size = st.selectbox(
    "選擇字體大小",
    ["小", "中", "大"],
    index=["小", "中", "大"].index(st.session_state.font_size),
    key="font_size"
)

css = f"""
<style>
    h1, h2, h3, h4, h5, h6, p, span, div, label {{
        font-size: {font_size_map[st.session_state.font_size]} !important;
    }}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

st.title("🎬 視頻腳本生成器")


with st.sidebar:
    openai_api_key = st.text_input("請輸入OpenAI API密鑰：", type="password")
    st.markdown("[獲取OpenAI API密鑰](https://platform.openai.com/account/api-keys)")

subject = st.text_input("💡 請輸入視頻的主題")
video_length = st.number_input("⏱️ 請輸入視頻的大致時長（單位：分鐘）", min_value=0.1, step=0.1)
creativity = st.slider("✨ 請輸入視頻腳本的創造力（數字小說明更嚴謹，數字大說明更多樣）", min_value=0.0,
                       max_value=1.0, value=0.2, step=0.1)
submit = st.button("生成腳本")

if submit and not openai_api_key:
    st.info("請輸入你的OpenAI API密鑰")
    st.stop()
if submit and not subject:
    st.info("請輸入視頻的主題")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("視頻長度需要大於或等於0.1")
    st.stop()
if submit:
    with st.spinner("AI正在思考中，請稍等..."):
        search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key)
    st.success("視頻腳本已生成！")
    st.subheader("🔥 標題：")
    st.write(title)
    st.subheader("📝 視頻腳本：")
    st.write(script)
    with st.expander("維基百科搜索結果 👀"):
        st.info(search_result)
