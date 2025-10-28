import sqlite3
import pandas as pd

# --- Connect to database ---
conn = sqlite3.connect("agriculture_data.db")
print("✅ Connected to database")

# --- Load tables ---
df_crops = pd.read_sql("SELECT * FROM commercial_crops", conn)
df_rain = pd.read_sql("SELECT * FROM rainfall", conn)

print(f"🌾 Crops rows: {len(df_crops)}, 🌧️ Rainfall rows: {len(df_rain)}")

# --- Clean column names ---
df_crops.columns = df_crops.columns.str.strip()
df_rain.columns = df_rain.columns.str.strip()

print("📋 Columns in commercial_crops:", list(df_crops.columns))
print("📋 Columns in rainfall:", list(df_rain.columns))

# --- Fix and standardize join keys ---
# Rename for easier joining
if "States" in df_crops.columns:
    df_crops.rename(columns={"States": "State"}, inplace=True)
if "SUBDIVISION" in df_rain.columns:
    df_rain.rename(columns={"SUBDIVISION": "State"}, inplace=True)

# --- Perform join ---
df_joined = pd.merge(df_crops, df_rain, on="State", how="inner")
print(f"✅ Joined dataset created with {len(df_joined)} rows.")

# --- Save joined table ---
df_joined.to_sql("joined_data", conn, if_exists="replace", index=False)
print("💾 Joined data saved as table 'joined_data' in agriculture_data.db")

conn.close()
print("✅ Phase 2 complete — data joined and saved successfully!")
