import pandas as pd
import streamlit as st
import plotly.express as px

# ===================== LOAD DATA =====================
file_path = "data_kuesioner.xlsx"
df = pd.read_excel(file_path)

questions = [f"Q{i}" for i in range(1, 18)]
scales = ["SS", "S", "CS", "CTS", "TS", "STS"]

# ===================== SCORE MAPPING =====================
score_map = {"SS":6, "S":5, "CS":4, "CTS":3, "TS":2, "STS":1}

# ===================== FLATTEN DATA =====================
all_answers = df[questions].values.flatten()
answer_counts = pd.Series(all_answers).value_counts().reindex(scales, fill_value=0)
total_responses = answer_counts.sum()
answer_percent = (answer_counts / total_responses * 100).round(2)

# ===================== DASHBOARD =====================
st.title("📊 Dashboard Visualisasi Kuesioner")

# --------- BAR CHART DISTRIBUSI ---------
st.subheader("Distribusi Jawaban Keseluruhan (Bar Chart)")
fig_bar = px.bar(x=scales, y=answer_counts.values, text=answer_counts.values)
st.plotly_chart(fig_bar)

# --------- PIE CHART ---------
st.subheader("Proporsi Jawaban Keseluruhan (Pie Chart)")
fig_pie = px.pie(values=answer_counts.values, names=scales)
st.plotly_chart(fig_pie)

# --------- STACKED BAR PER PERTANYAAN ---------
st.subheader("Distribusi Jawaban per Pertanyaan (Stacked Bar)")
stack_data = []
for q in questions:
    counts = df[q].value_counts().reindex(scales, fill_value=0)
    temp = pd.DataFrame({"Pertanyaan": q, "Skala": scales, "Jumlah": counts.values})
    stack_data.append(temp)

stack_df = pd.concat(stack_data)
fig_stack = px.bar(stack_df, x="Pertanyaan", y="Jumlah", color="Skala", barmode="stack")
st.plotly_chart(fig_stack)

# --------- RATA-RATA SKOR PER PERTANYAAN ---------
st.subheader("Rata-rata Skor per Pertanyaan")
score_df = df[questions].replace(score_map)
mean_scores = score_df.mean()

fig_mean = px.bar(x=questions, y=mean_scores.values, text=mean_scores.round(2))
st.plotly_chart(fig_mean)

# --------- KATEGORI POSITIF / NETRAL / NEGATIF ---------
st.subheader("Distribusi Kategori Jawaban")
category_map = {
    "positif": ["SS", "S"],
    "netral": ["CS"],
    "negatif": ["CTS", "TS", "STS"]
}

cat_counts = {
    "positif": answer_counts[["SS", "S"]].sum(),
    "netral": answer_counts[["CS"]].sum(),
    "negatif": answer_counts[["CTS", "TS", "STS"]].sum()
}

fig_cat = px.bar(x=list(cat_counts.keys()), y=list(cat_counts.values()))
st.plotly_chart(fig_cat)

# ===================== AUTO ANSWER SYSTEM =====================
def print_answer(q):
    if q == "q1":
        scale = answer_counts.idxmax()
        print(f"{scale}|{answer_counts.max()}|{answer_percent[scale]}")

    elif q == "q2":
        scale = answer_counts.idxmin()
        print(f"{scale}|{answer_counts.min()}|{answer_percent[scale]}")

    elif q in ["q3","q4","q5","q6","q7","q8"]:
        target_scale = {"q3":"SS","q4":"S","q5":"CS","q6":"CTS","q7":"TS","q8":"STS"}[q]
        best_q = None
        best_count = 0
        
        for question in questions:
            c = (df[question] == target_scale).sum()
            if c > best_count:
                best_count = c
                best_q = question
        
        percent = round(best_count / len(df) * 100, 2)
        print(f"{best_q}|{best_count}|{percent}")

    elif q == "q9":
        results = []
        for question in questions:
            c = (df[question] == "STS").sum()
            if c > 0:
                percent = round(c / len(df) * 100, 2)
                results.append(f"{question}:{percent}")
        print("|".join(results))

    elif q == "q10":
        total_score = score_df.values.mean()
        print(round(total_score, 2))

    elif q == "q11":
        best_q = mean_scores.idxmax()
        print(f"{best_q}:{round(mean_scores.max(),2)}")

    elif q == "q12":
        worst_q = mean_scores.idxmin()
        print(f"{worst_q}:{round(mean_scores.min(),2)}")

    elif q == "q13":
        total = sum(cat_counts.values())
        output = []
        for k,v in cat_counts.items():
            percent = round(v/total*100,2)
            output.append(f"{k}={v}:{percent}")
        print("|".join(output))


# ===================== RUN QUESTION ANSWER =====================
target_question = st.text_input("Masukkan kode pertanyaan (q1 - q13):")

if target_question:
    st.write("Output:")
    print_answer(target_question)
