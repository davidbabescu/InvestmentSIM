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
    rata_dobanzii = st.slider("Dobândă Anuală (%)", 1.0, 20.0, 7.0, 0.5)
    perioada_ani = st.slider("Durata (Ani)", 1, 40, 10)
    rata_inflatie = st.slider("Inflație (%)", 0.0, 10.0, 3.5, 0.1)
    rata_impozit = st.number_input("Impozit Profit (%)", value=10)

# 3. Calcule
df = calculeaza_dobanda_compusa(
    suma_initiala, contributie_lunara, rata_dobanzii, perioada_ani, rata_inflatie, rata_impozit
)

# Filtram datele pentru scenariul Realist
df_realist = df[df["Scenariu"] == "Realist"]
final = df_realist.iloc[-1] # Ultimul an

# 4. Afisare coloane principale
col1, col2, col3, col4 = st.columns(4)
col1.metric("TOTAL INVESTIT", f"{final['Total Investit']:,.0f} RON")
col2.metric("SOLD FINAL (NET)", f"{final['Sold Nominal'] - (final['Profit NET'] / (1-rata_impozit/100) * rata_impozit/100):,.0f} RON") # Sold dupa taxe aprox
col3.metric("PROFIT NET", f"{final['Profit NET']:,.0f} RON", delta="După taxe")
col4.metric("ROI FINAL", f"{final['ROI(%)']}%", help="Return on Investment (Randament Net)")

# 5. Grafice și Tabele
st.markdown("### 📊 Vizualizare Detaliată")
tab1, tab2, tab3 = st.tabs(["💰 Evoluție Sold", "📈 Evoluție ROI", "📋 Tabel Date"])

with tab1:
    st.subheader("Sold Nominal vs. Scenarii")
    st.line_chart(df, x="An", y="Sold Nominal", color="Scenariu")

with tab2:
    st.subheader("Evoluția ROI (%) în timp")
    st.markdown("Acest grafic arată cât de eficient devine capitalul tău pe măsură ce trec anii...")
    st.line_chart(df, x="An", y="ROI (%)", color="Scenariu")

with tab3:
    st.dataframe(df)

# Buton de download fisier CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descarcă Raport CSV", csv, "raport_investitii.csv", "text/csv")