import streamlit as st
from streamlit_option_menu import option_menu
import Account, About, Feedback, Contact, Chatbot, Home

st.set_page_config(
    page_title="PriceProbe",
    layout="wide",
    page_icon="💰",
)

st.markdown("""
<style>
[data-testid="stSidebar"] > div:first-child {
    background-color: #403B83;
}
</style>
""", unsafe_allow_html=True)


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        # Check if a button triggered a navigation override
        nav_override = st.session_state.get("nav_override", None)

        # Map override names to option_menu index
        page_index_map = {
            "Home": 0,
            "Account": 1,
            "About": 2,
            "Feedback": 3,
            "ChatBot": 4,
            "Contact": 5,
        }

        default_index = page_index_map.get(nav_override, 0) if nav_override else 0

        with st.sidebar:
            try:
                st.image("Images/robo1.png", use_container_width=True)
            except Exception:
                pass

            app = option_menu(
                menu_title="PriceProbe",
                options=["Home", "Account", "About", "Feedback", "ChatBot", "Contact"],
                icons=[
                    "house-fill",
                    "person-circle",
                    "info-circle-fill",
                    "gear-wide-connected",
                    "chat-left-dots-fill",
                    "telephone-fill",
                ],
                menu_icon="bag-heart",
                default_index=default_index,
                styles={
                    "container":         {"padding": "5!important", "background-color": "#403B83"},
                    "icon":              {"color": "white", "font-size": "23px"},
                    "nav-link":          {
                        "color": "white",
                        "font-size": "20px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#36316D",
                    },
                    "nav-link-selected": {"background-color": "#797AC5"},
                },
            )

        # Clear the override after it's been used
        if nav_override:
            del st.session_state["nav_override"]

        if app == "Home":
            Home.app()
        elif app == "Account":
            Account.app()
        elif app == "About":
            About.app()
        elif app == "Feedback":
            Feedback.app()
        elif app == "ChatBot":
            Chatbot.app()
        elif app == "Contact":
            Contact.app()
        


multi_app = MultiApp()
multi_app.run()