from kontrollinstans import Kontrollinstans
from easygui import *
import pandas as pd
import logging
import os
from gui import Gui

"""
Komma 400,0 = 4000
Id-tyveriforsikring har ikke gsmnr
"""

production = False

def main():



    gui = Gui()
    gui.start()



    tittel = ""
    start = True
    while start:
        ki = Kontrollinstans()

        # Hvilken operatør skal kontrolleres?
        op = None
        while op is None:
            op = choicebox("Hvilken opperatør vil du sjekke?", tittel, ["telenor", "telia", "ice"])

        # Lag Elguide-Kunder
        msgbox("Velg Elguidefil", tittel)
        elguideFil = None
        while elguideFil is None:
            elguideFil = fileopenbox("Velg Elguidefil", tittel, "*.csv", ["*.csv"])
        egInfo = None
        while egInfo is None:
            with open(elguideFil, "r") as fil:
                linje = fil.readline().strip().split(";")
                kol_str = ""
                for i in range(len(linje)):
                    kol_str += f"{i}: {linje[i]}, "
                egInfo = multenterbox(
                    f"{kol_str}\nSkriv inn kolonnenummer til følgende verdier. OBS: Kolonne A = Kolonne 0", tittel,
                    ["GSM", "Beløp", "Varekode", "Merke",
                     "Bilagsnr"])
        merke = None
        while merke is None:
            merke = enterbox(f"Hvilket Elguide-merke er {op}?", tittel)
        for i in range(5):
            egInfo[i] = int(egInfo[i])
        egInfoDict = {"gsm": egInfo[0], "prov": egInfo[1], "varekode": egInfo[2], "merke_col": egInfo[3],
                      "merke_id": merke,
                      "bilag": egInfo[4]}
        ki.lagKundeKontoer("elguide", elguideFil, egInfoDict)

        # Lag OpertørKunder
        opLoop = True
        huskekol = False
        while opLoop:
            msgbox(f"Velg {op} fil", tittel)
            opFil = None
            while opFil is None:
                opFil = fileopenbox(f"Velg {op} fil", tittel)
            typeFil = None
            while typeFil is None:
                typeFil = choicebox(f"Hvilken type fil er {opFil}?", tittel, ["excel", "csv", "html"])
            if typeFil == "excel":
                arknavn = None
                while arknavn is None:
                    arknavn = enterbox("Skriv inn navn på arket hvor provisjonstabell ligger", tittel)
                opInfoDict = {"filbane": opFil, "arknavn": arknavn, "filtype": typeFil}
                dfOp = ki.lagDFFraOP(opInfoDict)
                colTest = None
                while colTest is None:
                    colTest = int(enterbox(f"""Slik ser df ut:\n{dfOp}\nHvilken rad inneholder kolonnetitler?(skriv -1 
dersom nåværende er riktig).""", tittel))
                if colTest == -1:
                    dropRows = False
                else:
                    dropRows = True
                    drops = 0
                    dropn = colTest - 1
                    headers = colTest

                if dropRows:
                    try:
                        dfOp = dfOp.rename(columns=dfOp.iloc[headers])
                        dfOp = dfOp.drop(dfOp.index[headers])
                    except KeyError:
                        pass
                    rowstodrop = [row for row in range(drops, dropn + 1)]
                    dfOp = dfOp.drop(index=rowstodrop)

                kolonnenavn = dfOp.columns.tolist()
                for i in range(len(kolonnenavn)):
                    kolonnenavn[i] = str(kolonnenavn[i]) + str(i)

                dfOp.columns = kolonnenavn

                if not huskekol:
                    kolinfo = None

                while kolinfo is None:
                    kolinfo = multenterbox(f"""{list(dfOp)}\nSkriv inn kolonnenavn til følgende verdier.
OBS: Pass på mellomrom""", tittel, ["GSM", "Beløp", "Årsak (deskriptiv beskrivelse av grunnlag for provisjon)",
                                    "Bilag"])

                endreGSM = ynbox("Inneholder GSM-nummer 47 forran?", tittel)
                if endreGSM:
                    def rm47(x):
                        return int(str(x)[2:])

                    dfOp[kolinfo[0]] = dfOp[kolinfo[0]].apply(rm47)

                kolDict = {"filtype": typeFil, "cid_gsm": kolinfo[0], "cid_prov": kolinfo[1],
                           "cid_årsak": kolinfo[2], "cid_bilag": kolinfo[3]}
                if ynbox("MVA på topp av tabell?", tittel):
                    kolDict["mvatopp"] = True
                else:
                    kolDict["mvatopp"] = False
                ki.lagKundeKontoer(op, dfOp, kolDict)
            elif typeFil == "html":
                dfOp = ki.lagDFFraOP({"filbane": opFil, "filtype": "html"})
                aboTabell = None
                i = 0
                while aboTabell is None:
                    aboTabellBool = ynbox(f"Er dette tabellen for provisjon?\n{dfOp[i]}", tittel)
                    if aboTabellBool:
                        aboTabell = i
                    i += 1
                    if i >= len(dfOp):
                        msgbox("Prøv på ny.", tittel)
                        i = 0

                if not huskekol:
                    kolinfo = None

                while kolinfo is None:
                    kolinfo = multenterbox(f"{list(dfOp[aboTabell])}\nSkriv inn kolonnenavn:", tittel,
                                           ["GSM", "Beløp", "Årsak (deskriptiv beskrivelse av grunnlag for provisjon)",
                                            "Bilag", "Kundenavn"])
                kolDict = {"filtype": "html", "id_tabell": aboTabell, "cid_gsm": kolinfo[0],
                           "cid_prov": kolinfo[1], "cid_årsak": kolinfo[2], "cid_bilag": kolinfo[3], "cid_navn":kolinfo[4]}
                if ynbox("MVA på topp av tabell?", tittel):
                    kolDict["mvatopp"] = True
                else:
                    kolDict["mvatopp"] = False
                ki.lagKundeKontoer(op, dfOp, kolDict)
            elif typeFil == "csv":
                msgbox("CSV opperatørfiler er ikke støttet!\nFor å foreslå endringer, kontakt kritjo@uio.no.")

            nyOpFil = ynbox("Vil du legge til flere opperatørfiler?", tittel)
            if not nyOpFil:
                opLoop = False
            else:
                huskekol = ynbox("Vil du huske valg for kolonnenavn?", tittel)

        # Gjør kontroll
        kontrolliste = ki.gjørKontroll()
        lagrenavn = filesavebox("Lagre Differanser", tittel, "avviksliste.xlsx", ["*.xlsx"])
        with open("_temp.csv", "w") as dfil:
            dfil.writelines(["GSM;PROV;ÅRSAK;BILAG;TYPE\n"])
            for kunde in kontrolliste:
                for provobj in kunde._forventetprov:
                    dfil.writelines([f"{provobj._gsm};{provobj._prov};{provobj._årsak};{provobj._id};Forventet\n"])
                for provobj in kunde._faktiskprov:
                    dfil.writelines([f"{provobj._gsm};{provobj._prov};{provobj._årsak};{provobj._id};Faktisk\n"])
        df = pd.read_csv("_temp.csv", sep=";", encoding='latin-1')
        df.to_excel(lagrenavn)
        start = ynbox("Vil du kjøre en ny kontroll?", tittel)


dir_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.DEBUG, filename=f'{dir_path}/loklingsbane.log')

if production:
    try:
        main()
    except Exception as ex:
        msgbox(ex)
        logging.exception("Exception:")
else:
    main()
