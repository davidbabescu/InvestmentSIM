import pandas as pd
import sys

from calculations import calculeaza_dobanda_compusa

def deseneaza_grafic_ascii(df, scenariu="Realist"):
    """
    Deseneaza un grafic simplu folosind caractere text (*)
    Afisieaza doar scenariul specificat
    """
    print(f"\n--- GRAFIC EVOLUTIE (Scenariu: {scenariu}) ---")
    print("Fiecare '*' reprezinta aprox. 5% din valoarea maxima.\n")

    df_filtrat = df [df["Scenariu"] == scenariu]

    if df_filtrat.empty:
        print("Eroare: scenariul nu a fost gasit")
        return

    # Aflam valoarea maxima pentru a scala graficul (sa incapa pe ecran)
    maxim_sold = df_filtrat["Sold Nominal"].max()

    for index, row in df_filtrat.iterrows():
        an = int(row["An"])
        suma = row["Sold Nominal"]

        # Matematica pentru desenare:
        # Daca suma e maxima, afisam 50 de stelute.
        # Daca e jumatate, 25 de stelute.
        lungime_bara = int((suma / maxim_sold) * 50)
        bara = "*" * lungime_bara

        # Afisam: Anul | Stelute | Suma in cifre
        print(f"An {an:2d} | {bara} ({suma:,.0f} RON)")

def main():
    print("==============================================")
    print("   SIMULATOR INVESTITII - INTERFATA CONSOLA   ")
    print("==============================================\n")

    try:
        # 1. Colectarea datelor de la tastatura
        suma_init = float(input("1. Introdu suma initiala (RON): "))
        contributie = float(input("2. Contributie lunara (RON): "))
        dobanda = float(input("3. Rata dobanzii anuale (%): "))
        ani = int(input("4. Perioada investitiei (Ani): "))
        inflatie = float(input("5. Rata inflatiei estimata (%): "))

        print("\n[INFO] Se efectueaza calculele...")

        # 2. Apelam functia din calculations.py
        df_rezultate = calculeaza_dobanda_compusa(
            suma_init,
            contributie,
            dobanda,
            ani,
            inflatie
        )
        # 3. Afisare Tabel Scurt (primele si ultimele randuri)
        print("\n--- REZULTATE SUMARE (Tabel) ---")
        # Afisam doar coloanele importante
        cols = ["An", "Scenariu", "Sold Nominal", "Profit NET"]
        print(df_rezultate[cols].head(3))  # Primii 3 ani
        print("...")
        print(df_rezultate[cols].tail(3))  # Ultimii 3 ani

        # 4. Afisare Grafic Text (Doar pentru scenariul Realist)
        deseneaza_grafic_ascii(df_rezultate, scenariu="Realist")

        # 5. Export CSV (Cerinta obligatorie)
        nume_fisier = "rezultate_investitie.csv"
        df_rezultate.to_csv(nume_fisier, index=False)
        print(f"\n[SUCCES] Datele au fost salvate in fisierul '{nume_fisier}'.")
        print("Poti deschide acest fisier in Excel.")

    except ValueError:
        print("\n[EROARE] Te rog sa introduci doar numere valide (foloseste punctul '.' pentru zecimale).")
    except Exception as e:
        print(f"\n[EROARE] Ceva nu a mers bine: {e}")


if __name__ == "__main__":
    main()
