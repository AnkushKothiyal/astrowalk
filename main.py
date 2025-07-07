"""
Astrowalk
Author: Ankush kothiyal
"""
import streamlit as st
import datetime
import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.0-flash")

# Page config
st.set_page_config(
    page_title="Astrowalk: Let the stars guide you", 
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Function to load CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Load CSS from external file
load_css('styles.css')


# Main title with custom styling
st.markdown('<h1 class="main-title">✨ Astrowalk: Let the stars guide you ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter your date of birth and what you\'d like guidance on, and we\'ll craft a personalized reading.</p>', unsafe_allow_html=True)

# Form inputs with custom styling
st.markdown("### 📅 Enter your Date of Birth")
date = st.date_input("", min_value=datetime.date(1950, 1, 1), label_visibility="collapsed")

st.markdown("### 💭 What do you need help with?")
situation = st.text_area("", placeholder="I am struggling to find love", label_visibility="collapsed")

# Get zodiac sign function
def get_zodiac_sign(month: int, day: int) -> str:
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    else:
        return "Capricorn"

zodiac_sign = get_zodiac_sign(date.month, date.day)

# Prompt for AI
prompt = f"""
    You are an AI assistant designed to console people who share their problems with you. Your response should:

    1. Be brief and empathetic, limited to 3–4 lines.

    2. Reassure them by normalizing their experience, emphasizing that many others face similar struggles.

    3. Affirm that they are doing well despite the challenges.

    4. Provide a few simple, practical suggestions they can implement to help improve their situation.

    5. Avoid any introductory or concluding phrases — respond directly with the consolation message only.

    6. Focus on balancing empathy with actionable advice, offering comfort while empowering the person to take small positive steps.

    Here is the situation: {situation}
"""

# Configure API
genai.configure(api_key=st.secrets["key"])

# Remarks
remark1 = f'''As a {zodiac_sign}, you share this sign with nearly a billion others. While astrology can be fun and meaningful to some, 
it's important to remember that scientific studies have found no evidence that planets or stars influence our personalities or destinies. 
You are unique because of who you are, not because of your birth sign.'''

remark2 = "Don't let them fool you, Astrology is a proven Pseudoscience: https://en.wikipedia.org/wiki/Astrology_and_science"

# Submit button
if st.button("🌟 Submit"):
    if not situation.strip():
        st.error("Please enter what you need help with!")
    else:
        try:
            # Loading message
            with st.spinner('✨ Figuring out your zodiac sign and crafting your reading...'):
                response = model.generate_content(prompt)
                
                # Display results with custom background container
                st.markdown(f'''
                <div class="results-container">
                    <h3>🔮 Your Personalized Reading</h3>
                    <p>{response.text}</p>
                    <div class="remark1">{remark1}</div>
                    <div class="remark2">{remark2}</div>
                </div>
                ''', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {e}")
            st.error("Oops, the program isn't working for some reason, try some nearby baba please")

# Footer
st.markdown('<div class="footer">Created by Ankush Kothiyal</div>', unsafe_allow_html=True)
