"""
Oppretter en kontrollinstans som håndterer selve provisjonskontrollen,
samt opprettelse av opperatør- og elguideeksport objekter.
"""

from opperatørlister import OP
from opperatørlister import DF
from forventetutbetaling import Forventetutbetaling

__author__ = "Kristian Tjelta Johansen"
__copyright__ = "Copyright 2020, kritjo@uio"
__license__ = "CC-BY-SA 4.0 Int"
__version__ = "1.0"
__status__ = "Alpha"

class Kontrollinstans:
    def __init__(self):
        self._kundekontoer = []

    def lagDFFraOP(self, filinfo):
        df = OP(filinfo)
        return df.lesFil()

    def lagKunderFraEg(self, indata, filinfo):
        elguide = Forventetutbetaling(indata, filinfo)
        return elguide.kunder()

    def lagKunderFraOP(self, frafil, filinfo):
        opperatør = DF(frafil, filinfo)
        return opperatør.kunder()

    def lagKundeKontoer(self, fra, frafil, filinfo):
        if fra == "elguide":
            kunder = self.lagKunderFraEg(frafil, filinfo)
        elif fra == "ice":
            kunder = self.lagKunderFraOP(frafil, filinfo)
        elif fra == "telia":
            kunder = self.lagKunderFraOP(frafil, filinfo)
        elif fra == "telenor":
            kunder = self.lagKunderFraOP(frafil, filinfo)

        for kunde in kunder:
            eksisterendeKonto = False
            for kundekonto in self._kundekontoer:
                if kunde.GSM() == kundekonto.GSM():
                    eksisterendeKonto = True

            if not eksisterendeKonto:
                self._kundekontoer.append(kunde)
            elif eksisterendeKonto:
                for kundekonto in self._kundekontoer:
                    if kunde.GSM() == kundekonto.GSM():
                        kundekonto.leggTilData(kunde)
            else:
                raise Exception("FATAL! Customer", kunde.GSM(), "was neither existing or not existing")

    def gjørKontroll(self):
        feil = []
        for kunde in self._kundekontoer:
            if kunde.avvik():
                feil.append(kunde)
        return feil

    def forventetFil(self, indatafil):
        pass

    def indatafil(self, indatafil, opperatør):
        pass

