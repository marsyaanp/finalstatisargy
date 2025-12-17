import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Survey Data Analysis WebApp",
    layout="wide"
)

# ---------------- LANGUAGE ----------------
language = st.sidebar.selectbox(
    "Language / Bahasa",
    ["English", "Indonesia"]
)

# ---------------- TEXT ----------------
if language == "English":
    title = "Survey Data Analysis Web Application"
    upload_text = "Upload Survey Data (CSV)"
    desc_title = "Descriptive Analysis"
    assoc_title = "Association Analysis (X vs Y)"
    select_x = "Select Variable X"
    select_y = "Select Variable Y"
    freq_table = "Frequency Table"
    percentage = "Percentage (%)"
else:
    title = "Aplikasi Analisis Data Survei"
    upload_text = "Unggah Data Survei (CSV)"
    desc_title = "Analisis Deskriptif"
    assoc_title = "Analisis Asosiasi (X vs Y)"
    select_x = "Pilih Variabel X"
    select_y = "Pilih Variabel Y"
    freq_table = "Tabel Frekuensi"
    percentage = "Persentase (%)"

# ---------------- TITLE ----------------
st.title(title)

# ---------------- UPLOAD DATA ----------------
uploaded_file = st.file_uploader(upload_text, type=["csv"])

if uploaded_file is not None:
    # 🔴 TAMBAHAN PENTING DI SINI
    df = pd.read_csv(uploaded_file, sep=';')

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # ================= DESCRIPTIVE ANALYSIS =================
    st.header(desc_title)

    col_desc = st.selectbox("Select Column", df.columns)

    freq = df[col_desc].value_counts().reset_index()
    freq.columns = [col_desc, freq_table]
    freq[percentage] = round((freq[freq_table] / freq[freq_table].sum()) * 100, 2)

    st.dataframe(freq)

    # Plot
    fig, ax = plt.subplots()
    ax.bar(freq[col_desc].astype(str), freq[freq_table])
    ax.set_xlabel(col_desc)
    ax.set_ylabel(freq_table)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ================= ASSOCIATION ANALYSIS =================
    st.header(assoc_title)

    # 🔴 TAMBAHAN: FILTER KOLOM X & Y OTOMATIS
    x_columns = [c for c in df.columns if c.startswith("X")]
    y_columns = [c for c in df.columns if c.startswith("Y")]

    col1, col2 = st.columns(2)
    with col1:
        x_var = st.selectbox(select_x, x_columns)
    with col2:
        y_var = st.selectbox(select_y, y_columns)

    if x_var and y_var:
        # Crosstab
        crosstab = pd.crosstab(df[x_var], df[y_var])

        st.subheader("Crosstab (X vs Y)")
        st.dataframe(crosstab)

        # Percentage Crosstab
        crosstab_pct = crosstab.div(crosstab.sum(axis=1), axis=0) * 100
        st.subheader("Crosstab Percentage (%)")
        st.dataframe(round(crosstab_pct, 2))

        # Plot Association
        fig2, ax2 = plt.subplots()
        crosstab.plot(kind="bar", ax=ax2)
        ax2.set_xlabel(x_var)
        ax2.set_ylabel("Count")
        ax2.set_title(f"{x_var} vs {y_var}")
        plt.xticks(rotation=45)
        st.pyplot(fig2)
