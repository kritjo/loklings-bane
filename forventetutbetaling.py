"""

"""
from provisjonsobjekt import Provisjonsobjekt
from kunde import Kunde
import pandas as pd
from easygui import *

__author__ = "Kristian Tjelta Johansen"
__copyright__ = "Copyright 2020, kritjo@uio"
__license__ = "CC-BY-SA 4.0 Int"
__version__ = "1.0"
__status__ = "Alpha"


class Forventetutbetaling:
    def __init__(self, indata, filinfo):
        self._kunder = []
        self.lesFil(indata, filinfo)

    # filinfo skal inneholde dict med gsm, prov og årsak som nøkkel.
    # nøkkel skal være indeksverdi til kolonne i csv-fil
    def lesFil(self, indata, filinfo):
        gsm = filinfo["gsm"]
        prov = filinfo["prov"]
        varekode = filinfo["varekode"]
        merke_col = filinfo["merke_col"]
        merke_id = filinfo["merke_id"]
        bilag = filinfo["bilag"]
        try:
            df = pd.read_csv(indata, sep=";", index_col=False, dtype=str)
            dfmerke = df.columns[merke_col]
            dfvkode = df.columns[varekode]
            indexNames = []
            for i in range(df[dfmerke].size):
                if int(df[dfmerke][i]) != merke_id:
                    indexNames.append(i)
            df.drop(indexNames, inplace=True)
            unikeVarekoder = df[dfvkode].unique()
            betalesHK = multchoicebox("Velg koder som betales av HK", "Løkling Bane", unikeVarekoder)
        except UnicodeDecodeError:
            df = pd.read_csv(indata, sep=";", index_col=False, dtype=str, encoding='latin-1')
            dfmerke = df.columns[merke_col]
            dfvkode = df.columns[varekode]
            indexNames = []
            for i in range(df[dfmerke].size):
                if int(df[dfmerke][i]) != merke_id:
                    indexNames.append(i)
            df.drop(indexNames, inplace=True)
            unikeVarekoder = df[dfvkode].unique()
            betalesHK = multchoicebox("Velg koder som betales av HK", "Løkling Bane", unikeVarekoder)

        with open(indata) as fil:
            linje = fil.readline().strip().split(";")
            for linje in fil:
                biter = linje.strip().split(";")
                if int(biter[merke_col]) == merke_id:
                    try:
                        if biter[varekode] in betalesHK:
                            bbtalesHK = True
                        else:
                            bbtalesHK = False
                    except TypeError:
                        bbtalesHK = False
                    try:
                        nykunde = Kunde(int(biter[gsm]))
                        nyprovobj = Provisjonsobjekt(int(float(biter[gsm].replace(",", "."))),
                                                     int(float(biter[prov].replace(",", ".")))*1.25, str(biter[varekode]),
                                                     idno=biter[bilag], betalesHK=bbtalesHK)
                    except ValueError:
                        nykunde = Kunde(33333333)
                        nyprovobj = Provisjonsobjekt(33333333, int(float(biter[prov].replace(",", ".")))*1.25,
                                                     str(biter[varekode]), idno=biter[bilag], betalesHK=bbtalesHK)
                    nykunde.leggTilNyData("forventet", nyprovobj)
                    self._kunder.append(nykunde)

    def kunder(self):
        return self._kunder