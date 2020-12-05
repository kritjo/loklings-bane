"""

"""


class Provisjonsobjekt:
    def __init__(self, gsm, prov, årsak, kundenavn=None, dato=None, idno=None, betalesHK=False, egID=None):
        self._gsm = gsm
        self._prov = int(prov)
        self._årsak = årsak
        self._kundenavn = kundenavn
        self._dato = dato
        self._id = idno
        self._betalesHK = betalesHK
        self._egID = egID

    def betalesHK(self):
        return self._betalesHK

    def prov(self):
        return self._prov

    def GSM(self):
        return self._gsm
