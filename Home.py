import streamlit as st
import base64
from PIL import Image
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

goal_img = Image.open("Images/about.png")
lottie_robo = load_lottieurl("https://lottie.host/163566a4-aa6a-4317-8da9-38488f3a179e/eHSnBc2526.json")

def app():

    @st.cache_data
    def get_img_as_base64(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    bg  = get_img_as_base64("Images/main bg.png")
    hero_img = get_img_as_base64("Images/home_1.png")

    page_bg_img = f"""
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

    .block-container {{
        padding-top: 0.5rem !important;
    }}

    /* Hero layout */
    .hero-section {{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        padding: 0px 0px 20px 0px;
    }}

    .hero-left {{
        flex: 1.2;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .hero-right {{
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .hero-right img {{
        width: 100%;
        max-height: 420px;
        object-fit: contain;
    }}

    .hero-title {{
        color: #95e6ff !important;   /* changed from #b7e7f6 */
        font-weight: 900;
        font-size: 90px;
        line-height: 1;
        margin: 0 0 16px 0;
    }}

    .hero-text {{
        color: black !important;
        font-style: italic;
        font-size: 17px;
        margin-bottom: 28px;
    }}

    .hero-buttons {{
        display: flex;
        gap: 16px;
    }}

    .btn-learn {{
        background-color: #b7e7f6;
        color: #95e6ff !important;   /* changed text color */
        border: none;
        border-radius: 8px;
        font-weight: bold;
        font-size: 15px;
        padding: 12px 32px;
        cursor: pointer;
        text-decoration: none;
    }}

    .btn-demo {{
        background-color: transparent;
        color: #95e6ff !important;   /* changed text color */
        border: 2px solid #65F6FF;
        border-radius: 8px;
        font-weight: bold;
        font-size: 15px;
        padding: 12px 32px;
        cursor: pointer;
    }}

    /* Streamlit button styling for below sections */
    div[data-testid="stButton"] > button {{
        border-radius: 8px;
        font-weight: bold;
        font-size: 15px;
        padding: 10px 28px;
        width: 100%;
    }}

    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

    # ── Hero section: pure HTML so image and text are truly parallel ──────────
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-left">
            <h1 class="hero-title">PriceProbe</h1>
            <p class="hero-text">
                Welcome to Price Probe, your go-to destination for E-commerce products at the lowest prices.
                We understand the importance of affordability without compromising on quality, 
                and we are here to make your online shopping experience more budget-friendly.
            </p>
            <div class="hero-buttons">
                <span style="color:white; font-size:13px; opacity:0.7;">👇 Use the sidebar buttons below to navigate</span>
            </div>
        </div>
        <div class="hero-right">
            <img src="data:image/png;base64,{hero_img}" alt="PriceProbe Shopping"/>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Real Streamlit buttons for navigation ─────────────────────────────────
    btn_col1, btn_col2, _ = st.columns((1, 1, 3))
    with btn_col1:
        if st.button("📖 Learn More", key="learn_more"):
            st.session_state["nav_override"] = "About"
            st.rerun()
    with btn_col2:
        if st.button("🤖 Demo", key="demo"):
            st.session_state["nav_override"] = "ChatBot"
            st.rerun()

    st.write("---")

    # ── About section ─────────────────────────────────────────────────────────
    with st.container():
        image_column, text_column = st.columns((1.7, 2))
        with image_column:
            st.image(goal_img, use_container_width=True)
        with text_column:
            st.header("About Price Probe")
            st.write("""
            At Price Probe, we pride ourselves on offering a wide range of E-commerce products ranging from electronics to fashion,
            all carefully selected to provide you with the best value for your money. 
            Our team works tirelessly to ensure that our inventory is up-to-date with the latest trends and deals in the market.
            """)

    st.write("---")

    # ── Compares Websites ─────────────────────────────────────────────────────
    with st.container():
        st.header("Compares Websites")
        st.image('Images/web_main.png', caption='Websites Available in our website', use_container_width=True)

    st.write("---")

    # ── Product Categories ────────────────────────────────────────────────────
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Product Categories")
            st.write(
                """
                Explore our diverse product categories to find exactly what you're looking for at a fraction of the cost.
                From gadgets and accessories to clothing and home essentials, Price Probe has everything you need and more.
                """
            )
        with right_column:
            st_lottie(lottie_robo, height=300, key="coding")


if __name__ == "__main__":
    app()