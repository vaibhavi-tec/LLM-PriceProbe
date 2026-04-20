import streamlit as st
import base64


def app():
    @st.cache_data
    def get_img_as_base64(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    img = get_img_as_base64("Images/Contact_1.png")

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url("data:Images/Contact.png;base64,{img}");
    background-size: cover;
    opacity: 100%;  # Adjust the opacity as needed
    z-index: -1;  # Ensure it's in the background
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)



# Remember to call the app function to display the app
if __name__ == "__main__":
    app()
