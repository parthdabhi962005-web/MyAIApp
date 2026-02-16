import streamlit as st
import google.generativeai as genai
import youtube_transcript_api as yta # લાયબ્રેરીને Alias આપ્યો છે

# પેજ કન્ફિગરેશન
st.set_page_config(page_title="Video to Blog AI", page_icon="📝")
st.title("🎥 YouTube Video to Blog Post Generator")

api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")
youtube_link = st.text_input("Paste YouTube Video Link Here:")

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

if youtube_link:
    video_id = get_video_id(youtube_link)
    if video_id:
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg")

        if st.button("Generate Blog Post"):
            if not api_key:
                st.error("મહેરબાની કરીને API Key નાખો!")
            else:
                try:
                    with st.spinner("Transcript મેળવી રહ્યા છીએ..."):
                        # એરર દૂર કરવા માટેની નવી પદ્ધતિ
                        transcript_list = yta.YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
                        text = " ".join([i['text'] for i in transcript_list])

                    with st.spinner("Gemini AI બ્લોગ લખી રહ્યું છે..."):
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(f"Write a viral, detailed blog post with headings based on this video transcript: {text}")
                        
                        st.markdown("---")
                        st.markdown("### 📝 Your Generated Blog Post")
                        st.write(response.text)
                        st.success("સફળતાપૂર્વક બ્લોગ તૈયાર થઈ ગયો!")
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("જો હજુ પણ એરર આવે, તો એકવાર Streamlit Dashboard પર જઈને 'Reboot App' કરો.")
