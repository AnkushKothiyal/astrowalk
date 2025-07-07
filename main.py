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

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated stars background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #eee, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, #fff, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 160px 30px, #fff, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: twinkle 10s linear infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    
    /* Container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
        position: relative;
        z-index: 2;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 4px 20px rgba(255,255,255,0.5); }
        to { text-shadow: 0 4px 30px rgba(255,255,255,0.8); }
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #e0e0e0;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Form container styling */
    .form-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(10px);
    }
    
    /* CUSTOM RESULTS CONTAINER STYLING */
    .results-container {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        margin: 2rem 0;
        border: 2px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }
    
    .results-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        animation: float 20s linear infinite;
        pointer-events: none;
    }
    
    @keyframes float {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-20px, -20px); }
    }
    
    .results-container h3 {
        color: #ecf0f1;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        text-align: center;
        position: relative;
        z-index: 1;
    }
    
    .results-container p {
        color: #bdc3c7;
        font-size: 1.1rem;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Update remark styling for the new container */
    .results-container .remark1 {
        background: rgba(255, 193, 7, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #f1c40f;
        margin: 1.5rem 0;
        font-style: italic;
        color: #f39c12;
        position: relative;
        z-index: 1;
    }
    
    .results-container .remark2 {
        background: rgba(220, 53, 69, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #e74c3c;
        margin: 1.5rem 0;
        font-weight: 600;
        color: #e74c3c;
        position: relative;
        z-index: 1;
    }
    
    /* Input field styling */
    .stDateInput > div > div > input {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px;
        font-size: 16px;
        transition: all 0.3s ease;
        background: #f8f9fa;
    }
    
    .stDateInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        transform: translateY(-2px);
    }
    
    .stTextArea > div > div > textarea {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px;
        font-size: 16px;
        transition: all 0.3s ease;
        background: #f8f9fa;
        font-family: 'Poppins', sans-serif;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        transform: translateY(-2px);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 18px 0;
        font-size: 18px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Result container styling */
    .result-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
        border-left: 5px solid #667eea;
        backdrop-filter: blur(10px);
    }
    
    /* Remark styling */
    .remark1 {
        background: rgba(255, 193, 7, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        font-style: italic;
        color: #333;
    }
    
    .remark2 {
        background: rgba(220, 53, 69, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
        font-weight: 600;
        color: #333;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #ffffff;
        font-size: 1.1rem;
        margin-top: 2rem;
    }
    
    /* Loading spinner */
    .loading-text {
        text-align: center;
        color: #667eea;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .form-container {
            padding: 1.5rem;
        }
        .results-container {
            padding: 1.5rem;
        }
    }
    /* More specific textarea targeting with higher specificity */
    .stTextArea textarea,
    .stTextArea > div > div > textarea,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextArea"] > div > div > textarea {
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        background: #f8f9fa !important;
        font-family: 'Poppins', sans-serif !important;
        color: #333333 !important; /* Explicit text color */
    }

    .stTextArea textarea:focus,
    .stTextArea > div > div > textarea:focus,
    div[data-testid="stTextArea"] textarea:focus,
    div[data-testid="stTextArea"] > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        transform: translateY(-2px) !important;
        color: #333333 !important; /* Explicit text color on focus */
    }

    /* Placeholder styling */
    .stTextArea textarea::placeholder,
    .stTextArea > div > div > textarea::placeholder,
    div[data-testid="stTextArea"] textarea::placeholder,
    div[data-testid="stTextArea"] > div > div > textarea::placeholder {
        color: #999999 !important;
        opacity: 1 !important;
    }

    /* Alternative approach - target by attribute */
    textarea[aria-label=""],
    textarea[placeholder*="struggling"] {
        background: #f8f9fa !important;
        color: #333333 !important;
    }

    /* Fallback for all textareas */
    textarea {
        background: #f8f9fa !important;
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main title with custom styling
st.markdown('<h1 class="main-title">✨ Astrowalk: Let the stars guide you ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter your date of birth and what you\'d like guidance on, and we\'ll craft a personalized reading.</p>', unsafe_allow_html=True)

# Form inputs with custom styling
st.markdown("### 📅 Enter your Date of Birth")
date = st.date_input("", min_value=datetime.date(1950, 1, 1), label_visibility="collapsed")

st.markdown("### 💭 What do you need help with?")
situation = st.text_area("", placeholder="I am struggling to get married", label_visibility="collapsed")

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
