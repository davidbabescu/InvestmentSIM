import pandas as pd

def calculeaza_dobanda_compusa(suma_initiala, contributie_lunara, rata_dobanzii, ani, rata_inflatie, rata impozit=10):
    """
    Calculeaza evolutia investitiei luand in calcul inflatia si scenarii diferite
    CELE 3 SCENARII:
    1.Realist: Rata dobanzii introdusa de utilizator
    2. Optimist: Rata dobanzii + 3%
    3. Pesimist: Rata dobaznii - 3%
    Args:
    suma_initiala (float): Banii de start.
        contributie_lunara (float): Banii adaugati lunar.
        rata_dobanzii (float): Rata anuala estimata (in procente, ex: 7).
        ani (int): Durata investitiei.
        rata_inflatie (float): Inflatia anuala (ex: 3.5).
        rata_impozit (float): Impozitul pe profit (standard 10%).

    Return:
        DataFrame cu date necesare pt grafic.
    """

    scenarii = {
        "Realist": 0,
        "Optimist": 3.0, #+3%
        "Pesimist": -3.0 #-3%
    }

    #lista unde colectam randurile tabelului
    date_colectate = []
    #luam fiecare scenariu (realist -> optimist -> pesimist)
    for nume_scenariu, marja in scenarii.items():
        # Calculam rata specifica scenariului
        # Daca rata e 7% si marja e -3% (Pesimist), rata finala e 4%
        rata_calculata_procent = rata_dobanzii + marja

        if rata_calculata_procent < 0:
            rata_calculata_procent = 0

        rata_dec = rata_calculata_procent / 100
        inflatie_dec = rata_inflatie / 100

        #variabile pentru bucla:
        sold_curent = suma_initiala
        total_investit = suma_initiala

        #Adaugam anul 0(start)
        date_colectate.append({
            "An" : 0,
            "Scenariu" : nume_scenariu,
            "Total investit" : round(total_investit, 2),
            "Sold nominal": round(sold_curent, 2),
            "Sold real (ajustat pentru inflatie)": round(sold_curent, 2),
            "Profit NET": 0
        })

    #Simularea trecerii anilor:
    for an in range(ani, ani + 1):
        #1. Adaugam contributiile din an
        contributie_anuala = contributie_lunara * 12
        sold_curent += contributie_anuala
        total_investit += contributie_anuala
        #2. Aplicam dobanda compusa la suma acumulata
        dobanda_generata += sold_curent * rata_dec
        sold_curent += dobanda_generata