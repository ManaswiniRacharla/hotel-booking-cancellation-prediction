import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Hotel Booking Cancellation",
    page_icon="🏨",
    layout="centered"
)

# ---------------- ULTRA ADVANCED STYLING ----------------
st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* App background */
.stApp {
    background-color: #0b1d51;
    font-family: 'Poppins', sans-serif;
}

/* Glassmorphism main card */
.block-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: none;
    padding: 3rem 3.5rem;
    border-radius: 22px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.5);
    max-width: 950px;
    animation: floatIn 1s ease forwards;
}

/* Floating animation */
@keyframes floatIn {
    from {
        opacity: 0;
        transform: translateY(30px) scale(0.97);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* Main Title */
h1, .shimmer-title {
    text-align: center;
    font-weight: 700;
    font-size: 2.6rem;
    color: #FFFFFF;
    text-shadow: 0 0 6px rgba(255,255,255,0.3);
}


/* Subtitle */
.subtitle {
    text-align: center;
    color: #FFFFFF;
    font-size: 16px;
    margin-bottom: 2rem;
    text-shadow: 0 0 10px rgba(255,255,255,0.4);
    background: linear-gradient(90deg, #ffffff, #ffe066, #ffffff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 2s linear infinite;
}

/* Section headers */
.shimmer-header {
    color: #FFFFFF;
    font-weight: 600;
    font-size: 1.8rem;
    text-shadow: 0 0 4px rgba(255,255,255,0.2);
}


/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #ffffff50, transparent);
    margin: 2rem 0;
}

/* Labels */
label {
    color: #FFFFFF !important;
    font-weight: 500;
}

/* Inputs */
input, select {
    background-color: rgba(255, 255, 255, 0.0) !important;
    color: #000000 !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    transition: all 0.25s ease;
    padding-left: 10px;
}

/* Input focus */
input:focus, select:focus {
    border-color: #FFFFFF !important;
    box-shadow: 0 0 0 3px rgba(255,255,255,0.25) !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: #FFFFFF;
    font-size: 17px;
    font-weight: 600;
    padding: 14px 28px;
    border-radius: 14px;
    border: none;
    width: 100%;
    margin-top: 1.8rem;
    transition: all 0.35s ease;
    box-shadow: 0 0 25px rgba(255,255,255,0.3);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #3555a2, #4067c0);
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 0 35px rgba(255,255,255,0.5);
}

.footer {
    text-align: center;
    font-size: 13px;
    color: #FFFFFF;
    margin-top: 3rem;
    text-shadow: 0 0 5px rgba(255,255,255,0.3);
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1 class='shimmer-title'>🏨 Hotel Booking Cancellation Prediction</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>AI-powered intelligent system for predicting hotel booking cancellations</div>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return joblib.load("hotel_booking_best_model.pkl")

model = load_model()

# ---------------- INPUTS ----------------
st.markdown("<h2 class='shimmer-header'>Booking Details</h2>", unsafe_allow_html=True)
st.info("Please fill in the booking details below.")

lead_time = st.number_input("How many days before arrival was the booking made?", 0, 500, 50)
adults = st.number_input("Number of adults staying", 1, 5, 2)
children = st.number_input("Number of children staying", 0, 5, 0)
babies = st.number_input("Number of babies (infants)", 0, 2, 0)

meal_display = st.selectbox(
    "Meal plan selected",
    [
        "BB – Bed & Breakfast",
        "HB – Half Board (Breakfast + Dinner)",
        "FB – Full Board (All meals included)",
        "SC – Self Catering (No meals)"
    ]
)
meal = meal_display.split(" ")[0]

market_segment_display = st.selectbox(
    "How was the booking made?",
    [
        "Direct – Booked directly with the hotel",
        "Corporate – Company or business booking",
        "Online TA – Online travel website",
        "Offline TA/TO – Travel agent or tour operator"
    ]
)
market_segment = market_segment_display.split(" – ")[0]

deposit_display = st.selectbox(
    "Deposit type",
    [
        "No Deposit – Nothing paid in advance",
        "Non Refund – Advance payment, not refundable",
        "Refundable – Advance payment, refundable"
    ]
)
deposit_type = deposit_display.split(" – ")[0]

customer_display = st.selectbox(
    "Customer type",
    [
        "Transient – Individual traveler",
        "Contract – Long-term contract booking",
        "Transient-Party – Group of individuals",
        "Group – Large group booking"
    ]
)
customer_type = customer_display.split(" – ")[0]

arrival_date_month = st.selectbox(
    "Arrival month",
    [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]
)

country = st.text_input(
    "Guest country code (e.g., IND for India, USA for United States)",
    "PRT"
)

# ---------------- PREDICTION ----------------
if st.button("🚀 Predict Booking Status"):
    input_df = pd.DataFrame({
        "lead_time": [lead_time],
        "adults": [adults],
        "children": [children],
        "babies": [babies],
        "meal": [meal],
        "market_segment": [market_segment],
        "deposit_type": [deposit_type],
        "customer_type": [customer_type],
        "arrival_date_month": [arrival_date_month],
        "country": [country],
        "booking_changes": [0],
        "stays_in_weekend_nights": [0],
        "stays_in_week_nights": [1],
        "required_car_parking_spaces": [0],
        "adr": [100.0],
        "days_in_waiting_list": [0],
        "previous_bookings_not_canceled": [0],
        "previous_cancellations": [0],
        "is_repeated_guest": [0],
        "total_of_special_requests": [0]
    })

    prediction = model.predict(input_df)[0]

    if prediction == 1:
        st.error("❌ Prediction: High chance of booking cancellation")
    else:
        st.success("✅ Prediction: Booking is likely to be confirmed")

# ---------------- FOOTER ----------------
st.markdown(
    "<div class='footer'>Powered by Machine Learning • Hotel Analytics System</div>",
    unsafe_allow_html=True
)
