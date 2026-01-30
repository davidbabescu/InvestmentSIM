import pandas as pd
import numpy as np

def calculeaza_dobanda_compusa(suma_initiala, contributie_lunara, rata_dobanzii, ani, rata_inflatie, rata_impozit=10):

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
        "Pesimist": -3.0, #-3%
        "Volatil (Realist)": "RANDOM"
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
            "Sold Nominal": round(sold_curent, 2),
            "Sold real (ajustat pentru inflatie)": round(sold_curent, 2),
            "Profit NET": 0,
            "ROI (%)": 0.0,
            "Rata Anuala (%)": 0.0 #Vedem cat a fost dobanda in anul respectiv
        })

    #Simularea anilor ce trec pe langa noi:
        for an in range(1, ani + 1):
            #1. Adaugam contributiile din an
            contributie_anuala = contributie_lunara * 12
            sold_curent += contributie_anuala
            total_investit += contributie_anuala

            #LOGICA RATA VARIABILA
            if marja == "RANDOM":
                #Generam o rata aleatorie
                #Media = rata_dobanzii, Deviatia standard = 15% (Volatilitate mare)
                rata_anuala_simulata = np.random.normal(rata_dobanzii, 15)
                #Punem limita sa nu se piarda toti banii (Ex max: -40%)
                if rata_anuala_simulata < -40: rata_anuala_simulata = -40

                rata_calculata_procent = rata_anuala_simulata
            else:
                #Scenarii fixe
                rata_calculata_procent = rata_dobanzii + marja
                if rata_calculata_procent < 0: rata_calculata_procent = 0

            #2. Aplicam dobanda compusa la suma acumulata
            dobanda_generata = sold_curent * rata_dec
            sold_curent += dobanda_generata

            #3. Scadem inflatia
            #Formula : Valoare / (1 + inflatie)^numar_ani
            factor_actualizare = (1 + inflatie_dec) ** an
            sold_real = sold_curent / factor_actualizare

            #4. Calcul taxe
            profit_brut = sold_curent - total_investit
            impozit = (profit_brut * rata_impozit / 100) if profit_brut > 0 else 0
            profit_net = profit_brut - impozit

            #ROI
            if total_investit > 0:
                roi_procent = (profit_net / total_investit) * 100
            else:
                roi_procent = 0

            #Salvam datele anului curent
            date_colectate.append ({
                "An" : an,
                "Scenariu" : nume_scenariu,
                "Total Investit" : round(total_investit, 2),
                "Sold Nominal": round(sold_curent, 2),
                "Sold Real (Ajustat inflatiei)" : round(sold_real, 2),
                "Profit NET": round(profit_net, 2), #Primeste si statul 10%... !! Sa fim cinstiti daca tot.. :D
                "ROI (%)": round(roi_procent, 2),
                "Rata Anuala (%)": round(rata_calculata_procent, 1)
            })

    df = pd.DataFrame(date_colectate)
    return df