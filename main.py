import pandas as pd
import sys
from calculations import calculeaza_dobanda_compusa


def deseneaza_grafic_ascii(df, scenariu):
    print(f"\n--- GRAFIC EVOLUTIE (Scenariu: {scenariu}) ---")
    print("Fiecare '*' reprezinta aprox. 5% din valoarea maxima.\n")

    df_filtrat = df[df["Scenariu"] == scenariu]

    if df_filtrat.empty:
        print(f"Eroare: Scenariul '{scenariu}' nu a fost gasit.")
        return

    maxim_sold = df_filtrat["Sold Nominal"].max()

    for index, row in df_filtrat.iterrows():
        an = int(row["An"])
        suma = row["Sold Nominal"]
        rata = row["Rata Anuala (%)"]

        # Desenam bara
        if maxim_sold > 0:
            lungime_bara = int((suma / maxim_sold) * 50)
        else:
            lungime_bara = 0
        bara = "*" * lungime_bara

        # Afisam si rata din anul respectiv (ca sa vedem volatilitatea)
        print(f"An {an:2d} | {bara} ({suma:,.0f} RON) [Randament: {rata:>5.1f}%]")


def main():
    print("==============================================")
    print("   SIMULATOR INVESTITII - INTERFATA CONSOLA   ")
    print("==============================================\n")

    try:
        # Input-uri
        suma_init = float(input("1. Introdu suma initiala (RON): "))
        contributie = float(input("2. Contributie lunara (RON): "))
        dobanda = float(input("3. Rata dobanzii anuale (Media, %): "))
        ani = int(input("4. Perioada investitiei (Ani): "))
        inflatie = float(input("5. Rata inflatiei estimata (%): "))

        print("\n[INFO] Se genereaza scenariile (inclusiv cel VOLATIL)...")

        df_rezultate = calculeaza_dobanda_compusa(
            suma_init, contributie, dobanda, ani, inflatie
        )

        # Afisam rezultatele pentru scenariul VOLATIL (cel mai interesant)
        scenariu_target = "Volatil (Piata Reala)"

        print(f"\n--- REZULTATE PENTRU: {scenariu_target} ---")
        cols = ["An", "Sold Nominal", "Profit NET", "ROI (%)", "Rata Anuala (%)"]

        df_target = df_rezultate[df_rezultate["Scenariu"] == scenariu_target]
        print(df_target[cols].head())
        print("...")
        print(df_target[cols].tail())

        # Grafic text
        deseneaza_grafic_ascii(df_rezultate, scenariu=scenariu_target)

        # Export
        df_rezultate.to_csv("rezultate_investitie.csv", index=False)
        print(f"\n[SUCCES] Fisier CSV generat.")

    except ValueError:
        print("\n[EROARE] Introdu doar numere!")
    except Exception as e:
        print(f"\n[EROARE] {e}")


if __name__ == "__main__":
    main()