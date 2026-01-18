import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'Wyniki_algorytmow.xlsx'  
sheet_name = 'Wizualizacja'
df = pd.read_excel(file_path, sheet_name=sheet_name)
df.columns = [col.strip() for col in df.columns]

numeric_columns = ['Fitness', 'Avg load', 'STD', 'Czas [s]']
for col in numeric_columns:
    df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

sns.set(style="whitegrid")
plt.rcParams.update({'figure.figsize': (10, 6), 'font.size': 12})


# 1. Fitness dla kazdego scenariusza i algorytmu

plt.figure()
sns.barplot(data=df, x="Scenariusz", y="Fitness", hue="Algorytm")
plt.title("Fitness w scenariuszach")
plt.ylabel("Fitness")
plt.tight_layout()
plt.show()


# 2. Czas obliczeń ---- podział na S1–S5 i S6
#print(df["Scenariusz"].unique())

df_s1_s5 = df[df["Scenariusz"].isin(["S1 (mały, gęstszy)", "S2 (średni, umiarkowany)", "S3 (duży, rzadki)", "S4 (średni gęsty)", "S5 (średni, bardzo gęsty)"])]
df_s6 = df[df["Scenariusz"] == "S6 (bardzo duży, bardzo gęsty)"]

# Wykres S1–S5
plt.figure()
sns.barplot(data=df_s1_s5, x="Scenariusz", y="Czas [s]", hue="Algorytm")
plt.title("Czas obliczeń w scenariuszach S1–S5")
plt.ylabel("Czas [s]")
plt.tight_layout()
plt.show()

# Osobny wykres dla S6
plt.figure()
sns.barplot(
    data=df_s6,
    x="Algorytm",
    y="Czas [s]",
    palette=["#5975A4", "#CC8963", "#5F9E6E"]  
)
plt.title("Czas obliczeń w scenariuszu S6")
plt.ylabel("Czas [s]")
plt.tight_layout()
plt.show()



# 3. Średnie obciążenie
plt.figure()
sns.lineplot(data=df, x="Scenariusz", y="Avg load", hue="Algorytm", marker="o")
plt.title("Średnie obciążenie w scenariuszach")
plt.ylabel("Avg load")
plt.tight_layout()
plt.show()


# 4. Odchylenie standardowe
plt.figure()
sns.lineplot(data=df, x="Scenariusz", y="STD", hue="Algorytm", marker="o")
plt.title("Odchylenie standardowe w scenariuszach")
plt.ylabel("STD")
plt.tight_layout()
plt.show()
