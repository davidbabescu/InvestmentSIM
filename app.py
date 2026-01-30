import streamlit as st
import pandas as pd
from calculations import calculeaza_dobanda_compusa

# 1. Configurare Pagina
st.set_page_config(page_title="Simulator Investiții", page_icon="📈", layout="wide")

st.title("💰 Simulator de investiții")
st.markdown("Cu un plan întreg... dobândă, perioadă, inflație!!!")

# 2. Sidebar
with st.sidebar:
    st.header("⚙️ Configurare")
    suma_initiala = st.number_input("Suma Inițială (RON)", value=5000, step=100)
    contributie_lunara = st.number_input("Contribuție Lunară (RON)", value=500, step=50)
    st.markdown("---")
    rata_dobanzii = st.slider("Dobândă Medie Anuală (%)", 1.0, 20.0, 7.0, 0.5, help="Media pieței. În scenariul Volatil, aceasta va varia anual...")
    perioada_ani = st.slider("Durata (Ani)", 1, 40, 10)
    rata_inflatie = st.slider("Inflație (%)", 0.0, 10.0, 3.5, 0.1)
    rata_impozit = st.number_input("Impozit Profit (%)", value=10)

    if st.button("🪙Mai bagă o fisă!🔄"):
        st.cache_data.clear()  # Fortam recalcularea numerelor random

# 3. Calcule
df = calculeaza_dobanda_compusa(
    suma_initiala, contributie_lunara, rata_dobanzii, perioada_ani, rata_inflatie, rata_impozit
)

#Scenariul volatil este cel de baza pentru afisare
nume_scenariu_baza = "Volatil (Realist)"
df_baza = df[df["Scenariu"] == nume_scenariu_baza]
final = df_baza.iloc[-1] #Ultimul an

# 4. Afisare coloane principale
st.subheader(f"Rezultate Estimate: {nume_scenariu_baza}")
col1, col2, col3, col4 = st.columns(4)
col1.metric("TOTAL INVESTIT", f"{final['Total Investit']:,.0f} RON")
col2.metric("SOLD FINAL (Mediu)", f"{final['Sold Nominal']:,.0f} RON")
col3.metric("PROFIT NET", f"{final['Profit NET']:,.0f} RON", delta="După taxe")
col4.metric("ROI FINAL", f"{final['ROI (%)']}%", help=f"Randamentul în scenariul {nume_scenariu_baza}")

# 5. Grafice și Tabele
st.markdown("### 📊 Vizualizare Detaliată")
tab1, tab2, tab3 = st.tabs(["💰 Evoluție Sold (Toate Scenariile)", "📉 Volatilitate Anuală", "📋 Tabel Date"])

with tab1:
    st.subheader("")
    st.line_chart(df, x="An", y="Sold Nominal", color="Scenariu")

with tab2:
    st.subheader("🥁Drum roll... Ce dobândă ai prins în fiecare an?💲")
    st.markdown("În scenariul volatil, unii ani sunt negativi (din pacate pierdere), alții pozitivi! :)")
    # Afisam doar pentru scenariul Volatil ca sa se vada variatia
    st.bar_chart(df_baza, x="An", y="Rata Anuala (%)")

with tab3:
    st.dataframe(df)

# Buton de download fisier CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descarcă Raport CSV", csv, "raport_investitii.csv", "text/csv")