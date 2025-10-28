import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------
# 🌱 Title and Page Setup
# ---------------------------------------------
st.set_page_config(page_title="Samarth – Agri Data Insights", page_icon="🌾", layout="wide")

st.title("🌾 SAMARTH: Smart Agriculture Insights Dashboard")
st.markdown("""
Welcome to **SAMARTH**, an interactive dashboard that helps you explore India's crop production and rainfall data.  
Ask questions like:
- *Show top 5 crops by production in Tamil Nadu*  
- *Average rainfall in Maharashtra*  
- *Compare rainfall and crop production in Karnataka*  
- *Show rice production trend in Tamil Nadu*  
- *Compare rainfall between Punjab and Bihar*
""")

# ---------------------------------------------
# 📦 Database Connection
# ---------------------------------------------
DB_PATH = "agriculture_data.db"

@st.cache_data
def run_query(query, params=None):
    conn = sqlite3.connect(DB_PATH)
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# ---------------------------------------------
# 🧠 Helper Functions
# ---------------------------------------------
def extract_state(user_input):
    words = user_input.split()
    for i, word in enumerate(words):
        if word in ["in", "of", "for"] and i + 1 < len(words):
            return words[i + 1].capitalize()
    return None

def extract_two_states(user_input):
    parts = user_input.replace("and", ",").split(",")
    states = [p.strip().capitalize() for p in parts if p.strip()]
    return states[:2] if len(states) >= 2 else None


# ---------------------------------------------
# 🤖 Query Handler Function
# ---------------------------------------------
def answer_query(user_input):
    user_input = user_input.lower()

    # 1️⃣ Top crops by production
    if "top" in user_input and "crop" in user_input:
        state = extract_state(user_input)
        if state:
            query = f"""
            SELECT Item, SUM([2017-18]) AS Production
            FROM joined_crops_rainfall
            WHERE States LIKE '%{state}%'
            GROUP BY Item
            ORDER BY Production DESC
            LIMIT 5;
            """
            df = run_query(query)
            if not df.empty:
                st.subheader(f"🌾 Top 5 Crops by Production in {state} (2017-18)")
                st.bar_chart(df.set_index("Item"))
                st.dataframe(df)
            else:
                st.warning(f"No data found for {state}. Try another state.")

    # 2️⃣ Average rainfall in a state
    elif "rainfall" in user_input and "compare" not in user_input:
        state = extract_state(user_input)
        if state:
            query = f"""
            SELECT States, AVG(ANNUAL) AS Avg_Rainfall
            FROM joined_crops_rainfall
            WHERE States LIKE '%{state}%'
            GROUP BY States;
            """
            df = run_query(query)
            if not df.empty:
                st.subheader(f"🌧️ Average Annual Rainfall in {state}")
                st.metric(label="Average Rainfall (mm)", value=round(df["Avg_Rainfall"][0], 2))
            else:
                st.warning(f"No rainfall data available for {state}.")

    # 3️⃣ Compare rainfall and crop production in one state
    elif "compare" in user_input and "rainfall" in user_input and "production" in user_input:
        state = extract_state(user_input)
        if state:
            query = f"""
            SELECT YEAR, AVG(ANNUAL) AS Avg_Rainfall, SUM([2017-18]) AS Total_Production
            FROM joined_crops_rainfall
            WHERE States LIKE '%{state}%'
            GROUP BY YEAR
            ORDER BY YEAR;
            """
            df = run_query(query)
            if not df.empty:
                st.subheader(f"📊 Rainfall vs Crop Production Trend in {state}")
                fig, ax1 = plt.subplots(figsize=(8, 4))
                ax1.set_xlabel("Year")
                ax1.set_ylabel("Rainfall (mm)", color="tab:blue")
                ax1.plot(df["YEAR"], df["Avg_Rainfall"], color="tab:blue", marker="o", label="Rainfall")
                ax1.tick_params(axis="y", labelcolor="tab:blue")

                ax2 = ax1.twinx()
                ax2.set_ylabel("Production", color="tab:green")
                ax2.plot(df["YEAR"], df["Total_Production"], color="tab:green", marker="s", label="Production")
                ax2.tick_params(axis="y", labelcolor="tab:green")

                st.pyplot(fig)
                st.dataframe(df)
            else:
                st.warning(f"No comparison data found for {state}.")

    # 4️⃣ Crop production trend for one crop
    elif "trend" in user_input and "production" in user_input:
        words = user_input.split()
        crop = None
        state = extract_state(user_input)
        for i, word in enumerate(words):
            if word not in ["show", "production", "trend", "in", "of", "for", "and"]:
                crop = word.capitalize()
                break

        if crop and state:
            query = f"""
            SELECT YEAR, SUM([2017-18]) AS Production
            FROM joined_crops_rainfall
            WHERE States LIKE '%{state}%' AND Item LIKE '%{crop}%'
            GROUP BY YEAR
            ORDER BY YEAR;
            """
            df = run_query(query)
            if not df.empty:
                st.subheader(f"📈 {crop} Production Trend in {state}")
                st.line_chart(df.set_index("YEAR"))
                st.dataframe(df)
            else:
                st.warning(f"No data found for {crop} in {state}.")

    # 5️⃣ Compare rainfall between two states
    elif "compare" in user_input and "rainfall" in user_input:
        states = extract_two_states(user_input)
        if states and len(states) == 2:
            query = f"""
            SELECT States, AVG(ANNUAL) AS Avg_Rainfall
            FROM joined_crops_rainfall
            WHERE States IN ('{states[0]}', '{states[1]}')
            GROUP BY States;
            """
            df = run_query(query)
            if not df.empty:
                st.subheader(f"🌦️ Rainfall Comparison: {states[0]} vs {states[1]}")
                st.bar_chart(df.set_index("States"))
                st.dataframe(df)
            else:
                st.warning("No rainfall comparison data available for these states.")

    else:
        st.info("❓ Try asking about crop production, rainfall, comparison, or trend by state!")


# ---------------------------------------------
# 💬 User Input Box
# ---------------------------------------------
st.markdown("### 🔍 Ask Your Question")
user_question = st.text_input("Type your question below:")

if user_question:
    answer_query(user_question)

# ---------------------------------------------
# 📊 Footer and Credits
# ---------------------------------------------
st.markdown("---")
st.markdown("""
**📘 Data Sources:**  
- Ministry of Agriculture & Farmers Welfare  
- Indian Meteorological Department (IMD)  
- [data.gov.in](https://data.gov.in)

**Developed as part of:** Samarth Project – Phase 2 (Mini Web App)
""")
