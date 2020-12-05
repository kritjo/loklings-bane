"""

"""
import pandas as pd
from kunde import Kunde
from provisjonsobjekt import Provisjonsobjekt
import re

class OP:
    def __init__(self, filinfo):
        self._filinfo = filinfo

    def readCsv(self, filinfo):
        filbane = filinfo["filbane"]
        seperator = filinfo["seperator"]
        pd_df_csv = pd.read_csv(filbane, sep=seperator)
        return pd_df_csv

    def readHTML(self, filinfo):
        filbane = filinfo["filbane"]
        pd_df_html = pd.read_html(filbane, decimal=",", thousands=".")
        return pd_df_html

    def readExcel(self, filinfo):
        filbane = filinfo["filbane"]
        arknavn = filinfo["arknavn"]
        pd_df_excel = pd.read_excel(filbane)
        return pd_df_excel

    def lesFil(self):
        filinfo = self._filinfo
        filtype = filinfo["filtype"]
        if filtype == "csv":
            df = self.readCsv(filinfo)
            return df
        elif filtype == "html":
            df = self.readHTML(filinfo)
            return df
        elif filtype == "excel":
            df = self.readExcel(filinfo)
            return df
        else:
            raise Exception(f"FATAL! {filtype} er ikke støttet! Velg html/excel/csv.")

class DF:
    def __init__(self, df, filinfo):
        self._df = df
        self._filinfo = filinfo
        self._kunder = []

    def kunder(self):
        if self._filinfo["filtype"] == "excel":
            gsmCol = self._filinfo["cid_gsm"]
            provCol = self._filinfo["cid_prov"]
            årsakCol = self._filinfo["cid_årsak"]
            bilagCol = self._filinfo["cid_bilag"]
            mvatopp = self._filinfo["mvatopp"]
            for index, row in self._df.iterrows():
                try:
                    gsm = int(row[gsmCol])
                    if mvatopp:
                        prov = int(row[provCol])*1.25
                    else:
                        prov = int(row[provCol])
                    årsak = str(row[årsakCol])
                    bilag = row[bilagCol]
                    nyKunde = Kunde(gsm)
                    nyprovobj = Provisjonsobjekt(gsm, prov, årsak, idno=bilag)
                    nyKunde.leggTilNyData("faktisk", nyprovobj)
                    self._kunder.append(nyKunde)
                except ValueError:
                    print(f"Kunne ikke legge til kundekonto for: {row}")
        elif self._filinfo["filtype"] == "html":
            tabell = self._filinfo["id_tabell"]
            gsmCol = self._filinfo["cid_gsm"]
            provCol = self._filinfo["cid_prov"]
            årsakCol = self._filinfo["cid_årsak"]
            bilagCol = self._filinfo["cid_bilag"]
            mvatopp = self._filinfo["mvatopp"]
            navn = self._filinfo["cid_navn"]
            for index, row in self._df[tabell].iterrows():
                try:
                    gsm = int(row[gsmCol])
                    if int(row[gsmCol]) == 90364001:
                        print()
                    if mvatopp:
                        prov = int(row[provCol]) * 1.25
                    else:
                        prov = int(row[provCol])
                    årsak = str(row[årsakCol])
                    bilag = row[bilagCol]
                    nyKunde = Kunde(gsm)
                    nyprovobj = Provisjonsobjekt(gsm, prov, årsak, idno=bilag)
                    nyKunde.leggTilNyData("faktisk", nyprovobj)
                    self._kunder.append(nyKunde)
                except ValueError:
                    ok = False
                    for i in self._df[tabell].index:
                        try:
                            if re.search(f"{row[navn]}$", self._df[tabell].at[i, navn], re.IGNORECASE) and i != index and not ok:
                                gsm = int(self._df[tabell].at[i, gsmCol])
                                if mvatopp:
                                    prov = int(row[provCol]) * 1.25
                                else:
                                    prov = int(row[provCol]) * 1.25
                                årsak = str(row[årsakCol])
                                bilag = str(row[bilagCol])
                                ok = True
                        except ValueError:
                            pass
                    if ok:
                        nyKunde = Kunde(gsm)
                        nyprovobj = Provisjonsobjekt(gsm, prov, årsak, idno=bilag)
                        nyKunde.leggTilNyData("faktisk", nyprovobj)
                        self._kunder.append(nyKunde)
                    else:
                        try:
                            if row[navn] != row[gsmCol]:
                                nyKunde = Kunde(33333333)
                                if mvatopp:
                                    prov = int(row[provCol]) * 1.25
                                else:
                                    prov = int(row[provCol])
                                nyprovobj = Provisjonsobjekt(33333333, prov, row[årsakCol])
                                nyKunde.leggTilNyData("faktisk", nyprovobj)
                                self._kunder.append(nyKunde)
                            else:
                                raise ValueError
                        except ValueError:
                            print(f"Kunne ikke legge til kundekonto {row}")

        return self._kunder
