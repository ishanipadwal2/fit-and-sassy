import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os

# ---------- App Config ----------
st.set_page_config(page_title="Fit & Sassy 💃", page_icon="💓", layout="wide")
DATA_FILE = "health_data.csv"

# ---------- Load or create CSV ----------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
else:
    df = pd.DataFrame(columns=["Date", "Weight", "Height", "BMI", "Calories", "Water", "HeartRate", "Steps"])
    df.to_csv(DATA_FILE, index=False)

# ---------- Sidebar Navigation ----------
st.sidebar.title("🏥 Fit & Sassy Navigation")
page = st.sidebar.selectbox("Choose your page", ["Home", "💪 Buff or Fluff?", "🍔 Calorie Confessions",
                                                 "💧 Hydration Station", "❤️ Heart & Hustle",
                                                 "📋 Daily Summary", "📅 Weekly Targets"])

# ---------- Helper Functions ----------
def get_today_entries():
    today = pd.to_datetime(date.today())
    return df[df["Date"] == today]

# ---------- Dynamic Comments ----------
def calorie_comment(calories):
    calories = int(calories)
    if calories == 0:
        return "No calories logged today 😶 Are you fasting or just forgot?"
    elif calories < 1500:
        return "Light eater today 🍃 Good for you!"
    elif calories < 2500:
        return "Average human intake 😎 Nothing crazy."
    else:
        return "Whoa! 🍔🍕 Someone's having a feast today!"

def water_comment(water):
    if water == 0:
        return "Not a drop yet 😱 Go drink something!"
    elif water < 1.5:
        return "A little hydration, could do better 💦"
    elif water < 2.5:
        return "Perfect! Keep it flowing 💧"
    else:
        return "Hydration overload! 💦 You’re basically a fountain."

def steps_comment(steps):
    if steps == 0:
        return "Couch potato alert 🥔 Move your legs!"
    elif steps < 5000:
        return "A few steps today 👣 Not bad… barely."
    elif steps < 10000:
        return "Good job! 🚶‍♂️ Keep going."
    else:
        return "Step superstar 👑 Crushing it today!"

# ---------- Home Page ----------
if page == "Home":
    st.title("Fit & Sassy 💃")
    st.markdown("**Tracking your health… and judging your life choices 😏**")
    st.markdown("""
Hey there, human! 👋  

Welcome to **Fit & Sassy**, your **sarcastic, slightly rude health buddy**.  

Here, you can log your **Calories, Water intake, Steps, and Heart Rate**, and get **daily insights** sprinkled with humor.  

- 🎯 Check out your **Daily Summary** for a fun health snapshot.  
- 💧 Keep track of water and stay hydrated (or suffer the consequences 😉).  
- 👟 Log steps and pretend you did a workout today.  
- 🍔 Count calories while silently judging your snack choices.  
- ❤️ Monitor heart rate and see if your heart loves you back.  

Use the sidebar to navigate through the pages.
""")

    if st.button("🔄 Restart Weekly Logs"):
        df[['Weight','Height','BMI','Calories','Water','HeartRate','Steps']] = 0
        df.to_csv(DATA_FILE, index=False)
        st.success("All daily logs have been reset to 0! Weekly targets cleared.")
        st.experimental_rerun()

# ---------- BMI Page ----------
elif page == "💪 Buff or Fluff?":
    st.title("💪 Buff or Fluff?")
    st.markdown("**Let’s see if you’re a snack or a full buffet 🥗🍔**")

    weight = st.number_input("Enter your weight (kg):", min_value=0.0, step=0.1, format="%.1f", value=0.0)
    height = st.number_input("Enter your height (m):", min_value=0.0, step=0.01, format="%.2f", value=0.0)

    if st.button("Calculate BMI"):
        if height > 0 and weight > 0:
            bmi = weight / ((height /100)** 2)
            if bmi < 18.5:
                st.warning(f"Your BMI is **{bmi:.2f}** → Underweight 🥺 Eat a burger!")
            elif bmi < 24.9:
                st.success(f"Your BMI is **{bmi:.2f}** → Normal 😎 Looking good!")
            elif bmi < 29.9:
                st.info(f"Your BMI is **{bmi:.2f}** → Overweight 🤔 Maybe skip cake...")
            else:
                st.error(f"Your BMI is **{bmi:.2f}** → Obese 😱 Doctor alert!")
        else:
            st.error("Enter both weight and height greater than 0!")

# ---------- Calories Page ----------
elif page == "🍔 Calorie Confessions":
    st.title("🍔 Calorie Confessions")
    st.markdown("**Counting calories… because someone has to 😅**")
    calories_today = st.number_input("Enter calories consumed:", min_value=0, step=1, value=0)

    if st.button("Log Calories"):
        today = pd.to_datetime(date.today())
        entry = {"Date": today, "Weight": 0, "Height": 0, "BMI": 0,
                 "Calories": calories_today, "Water": 0.0, "HeartRate": 0, "Steps": 0}
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Calories logged: {calories_today} kcal → {calorie_comment(calories_today)}")

