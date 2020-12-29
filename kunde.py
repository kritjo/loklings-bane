"""

"""

__author__ = "Kristian Tjelta Johansen"
__copyright__ = "Copyright 2020, kritjo@uio"
__license__ = "CC-BY-SA 4.0 Int"
__version__ = "1.0"
__status__ = "Alpha"

class Kunde:
    def __init__(self, gsm):
        self._GSM = gsm
        self._forventetprov = []
        self._faktiskprov = []

    def GSM(self):
        return self._GSM

    def forventetprov(self):
        return self._forventetprov

    def faktiskprov(self):
        return self._faktiskprov

    def leggTilData(self, annenKunde):
        assert self._GSM == annenKunde.GSM(), f"{self._GSM} and {annenKunde.GSM()} should be equal"

        for provobj in annenKunde.forventetprov():
            self._forventetprov.append(provobj)

        for provobj in annenKunde.faktiskprov():
            self._faktiskprov.append(provobj)

    def leggTilNyData(self, type, provobj):
        assert self._GSM == provobj.GSM(), f"{self._GSM} and {provobj.GSM()} should be equal"

        assert provobj.GSM
        if type == "forventet":
            self._forventetprov.append(provobj)
        elif type == "faktisk":
            self._faktiskprov.append(provobj)
        else:
            raise Exception("Provision type should be either 'forventet' or 'faktisk'!")

    def avvik(self):
        forventet = 0
        faktisk = 0
        for provobj in self._forventetprov:
            if not provobj.betalesHK():
                forventet += provobj.prov()

        for provobj in self._faktiskprov:
            if not provobj.betalesHK():
                faktisk += provobj.prov()

        if forventet-2 <= faktisk <= forventet+2 and faktisk-2 <= forventet <= faktisk+2:
            avvik = False
        else:
            avvik = True

        return avvik
