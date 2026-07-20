import requests
import streamlit as st
import requests
import streamlit as st

import requests
import streamlit as st

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="Boston House Price Prediction",
    page_icon="🏡",
    layout="wide"
)

# ----------------------------------------------------
# Custom CSS (Red Buttons)
# ----------------------------------------------------

st.markdown("""
<style>

.stButton > button{
    background-color:#DC2626;
    color:white;
    border:none;
    border-radius:8px;
    height:50px;
    font-size:16px;
    font-weight:bold;
}

.stButton > button:hover{
    background-color:#B91C1C;
    color:white;
}

[data-testid="stMetricValue"]{
    color:green;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

with st.sidebar:

    st.title("🏡 Model Information")

    st.info("""
**Model Name**
Boston House Price Prediction
""")

    st.divider()

    st.subheader("API Status")

    try:

        response = requests.get("http://127.0.0.1:8000/")

        if response.status_code == 200:
            st.success("🟢 API Online")
        else:
            st.error("🔴 API Offline")

    except:
        st.error("🔴 API Offline")

# ----------------------------------------------------
# Title
# ----------------------------------------------------

st.title("🏡 This is House Price Prediction Model for Boston Region of California, USA")

st.write(
    "Fill in the housing details below and click **Predict House Price**."
)

st.divider()

# ----------------------------------------------------
# Session State
# ----------------------------------------------------

if "prediction" not in st.session_state:
    st.session_state.prediction = None

# ----------------------------------------------------
# Reset Function
# ----------------------------------------------------

def reset_form():
    st.session_state.clear()
    st.rerun()

# ----------------------------------------------------
# Input Section
# ----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    income = st.number_input(
        "Average Area Income",
        min_value=0,
        value=80000
    )

    age = st.number_input(
        "Average House Age",
        min_value=0,
        value=5
    )

with col2:

    rooms = st.number_input(
        "Average Number of Rooms",
        min_value=1,
        value=7
    )

    population = st.number_input(
        "Area Population",
        min_value=0,
        value=25000
    )

st.divider()

# ----------------------------------------------------
# Buttons
# ----------------------------------------------------

button1, button2 = st.columns(2)

with button1:

    if st.button("Predict House Price", use_container_width=True):

        payload = {

            "Avg_Area_Income": income,
            "Avg_Area_House_Age": age,
            "Avg_Area_Number_of_Rooms": rooms,
            "Area_Population": population
        }

        with st.spinner("Predicting..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=payload
                )

                if response.status_code == 200:

                    prediction = response.json()["Predicted House Price"]

                    st.session_state.prediction = prediction

                else:

                    st.error("Prediction Failed.")

            except Exception as e:

                st.error("Unable to connect to FastAPI Server.")
                st.exception(e)

with button2:

    if st.button("Reset Inputs", use_container_width=True):
        reset_form()

# ----------------------------------------------------
# Prediction Result
# ----------------------------------------------------

if st.session_state.prediction is not None:

    st.divider()
    
    st.success("Prediction Completed Successfully!")

    st.metric(
        label="Estimated House Price",
        value=f"${st.session_state.prediction:,.2f}"
    ) 
# ----------------------------------------------------
# Footer
# ----------------------------------------------------
st.divider()

st.caption(
    "Boston Housing Price Prediction System | FastAPI + Streamlit"
)