# ---------- Water Page ----------
elif page == "💧 Hydration Station":
    st.title("💧 Hydration Station")
    st.markdown("**Drink or shrivel – your choice 🥲**")
    water_today = st.number_input("Enter water intake today (L):", min_value=0.0, step=0.1, value=0.0)

    if st.button("Log Water"):
        today = pd.to_datetime(date.today())
        entry = {"Date": today, "Weight": 0, "Height": 0, "BMI": 0,
                 "Calories": 0, "Water": water_today, "HeartRate": 0, "Steps": 0}
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Water logged: {water_today} L → {water_comment(water_today)}")

# ---------- Heart & Activity Page ----------
elif page == "❤️ Heart & Hustle":
    st.title("❤️ Heart & Hustle")
    st.markdown("**Steps, heartbeats, and judging your laziness 👀**")

    heart_rate = st.number_input("Enter your resting heart rate (bpm):", min_value=0, max_value=200, step=1, value=0)
    steps = st.number_input("Enter steps today:", min_value=0, step=100, value=0)

    if st.button("Log Heart & Activity"):
        today = pd.to_datetime(date.today())
        entry = {"Date": today, "Weight": 0, "Height": 0, "BMI": 0,
                 "Calories": 0, "Water": 0.0, "HeartRate": heart_rate, "Steps": steps}
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Heart rate: {heart_rate} bpm, Steps: {steps} → {steps_comment(steps)}")

# ---------- Daily Summary Page ----------
elif page == "📋 Daily Summary":
    st.title("📋 Daily Summary Dashboard")
    st.markdown("**Today’s health snapshot 😏**")

    today_entries = get_today_entries()
    if not today_entries.empty:
        latest_calories = today_entries[today_entries['Calories'] > 0]['Calories'].iloc[-1] if not today_entries[today_entries['Calories'] > 0].empty else 0
        latest_water = today_entries[today_entries['Water'] > 0]['Water'].iloc[-1] if not today_entries[today_entries['Water'] > 0].empty else 0
        latest_steps = today_entries[today_entries['Steps'] > 0]['Steps'].iloc[-1] if not today_entries[today_entries['Steps'] > 0].empty else 0
        latest_hr = today_entries[today_entries['HeartRate'] > 0]['HeartRate'].iloc[-1] if not today_entries[today_entries['HeartRate'] > 0].empty else 0

        st.markdown(f"- Calories: {latest_calories} kcal → {calorie_comment(latest_calories)}")
        st.markdown(f"- Water: {latest_water} L → {water_comment(latest_water)}")
        st.markdown(f"- Steps: {latest_steps} → {steps_comment(latest_steps)}")

        if latest_hr > 0:
            if latest_hr < 60: hr_msg = f"❤️ Heart Rate: {latest_hr} bpm → Bradycardia 🐢"
            elif latest_hr <= 100: hr_msg = f"❤️ Heart Rate: {latest_hr} bpm → Normal 😎"
            else: hr_msg = f"❤️ Heart Rate: {latest_hr} bpm → Tachycardia ⚡"
        else:
            hr_msg = "Heart rate not logged."
        st.markdown(f"- {hr_msg}")
    else:
        st.info("No logs today yet!")

# ---------- Weekly Targets Page ----------
elif page == "📅 Weekly Targets":
    st.title("📅 Weekly Targets Dashboard")
    st.markdown("**Your weekly progress based on all daily logs 😏**")

    last_7_days = df[df['Date'] >= (pd.to_datetime(date.today()) - timedelta(days=6))]

    if not last_7_days.empty:
        total_steps = last_7_days['Steps'].sum()
        total_water = last_7_days['Water'].sum()
        total_calories = last_7_days['Calories'].sum()

        st.metric("👟 Steps (goal: 35,000)", f"{total_steps} / 35,000")
        st.metric("💧 Water (goal: 14L)", f"{total_water:.1f} / 14")
        st.metric("🍔 Calories (goal: 12,500 kcal)", f"{total_calories} / 12,500")

        if total_steps >= 35000: st.success("🏃 Step champion! Weekly goal achieved!")
        else: st.info("👟 Keep walking! You haven’t hit 35k yet.")
        if total_water >= 14: st.success("💦 Hydration hero! Weekly water goal achieved!")
        else: st.info("💧 Drink more water to reach 14L this week!")
        if total_calories <= 12500: st.success("🍽️ Calorie control on point!")
        else: st.info("⚠️ Calories exceeded weekly target!")
    else:
        st.info("No logs in the last 7 days yet.")
