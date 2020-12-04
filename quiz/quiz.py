import random
import os
import json
import math
import time

# pdoc --html quiz.py


def main():
    """Henter fil og starter menyen

    Returns
    -------
    function
        meny(data)
    """

    data = hent_fra_fil()
    return meny(data)


def quiz(data):
    """Logikken til quizen

    Parameters
    ----------
    data : list
        En list med dictionarys

    Returns
    -------
    function
        skriv_ut_raport(data)
    """
    nr = 0
    oppgaver = [x for x in range(len(data))]
    while len(oppgaver) > 0:
        i = random.randrange(0, len(oppgaver))
        nr += 1

        skriv_ut_sporsmal_quiz(oppgaver[i], data, nr)
        data[oppgaver[i]]["svart"].append(quiz_svar() - 1)

        del oppgaver[i]

    skriv_ut_rapport(data)


def meny(data):
    """Skriver ut meny og håndterer brukervalg.

    Parameters
    ----------
    data : list
        En list med dictionarys

    Returns
    -------
    function
        Avhenger av brukerens valg

    Raises
    ------
    ValueError
        Input-et må være et heltall mellom 1 og 3
    """

    rydd_terminal()
    skriv_ut_linjer()
    print("")
    print("            ░██████╗░██╗░░░██╗██╗███████╗\n            ██╔═══██╗██║░░░██║██║╚════██║\n            ██║██╗██║██║░░░██║██║░░███╔═╝\n            ╚██████╔╝██║░░░██║██║██╔══╝░░\n            ░╚═██╔═╝░╚██████╔╝██║███████╗\n            ░░░╚═╝░░░░╚═════╝░╚═╝╚══════╝\n")

    print(f"  1. Start")
    print(f"  2. Statistikk")
    print(f"  3. Avslutt")
    print(f"  4. Slett historikk\n")

    skriv_ut_linjer()

    try:
        svar = int(input("\nSvar: "))
        if not 1 <= svar <= 4:
            raise ValueError()
        elif math.floor(svar) != svar:
            raise ValueError()
        elif svar == 1:
            return quiz(data)
        elif svar == 2:
            return skriv_ut_statistikk(data)
        elif svar == 3:
            return avslutt()
        elif svar == 4:
            return slett_data(data)

    except ValueError:
        rydd_terminal()
        skriv_ut_linjer()
        print("")
        print("Skrive inn et tall fra 1 til og med 3.\n")
        skriv_ut_linjer()
        time.sleep(1.5)
        return meny(data)


def skriv_ut_linjer():
    """Skriver ut to linjer"""
    print("_"*55)
    print("-"*55)


def avslutt():
    """Tømmer terminalen og avslutter programmet"""

    rydd_terminal()
    exit()


def quiz_svar():
    """Henter svar fra brukeren om hvilket alternativ som er valgt.

    Parameters
    ----------
    data : list
        En list med dictionarys

    Returns
    -------
    int
        Brukerens svar på flervalgsoppgaven

    Raises
    ------
    ValueError
        Input-et må være et heltall mellom 1 og 3
    """

    try:
        svar = int(input("\nSvar: "))
        if not 1 <= svar <= 3:
            raise ValueError()
        if math.floor(svar) != svar:
            raise ValueError()

        else:
            return svar

    except ValueError:
        print("*** Du små skrive inn et tall fra 1 til og med 3. ***\n")
        return quiz_svar()


def gaa_til_meny(data):
    """Henter svar fra brukeren om quizen skal avsluttes eller gjentas

    Parameters
    ----------
    data : list
        En list med dictionarys

    Returns
    -------
    function
        meny(data)

    Raises
    ------
    ValueError
        Input-et må være en tom streng

    """

    print("*** Trykke enter for å gå til meny. ***\n")

    try:
        svar = input("")

        if svar == "":
            return meny(data)

        else:
            raise ValueError()

    except ValueError:
        return gaa_til_meny(data)


def skriv_ut_sporsmal_quiz(i, data, nr):
    """Skriver ut spørsmålet og tilhørende svaralternativer.

    Parameters
    ----------
    i : int
        Indeksen til dictionaryen i data-lista vi skal skrive ut

    data : list
        En list med dictionarys

    n : int
        Nummer på spørsmålet
    """
    rydd_terminal()
    skriv_ut_linjer()
    print("")
    print(f'Spørsmål {nr} av {len(data)}:\n  {data[i]["sporsmal"]} \n')
    print("Alternativer : \n ")
    for j, alternativ in enumerate(data[i]["alternativer"]):
        print(f'  {j+1}  {alternativ}')

    print("")
    skriv_ut_linjer()


