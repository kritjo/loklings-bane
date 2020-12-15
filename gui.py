import tkinter as tk
from tkinter.filedialog import askopenfilename
from kontrollinstans import Kontrollinstans
import pandas as pd

class Gui:
    def __init__(self):
        self._vindu = tk.Tk()
        self._vindu.title("Løklings Bane")
        self._vindu.state("zoomed")
        velkommen = tk.Label(self._vindu, text="Løkling Bane - et provisjonskontrollprogram\nAv kritjo@uio\nLisens: CC-BY-SA-4.0")
        velkommen.pack()
        self._focus = None
        self._op = None
        self._elguideFil = None
        self._opFil = None
        self._opFil2 = None
        self._opfilType = None
        self._colTest = None
        self._dfOp = None
        self._ki = Kontrollinstans()

    def start(self):

        def telenor():
            self._op = "telenor"
            opFrame.destroy()

        def telia():
            self._op = "telia"
            opFrame.destroy()

        def ice():
            self._op = "ice"
            opFrame.destroy()

        opFrame = tk.Frame(self._vindu)
        optekst = tk.Label(opFrame, text="Hvilken opperatør vil du kontrollere?")
        optekst.pack()
        telenor = tk.Button(opFrame, text="Telenor", command=telenor)
        telenor.pack()
        telia = tk.Button(opFrame, text="Telia", command=telia)
        telia.pack()
        ice = tk.Button(opFrame, text="Ice", command=ice)
        ice.pack()
        opFrame.pack()

        def open_file_csv():
            self._elguideFil = askopenfilename(filetypes=[("CSV", "*.csv")])
            filFrame.destroy()

        filFrame = tk.Frame(self._vindu)
        tekst = tk.Label(filFrame, text="Velg Elguide-fil")
        tekst.pack()
        åpneknapp = tk.Button(filFrame, text="Åpne", command=open_file_csv)
        åpneknapp.pack()
        filFrame.wait_window(opFrame)
        filFrame.pack()

        eginfo = {}
        def listselect(event):
            name = str(event.widget).split(".")[-1]
            selection = event.widget.curselection()
            value = event.widget.get(selection[0])
            idx = int(selection[0])
            print(f"{name}|{value}|{idx}")
            nameconv = {
                "gsm": "gsm",
                "beløp": "prov",
                "varekode": "varekode",
                "merke": "merke_col",
                "bilagsnr": "bilag"
            }
            eginfo[nameconv[name]] = idx

        egInfoFrame = tk.Frame(self._vindu)
        egInfoFrame.wait_window(filFrame)
        with open(self._elguideFil, "r") as fil:
            linje = fil.readline().strip().split(";")
            linjedict = {}
            for i in range(len(linje)):
                linjedict[i] = linje[i]
        for i in ["GSM", "Beløp", "Varekode", "Merke", "Bilagsnr"]:
            comFrame = tk.Frame(egInfoFrame)
            comTitle = tk.Label(comFrame, text=f"Velg kolonnenavn for {i}:")
            comTitle.pack()
            liste = tk.Listbox(comFrame, exportselection=0, name=i.lower())
            for key, value in linjedict.items():
                liste.insert(key, value)
            liste.bind("<<ListboxSelect>>", listselect)
            liste.pack()
            comFrame.pack(side="left")
        egInfoFrame.pack()

        with open("config.txt", "r") as fil:
            for linje in fil:
                biter = linje.strip().split("=")
                if biter[0] == "ice_merke" and self._op == "ice":
                    eginfo["merke_id"] = int(biter[1])
                elif biter[0] == "telenor_merke" and self._op == "telenor":
                    eginfo["merke_id"] = int(biter[1])
                elif biter[0] == "telia_merke" and self._op == "telia":
                    eginfo["merke_id"] = int(biter[1])


        def click():
            egInfoFrame.destroy()
        ferdig = tk.Button(egInfoFrame, command=click, text="OK")
        ferdig.pack(side="bottom")

        def open_file():
            self._opFil = askopenfilename(filetypes=[("Alle filtyper", "*.*")])

        def open_file2():
            self._opFil2 = askopenfilename(filetypes=[("Alle filtyper", "*.*")])

        def sel():
            self._opfilType = str(var.get())

        def opfilKill():
            opfilFrame.destroy()

        opfilFrame = tk.Frame(self._vindu)
        opfilFrame.wait_window(egInfoFrame)
        tekst = tk.Label(opfilFrame, text=f"Velg {self._op}-fil:")
        tekst.pack()
        åpneknapp = tk.Button(opfilFrame, text="Åpne", command=open_file)
        åpneknapp.pack()
        if self._op == "telenor":
            tekst = tk.Label(opfilFrame, text=f"Velg (om ønskelig) en til {self._op}-fil:")
            tekst.pack()
            åpneknapp = tk.Button(opfilFrame, text="Åpne", command=open_file2)
            åpneknapp.pack()
        tekst = tk.Label(opfilFrame, text=f"Velg filtype:")
        tekst.pack()
        var = tk.StringVar()
        filtypeExcel = tk.Radiobutton(opfilFrame, text="Excel", variable=var, value="excel", command=sel)
        filtypeExcel.pack()
        filtypeHtml = tk.Radiobutton(opfilFrame, text="HTML", variable=var, value="html", command=sel)
        filtypeHtml.pack()
        okKnapp = tk.Button(opfilFrame, text="OK", command=opfilKill)
        okKnapp.pack()
        opfilFrame.pack()

        def opdfframekill():
            self._colTest = colNavnSjekk.get()
            try:
                self._colTest = int(self._colTest)
                opdfFrame.destroy()
                if self._colTest == -1:
                    dropRows = False
                else:
                    dropRows = True
                    drops = 0
                    dropn = self._colTest - 1
                    headers = self._colTest

                if dropRows:
                    try:
                        self._dfOp = self._dfOp.rename(columns=self._dfOp.iloc[headers])
                        self._dfOp = self._dfOp.drop(self._dfOp.index[headers])
                    except KeyError:
                        pass
                    rowstodrop = [row for row in range(drops, dropn + 1)]
                    self._dfOp = self._dfOp.drop(index=rowstodrop)

                kolonnenavn = self._dfOp.columns.tolist()
                for i in range(len(kolonnenavn)):
                    kolonnenavn[i] = str(kolonnenavn[i]) + str(i)

                self._dfOp.columns = kolonnenavn

            except ValueError:
                raise Exception("RADNUMMER MÅ VÆRE ET TALL!")

        opdfFrame = tk.Frame(self._vindu)
        opdfFrame.wait_window(opfilFrame)
        opInfoDict = {"filbane": self._opFil, "filtype": self._opfilType}
        self._dfOp = self._ki.lagDFFraOP(opInfoDict)
        tk.Label(opdfFrame, text="Slik ser filen ut:").pack()
        if self._opfilType == "excel":

            visningContainer = tk.Frame(opdfFrame)
            visningCanvas = tk.Canvas(visningContainer)
            scroll = tk.Scrollbar(visningContainer, orient="vertical", command=visningCanvas.yview)
            scrollx = tk.Scrollbar(visningContainer, orient="horizontal", command=visningCanvas.xview)
            scrollFrame = tk.Frame(visningCanvas)
            scrollFrame.bind(
                "<Configure>",
                lambda e: visningCanvas.configure(
                    scrollregion=visningCanvas.bbox("all")
                )
            )
            visningCanvas.create_window((0, 0), window=scrollFrame, anchor="nw")
            visningCanvas.configure(yscrollcommand=scroll.set)
            visningCanvas.configure(xscrollcommand=scrollx.set)

            tk.Label(scrollFrame, text=f"{self._dfOp.to_string()}").pack()
            visningContainer.pack()
            visningCanvas.pack(side="left", fill="both", expand=True)
            scroll.pack(side="right", fill="y")
            scrollx.pack(side="bottom", fill="x")

            tk.Label(opdfFrame, text="Skriv inn radnummer som inneholder kolonnetitler, hvis riktig as-is skriv -1").pack()
            colNavnSjekk = tk.Entry(opdfFrame, text="Radnummer / -1")
            colNavnSjekk.pack()
            kolonneOK = tk.Button(opdfFrame, text="OK", command=opdfframekill)
            kolonneOK.pack()
            opdfFrame.pack()

            kolDict = {}

            def listselectOp(event):
                name = str(event.widget).split(".")[-1]
                selection = event.widget.curselection()
                valueOp = event.widget.get(selection[0])
                idx = int(selection[0])
                print(f"{name}|{valueOp}|{idx}")
                nameconv = {
                    "gsm": "cid_gsm",
                    "beløp": "cid_prov",
                    "aarsak": "cid_årsak",
                    "bilag": "cid_bilag"
                }
                kolDict[nameconv[name]] = valueOp

            opInfoFrame = tk.Frame(self._vindu)
            opInfoFrame.wait_window(opdfFrame)
            colopnavn = list(self._dfOp)
            for i in ["GSM", "Beløp", "Aarsak", "Bilag"]:
                comFrame = tk.Frame(opInfoFrame)
                comTitle = tk.Label(comFrame, text=f"Velg kolonnenavn for {i}:")
                comTitle.pack()
                liste = tk.Listbox(comFrame, exportselection=0, name=i.lower())
                for i in range(len(colopnavn)):
                    liste.insert(i, colopnavn[i])
                liste.bind("<<ListboxSelect>>", listselectOp)
                liste.pack()
                comFrame.pack(side="left")
            opInfoFrame.pack()

            def opInfoKill():
                opInfoFrame.destroy()

            ferdig = tk.Button(opInfoFrame, command=opInfoKill, text="OK")
            ferdig.pack(side="bottom")

            def rm47a():
                def rm47(x):
                    return int(str(x)[2:])

                self._dfOp[kolDict["cid_gsm"]] = self._dfOp[kolDict["cid_gsm"]].apply(rm47)
                rm47Frame.destroy()

            def kill47():
                rm47Frame.destroy()

            rm47Frame = tk.Frame(self._vindu)
            rm47Frame.wait_window(opInfoFrame)
            tk.Label(rm47Frame, text="Inneholder GSM-nr 47 forran?").pack()
            rmYes = tk.Button(rm47Frame, text="JA", command=rm47a)
            rmNo = tk.Button(rm47Frame, text="NEI", command=kill47)
            rmYes.pack()
            rmNo.pack()
            rm47Frame.pack()

            def mvaJa():
                kolDict["mvatopp"] = True
                mvaFrame.destroy()

            def mvaNei():
                kolDict["mvatopp"] = False
                mvaFrame.destroy()

            mvaFrame = tk.Frame(self._vindu)
            mvaFrame.wait_window(rm47Frame)
            tk.Label(mvaFrame, text="MVA på topp av tabell?").pack()
            mvaYes = tk.Button(mvaFrame, text="JA", command=mvaJa)
            mvaNo = tk.Button(mvaFrame, text="NEI", command=mvaNei)
            mvaYes.pack()
            mvaNo.pack()
            mvaFrame.pack()

            waitFrame = tk.Frame(self._vindu)
            waitFrame.wait_window(mvaFrame)
            kolDict["filtype"] = self._opfilType
            self._ki.lagKundeKontoer(self._op, self._dfOp, kolDict)
















