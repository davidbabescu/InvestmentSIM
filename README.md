# Simulator de investitii
- In liceu am facut multa economie datorita profilului... :D
- "Aplicatie web" construita in **Pyhton** cu **Streamlit** care simuleaza evolutia investitiilor pe termen lung, luand in calcul inflatia, taxele si volatilitatea pietei
# Functionalitati: 
- **Scenarii multiple:** Realist, Optimist, Pesimist si Volatil (realist, random)
- **Ajustarea inflatiei** si includerea taxelor
- **Vizualuzare grafica pe tabele:** pentru evolutia soldului
- **Export date:** posibilitatea de a descarca un raport CSV
- **Meniu de configurare interactiv:** personalizabil
- 
# Rularea proiectului: 
- **Local:**
1. Clone repository:
2. Install dependencies cu : pip install -r requirements.txt
3. In terminal: streamlit run app.py

- **Docker**
1. docker build -t investment-sim 
2. docker run -p 8501:8501 investment-sim .
3. In browser la adresa: http://localhost:8501
