FROM python:3.9-slim

# Setam folderul de lucru in container
WORKDIR /app

# Copiem fisierul de cerinte si instalam librariile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiem tot codul aplicatiei in container
COPY . .

#Ruleaza pe portul 8501
EXPOSE 8501

# Comanda de start
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]