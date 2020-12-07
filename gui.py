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
                if biter[0] == "telia_merke" and self._op == "telia":
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

        if self._opfilType == "excel":
            opInfoDict = {"filbane": self._opFil, "filtype": self._opfilType}
            dfOp = self._ki.lagDFFraOP(opInfoDict)














