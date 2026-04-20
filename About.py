import streamlit as st
import requests
import base64
from streamlit_lottie import st_lottie
from PIL import Image

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_chat = load_lottieurl("https://lottie.host/5ffa2a08-5d35-471b-9bfd-0674c8f6e509/LpYaKfQbPj.json")
goal_img = Image.open("Images/about.png")
robo2_img = Image.open("Images/robo2.png")

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
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] div,
    [data-testid="stAppViewContainer"] label {{
        color: white !important;
    }}
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3 {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Introduction to the Team")
            st.write(
                """
                Our team at priceProbe is a dedicated group of individuals with a passion for technology and e-commerce. 
                From software engineers to data scientists, each member brings a unique skillset that drives our mission to provide top-notch service to our customers.
                Together, we work tirelessly to enhance the user experience and deliver exceptional results.
                """
            )
        with right_column:
            st_lottie(lottie_chat, height=300, key="coding")

    st.write("---")

    with st.container():
        image_column, text_column = st.columns((1, 2))
        with image_column:
            st.image(goal_img, use_container_width=True)
        with text_column:
            st.header("Purpose and Goals")
            st.write("""
            Our primary goal at priceProbe is to offer our customers a seamless shopping experience by 
            comparing prices from various websites and providing personalized recommendations based on their preferences.
            We strive to help our customers save time and money by ensuring they receive the best deals available in the market.
            """)

    st.write("---")

    with st.container():
        text_column, image_column = st.columns((2, 1))
        with text_column:
            st.header("Offerings")
            st.write("""
            At priceProbe, we offer a wide range of products across various categories, including electronics, fashion, home goods, and more.
            Our platform uses machine learning algorithms to analyze pricing data and make personalized recommendations to help you find the best deals.
            With our user-friendly interface, shopping has never been easier.
            """)
        with image_column:
            st.image(robo2_img, use_container_width=True)

    st.write("---")

    st.image('Images/web_main.png', caption='Websites Available in our website', use_container_width=True)


if __name__ == "__main__":
    app()