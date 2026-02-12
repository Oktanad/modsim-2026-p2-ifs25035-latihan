import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Dashboard Visualisasi Kuesioner")

# ===============================
# LOAD DATA
# ===============================
file_path = "data_kuesioner.xlsx"
df = pd.read_excel(file_path)

if "Partisipan" in df.columns:
    df = df.drop(columns=["Partisipan"])

df_long = df.melt(var_name="Pertanyaan", value_name="Jawaban")

df_long["Jawaban"] = (
    df_long["Jawaban"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ===============================
# MAPPING SKOR
# ===============================
skor_map = {
    "SS": 6,
    "S": 5,
    "CS": 4,
    "CTS": 3,
    "TS": 2,
    "STS": 1
}

df_long["Skor"] = df_long["Jawaban"].map(skor_map)

# ===============================
# URUTAN Q1 - Q17
# ===============================
urutan_pertanyaan = [f"Q{i}" for i in range(1, 18)]

df_long["Pertanyaan"] = pd.Categorical(
    df_long["Pertanyaan"],
    categories=urutan_pertanyaan,
    ordered=True
)

# ===============================
# 1️⃣ DISTRIBUSI KESELURUHAN
# ===============================
st.subheader("1️⃣ Distribusi Jawaban Keseluruhan")

distribusi = df_long["Jawaban"].value_counts().reset_index()
distribusi.columns = ["Jawaban", "Jumlah"]

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        distribusi,
        x="Jawaban",
        y="Jumlah",
        text_auto=True,
        title="Bar Chart Distribusi Jawaban"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(
        distribusi,
        names="Jawaban",
        values="Jumlah",
        title="Pie Chart Proporsi Jawaban"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ===============================
# 2️⃣ STACKED BAR PER PERTANYAAN
# ===============================
st.subheader("2️⃣ Distribusi Jawaban per Pertanyaan (Q1 - Q17)")

stacked = (
    df_long
    .groupby(["Pertanyaan", "Jawaban"])
    .size()
    .reset_index(name="Jumlah")
    .sort_values("Pertanyaan")
)

fig3 = px.bar(
    stacked,
    x="Pertanyaan",
    y="Jumlah",
    color="Jawaban",
    title="Stacked Bar per Pertanyaan"
)

fig3.update_layout(barmode="stack")

st.plotly_chart(fig3, use_container_width=True)

# ===============================
# 3️⃣ RATA-RATA SKOR
# ===============================
st.subheader("3️⃣ Rata-Rata Skor per Pertanyaan")

rata_skor = (
    df_long
    .groupby("Pertanyaan")["Skor"]
    .mean()
    .reset_index()
    .sort_values("Pertanyaan")
)

fig4 = px.bar(
    rata_skor,
    x="Pertanyaan",
    y="Skor",
    text_auto=True,
    title="Rata-Rata Skor (Q1 - Q17)"
)

st.plotly_chart(fig4, use_container_width=True)

# ===============================
# 4️⃣ KATEGORI JAWABAN
# ===============================
st.subheader("4️⃣ Distribusi Kategori Jawaban")

def kategori(j):
    if j in ["SS", "S"]:
        return "Positif"
    elif j == "CS":
        return "Netral"
    else:
        return "Negatif"

df_long["Kategori"] = df_long["Jawaban"].apply(kategori)

kategori_dist = df_long["Kategori"].value_counts().reset_index()
kategori_dist.columns = ["Kategori", "Jumlah"]

fig5 = px.bar(
    kategori_dist,
    x="Kategori",
    y="Jumlah",
    text_auto=True,
    title="Distribusi Positif, Netral, Negatif"
)

st.plotly_chart(fig5, use_container_width=True)