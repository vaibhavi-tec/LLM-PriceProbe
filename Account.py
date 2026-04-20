import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests
import os
from dotenv import load_dotenv
from PIL import Image
import base64

load_dotenv()

firebase_api_key = os.getenv("FIREBASE_API_KEY")

if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    firebase_admin.initialize_app(cred)


def app():

    @st.cache_data
    def get_img_as_base64(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    bg = get_img_as_base64("Images/main bg.png")

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stAppViewContainer"] > .main {{
        background: transparent !important;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0) !important;
    }}

    /* White text for general labels and headings */
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] label {{
        color: white !important;
    }}
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3 {{
        color: white !important;
    }}

    /* Input fields — dark text so it's readable on white background */
    input[type="text"],
    input[type="email"],
    input[type="password"],
    input {{
        color: #1a1a1a !important;
        background-color: #f0f0f0 !important;
    }}

    /* Selectbox text */
    [data-testid="stSelectbox"] div[data-baseweb="select"] div {{
        color: #1a1a1a !important;
    }}

    /* Button text dark */
    div[data-testid="stButton"] > button {{
        color: #1a0a3d !important;
        background-color: #b7e7f6;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 8px 20px;
    }}

    div[data-testid="stButton"] > button:hover {{
        background-color: #81d7f1;
        color: #1a0a3d !important;
    }}

    </style>
    """, unsafe_allow_html=True)

    st.title('Welcome to :color[PriceProbe]{foreground="#95e6ff"} :sunglasses:')

    if 'username'       not in st.session_state: st.session_state.username       = ''
    if 'useremail'      not in st.session_state: st.session_state.useremail      = ''
    if 'signedout'      not in st.session_state: st.session_state.signedout      = False
    if 'signout'        not in st.session_state: st.session_state.signout        = False
    if 'email_input'    not in st.session_state: st.session_state.email_input    = ''
    if 'password_input' not in st.session_state: st.session_state.password_input = ''

    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = json.dumps({
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token,
                **({"displayName": username} if username else {})
            })
            r = requests.post(rest_api_url, params={"key": firebase_api_key}, data=payload)
            try:
                return r.json()['email']
            except Exception:
                st.warning(r.json())
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    def sign_in_with_email_and_password(email, password, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            payload = json.dumps({
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token,
            })
            r = requests.post(rest_api_url, params={"key": firebase_api_key}, data=payload)
            data = r.json()
            try:
                return data['email'], data.get('displayName', '')
            except Exception:
                st.warning(data)
        except Exception as e:
            st.warning(f'Login failed: {e}')

    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
            r = requests.post(rest_api_url, params={"key": firebase_api_key}, data=payload)
            if r.status_code == 200:
                return True
            else:
                st.warning(r.json())
                return False
        except Exception as e:
            st.warning(f'Password reset failed: {e}')
            return False

    def login():
        result = sign_in_with_email_and_password(
            st.session_state.email_input,
            st.session_state.password_input
        )
        if result:
            email, username = result
            st.session_state.username  = username
            st.session_state.useremail = email
            st.session_state.signedout = True
            st.session_state.signout   = True

    def logout():
        st.session_state.username  = ''
        st.session_state.useremail = ''
        st.session_state.signedout = False
        st.session_state.signout   = False

    def forgot_password():
        email = st.session_state.get('email_input', '')
        if email:
            if reset_password(email):
                st.success(f'Password reset email sent to {email}')
        else:
            st.warning('Please enter your email address first.')

    if not st.session_state.signedout:
        choice   = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email    = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        st.session_state.email_input    = email
        st.session_state.password_input = password

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            if st.button('Create my account'):
                user = sign_up_with_email_and_password(
                    email=email, password=password, username=username
                )
                if user:
                    st.success('Account created successfully!')
                    st.info('Please login using your email and password.')
                    st.balloons()
        else:
            st.button('Login', on_click=login)
            if st.button('Forgot Password?'):
                forgot_password()

    if st.session_state.signout:
        st.success(f'Welcome back, {st.session_state.username or st.session_state.useremail}!')
        st.text('Name : ' + st.session_state.username)
        st.text('Email: ' + st.session_state.useremail)
        st.button('Sign out', on_click=logout)