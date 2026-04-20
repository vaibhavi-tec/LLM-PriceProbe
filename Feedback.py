import streamlit as st
import base64

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
    /* Keep textarea text dark and readable */
    textarea {{
        color: #1a1a1a !important;
        background-color: #f0f0f0 !important;
    }}
    /* Button styling */
    div[data-testid="stButton"] > button {{
        background-color: #b7e7f6;
        color: #1a0a3d !important;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 8px 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.title("Feedback")
    st.write("We would love to hear your feedback!")

    st.subheader("Rate your experience (out of 5 stars):")
    rating = st.slider("", 1, 5, 3)

    stars = '⭐' * rating
    st.write("You selected:", stars)

    feedback = st.text_area("Please leave your feedback here:")

    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")


if __name__ == "__main__":
    app()