def antall_rette(data, i):
    """Sammenligner avgitt svar med riktig svar og returnerer den summerte verdien.

    Parameters
    ----------
    data : list
        En list med dictionarys

    i : int
        indeksen til frorsøket som det skal returneres antall rette til

    Returns
    -------
    int
        Antall rette svar
    """
    rette = 0
    for q in data:
        if q["rett"] == q["svart"][i]:
            rette += 1

    return rette


def oppgaver_med_feil(data):
    """Sammenligner avgitt svar med riktig svar returnerer liste med indeksene til svarene som er feil.

    Parameters
    ----------
    data : list
        En list med dictionarys

    Returns
    -------
    list
        En list med indeksene til de spørsmålene som er besvart feil.
    """
    feil = []
    for i, q in enumerate(data):
        if q["rett"] != q["svart"][-1]:
            feil.append(i)

    return feil


def skriv_ut_feil(data):
    """Skriver ut hvilke spørsmål og besvart alternativ som ble feil.

    Parameters
    ----------
    data : list
        En list med dictionarys
    """
    for i in oppgaver_med_feil(data):
        print(f'Spørsmål:   {data[i]["sporsmal"]}')
        print(
            f'Ditt svar:  {data[i]["alternativer"][data[i]["svart"][-1]]}\n')


def skriv_til_fil(data):
    """Skriver listen med dictionarys til fil.

    Parameters
    ----------
    data : list
        En list med dictionarys
    """
    with open('data.json', 'w') as fout:
        json.dump(data, fout)


def hent_fra_fil():
    """Henter json-fil

    Returns
    -------
    list
        En list med dictionarys
    """
    with open(r"data.json", "r") as read_file:
        return json.load(read_file)


def skriv_ut_rapport(data):
    """Skriver ut resultat of evt. feilene som er gjort.

    Parameters
    ----------
    data : list
        En list med dictionarys
    """

    rydd_terminal()
    skriv_ut_linjer()
    print("")
    if antall_rette(data, -1) == len(data):
        print(f'Gratulerer, du fikk alt rett!\n ')

    else:
        print(f'Du svarte feil på \n')
        skriv_ut_feil(data)

    skriv_ut_linjer()
    skriv_til_fil(data)
    gaa_til_meny(data)


def skriv_ut_statistikk(data):
    """Skriver ut tabell med resultaten til alle forsøkene

    Parameters
    ----------
    data : list
        En list med dictionarys

    Returns
    -------
    function
        gaa_til_meny(data)
    """
    rydd_terminal()
    skriv_ut_linjer()
    print("")
    antall = antall_forsoek(data)

    print(f"Du har prøvd quizen {antall} gang(er)\n")

    if antall > 0:
        print(f"{'nr':^5}    {'riktige':^7}   {'feil':^7}  {'spørsmål':^7}")
        print(f"-"*40)
        for n in range(antall):
            rette = antall_rette(data, n)
            print(
                f" {(n + 1):^5}   {rette:^7}  {(len(data) - rette):^7}   {len(data):^7} ")

    skriv_ut_linjer()

    return gaa_til_meny(data)


def antall_forsoek(data):
    """Finner antall forsøk som er gjennomført ved å 
    se på lengden til den første svart-lista i data

    Returns
    -------
    function
        meny(data)
    """
    return len(data[0]["svart"])


def slett_data(data):
    """Sletter listene med tidligere svar

    Parameters
    ----------
    data : list
        En list med dictionarys

    Returns
    -------
    function
        meny(data)
    """
    for d in data:
        d['svart'].clear()

    rydd_terminal()
    skriv_ut_linjer()
    print("")
    print("Historikken din er slettet.\n")
    skriv_ut_linjer()

    time.sleep(1.5)
    return meny(data)


def rydd_terminal():
    """Dytter innholde i terminalen opp slik at det
    oppleves som terminalen tømmes.
     """

    # windows
    if os.name == 'nt':
        return os.system('cls')

   # andre operativsystem
    else:
        return os.system('clear')


if __name__ == '__main__':
    main()
