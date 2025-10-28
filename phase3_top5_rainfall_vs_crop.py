import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# --- Connect to DB ---
conn = sqlite3.connect("agriculture_data.db")
print("✅ Connected to database")

# --- Load joined data ---
df = pd.read_sql("SELECT * FROM joined_data", conn)
print(f"📦 Loaded {len(df)} joined rows")

# --- Convert numeric columns safely ---
for col in ["ANNUAL", "2014-15", "2015-16", "2016-17", "2017-18"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Aggregate by State ---
rainfall_avg = df.groupby("State")["ANNUAL"].mean().reset_index(name="Avg_Rainfall")
crop_cols = [c for c in ["2014-15", "2015-16", "2016-17", "2017-18"] if c in df.columns]
crop_avg = df.groupby("State")[crop_cols].mean().mean(axis=1).reset_index(name="Avg_Crop")

summary = pd.merge(rainfall_avg, crop_avg, on="State", how="inner")

# --- Top 5 States ---
top5 = summary.nlargest(5, "Avg_Rainfall")
print("🌦️ Top 5 States by Rainfall:")
print(top5)

# --- Visualization ---
plt.figure(figsize=(10, 6))
plt.bar(top5["State"], top5["Avg_Rainfall"], color="skyblue", label="Avg Rainfall (mm)")
plt.bar(top5["State"], top5["Avg_Crop"], color="orange", alpha=0.7, label="Avg Crop Production")
plt.title("Top 5 States: Rainfall vs Crop Production")
plt.xlabel("State")
plt.ylabel("Values")
plt.legend()
plt.tight_layout()
plt.show()

conn.close()
print("✅ Phase 3 complete — visualization displayed successfully!")
