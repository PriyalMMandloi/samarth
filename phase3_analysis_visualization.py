import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIG ---
DB_PATH = "agriculture_data.db"

# --- STEP 1: Load joined data ---
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT * FROM joined_crops_rainfall;", conn)
conn.close()
print(f"✅ Loaded joined data — {len(df)} rows, {len(df.columns)} columns")

# --- STEP 2: Preview data ---
print("\n📋 Columns:", list(df.columns))
print("\n🔍 Sample data:")
print(df.head())

# --- STEP 3: Convert rainfall values & crop yields to numeric (ignore errors) ---
df = df.apply(pd.to_numeric, errors='ignore')

# --- STEP 4: Example 1 — Average annual rainfall by state ---
avg_rain = df.groupby('States')['ANNUAL'].mean().sort_values(ascending=False)
print("\n🌧️ Average Annual Rainfall by State:")
print(avg_rain)

# --- STEP 5: Example 2 — Compare rainfall and one crop’s yield ---
# Pick any crop item present in your data (check df['Item'].unique())
crop_name = df['Item'].unique()[0]  # you can replace with your crop, e.g. 'Sugarcane'
df_crop = df[df['Item'] == crop_name]

plt.figure(figsize=(10,6))
plt.plot(df_crop['YEAR'], df_crop['ANNUAL'], marker='o', label='Rainfall (mm)')
plt.title(f"Rainfall Trend for {crop_name}")
plt.xlabel("Year")
plt.ylabel("Rainfall (mm)")
plt.legend()
plt.grid(True)
plt.show()

# --- STEP 6: Example 3 — Correlation between rainfall & crop yield (2017-18 column) ---
if '2017-18' in df.columns:
    corr = df['ANNUAL'].corr(df['2017-18'])
    print(f"\n📈 Correlation between rainfall and {crop_name} yield (2017-18): {corr:.3f}")
