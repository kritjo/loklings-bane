import tkinter as tk
from tkinter.filedialog import askopenfilename
from kontrollinstans import Kontrollinstans
import pandas as pd


class Gui:
    def __init__(self):
        self._vindu = tk.Tk()
        self._vindu.title("Løklings Bane")
        self._vindu.state("zoomed")
        self._vindu.geometry("1920x1080")
        velkommen = tk.Label(self._vindu,
                             text="Løkling Bane - et provisjonskontrollprogram\nAv kritjo@uio\nLisens: CC-BY-SA-4.0")
        velkommen.pack()
        self._focus = None
        self._op = None
        self._elguideFil = None
        self._opFil = None
        self._opFil2 = None
        self._opfilType = None
        self._colTest = None
        self._dfOp = None
        self._dfOp2 = None
        self._ki = Kontrollinstans()
        self._avviksfil = None

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
            self._ki.lagKundeKontoer("elguide", self._elguideFil, eginfo)

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
        if self._opFil2 is not None:
            opInfoDict = {"filbane": self._opFil2, "filtype": self._opfilType}
            self._dfOp2 = self._ki.lagDFFraOP(opInfoDict)
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

            tk.Label(opdfFrame,
                     text="Skriv inn radnummer som inneholder kolonnetitler, hvis riktig as-is skriv -1").pack()
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
                if name == "gsm":
                    gsmLabelVar.set(f"GSM: {self._dfOp[valueOp].iloc[0]}")
                elif name == "beløp":
                    belopLabelVar.set(f"BELØP: {self._dfOp[valueOp].iloc[0]}")
                elif name == "aarsak":
                    aarsakLabelVar.set(f"ÅRSAK: {self._dfOp[valueOp].iloc[0]}")
                elif name == "bilag":
                    bilagLabelVar.set(f"BILAG: {self._dfOp[valueOp].iloc[0]}")

            gsmLabelVar = tk.StringVar()
            gsmLabelVar.set("GSM")
            belopLabelVar = tk.StringVar()
            belopLabelVar.set("BELØP")
            aarsakLabelVar = tk.StringVar()
            aarsakLabelVar.set("ÅRSAK")
            bilagLabelVar = tk.StringVar()
            bilagLabelVar.set("BILAG")

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
            tk.Label(opInfoFrame, text="Første linje i valgt kolonne:").pack()
            gsmLabel = tk.Entry(opInfoFrame, textvariable=gsmLabelVar, state="disabled")
            gsmLabel.pack()
            belopLabel = tk.Entry(opInfoFrame, textvariable=belopLabelVar, state="disabled")
            belopLabel.pack()
            aarsakLabel = tk.Entry(opInfoFrame, textvariable=aarsakLabelVar, state="disabled")
            aarsakLabel.pack()
            bilagLabel = tk.Entry(opInfoFrame, textvariable=bilagLabelVar, state="disabled")
            bilagLabel.pack()
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

            waitframe = tk.Frame(self._vindu)
            waitframe.wait_window(mvaFrame)
            kolDict["filtype"] = self._opfilType
            self._ki.lagKundeKontoer(self._op, self._dfOp, kolDict)
            waitframe.pack()
            waitframe.destroy()


        elif self._opfilType == "html":
            tk.Label(opdfFrame, text="Velg tabeller som skal sjekkes for provisjon og trykk OK når ferdig.").pack()
            htmlContainer = tk.Frame(opdfFrame)
            htmlCanvas = tk.Canvas(htmlContainer)
            htmlscrollbar = tk.Scrollbar(htmlContainer, orient="vertical", command=htmlCanvas.yview)
            htmlscrollFrame = tk.Frame(htmlCanvas)

            htmlscrollFrame.bind(
                "<Configure>",
                lambda e: htmlCanvas.configure(
                    scrollregion=htmlCanvas.bbox("all")
                )
            )
            htmlCanvas.create_window((0, 0), window=htmlscrollFrame, anchor="nw")
            htmlCanvas.configure(yscrollcommand=htmlscrollbar.set)

            htmlTableSelected = [tk.IntVar() for i in range(len(self._dfOp))]
            htmlMvaTable = [tk.IntVar() for i in range(len(self._dfOp))]
            htmlTable2Selected = [tk.IntVar() for i in range(len(self._dfOp))]
            htmlMvaTable2 = [tk.IntVar() for i in range(len(self._dfOp))]
            tk.Label(htmlscrollFrame, text="\n\n-----------------------\n\n").pack()
            for i in range(len(self._dfOp)):
                htmlTable = tk.Label(htmlscrollFrame, text=f"{self._dfOp[i]}")
                htmlTable.pack()
                checkTable = tk.Checkbutton(htmlscrollFrame, text="Provisjonstabell?", variable=htmlTableSelected[i],
                                            onvalue=1, offvalue=0)
                checkTable.pack()
                checkMva = tk.Checkbutton(htmlscrollFrame, text="MVA?", variable=htmlMvaTable[i],
                                          onvalue=1, offvalue=0)
                checkMva.pack()
                tk.Label(htmlscrollFrame, text="\n\n-----------------------\n\n").pack()

            for i in range(len(self._dfOp2)):
                htmlTable = tk.Label(htmlscrollFrame, text=f"{self._dfOp2[i]}")
                htmlTable.pack()
                checkTable = tk.Checkbutton(htmlscrollFrame, text="Provisjonstabell?", variable=htmlTable2Selected[i],
                                            onvalue=1, offvalue=0)
                checkTable.pack()
                checkMva = tk.Checkbutton(htmlscrollFrame, text="MVA?", variable=htmlMvaTable2[i],
                                          onvalue=1, offvalue=0)
                checkMva.pack()
                tk.Label(htmlscrollFrame, text="\n\n-----------------------\n\n").pack()

            htmlContainer.pack(fill=tk.BOTH, expand=True)
            htmlCanvas.pack(side="left", fill=tk.BOTH, expand=True)
            htmlscrollbar.pack(side="right", fill="y")

            def killopdfFrame():
                opdfFrame.destroy()

            htmlok = tk.Button(opdfFrame, text="OK", command=killopdfFrame)
            htmlok.pack()
            opdfFrame.propagate(0)
            opdfFrame.pack(fill=tk.BOTH, expand=True)

            htmlcolParamFrame = tk.Frame()
            htmlcolParamFrame.wait_window(opdfFrame)

            for i in range(len(htmlTableSelected)):
                if htmlTableSelected[i].get() == 1:
                    riktightmltab = i

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
                    "bilag": "cid_bilag",
                    "kundenavn": "cid_navn"
                }
                kolDict[nameconv[name]] = valueOp
                if name == "gsm":
                    gsmLabelVar.set(f"GSM: {self._dfOp[riktightmltab][valueOp].iloc[0]}")
                elif name == "beløp":
                    belopLabelVar.set(f"BELØP: {self._dfOp[riktightmltab][valueOp].iloc[0]}")
                elif name == "aarsak":
                    aarsakLabelVar.set(f"ÅRSAK: {self._dfOp[riktightmltab][valueOp].iloc[0]}")
                elif name == "bilag":
                    bilagLabelVar.set(f"BILAG: {self._dfOp[riktightmltab][valueOp].iloc[0]}")
                elif name == "kundenavn":
                    navnLabelVar.set(f"KUNDENAVN: {self._dfOp[riktightmltab][valueOp].iloc[0]}")

            gsmLabelVar = tk.StringVar()
            gsmLabelVar.set("GSM")
            belopLabelVar = tk.StringVar()
            belopLabelVar.set("BELØP")
            aarsakLabelVar = tk.StringVar()
            aarsakLabelVar.set("ÅRSAK")
            bilagLabelVar = tk.StringVar()
            bilagLabelVar.set("BILAG")
            navnLabelVar = tk.StringVar()
            navnLabelVar.set("NAVN")

            def htmlcolparamkill():
                htmlcolParamFrame.destroy()

            colopnavn = list(self._dfOp[riktightmltab])
            for i in ["GSM", "Beløp", "Aarsak", "Bilag", "Kundenavn"]:
                comFrame = tk.Frame(htmlcolParamFrame)
                comTitle = tk.Label(comFrame, text=f"Velg kolonnenavn for {i}:")
                comTitle.pack()
                liste = tk.Listbox(comFrame, exportselection=0, name=i.lower())
                for i in range(len(colopnavn)):
                    liste.insert(i, colopnavn[i])
                liste.bind("<<ListboxSelect>>", listselectOp)
                liste.pack()
                comFrame.pack(side="left")
            tk.Label(htmlcolParamFrame, text="Første linje i valgt kolonne:").pack()
            gsmLabel = tk.Entry(htmlcolParamFrame, textvariable=gsmLabelVar, state="disabled")
            gsmLabel.pack()
            belopLabel = tk.Entry(htmlcolParamFrame, textvariable=belopLabelVar, state="disabled")
            belopLabel.pack()
            aarsakLabel = tk.Entry(htmlcolParamFrame, textvariable=aarsakLabelVar, state="disabled")
            aarsakLabel.pack()
            bilagLabel = tk.Entry(htmlcolParamFrame, textvariable=bilagLabelVar, state="disabled")
            bilagLabel.pack()
            navnLabel = tk.Entry(htmlcolParamFrame, textvariable=navnLabelVar, state="disabled")
            navnLabel.pack()
            okcolparam = tk.Button(htmlcolParamFrame, text="OK", command=htmlcolparamkill)
            okcolparam.pack()
            htmlcolParamFrame.pack()

            waitframe = tk.Frame()
            waitframe.wait_window(htmlcolParamFrame)
            for i in range(len(htmlTableSelected)):
                if htmlTableSelected[i].get() == 1:
                    kolDict["mvatopp"] = htmlMvaTable[i].get()
                    kolDict["filtype"] = "html"
                    kolDict["id_tabell"] = i
                    self._ki.lagKundeKontoer(self._op, self._dfOp, kolDict)
            if self._dfOp2 is not None:
                for i in range(len(htmlTable2Selected)):
                    if htmlTable2Selected[i].get() == 1:
                        kolDict["mvatopp"] = htmlMvaTable2[i].get()
                        kolDict["filtype"] = "html"
                        kolDict["id_tabell"] = i
                        self._ki.lagKundeKontoer(self._op, self._dfOp2, kolDict)
            waitframe.pack()
            waitframe.destroy()

        def lagresom():
            self._avviksfil = tk.filedialog.asksaveasfilename(title="Lagre avviksfil som...", initialfile="avviksliste.xlsx",
                                                              filetypes=[("Excel", "*.xlsx")])
            avviksframe.destroy()

        avviksframe = tk.Frame(self._vindu)
        kontrolliste = self._ki.gjørKontroll()
        tk.Label(avviksframe, text="Lagre avviksfil: ").pack()
        lagreSomKnapp = tk.Button(avviksframe, text="Lagre som..", command=lagresom)
        lagreSomKnapp.pack()
        avviksframe.pack()

        finalwait = tk.Frame(self._vindu)
        finalwait.wait_window(avviksframe)
        with open("_temp.csv", "w") as dfil:
            dfil.writelines(["GSM;PROV;ÅRSAK;BILAG;TYPE\n"])
            for kunde in kontrolliste:
                for provobj in kunde._forventetprov:
                    dfil.writelines([f"{provobj._gsm};{provobj._prov};{provobj._årsak};{provobj._id};Forventet\n"])
                for provobj in kunde._faktiskprov:
                    dfil.writelines([f"{provobj._gsm};{provobj._prov};{provobj._årsak};{provobj._id};Faktisk\n"])
        df = pd.read_csv("_temp.csv", sep=";", encoding='latin-1')
        df.to_excel(self._avviksfil)
        tk.Label(finalwait, text="Kontroll utført. Du kan trygt lukke vinduet.").pack()
        finalwait.pack()
        self._vindu.mainloop()
