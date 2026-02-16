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
                    with st.spinner("વિડિયોમાંથી લખાણ (Transcript) મેળવી રહ્યા છીએ..."):
                        # ટ્રાન્સક્રિપ્ટ મેળવવાની એડવાન્સ રીત (Auto-generated સબટાઈટલ માટે)
                        try:
                            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                            
                            # પહેલા હિન્દી અને પછી ઇંગ્લિશ ટ્રાન્સક્રિપ્ટ શોધશે (મેન્યુઅલ અથવા ઓટો-જનરેટેડ)
                            try:
                                transcript = transcript_list.find_transcript(['hi', 'en'])
                            except:
                                # જો મેન્યુઅલ ન મળે તો જે પણ ઉપલબ્ધ હોય તે લેશે
                                transcript = transcript_list.find_generated_transcript(['hi', 'en'])
                            
                            transcript_data = transcript.fetch()
                            text = " ".join([i['text'] for i in transcript_data])
                        
                        except Exception as t_e:
                            st.error(f"Transcript Error: આ વિડિયોમાં સબટાઈટલ પકડવામાં સમસ્યા આવી રહી છે. ({t_e})")
                            st.stop()

                    with st.spinner("AI બ્લોગ પોસ્ટ લખી રહ્યું છે..."):
                        # Gemini AI કોન્ફિગરેશન
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-pro")
                        
                        prompt = f"""
                        You are a professional blog writer. 
                        Use the following YouTube transcript to write a detailed, engaging, and SEO-friendly blog post. 
                        Make sure to use proper headings (H1, H2, H3), bullet points, and a summary.
                        
                        Transcript: {text}
                        """
                        
                        response = model.generate_content(prompt)
                        
                        st.markdown("---")
                        st.markdown("### 📝 Your Generated Blog Post")
                        st.write(response.text)
                        st.success("બ્લોગ પોસ્ટ તૈયાર થઈ ગઈ છે!")
                        
                except Exception as e:
                    st.error(f"એક સમસ્યા આવી છે: {e}")

# Footer
st.markdown("---")
st.caption("નોંધ: આ એપ ફક્ત એવા જ વિડિયો પર કામ કરશે જેમાં સબટાઈટલ્સ (CC) ચાલુ હોય.")
