import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# પેજ કન્ફિગરેશન
st.set_page_config(page_title="Video to Blog AI", page_icon="📝")
st.title("🎥 YouTube Video to Blog Post Generator")

# સાઈડબારમાં API Key ઇનપુટ
api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")
youtube_link = st.text_input("Paste YouTube Video Link Here:")

# વિડિયો ID કાઢવાનું ફંક્શન
def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

if youtube_link:
    video_id = get_video_id(youtube_link)
    if video_id:
        # વિડિયોનું થંબનેલ બતાવવા માટે
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg")

        if st.button("Generate Blog Post"):
            if not api_key:
                st.error("મહેરબાની કરીને સાઈડબારમાં Gemini API Key નાખો!")
            else:
                try:
                    with st.spinner("વિડિયોમાંથી સબટાઈટલ (Transcript) મેળવી રહ્યા છીએ..."):
                        # સૌથી સ્ટેબલ રીત: સીધું જ હિન્દી કે ઇંગ્લિશ ટ્રાન્સક્રિપ્ટ મંગાવવી
                        # languages=['hi', 'en'] એટલે પહેલા હિન્દી ટ્રાય કરશે, નહીંતર ઇંગ્લિશ લેશે
                        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
                        text = " ".join([i['text'] for i in transcript_data])

                    with st.spinner("AI બ્લોગ પોસ્ટ લખી રહ્યું છે..."):
                        # Gemini AI કોન્ફિગરેશન
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-pro")
                        
                        prompt = f"""
                        You are a professional blog writer. 
                        Using the transcript below, write a detailed, viral, and SEO-friendly blog post. 
                        Transcript: {text}
                        """
                        
                        response = model.generate_content(prompt)
                        
                        st.markdown("---")
                        st.markdown("### 📝 Your Generated Blog Post")
                        st.write(response.text)
                        st.success("બ્લોગ તૈયાર થઈ ગયો છે!")
                        
                except Exception as e:
                    st.error(f"Transcript Error: આ વિડિયોમાં સબટાઈટલ મળ્યા નથી. મહેરબાની કરીને એવો વિડિયો વાપરો જેમાં Subtitles (CC) ચાલુ હોય. (Error: {e})")

# Footer
st.markdown("---")
st.caption("નોંધ: આ એપ ફક્ત સબટાઈટલ (CC) ધરાવતા વિડિયો પર જ કામ કરશે.")
