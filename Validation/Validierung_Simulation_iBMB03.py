
# coding: utf-8

# # Entwicklung einer Software zur Überprüfung und Bewertung der Prognosefähigkeit von Brandsimulationsergebnissen

# <img src="Logo_iBMB.png" alt="iBMB Logo" title="iBMB" style="width: 250px;" align="right"/>
# #### Institut für Baustoffe, Massivbau und Brandschutz - Fachgebiet Brandschutz
# 
# Vorgelegt von:<br>
# Marcel Aurich
# 
# Betreuer:<br>
# Dr.-Ing. Dipl.-Phys. Olaf Riese<br>
# Dr.-Ing. Matthias Siemon

# # Aufgabe
# 
# Der Einsatz numerischer Methoden hat nicht nur im Brandschutzingenieurwesen enorm an Bedeutung gewonnen. Die Entwicklung von Brandsimulationsmodellen ist einerseits noch nicht abgeschlossen, andererseits muss die Eignung der Modelle für Vorhersagen bewertet werden. Hierbei erscheint es notwendig nicht nur einzelne Werte (z. B. Maxima), sondern den ganzen Verlauf zweier Zeitreihen z. B. bestehend aus Versuchs- und Simulationsergebnissen bestimmter Größen zu vergleichen.
# 
# Zur Überprüfung der Prognosefähigkeit wurden verschiedene Bewertungskriterien definiert und bereits in Validierungsrechnungen eingesetzt. Ziel der Arbeit ist die Entwicklung einer Software, die eine einfache und übersichtliche Auswertung von Brandsimulationsergebnissen mit Referenzwerten (z. B. aus Brandversuchen) ermöglicht.
# 
# #### Aufgabenschwerpunkte bei der Entwicklung der Software: 
# 
# - Darstellen der Ergebnisse und der Referenzwerte (z. B. Versuchsergebnisse) jeder Kenngröße/Messfühlers als Zeitreihen
# - Darstellen der Ergebnisse und der Referenzwerte als Mittelwerte der ausgewählten Kenngrößen/Messfühler als Zeitreihen
# - PEAK / PEAK Plots mit Vertrauensbereichen
# - PEAK / PEACOCK Plots mit Vertrauensbereichen
# - Darstellung der Häufigkeit der Messgrößen
# - Darstellen und Auswerten der Ergebnisse als Boxplots
# - Auswahl von Messgruppen (z. B. alle Gastemperaturen des Messbaumes CW, alle Strömungsgeschwindigkeiten in Türprofile L1_L2)
# - Speichern der Ergebnisse als Plot und *.csv Daten
# 
# # Funktionalitäten der Software:
# 
# Die gestellten Anforderungen an die Software wurden vollständig erreicht und umgesetzt. Mithilfe des Programms können verschiedene Daten des Brandschutzingenieurwesens miteinander verglichen und Daten aus Simulationen validiert werden. Die Software bietet eine intuitive und schnelle Steuerung über Konfigurationsdateien (.ini - Dateien) und kann alternativ auch direkt über die Konsole gesteuert werden. Die Konfigurationsdateien ermöglichen eine Automatisierung des Programmablaufs und eine schnelle Auswertung der Daten, nach einmaliger Konfiguration seitens des Benutzers.
# 
# Die Anwendung kann dabei auch so konfiguriert werden, dass sie selbständig mehrere Validierungen mit unterschiedlichen Daten durchführt. Sie liest eigenständig die hinterlegten Daten ein und beginnt im Anschluss mit den in der Konfigurationsdatei festgelegten Vergleichs- und Validierungs-Routinen. Dazu stehen die folgenden Operationen zu Verfügung:
# 
# - Darstellung der Häufigkeit der verschiedenen Messgrößen
# - Vergleich der Zeitreihen der Referenz- und Simulationsdaten
# - Vergleich der gemittelten Zeitreihen der Referenz- und Simulationsdaten
# - Vergleich der ursprünglichen und gemittelten Zeitreihen
# - Darstellung der Peaks auf den gemittelten Zeitreihen der Referenz- und Simulationsdaten
# - Vergleich der Zeitreihen der Referenz- und Simulationsdaten mittels Boxplots
# - Durchführung eines PEAK-Vergleichs und Darstellung der zugehörigen Vertrauensbereiche
# - Durchführung eines PEACOCKS-Vergleichs und Darstellung der zugehörigen Vertrauensbereiche
#   
# Darüber hinaus kann der Benutzer genau spezifizieren, welche Messfühler verglichen werden sollen. Über eine intelligente Erkennung der Eingaben in der Konfigurationsdatei oder Konsole, kann das Programm die zu vergleichenden Messfühler identifizieren. Bei Bedarf können auch nur Daten aus einer Datei visualisiert werden.
# 
# Die Ergebnisse werden als ".csv"-Dateien und als Bilder exportiert. Das Herzstück der Anwendung bildet jedoch die automatisch erzeugte PDF-Datei, die übersichtlich alle Ergebnisse (Daten und Bilder), sowie die wichtigsten Informationen aus der Konfigurationsdatei zusammenfasst. Die Datei wird vollständig automatisiert generiert und kann beispielsweise als Anhang einer Auswertung oder Validierung der Daten beigelegt werden. Der Benutzer wird auf diese Weise sehr durch die Software im weiteren Verfahren unterstützt.
# 
# 
# # Softwareentwicklung
# 
# Die Anwendung erfüllt die in der Softwareentwicklung ausgewiesenen Softwarequalitäten und - Standards und verwendet für die Umsetzung etablierte Entwurfsmuster der Softwarearchitektur. Das Ziel war es die folgenden Anwendungsqualitäten zu erreichen:
# 
# - Erweiterbarkeit und Wartbarkeit der Software
# - Verständlichkeit der Handhabung und des Quellcodes der Software
# - Robustheit gegenüber unvorhergesehenen Änderungen der Randbedingungen
# - Effizienz bei der Verarbeitung großer Datenmengen
# - Portierbarkeit auf verschiedene Systeme
# - Zuverlässigkeit im Hinblick auf die Fehleranfälligkeit der Software
# - Genauigkeit bei den Berechnungen
#     
# Auf den nachfolgenden Seiten wird der Quellcode der Software präsentiert und erläutert. Das Programm ist objektorientiert entwickelt worden und besteht im Einzelnen aus diversen Modulen (Klassen). Die verschiedenen Klassen werden vor ihrer Implementierung jeweils kurz beschrieben, um ihre Funktionalität darzustellen.

# # Import der verwendeten Bibliotheken
# 
# Im folgenden Anweisungsblock werden die verwendeten Bibliotheken importiert. Diese bringen Funktionalitäten mit, die für die Software benötigt werden und bereits zur Verfügung stehen. Darunter fällt beispielsweise die Bibliothek "csv", die Unterstützung bei der Verarbeitung von ".csv"-Dateien liefert. Bibliotheken bieten jedoch keine fertigen Softwarelösungen. Sie können als Bausteine betrachtet werden, auf die zugegriffen werden kann, um Lücken im bestehenden Programmablauf zu füllen.
# 
# Eine weitere verwendete und sehr mächtige Bibliothek ist "matplotlib". Diese liefert Operationen und Hilfestellungen bei der Erzeugung von Diagrammen und findet Anwendung bei der Erzeugung der Grafiken in diesem Programm. Die Bibliothek "configparser" ist sehr hilfreich im Umgang mit Konfigurationsdateien. Mit ihrer Hilfe können die Konfigurationen schnell und einfach eingelesen und verarbeitet werden. Über vordefinierte Routinen kann nach Schlüsselwörtern innerhalb der Dateien gesucht und deren zugewiesener Wert eingelesen werden.
# 
# Zum Schluss soll noch die Bibliothek "numpy" vorgestellt werden, die viele nützliche Funktionen für die wissenschaftliche Verarbeitung von Daten bietet. So können beispielsweise Arrays (auch multidimensional) angelegt und auf unterschiedlichste Art bearbeitet werden.

# In[40]:


# Bibliothek zum Einlesen der CSV-Dateien
import csv
# Bibliothek zur Darstellung von Plots
import matplotlib.pyplot as plot
# Bibliothek für System-interne Funktionen
import os, sys
# Bibliothek für Zeitoperationen
import time
# Bibliothek zur Verarbeitung von Konfigurations-Dateien
import configparser
# Bibliothek zur Erstellung von Splines
from scipy.interpolate import spline
# Bibliothek für Interpolationen
from scipy.interpolate import interpolate
# Bibliothek für wissenschaftliche Funktionalitäten
import numpy as np
# Bibliothek für mathematische Operationen
import math
# Bibliothek für das Verarbeiten von Warnungen
import warnings
warnings.filterwarnings("ignore")
# Bibliothek für die Erstellung und Bearbeitung von PDF-Dokumenten
from fpdf import FPDF
# Bibliothek für statistische Operationen
import statistics


# # Klasse: ConfigReader
# 
# Die Klasse "ConfigReader" dient dem Einlesen der Konfigurationsdateien und dient in diesem Fall ausschließlich der Verwaltung und Vorhaltung der zugewiesenen Instanz der Klasse "ConfigParser" aus der Bibliothek "configparser".

# In[41]:


class ConfigReader:
    config = 0

    def __init__(self, configName):
        self.config = configparser.ConfigParser()

        # Konfigurationsdatei einlesen
        self.config.read(configName)


# # Klasse: Sensor
# Die Aufgabe der Klasse "Sensor" ähnelt derer der Klasse "ConfigReader". Sie hält ebenfalls Informationen vor, in diesem Fall jedoch über die verschiedenen eingelesenen Messfühler. Für jeden Fühler wird sein ganzer Name, seine Untersuchungsgröße und sein Index in der Speicherstruktur hinterlegt.

# In[42]:


class Sensor:
    # Name des Sensors (z.B. "TG_L0_CC_390")
    originalName = "NA"
    # Speicherort des Sensors intern (Index)
    col = -1
    # Sensorgruppe, d.h. Untersuchungsgröße des Sensors (z.B. "TG")
    group = "NA"
    # Factor der 1. Datendatei
    factor = "1"

    def __init__(self, originalName, col, group, factor):
        self.originalName = originalName
        self.col = col
        self.group = group
        self.factor = factor


# # Klasse: SensorDictionary
# Die verschiedenen Instanzen der Klasse "Sensor" werden in der Klasse "SensorDictionary" gespeichert und gruppiert nach ihrer Untersuchungsgröße. Zusätzlich werden aus der Konfigurationsdatei weitere Informationen zu den verschiedenen Untersuchungsgrößen eingelesen. Dazu zählen:
# 
# - der vollständige Name der Untersuchungsgröße (z. B. "Gastemperatur" für "TG")
# - die Einheit der Größe (z. B. "°C" für "TG")
# - der Vertrauensbereich im Hinblick auf PEAK und PEACOCK - Vergleiche (z. B. "30" (%))
# - die Art der Peak-Bestimmung, d. h. ob das Maximum, das Minimum oder der absolute Wert der Zeitreihe für die Messgröße relevant sind (z. B. "max" für "TG")
# 
# Des Weiteren werden noch für die bessere Handhabung der verschiedenen Messfühler einige Unterstützungs-Methoden implementiert. Auf diese Weise kann zum Beispiel über eine bestimmte Untersuchungsgröße auf alle zugehörigen Fühler zugegriffen werden.

# In[43]:


class SensorDictionary:
    # Liste aller ausgelesenen Sensoren zur besseren Verwaltung
    sensorList = []
    # Dictionary aller Sensorgruppen (=Untersuchungsgrößen)
    sensorGroupNames = dict()
    # Dictionary aller Einheiten der Sensorgruppen
    sensorGroupUnits = dict()
    # Dictionary aller Faktoren der Sensorgruppen der 1. Datei
    sensorGroupFactors = dict()
    # Dictionary aller maximal zugelassenen Unsicherheiten der Sensorgruppen
    sensorGroupUcwPeak = dict()
    sensorGroupUcwPeacock = dict()
    # Dictionary für Art der Peak-Bestimmung je Messgröße
    sensorGroupPeakTypes = dict()

    configReader = ConfigReader

    def __init__(self, configReader):
        self.sensorList = []
        self.configReader = configReader
        self.__registerSensorParams__()

    def createNewSensor(self, originalName, col):
        # Neuen Sensor anlegen und registrieren
        group = originalName.split("_")[0]

        # Falls Untersuchungsgröße unbekannt (NA = Not Available)
        if group not in self.sensorGroupNames:
            self.sensorGroupNames[group] = "NA"
            self.sensorGroupUnits[group] = "-"
            self.sensorGroupFactors[group] = "1"
            self.sensorGroupUcwPeak[group] = "0"
            self.sensorGroupUcwPeacock[group] = "0"
            self.sensorGroupPeakTypes[group] = "max"
            
        factor = self.sensorGroupFactors[group]
        #print("factor=", factor)
        newSensor = Sensor(originalName, col, group, factor)
        self.sensorList.append(newSensor) 

    def getSensorByCol(self, col):
        # Sensor anhand seinem Speicherort (Spalte) in der Matrix ermitteln
        for sensor in self.sensorList:
            if sensor.col == col:
                return sensor
        return "NoSensorFound"

    def getSensorsByGroup(self, group):
        # Sensoren anhand ihrer Untersuchungsgröße ermitteln
        sensorsFromGroup = []
        for sensor in self.sensorList:
            if sensor.group == group:
                sensorsFromGroup.append(sensor)
        return sensorsFromGroup

    def getFirstSensorFromGroup(self, group):
        # Ersten Sensor einer Untersuchungsgröße ermitteln
        for sensor in self.sensorList:
            if sensor.group == group:
                return sensor
        return "No Sensor found"

    def listAllSensorsSortedByGroup(self):
        # Sensoren nach Untersuchungsgrößen sortieren und auflisten
        for group in self.sensorGroupNames:
            print("")
            print(group,"=",self.sensorGroupNames.get(group),"- Sensoren:")
            print("--------------------")
            for sensor in self.getSensorsByGroup(group):
                print(sensor.originalName)

    def __registerSensorParams__(self):
        # Dictionary aller Sensorgruppen (=Untersuchungsgrößen)
        sensorGroups = self.configReader.config.get("Variables",
                                        "Sensor_Types").split(",")
        sensorNames = self.configReader.config.get("Variables",
                                        "Sensor_Names").split(",")
        sensorUnits = self.configReader.config.get("Variables",
                                        "Sensor_Units").split(",")
        sensorFactors = self.configReader.config.get("Variables",
                                        "Sensor_Factors").split(",")
        sensorPeakTypes = self.configReader.config.get(
            "Variables", "Sensor_Peak_Type").split(",")
        sensorUncertaintiesPeak = self.configReader.config.get(
            "Variables", "Sensor_Uncertainty_PEAK").split(",")
        sensorUncertaintiesPeacock = self.configReader.config.get(
            "Variables", "Sensor_Uncertainty_PEACOCK").split(",")
        counter = 0
        for sensorGroup in sensorGroups:
            self.sensorGroupNames[sensorGroup] = sensorNames[counter]
            self.sensorGroupUnits[sensorGroup] = sensorUnits[counter]
            self.sensorGroupFactors[sensorGroup] = sensorFactors[counter]
            self.sensorGroupUcwPeak[sensorGroup] = sensorUncertaintiesPeak[
                counter]
            self.sensorGroupUcwPeacock[
                sensorGroup] = sensorUncertaintiesPeacock[counter]
            self.sensorGroupPeakTypes[sensorGroup] = sensorPeakTypes[counter]
            counter += 1


# # Klasse: ImportData
# Das Einlesen und Speichern der Daten aus den ".csv"-Dateien ist Aufgabe der Klasse "ImportData". Mit Hilfe der Bibliothek "csv" werden die Dateien geöffnet und zeilenweise eingelesen. Ein ";" zeigt dabei die Unterteilung der Zeilen in verschiedenen Spalten (Zellen) an. 
# 
# Zusätzlich wird während des Einlese-Vorgangs geprüft, ob die eingelesenen Daten auch symmetrisch in der ".csv"-Datei hinterlegt sind. Auf diese Weise können Fehler in der Ursprungsdatei ausgeschlossen werden und das Programm wird robuster. Abschließend wird für jede Datei ein Array mit deren Daten angelegt, auf das im weiteren Verlauf der Anwendung schnell und strukturiert zugegriffen werden kann.

# In[44]:


class ImportData:
    data = [[]]
    noRows = 0
    noCols = 0

    # Konstruktor
    def __init__(self, fileName):
        # Datei öffnen
        file = open(fileName, "rt")

        # Datenarray initialisieren
        arrayInitialized = self.__initializeDataArray__(file)
        if arrayInitialized == False:
            return

        # Datenarray füllen
        self.__fillDataArray__(file)

        file.close()

    def __initializeDataArray__(self, file):
        # Array einmalig zu Beginn vor der Belegung initialisieren
        reader = csv.reader(file, delimiter=";")

        noRows = 0
        noCols = 0
        for row in reader:
            noRows = noRows + 1
            noCols = 0
            for i in row:
                noCols = noCols + 1
                # Prüfen, ob die eingelesene Datei eine symmetrische 
                # Matrix von Sensoren enthält
                if i == "":
                    print(noRows, noCols)
                    print("ERROR: Keine symmetrische Daten-Matrix!")
                    return False

        # Datenarray mit "0" initialisieren
        self.data = [[0] * noCols for i in range(noRows)]
        self.noRows = noRows
        self.noCols = noCols
        return True

    def __fillDataArray__(self, file):
        # Datenarray mit Inhalten aus der eingelesenen Datei füllen
        file.seek(0)
        reader = csv.reader(file, delimiter=";")

        rowCounter = -1
        for row in reader:
            rowCounter = rowCounter + 1
            for i in range(0, len(row)):
                # Die "Time"-Zelle der Datei wird für spätere 
                # Untersuchungen vereinheitlicht
                row[i] = row[i].replace("FDS Time", "TIME")
                row[i] = row[i].replace("Time", "TIME")
                row[i] = row[i].replace("ATIME", "TIME")
                row[i] = row[i].replace('"', '')
            self.data[rowCounter] = row[:]


# # Klasse: CompareData
# Der nächste Schritt in der Verarbeitung der eingelesenen Daten wird von der Klasse "CompareData" übernommen. Zu Beginn werden mit Hilfe der Klasse "ImportData" die jeweiligen Dateien importiert und gespeichert. Die folgende Aufgabe ist es, die eingelesenen Daten zu vergleichen und gemeinsame Messfühler zu finden. Dieser Schritt ist notwendig, um eine Basis für einen Vergleich der Daten zu schaffen.
# 
# Wird ein gleicher Messfühler (z. B. "TG_L0_CC_390") gefunden, wird für ihn auch direkt ein Objekt der Klasse "Sensor" angelegt und er wird im "SensorDictionary" gespeichert. Es werden jedoch nur Messfühler für den weiteren Programmverlauf benötigt, die sich in beiden Dateien wiederfinden. Messfühler, die nur in einer der beiden Dateien vorliegen können nicht verglichen werden und werden auch nicht gespeichert. Auf diese Weise entstehen am Ende reduzierte Daten-Arrays (für jede Datei ein Array), die nur die Daten der Fühler enthalten, die in beiden Dateien vorliegen. Zusätzlich werden die Arrays so organisiert, dass sich entsprechende Fühler in beiden Speicherstrukturen sich auch in ihrem Index entsprechen. Im Falle des angehängten Validierungsbeispiels liegt der Fühler "TG_L0_CC_390" in beiden reduzierten Daten-Arrays auf dem Index "0".
# 
# Eine weitere Aufgabe der Klasse liegt in der Speicherung der zusammengefassten Daten als externe und neue ".csv"-Datei. Mit Hilfe der Methoden "writeDataCSVFiles" und "writeDataCSVFilesMean" werden die ursprünglichen und gemittelten Zeitreihen der Messfühler gespeichert. Der Aufruf zur Speicherung der gemittelten Daten erfolgt jedoch erst zu einem späteren Zeitpunkt im Programm, sobald diese für die Darstellung berechnet werden.

# In[45]:


class CompareData:
    # Importierte Datenarrays
    importData1 = ImportData
    importData2 = ImportData
    # Reduzierte Datenarrays, Messfühler entsprechen sich in beiden
    # Speicherstrukturen sowohl in der Anzahl als auch im Speicherort
    data1Red = [[]]
    data2Red = [[]]
    meanData1Red = []
    meanData2Red = []
    sensors = []

    sensorDict = SensorDictionary
    configReader = 0

    def __init__(self, configReader, sensorDict):
        self.configReader = configReader
        self.sensorDict = sensorDict

        # Import der 1. Datei, ggf. Referenzwert-Datei (z.B. aus Versuch)
        self.importData1 = ImportData(
            self.configReader.config.get("Import", "Import_File_1"))
        # Import der 2. Datei, ggf. Messwert-Datei aus Simulation
        self.importData2 = ImportData(
            self.configReader.config.get("Import", "Import_File_2"))

        # Initalisierung der reduzierten Datenarrays (NA = Not available)
        maxNoCols = max(self.importData1.noCols, self.importData2.noCols)
        maxNoRows = max(self.importData1.noRows, self.importData2.noRows)
        self.data1Red = [["NA"] * maxNoCols for i in range(maxNoRows)]
        self.data2Red = [["NA"] * maxNoCols for i in range(maxNoRows)]
        self.meanData1Red = [[0]]
        self.meanData2Red = [[0]]

        # Gleiche Sensoren in beiden Dateien finden und in neue Arrays 
        # schreiben, in denen sich die Spalten Fühler entsprechen
        self.__findSensors__()
        
        # Bei anderen Einheiten einzelner Fühler der 1. Datei
        # werden Faktoren entsprechend der config.ini angewendet 
        
        #faktor = 1
        
        # numpy array definieren und transponieren
        v = np.array(self.data1Red)
        v = v.T

        for row in range(len(v)):
            # Erste Zeile ("TIME") nicht berücksichtigen
            if row >= 1:
                try:
                    #Erste beiden Zellen nicht berücksichtigen
                    #Faktor bestimmen
                    vr = np.array(v[row][2:])
                    
                    try:
                        group = self.sensorDict.getSensorByCol(row).group
                        factor = float(self.sensorDict.sensorGroupFactors.get(group))
                        if factor != 1 and group == "CO":
                            print("Einheit =", v[row][1])
                            print("group = ",group)
                            print("factor =", factor)
                    except AttributeError:
                        pass
                    vr = vr.astype(np.float)
                    ur = vr * factor
                    ur = ["%.15f" % number for number in ur]
                    #ur = ur.astype(np.str)
                    if row > 0 and factor != 1 and group == "CO": 
                        print("row=", row)
                        print("vr=", vr)
                        print("v[row][2:]:", ur)
                        print()
                    v[row][2:] = ur
                except ValueError:
                    pass
        # Zurückschreiben in self.data1Red
        self.data1Red = v.T

        # Speichern der Ergebnisse als externe .csv - Datei
        if configReader.config.get("Export", "Export") == "1":
            self.__writeDataCSVFiles__()

    def __findSensors__(self):
        destCol = 0

        # Zeile mit den Bezeichnungen der Fühler in erster Datei suchen
        for row1 in range(self.importData1.noRows):
            #print(self.importData1)
            if self.importData1.data[row1][0].lower() == "time":
                for col1 in range(self.importData1.noCols):
                    destCol = self.__calculateDestinationColumn__(
                        row1, col1, destCol)
                break

    def __calculateDestinationColumn__(self, row1, col1, destCol):
        # Zeile mit den Bezeichnungen der Fühler in zweiter Datei suchen
        for row2 in range(self.importData2.noRows):
            if self.importData2.data[row2][0].lower() == "time":
                for col2 in range(self.importData2.noCols):
                    # Vergleich, ob die Sensoren den gleichen Namen haben
                    if self.importData1.data[row1][
                            col1] == self.importData2.data[row2][col2]:
                        self.__writeReducedData__(row1, row2, col1, col2,
                                                  destCol)
                        destCol += 1
                        return destCol
                break
        return destCol

    def __writeReducedData__(self, row1, row2, col1, col2, destCol):
        # Schreiben der Daten in neue reduzierte Arrays, in denen sich 
        # die Spalten der gleichen Fühler entsprechen       
        for newRow in range(self.importData1.noRows - row1):
            self.data1Red[newRow][destCol] = self.importData1.data[
                row1 + newRow][col1]
                        
        for newRow in range(self.importData2.noRows - row2):
            self.data2Red[newRow][destCol] = self.importData2.data[
                row2 + newRow][col2]  

        # Neuen Sensor dem Sensor-Dictionary hinzufügen
        sensorName = self.data1Red[0][destCol]
        if sensorName.lower() != "time":
            self.sensorDict.createNewSensor(sensorName, destCol)

    def __writeDataCSVFiles__(self):
        # Auslesen der Export-Dateinamen
        outputName1 = self.configReader.config.get("Export",
                                                   "Export_File_1_data")
        outputName2 = self.configReader.config.get("Export",
                                                   "Export_File_2_data")

        # Reduzierte Datenarrays mit gleichen Sensoren 
        # der beiden Dateien herrausschreiben
        if not os.path.exists("Results\\"):
            os.makedirs("Results\\")
        with open("Results\\" + outputName1, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", lineterminator="\n")
            writer.writerows(self.data1Red)
        with open("Results\\" + outputName2, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", lineterminator="\n")
            writer.writerows(self.data2Red)

    def writeDataCSVFilesMean(self, linesToPlot):
        # Gemittelte Zeitreihen in CSV-Datei speichern

        # Prüfen, ob der Ordner "Results" bereits existiert
        if not os.path.exists("Results\\"):
            os.makedirs("Results\\")

        # Matrizen transponieren, so dass die Fühler vertikal verlaufen
        self.meanData1Red = list(map(list, zip(*self.meanData1Red)))
        self.meanData2Red = list(map(list, zip(*self.meanData2Red)))

        # Prüfen, welche Dateien gespeichert werden sollen
        if linesToPlot == "1":
            with open("Results\\" + "Mean_" + self.configReader.config.get(
                    "Export", "Export_File_1_data"), "w") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=";", lineterminator="\n")
                writer.writerows(self.meanData1Red)
        elif linesToPlot == "2":
            with open("Results\\" + "Mean_" + self.configReader.config.get(
                    "Export", "Export_File_2_data"), "w") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=";", lineterminator="\n")
                writer.writerows(self.meanData2Red)
        else:
            with open("Results\\" + "Mean_" + self.configReader.config.get(
                    "Export", "Export_File_1_data"), "w") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=";", lineterminator="\n")
                writer.writerows(self.meanData1Red)
            with open("Results\\" + "Mean_" + self.configReader.config.get(
                    "Export", "Export_File_2_data"), "w") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=";", lineterminator="\n")
                writer.writerows(self.meanData2Red)

    def appendDataCSVFilesMean(self, axisList, dataFileNumber, sensor):
        # Neuen Fühler an Export-Datei mit gemittelten Zeitreihen anhängen

        # Zeile mit den Namen der Messfühler zu Beginn einfügen
        axisListNew = list(axisList)
        axisListNew[0] = axisListNew[0].tolist()
        axisListNew[1] = axisListNew[1].tolist()
        axisListNew[0].insert(0, "TIME")
        axisListNew[1].insert(
            0, self.sensorDict.getSensorByCol(sensor).originalName)
        axisListNew[0] = np.asarray(axisListNew[0])
        axisListNew[1] = np.asarray(axisListNew[1])

        # Prüfen, welche Datei gerade bearbeitet wird
        if dataFileNumber == "1":
            self.meanData1Red[0] = axisListNew[0]
            self.meanData1Red.append(axisListNew[1])
        elif dataFileNumber == "2":
            self.meanData2Red[0] = axisListNew[0]
            self.meanData2Red.append(axisListNew[1])

    def getData(self, dataNumber):
        # Getter-Methode, um das entsprechende Datenarray 
        # aus anderen Klassen aufzurufen
        if dataNumber == "1":
            return self.data1Red
        elif dataNumber == "2":
            return self.data2Red


# # Klasse: ExportResultTable
# Eine Anforderung an die Software ist es, die resultierenden Ergebnisse aus den verschiedenen Vergleichs-Operationen (wie z. B. dem PEAK-Vergleich) extern zu speichern. Zum einen sollen die dargestellten Diagramme als Bilddateien gespeichert, aber auch die damit verbundenen berechneten Daten exportiert werden. Die Aufgabe der Klasse "ExportResultTable" ist die Vorhaltung dieser Daten als strukturierte Tabelle. Auf diese Weise können die Daten leicht und schnell zu einem beliebigen Zeitpunkt im Programmablauf gespeichert oder dargestellt werden.
# 
# Die Verwendung der Tabelle erfolgt bei dem Export der Ergebnisse als ".csv"-Datei und am Ende bei der automatischen Erzeugung des PDF-Anhangs. Die Tabelle wird mit den Ergebnissen der verschiedenen Messfühler-Vergleiche gefüllt, sobald diese berechnet werden. Das Anhängen von neuen Ergebnissen erfolgt über die verschiedenen "append"-Methoden der Klasse.

# In[46]:


class ExportResultTable:
    configReader = ConfigReader
    sensorNames = []
    data = []
    index = 1
    organisation = "nA"
    series = "nA"
    test = "nA"
    number = "nA"
    version = "nA"

    def __init__(self, configReader):
        self.configReader = configReader
        self.organisation = self.configReader.config.get(
            "Names", "Title_Organisation")
        self.series = self.configReader.config.get("Names", "Title_Series")
        self.test = self.configReader.config.get("Names", "Title_Test")
        self.number = self.configReader.config.get("Names", "Title_Number")
        self.version = self.configReader.config.get("Names", "Title_Version")
        self.data = []
        self.sensorNames = []
        self.data.append([
            "#", "Org.", "Serie", "Test", "Nr.", "Version", "Messfühler", "PEAK",
            "PEACOCK", "Median_" + self.configReader.config.get(
                "Names", "Title_File_1_short"), "Median_" +
            self.configReader.config.get("Names", "Title_File_2_short")
        ])

    def __getIndex__(self, sensorName):
        if sensorName in self.sensorNames:
            # Sensor befindet sich bereits im Dictionary
            return self.sensorNames.index(sensorName) + 1
        else:
            # Sensor befindet sich noch nicht im Dictionary
            self.sensorNames.append(sensorName)
            # Die letzten vier Parameter sind Platzhalter für: 
            # PEAK, PEACOCK, Median1, Median2
            self.data.append([
                self.index, self.organisation, self.series, self.test,
                self.number, self.version, sensorName, "nA", "nA", "nA", "nA"
            ])
            self.index += 1
            return self.index - 1

    def appendPeak(self, sensorName, peak):
        dataIndex = self.__getIndex__(sensorName)
        self.data[dataIndex][7] = round(peak, 2)

    def appendPeacock(self, sensorName, peacock):
        dataIndex = self.__getIndex__(sensorName)
        self.data[dataIndex][8] = round(peacock, 2)

    def appendMedian(self, sensorName, timeline1, timeline2):
        dataIndex = self.__getIndex__(sensorName)
        median1 = statistics.median(timeline1)
        median2 = statistics.median(timeline2)
        self.data[dataIndex][9] = round(median1, 2)
        self.data[dataIndex][10] = round(median2, 2)

    def isEmpty(self):
        # Prüfen, ob bereits Daten zur Speicherung vorhanden sind
        if len(self.data) == 1:
            return True
        else:
            return False

    def exportData(self):
        if self.isEmpty() == False:
            # Prüfen, ob der Pfad "Results" im Ordner bereits existiert
            if not os.path.exists("Results\\"):
                # Pfad "Results" neu anlegen
                os.makedirs("Results\\")

            # Datei öffnen, füllen und anschließend wieder schließen
            with open("Results\\" + self.configReader.config.get(
                    "Export", "Export_File_Results"), "w") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=";", lineterminator="\n")
                writer.writerows(self.data)
                csvfile.close()


# # Klasse: UserInterface
# Die Klasse "UserInterface" bietet selbst keine interne Logik zur Berechnung oder Verarbeitung von Daten. Sie dient in erster Linie dazu die Benutzereingaben zu verwalten und intern vorzuhalten. Auf diese wird dann im weiteren Verlauf von anderen Modulen zugegriffen.
# 
# Sollte sich der Benutzer für eine Steuerung der Anwendung über die Konsole entschieden haben, wird diese ebenfalls über die Klasse "UserInterface" koordiniert. Sie fordert den Benutzer hintereinander zu verschiedenen Eingaben auf (wie z. B. die Eingabe der Messfühler-Auswahl) und speichert sie intern ab. Des Weiteren verarbeitet sie die eingegebenen Parameter und setzt in deren Abhängigkeit Variablen für die weitere Verarbeitung. Auf diese Weise wird beispielsweise die Variable "processBothDatas" auf "Wahr" gesetzt, sollte sich der Benutzer für einen Vergleich von zwei Dateien entschieden haben. Dies ist dann wiederum für die korrekte Ansteuerung der Vergleichs-Operationen in anderen Modulen wichtig.

# In[47]:


class UserInterface:
    # Festlegung, Daten welcher Datei (1., 2. oder beide) 
    # verarbeitet werden sollen
    linesToPlot = "xxx"
    # Festlegung der Vergleichsart (Zeitreihe, Boxplot, ...)
    plotType = "Zeitreihe"
    # Liste der ausgewählten Messfühler
    sensors = []
    # Flag zur schnelleren Abfrage der Dateianzahl
    processBothDatas = False
    # Dictionary aller verfügbaren Messfühler
    sensorDict = SensorDictionary

    def __init__(self, sensorDict):
        self.sensorDict = sensorDict

    def startInput(self):
        # Auflistung der zum Vergleich verfügbaren Sensoren
        self.__displaySensorsForUser__()
        # Abfrage des Benutzers starten
        self.__inputDataFileNumber__()
        self.__inputSensor__()
        self.__inputPlotType__()

    def __displaySensorsForUser__(self):
        # Sensoren nach Untersuchungsgrößen sortieren und auflisten
        self.sensorDict.listAllSensorsSortedByGroup()

    def __inputDataFileNumber__(self):
        # Abfrage welche Dateien eingelesen und verarbeitet werden 
        # sollen (1.,2. oder beide Dateien)
        self.linesToPlot = input(
            str("Datei-Index eingeben:\n1: 1. Datei (ggf. Refere"
            + "nzwert-Datei)\n2: 2. Datei (ggf. Simulations-Datei"
            + ")\n3: Vergleich beider Dateien\n")).lower()
        # Kleines "Easteregg"
        if self.linesToPlot.lower() == "wer":
            print(
                "\n-------------------------------------------------")
            print(
                "\nErstellt von:\nMarcel Aurich, 2017\n\nBetreut von"
                + ":\nDr.-Ing. Dipl.-Phys. Olaf Riese\nDr.-Ing. Matt"
                + "hias Siemon\n\nVielen Dank für die tolle Aufgabe"
                + " und Arbeit!"
            )
            print(
                "\n-------------------------------------------------")
        self.__setDataFiles__()

    def __setDataFiles__(self):
        # Prüfen, ob die Dateien verglichen werden sollen
        if self.linesToPlot != "1" and self.linesToPlot != "2":
            self.processBothDatas = True
        else:
            self.processBothDatas = False

    def __inputSensor__(self):
        # Abfrage welche Sensoren (Messfühler) verarbeitet werden sollen
        selectedSensor = input("Messfühler oder Gruppe eingeben:\n")
        self.__setSensors__(selectedSensor)

    def __setSensors__(self, selectedSensor):
        # Sensor-Liste zurücksetzen
        self.sensors = []
        # Alle verfügbaren Messfühler plotten
        if selectedSensor == "all":
            for group in self.sensorDict.sensorGroupNames:
                for sensor in self.sensorDict.getSensorsByGroup(group):
                    self.sensors.append(sensor.col)
        else:
            # Plotten von ausgewählten Sensoren oder/und ganzen Messgruppen
            sensorSplit = selectedSensor.split(",")
            for sensorX in sensorSplit:
                # Eingabe über Gruppenkürzel, z.B. "TG,P,V"
                if sensorX in self.sensorDict.sensorGroupNames:
                    for sensor in self.sensorDict.getSensorsByGroup(sensorX):
                        self.sensors.append(sensor.col)
                # Eingabe über den ganzen oder Teilnamen des Sensors
                else:
                    for sensor in self.sensorDict.sensorList:
                        if sensorX in sensor.originalName:
                            self.sensors.append(sensor.col)

        if len(self.sensors) == 0:
            print("\nEs wurden keine Sensoren gefunden für:", selectedSensor)
            print("\nMögliche Eingabe z.B.:",
                  self.sensorDict.sensorList[0].originalName)
            self.__setSensors__(self.sensorDict.sensorList[0].originalName)

    def setInputParams(self, selectedSensor, dataFileNumber):
        self.linesToPlot = dataFileNumber
        self.__setDataFiles__()
        self.__setSensors__(selectedSensor)

    def __inputPlotType__(self):
        # Abfrage, der Verarbeitungsart der Daten
        selectedPlotType = input(
            "Auswahl Verfahren:\n1: Verteilung der Messgrößen\n2:"
            + " Zeitreihe(n)\n3: Gemittelte Zeitreihe(n)\n4: Normal"
            + "er/Gemittelter Zeitreihen Vergleich\n5: Gemittelte Z"
            + "eitreihe(n) mit Peak\n6: Boxplot der Zeitreihen\n7: "
            + "PEAK-PEAK\n8: PEAK-PEACOCK\n"
        ).lower()
        if selectedPlotType == "2":
            self.plotType = "Zeitreihe"
        elif selectedPlotType == "3":
            self.plotType = "Zeitreihe gemittelt"
        elif selectedPlotType == "4":
            self.plotType = "Zeitreihen Vergleich"
        elif selectedPlotType == "5":
            self.plotType = "Zeitreihen Peak"
        elif selectedPlotType == "6":
            self.plotType = "Boxplot Zeitreihen"
        elif selectedPlotType == "7":
            self.plotType = "Peak-Peak"
        elif selectedPlotType == "8":
            self.plotType = "PEAK-PEACOCK"
        else:
            self.plotType = "Verteilung"


# # Klasse: PDFAttachment
# Die Klasse "PDFAttachment" dient der automatischen Generierung des PDF-Anhangs, in dem eine Zusammenfassung, übersichtliche Strukturierung und Aufbereitung aller Ergebnisse erfolgt. Diese werden zudem nicht nur als Zahlen, sondern vor allem auch grafisch präsentiert. Die grafische Präsentation stellt den Hauptanteil des PDF-Anhangs und ist bewusst sehr umfangreich gehalten, damit der Benutzer eine qualifizierte Aussage über die Qualität der Daten treffen kann. In Abhängigkeit der gewählten Operationen, kann auf diese Weise für jeden Messfühler und jede Operation ein eigenes Diagramm  dargestellt werden. Genauere Informationen zur grafischen Darstellung der Ergebnisse werden über der Klasse "PlotResults" beschrieben.
# 
# Vor der Präsentation der Ergebnisse werden auf den ersten Seiten des PDF-Anhangs die unterschiedlichen Randbedingungen der Validierung dargestellt. Diese werden zum Großteil direkt aus der Konfigurationsdatei eingelesen und umfassen:
# 
# - die Projektbezeichnung
# - eine Auflistung der verarbeiteten Datensätze und der zugehörigen Dateien
# - Informationen zu den Daten (wie z. B. die zuständige Organisation für die Daten)
# - die Darstellung des maßgeblichen Zeitraums (dieser wird aus den eingelesenen Daten ermittelt)
# - die durchgeführten Operationen (wie z. B. ein gemittelter Zeitreihen-Vergleich)
# 
# Des Weiteren enthält der PDF-Anhang eine Kopf- und Fußzeile, die ebenfalls über die Klasse "PDFAttachment" gesteuert werden. Die Kopfzeile umfasst den Projektnamen und das Logo des Instituts für Baustoffe, Massivbau und Brandschutz. Die Fußzeile besteht aus der aktuellen Seitenzahl im Bezug zu der Gesamtzahl der Seiten.

# In[48]:


class PDFAttachment(FPDF):
    configReader = ConfigReader
    sensorDict = SensorDictionary
    resultDictPeak = dict()
    resultDictPeacock = dict()
    resultDictPeakPeacock = dict()
    spacing = 7

    def setParams(self, configReader, sensorDict):
        self.configReader = configReader
        self.sensorDict = sensorDict
        self.resultDictPeak = dict()
        self.resultDictPeacock = dict()
        self.resultDictPeakPeacock = dict()
        self.set_title(self.configReader.config.get("Names", "Title_Project"))
        self.set_author(self.configReader.config.get("Names", "Title_Author"))
        self.alias_nb_pages()
        self.set_left_margin(22)

        # Erste Seite des PDF-Anhangs mit allgemeinen Informationen füllen
        self.add_page()
        self.printNewGroup("Allgemeines")
        self.ln(3)
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Projektbezeichnung:", 0, 1)
        self.set_font("Arial", "", 15)
        self.cell(0, self.spacing,
                  self.configReader.config.get("Names", "Title_Project"), 0, 1)
        self.ln(3)
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Verwendete Daten:", 0, 1)
        self.set_font("Arial", "", 15)
        self.cell(0, self.spacing, "1. Datei: " + self.configReader.config.get(
            "Import", "Import_File_1"), 0, 1)
        self.cell(0, self.spacing,
                  "Bezeichnung: " + self.configReader.config.get(
                      "Names", "Title_File_1"), 0, 1)
        self.cell(0, self.spacing,
                  "Kurzbezeichnung: " + self.configReader.config.get(
                      "Names", "Title_File_1_short"), 0, 1)
        self.ln(3)
        self.cell(0, self.spacing, "2. Datei: " + self.configReader.config.get(
            "Import", "Import_File_2"), 0, 1)
        self.cell(0, self.spacing,
                  "Bezeichnung: " + self.configReader.config.get(
                      "Names", "Title_File_2"), 0, 1)
        self.cell(0, self.spacing,
                  "Kurzbezeichnung: " + self.configReader.config.get(
                      "Names", "Title_File_2_short"), 0, 1)
        self.ln(3)
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Informationen zu den Daten:", 0, 1)
        self.set_font("Arial", "", 15)
        self.cell(0, self.spacing,
                  "Zuständige Organisation: " + self.configReader.config.get(
                      "Names", "Title_Organisation"), 0, 1)
        self.cell(
            0, self.spacing,
            "Serie: " + self.configReader.config.get("Names", "Title_Series"),
            0, 1)
        self.cell(
            0, self.spacing,
            "Test: " + self.configReader.config.get("Names", "Title_Test"), 0,
            1)
        self.cell(
            0, self.spacing,
            "Nummer: " + self.configReader.config.get("Names", "Title_Number"),
            0, 1)
        self.cell(
            0, self.spacing,
            "Version: " + self.configReader.config.get("Names", "Title_Version"),
            0, 1)
        self.ln(3)

    def printMaxTime(self, maxTime):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Maßgeblicher Zeitraum für die Validierung:", 0, 1)
        self.set_font("Arial", "", 15)
        self.cell(0, self.spacing, str(maxTime) + " Sekunden", 0, 1)
        self.ln(3)

    def printOperations(self):
        # Durchgeführte Operationen auflisten
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Durchgeführte Operationen:", 0, 1)
        self.set_font("Arial", "", 15)
        operationCounter = 1
        if self.configReader.config.get("Control", "Plot_Frequency") == "1":
            self.cell(
                0, self.spacing,
                str(operationCounter) + ". " + self.configReader.config.get(
                    "Names", "Title_Frequency"), 0, 1)
            operationCounter += 1
        if self.configReader.config.get("Control", "Plot_Timeline") == "1":
            self.cell(
                0, self.spacing,
                str(operationCounter) + ". " + self.configReader.config.get(
                    "Names", "Title_Timeline"), 0, 1)
            operationCounter += 1
        if self.configReader.config.get("Control",
                                        "Plot_Mean_Timeline") == "1":
            self.cell(
                0, self.spacing,
                str(operationCounter) + ". " + self.configReader.config.get(
                    "Names", "Title_Mean_Timeline"), 0, 1)
            operationCounter += 1
        if self.configReader.config.get("Control",
                                        "Plot_Timeline_Comparison") == "1":
            self.cell(
                0, self.spacing,
                str(operationCounter) + ". " + self.configReader.config.get(
                    "Names", "Title_Timeline_Comparison"), 0, 1)
            operationCounter += 1
        if self.configReader.config.get("Control",
                                        "Plot_Timeline_Peak") == "1":
            self.cell(
                0, self.spacing,
                str(operationCounter) + ". " + self.configReader.config.get(
                    "Names", "Title_Timeline_Peak"), 0, 1)
            operationCounter += 1
        if self.configReader.config.get("Control", "Plot_PEAK_PEAK") == "1":
            self.cell(
                0, self.spacing,
                str(operationCounter) + ". " + self.configReader.config.get(
                    "Names", "Title_PEAK_PEAK"), 0, 1)
            operationCounter += 1
        if self.configReader.config.get("Control", "Plot_PEAK_PEACOCK") == "1":
            self.cell(
                0, self.spacing,
                str(operationCounter) + ". " + self.configReader.config.get(
                    "Names", "Title_PEAK_PEACOCK"), 0, 1)
            operationCounter += 1
        if self.configReader.config.get("Control",
                                        "Plot_Timeline_Boxplot") == "1":
            self.cell(
                0, self.spacing,
                str(operationCounter) + ". " + self.configReader.config.get(
                    "Names", "Title_Timeline_Boxplot"), 0, 1)
            operationCounter += 1

    def printSensorList(self, sensors):
        self.add_page()
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Auflistung der untersuchten Messfühler", 0, 1)

        lastGroup = self.sensorDict.getSensorByCol(sensors[0]).group
        self.set_font("Arial", "B", 12)
        self.cell(1, 5,
                  self.sensorDict.sensorGroupNames.get(lastGroup) + " (" +
                  lastGroup + ") - Messfühler:", 0, 1)
        self.set_font("Arial", "", 12)
        for sensor in sensors:
            group = self.sensorDict.getSensorByCol(sensor).group
            if lastGroup != group:
                self.ln(3)
                self.set_font("Arial", "B", 12)
                self.cell(1, 5,
                          self.sensorDict.sensorGroupNames.get(group) + " (" +
                          group + ") - Messfühler:", 0, 1)
                self.set_font("Arial", "", 12)
            lastGroup = group
            self.cell(1, 5,
                      self.sensorDict.getSensorByCol(sensor).originalName, 0,
                      1)

    def printPeakPeacock(self):
        self.add_page()
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Ergebnisse der PEAKS und PEACOCKS:", 0, 1)
        self.set_font("Arial", "", 15)
        for group in self.resultDictPeak:
            self.cell(
                0, self.spacing,
                self.sensorDict.sensorGroupNames[group] + " - " + group + ":",
                0, 1)
            self.cell(0, self.spacing,
                      str(round(self.resultDictPeak.get(group), 1)) +
                      "% der PEAKS liegen im Vertrauensbereich", 0, 1)
            self.cell(0, self.spacing,
                      str(round(self.resultDictPeacock.get(group), 1)) +
                      "% der PEACOCKS liegen im Vertrauensbereich", 0, 1)
            self.cell(0, self.spacing,
                      str(round(self.resultDictPeakPeacock.get(group), 1)) +
                      "% der PEAK/PEACOCKS liegen im Vertrauensbereich", 0, 1)
            self.ln(3)

    def header(self):
        # Logo setzen
        self.image("Logo_iBMB.png", 172, 8, 25)
        # Schriftart setzen
        self.set_font("Arial", "B", 15)
        # Titel setzen
        self.cell(80)
        self.cell(30, 10,
                  self.configReader.config.get("Names", "Title_Project"), 0, 1,
                  "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        # Schriftart setzen
        self.set_font("Arial", "", 10)
        # Seitenzahl darstellen
        self.cell(0, 10, str(self.page_no()) + "/{nb}", 0, 0, "C")

    def printNewGroup(self, title):
        if (int(self.get_y()) > 240):
            self.add_page()
        # Schriftart setzen
        self.set_font("Arial", "", 12)
        # Kapitel schreiben
        self.set_fill_color(200, 220, 255)
        self.cell(175, 6, title, 0, 1, "L", 1)
        self.ln(1)

    def printResultTable(self, resultTable):
        # Ergebnis-Tabelle an PDF-Anhang anhängen
        self.add_page()
        self.printNewGroup("Messfühler Tabelle")
        self.ln(5)

        # Spalten-Breiten bestimmen
        widthList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for row in resultTable.data:
            for var in range(len(row)):
                widthVar = self.get_string_width(str(row[var]))
                if widthVar > widthList[var]:
                    widthList[var] = widthVar - 1 

        # Kopf-Zeile schreiben
        self.set_font("Arial", "B", 8)
        for var in range(len(resultTable.data[0])):
            if var == 6:
                width = widthList[var]
            else:
                width = widthList[var] + 1
            self.cell(width, 5, str(resultTable.data[0][var]), 0, 0, "", 0)
        self.ln(6)

        self.line(22, 42, 197, 42)

        # Ergebnisse/Fühler schreiben
        self.set_font("Arial", "", 8)
        for row in resultTable.data[1:]:
            for var in range(len(row)):
                if var == 6:
                    width = widthList[var]
                else:
                    width = widthList[var] + 1
                self.cell(width, 5, str(row[var]), 0, 0, "", 0)
            self.ln(5)


# # Klasse: PlotResults
# Die Klasse "PlotResults" ist zusammen mit der Klasse "ProcessData" die umfangreichste aller Klassen. "PlotResults" dient der grafischen Präsentation der Daten und berechneten Ergebnisse. Für die Darstellung von Diagrammen wird die Bibliothek "matplotlib" verwendet, die über die Variable "plot" angesprochen wird. Die Klasse verfügt über allgemeine Methoden, um beispielsweise in Abhängigkeit der Untersuchungsgröße die Beschriftung der Y-Achse von Zeitreihen zu ermitteln und über spezifische Methoden zur individuellen Darstellung der Ergebnisse der jeweiligen Vergleichs-Operation.
# 
# Jede Vergleichs-Operation verfügt über eine eigene Methode, die jeweils mit "plot" beginnen (z. B. "plotTimeline"). Zu Beginn wird der Umfang der Darstellung bestimmt. Dazu werden die zu untersuchenden Messfühler anhand ihrer Untersuchungsgröße unterteilt und die benötigte Anzahl an Diagrammen bestimmt. Zur Begrenzung der Länge des PDF-Anhangs und zur besseren Lesbarkeit und Vergleichbarkeit der Visualisierungen, werden diese in Abhängigkeit der Vergleichs-Operation in unterschiedlicher Größe dargestellt. Die Zeitreihen-Operationen (z. B. der gemittelte Zeitreihen-Vergleich) benötigen je Messfühler ein eigenes Diagramm und verfügen aus diesem Grund über eine weit größere Anzahl, als beispielsweise der PEAK-Vergleich, bei dem lediglich je Untersuchungsgröße ein Diagramm benötigt wird. Aus diesem Grund werden bei Zeitreihen-Operationen die Diagramme verkleinert und jeweils zu dritt nebeneinander dargestellt. Zu Beginn wird dazu die benötigte "Zeilen"-Anzahl an Diagrammen berechnet.
# 
# Im nächsten Schritt der Routinen findet eine Iteration über die ausgewählten Messfühler statt. Es werden die je nach gewählter Vergleichs-Operation benötigten Berechnungsmethoden der Klasse "ProcessData" aufgerufen und die resultierenden Ergebnisse dargestellt. Weitere Details zu den Berechnungsmethoden werden über der Klasse "ProcessData" erläutert. Je nach Darstellungsform werden Punkte (PEAK-Vergleich), Linien (Zeitreihen-Vergleiche) oder auch Boxplots dargestellt. Abhängig von der Darstellungsform werden im Anschluss noch weitere Einstellungen, wie die Achsenbeschriftung, die Überschrift, ein Hintergrundraster oder eine Legende festgelegt.
# 
# Am Ende jeder "plot"-Methode wird die Methode "plotShow" aufgerufen, um die Darstellung zu finalisieren und dem Benutzer anzuzeigen. Des Weiteren fügt sie das Diagramm, sollte es der Benutzer in der Konfigurationsdatei eingestellt haben, dem PDF-Anhang bei und exportiert es als externe Bilddatei in den Unterordner "Plots" im Hauptordner. Sollte dieser nicht vorhanden sein, wird er vorher automatisch erstellt. Die Auflösung kann dabei ebenfalls frei eingestellt werden und wird in "dpi" - "density per inch" gemessen. An dieser Stelle sei darauf hingewiesen, dass sich mit steigender Auflösung auch die Laufzeit erhöht, da für die Erstellung der Grafik mehr Rechenaufwand benötigt wird. Der Name der jeweiligen Bilddatei wird, in Abhängigkeit der gewählten Vergleichs-Operation und der jeweiligen Untersuchungsgröße des betrachteten Messfühlers, automatisch bestimmt durch die Methode "generateFileNameForPlotFile".

# In[49]:


class PlotResults:
    configReader = ConfigReader
    sensorDict = SensorDictionary
    ui = UserInterface
    pdf = PDFAttachment

    def __init__(self, configReader, sensorDict, ui, pdf):
        self.configReader = configReader
        self.sensorDict = sensorDict
        self.ui = ui
        self.pdf = pdf

    def getYAxisLabelSingle(self, col):
        group = self.sensorDict.getSensorByCol(col).group
        ylabel = self.sensorDict.sensorGroupNames.get(
            group) + " [" + self.sensorDict.sensorGroupUnits.get(group) + "]"
        return ylabel

    def getYAxisLabel(self, cols):
        # Y-Achsenbeschriftung ermitteln und darstellen
        differentSensorGroups = False
        lastSensorGroup = self.sensorDict.getSensorByCol(cols[0]).group

        for col in cols:
            # Prüfen, ob Sensoren mit verschiedenen 
            # Untersuchungsgrößen geplottet werden
            if lastSensorGroup != self.sensorDict.getSensorByCol(col).group:
                differentSensorGroups = True
                break
            lastSensorGroup = self.sensorDict.getSensorByCol(col).group

        # Y-Achsenbeschriftung (Einheit) setzen
        ylabel = "Verschiedene Einheiten"
        if differentSensorGroups == False:
            ylabel = self.sensorDict.sensorGroupNames.get(
                lastSensorGroup) + " [" + self.sensorDict.sensorGroupUnits.get(
                    lastSensorGroup) + "]"

        return ylabel

    def __generateFileNameForPlotFile__(self, plotType, cols):
        # Dateinamen für externe Bilddatei des Plots ermitteln
        namePlot = ""
        if len(cols) == 1:
            # Wenn nur ein Sensor geplottet wird, wird dessen Name 
            # für den Dateinamen verwendet
            namePlot = "Plot_" + plotType + "_" +                 self.sensorDict.getSensorByCol(cols[0]).originalName
        else:
            # Werden mehrere Sensoren gleichzeitig geplottet, werden 
            # deren Untersuchungsgrößen für den Dateinamen verwendet
            namePlot = "Plot_" + plotType
            alreadyExists = []
            for col in cols:
                group = self.sensorDict.getSensorByCol(col).group
                # Sicherstellen, dass die gleiche Untersuchungsgröße 
                # nicht mehrmals angehängt wird an den Dateinamen
                if group not in alreadyExists:
                    namePlot = namePlot + "_" + group
                    alreadyExists.append(group)

        return namePlot

    def plotTimeline(self, axisList, timeline):
        # Anzahl der Sub-Plots pro Zeile in der Plot-Ausgabe
        maxNoPlotCols = 3
        # Anzahl der Zeilen pro Plotdatei
        maxNoPlots = 1
        # Anzahl der zu plottenden Sensoren auslesen
        noSensors = len(self.ui.sensors)
        # Bezeichnungen der Daten auslesen
        label1 = self.configReader.config.get("Names", "Title_File_1_short")
        label2 = self.configReader.config.get("Names", "Title_File_2_short")

        # Anzahl der Spalten des Plots bestimmen
        noPlotCols = 0
        if noSensors < maxNoPlotCols:
            noPlotCols = noSensors
        else:
            noPlotCols = maxNoPlotCols

        # Anzahl der Zeilen des Plots bestimmen
        noPlotRows = 1
        counter = 0
        lastGroup = self.sensorDict.getSensorByCol(self.ui.sensors[0]).group
        for sensor in range(noSensors):
            newGroup = self.sensorDict.getSensorByCol(
                self.ui.sensors[sensor]).group
            if newGroup != lastGroup:
                noPlotRows += 1
                counter = 1
            else:
                counter += 1
                if counter > maxNoPlotCols:
                    noPlotRows += 1
                    counter = 1
            lastGroup = self.sensorDict.getSensorByCol(
                self.ui.sensors[sensor]).group

        # Anzahl der Hauptplots bestimmen
        noPlots = math.ceil(noPlotRows / maxNoPlots)

        # PDF-Anhang Seite hinzufügen
        self.pdf.add_page()

        # Iteration beginnen
        counterPlot = 0
        remainingPlotRows = noPlotRows
        axisCounter = 0
        counterSubPlots = 0
        sensor = self.ui.sensors[counterSubPlots]
        lastGroup1 = ""
        for plotNumber in range(noPlots):
            # Plot anlegen
            fig, ax = plot.subplots(
                nrows=min(remainingPlotRows, maxNoPlots),
                ncols=noPlotCols,
                facecolor="white",
                figsize=(8, 2.5 * min(remainingPlotRows, maxNoPlots)))

            counterCell = 0

            # Überschriften in PDF-Anhang schreiben
            sensor = self.ui.sensors[counterSubPlots]
            newGroup1 = self.sensorDict.getSensorByCol(sensor).group
            if lastGroup1 != newGroup1:
                lastGroup1 = self.sensorDict.getSensorByCol(sensor).group
                sensorGroupName = self.sensorDict.sensorGroupNames.get(
                    self.sensorDict.getSensorByCol(sensor).group)
                if timeline == "mean":
                    self.pdf.printNewGroup(
                        self.configReader.config.get(
                            "Names", "Title_Mean_Timeline") + " - " +
                        sensorGroupName)
                else:
                    self.pdf.printNewGroup(
                        self.configReader.config.get("Names", "Title_Timeline")
                        + " - " + sensorGroupName)

            while counterSubPlots < len(
                    self.ui.sensors
            ) and counterCell < maxNoPlotCols * maxNoPlots:
                # Auf neue Sensorgruppe prüfen (ggf. neuer Sub-Plot)
                lastGroup = self.sensorDict.getSensorByCol(sensor).group
                sensor = self.ui.sensors[counterSubPlots]
                newGroup = self.sensorDict.getSensorByCol(sensor).group
                if lastGroup != newGroup:
                    break

                # Bestimmen, welcher Sub-Plot gefüllen werden soll
                tempX = math.floor(counterCell / noPlotCols)
                tempY = counterCell % noPlotCols

                # Fallunterscheidung
                if min(remainingPlotRows, maxNoPlots) == 1 and noPlotCols == 1:
                    # Plotten von nur einem Sensor
                    ax.plot(
                        axisList[axisCounter][0],
                        axisList[axisCounter][1],
                        "-",
                        label=label1,
                        linewidth=1.0)
                elif min(remainingPlotRows, maxNoPlots) == 1:
                    # Plotten von weniger Sensoren
                    # als maximal zulässig pro Zeile
                    ax[tempY].plot(
                        axisList[axisCounter][0],
                        axisList[axisCounter][1],
                        "-",
                        label=label1,
                        linewidth=1.0)
                else:
                    # Plotten von mehreren Zeilen und Spalten an Sub-Plots
                    ax[tempX, tempY].plot(
                        axisList[axisCounter][0],
                        axisList[axisCounter][1],
                        "-",
                        label=label1,
                        linewidth=1.0)
                axisCounter += 1

                if self.ui.processBothDatas == True:
                    # Es werden Simulations- und Referenzdaten verglichen
                    if min(remainingPlotRows,
                           maxNoPlots) == 1 and noPlotCols == 1:
                        ax.plot(
                            axisList[axisCounter][0],
                            axisList[axisCounter][1],
                            "--",
                            label=label2,
                            linewidth=1.0)
                    elif min(remainingPlotRows, maxNoPlots) == 1:
                        ax[tempY].plot(
                            axisList[axisCounter][0],
                            axisList[axisCounter][1],
                            "--",
                            label=label2,
                            linewidth=1.0)
                    else:
                        ax[tempX, tempY].plot(
                            axisList[axisCounter][0],
                            axisList[axisCounter][1],
                            "--",
                            label=label2,
                            linewidth=1.0)
                    axisCounter += 1

                # Setzen von allgemeinen Parametern (erneut Fallunterscheidung)
                if min(remainingPlotRows, maxNoPlots) == 1 and noPlotCols == 1:
                    # Titel des Sub-Plots setzen
                    ax.set_title(
                        self.ui.sensorDict.getSensorByCol(sensor).originalName)
                    # Legende einblenden
                    ax.legend(loc=0)
                    # Raster einblenden im Hintergrund
                    ax.grid(True)
                    # Achsenbeschriftungen setzen
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax.set_xlabel("Zeit [s]")
                    if tempY == 0:
                        ax.set_ylabel(self.getYAxisLabelSingle(sensor))
                elif min(remainingPlotRows, maxNoPlots) == 1:
                    ax[tempY].set_title(
                        self.sensorDict.getSensorByCol(sensor).originalName)
                    ax[tempY].legend(loc=0)
                    ax[tempY].grid(True)
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax[tempY].set_xlabel("Zeit [s]")
                    if tempY == 0:
                        ax[tempY].set_ylabel(self.getYAxisLabelSingle(sensor))
                else:
                    ax[tempX, tempY].set_title(
                        self.sensorDict.getSensorByCol(sensor).originalName)
                    ax[tempX, tempY].legend(loc=0)
                    ax[tempX, tempY].grid(True)
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax[tempX, tempY].set_xlabel("Zeit [s]")
                    if tempY == 0:
                        ax[tempX, tempY].set_ylabel(
                            self.getYAxisLabelSingle(sensor))

                counterCell += 1
                counterSubPlots += 1

            counterPlot += 1
            remainingPlotRows -= min(remainingPlotRows, maxNoPlots)
            # Plot darstellen
            fig.tight_layout()
            if timeline == "mean":
                self.plotShow(
                    self.configReader.config.get("Names",
                                                 "Title_Mean_Timeline") +
                    " " + self.sensorDict.getSensorByCol(
                        self.ui.sensors[counterSubPlots - 1]).group + " " +
                    str(counterPlot))
            else:
                self.plotShow(
                    self.configReader.config.get("Names", "Title_Timeline") +
                    " " + self.sensorDict.getSensorByCol(
                        self.ui.sensors[counterSubPlots - 1]).group + " " +
                    str(counterPlot))

    def plotTimelineComparison(self, axisList, axisListMean):
        # Anzahl der Sub-Plots pro Zeile in der Plot-Ausgabe
        maxNoPlotCols = 3
        # Anzahl der Zeilen pro Plotdatei
        maxNoPlots = 1
        # Anzahl der zu plottenden Sensoren auslesen
        noSensors = len(self.ui.sensors)
        # Bezeichnungen der Daten auslesen
        label1 = self.configReader.config.get("Names", "Title_File_1_short")
        label2 = self.configReader.config.get("Names", "Title_File_2_short")

        # Anzahl der Spalten des Plots bestimmen
        noPlotCols = 0
        if noSensors < maxNoPlotCols:
            noPlotCols = noSensors
        else:
            noPlotCols = maxNoPlotCols

        # Anzahl der Zeilen des Plots bestimmen
        noPlotRows = 1
        counter = 0
        lastGroup = self.sensorDict.getSensorByCol(self.ui.sensors[0]).group
        for sensor in range(noSensors):
            newGroup = self.sensorDict.getSensorByCol(
                self.ui.sensors[sensor]).group
            if newGroup != lastGroup:
                noPlotRows += 1
                counter = 1
            else:
                counter += 1
                if counter > maxNoPlotCols:
                    noPlotRows += 1
                    counter = 1
            lastGroup = self.sensorDict.getSensorByCol(
                self.ui.sensors[sensor]).group

        # Anzahl der Hauptplots bestimmen
        noPlots = math.ceil(noPlotRows / maxNoPlots)

        # PDF-Anhang Seite hinzufügen
        self.pdf.add_page()

        # Iteration beginnen
        counterPlot = 0
        remainingPlotRows = noPlotRows
        axisCounter = 0
        counterSubPlots = 0
        sensor = self.ui.sensors[counterSubPlots]
        lastGroup1 = ""
        for plotNumber in range(noPlots):
            # Plot anlegen
            fig, ax = plot.subplots(
                nrows=min(remainingPlotRows, maxNoPlots),
                ncols=noPlotCols,
                facecolor="white",
                figsize=(8, 2.5 * min(remainingPlotRows, maxNoPlots)))

            counterCell = 0
            # Überschriften in PDF-Anhang schreiben
            sensor = self.ui.sensors[counterSubPlots]
            newGroup1 = self.sensorDict.getSensorByCol(sensor).group
            if lastGroup1 != newGroup1:
                lastGroup1 = self.sensorDict.getSensorByCol(sensor).group
                sensorGroupName = self.sensorDict.sensorGroupNames.get(
                    self.sensorDict.getSensorByCol(sensor).group)
                self.pdf.printNewGroup(
                    self.configReader.config.get(
                        "Names", "Title_Timeline_Comparison") + " - " +
                    sensorGroupName)

            while counterSubPlots < len(
                    self.ui.sensors
            ) and counterCell < maxNoPlotCols * maxNoPlots:
                # Auf neue Sensorgruppe prüfen (ggf. neuer Sub-Plot)
                lastGroup = self.sensorDict.getSensorByCol(sensor).group
                sensor = self.ui.sensors[counterSubPlots]
                newGroup = self.sensorDict.getSensorByCol(sensor).group
                if lastGroup != newGroup:
                    break

                # Bestimmen, welcher Sub-Plot gefüllen werden soll
                tempX = math.floor(counterCell / noPlotCols)
                tempY = counterCell % noPlotCols

                # Fallunterscheidung
                if min(remainingPlotRows, maxNoPlots) == 1 and noPlotCols == 1:
                    # Plotten von nur einem Sensor
                    ax.plot(
                        axisList[axisCounter][0],
                        axisList[axisCounter][1],
                        "-",
                        label=label1,
                        linewidth=1.0)
                    ax.plot(
                        axisListMean[axisCounter][0],
                        axisListMean[axisCounter][1],
                        "-",
                        label=label1 + "_MEAN",
                        linewidth=1.0)
                elif min(remainingPlotRows, maxNoPlots) == 1:
                    # Plotten von weniger Sensoren, 
                    # als maximal zulässig pro Zeile
                    ax[tempY].plot(
                        axisList[axisCounter][0],
                        axisList[axisCounter][1],
                        "-",
                        label=label1,
                        linewidth=1.0)
                    ax[tempY].plot(
                        axisListMean[axisCounter][0],
                        axisListMean[axisCounter][1],
                        "-",
                        label=label1 + "_MEAN",
                        linewidth=1.0)
                else:
                    # Plotten von mehreren Zeilen und Spalten an Sub-Plots
                    ax[tempX, tempY].plot(
                        axisList[axisCounter][0],
                        axisList[axisCounter][1],
                        "-",
                        label=label1,
                        linewidth=1.0)
                    ax[tempX, tempY].plot(
                        axisListMean[axisCounter][0],
                        axisListMean[axisCounter][1],
                        "-",
                        label=label1 + "_MEAN",
                        linewidth=1.0)
                axisCounter += 1

                if self.ui.processBothDatas == True:
                    # Es werden Simulations- und Referenzdaten verglichen
                    if min(remainingPlotRows,
                           maxNoPlots) == 1 and noPlotCols == 1:
                        ax.plot(
                            axisList[axisCounter][0],
                            axisList[axisCounter][1],
                            "--",
                            label=label2,
                            linewidth=1.0)
                        ax.plot(
                            axisListMean[axisCounter][0],
                            axisListMean[axisCounter][1],
                            "--",
                            label=label2 + "_MEAN",
                            linewidth=1.0)
                    elif min(remainingPlotRows, maxNoPlots) == 1:
                        ax[tempY].plot(
                            axisList[axisCounter][0],
                            axisList[axisCounter][1],
                            "--",
                            label=label2,
                            linewidth=1.0)
                        ax[tempY].plot(
                            axisListMean[axisCounter][0],
                            axisListMean[axisCounter][1],
                            "--",
                            label=label2 + "_MEAN",
                            linewidth=1.0)
                    else:
                        ax[tempX, tempY].plot(
                            axisList[axisCounter][0],
                            axisList[axisCounter][1],
                            "--",
                            label=label2,
                            linewidth=1.0)
                        ax[tempX, tempY].plot(
                            axisListMean[axisCounter][0],
                            axisListMean[axisCounter][1],
                            "--",
                            label=label2 + "_MEAN",
                            linewidth=1.0)
                    axisCounter += 1

                # Setzen von allgemeinen Parametern (erneut Fallunterscheidung)
                if min(remainingPlotRows, maxNoPlots) == 1 and noPlotCols == 1:
                    # Titel des Sub-Plots setzen
                    ax.set_title(
                        self.ui.sensorDict.getSensorByCol(sensor).originalName)
                    # Legende einblenden
                    ax.legend(loc=0)
                    # Raster einblenden im Hintergrund
                    ax.grid(True)
                    # Achsenbeschriftungen setzen
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax.set_xlabel("Zeit [s]")
                    if tempY == 0:
                        ax.set_ylabel(self.getYAxisLabelSingle(sensor))
                elif min(remainingPlotRows, maxNoPlots) == 1:
                    ax[tempY].set_title(
                        self.sensorDict.getSensorByCol(sensor).originalName)
                    ax[tempY].legend(loc=0)
                    ax[tempY].grid(True)
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax[tempY].set_xlabel("Zeit [s]")
                    if tempY == 0:
                        ax[tempY].set_ylabel(self.getYAxisLabelSingle(sensor))
                else:
                    ax[tempX, tempY].set_title(
                        self.sensorDict.getSensorByCol(sensor).originalName)
                    ax[tempX, tempY].legend(loc=0)
                    ax[tempX, tempY].grid(True)
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax[tempX, tempY].set_xlabel("Zeit [s]")
                    if tempY == 0:
                        ax[tempX, tempY].set_ylabel(
                            self.getYAxisLabelSingle(sensor))

                counterCell += 1
                counterSubPlots += 1

            counterPlot += 1
            remainingPlotRows -= min(remainingPlotRows, maxNoPlots)
            # Plot darstellen
            fig.tight_layout()
            self.plotShow(
                self.configReader.config.get(
                    "Names", "Title_Timeline_Comparison") + " " +
                self.sensorDict.getSensorByCol(
                    self.ui.sensors[counterSubPlots - 1]).group + " " +
                str(counterPlot))

    def plotTimelinePeaks(self, axisList, peakList):
        # Anzahl der Sub-Plots pro Zeile in der Plot-Ausgabe
        maxNoPlotCols = 3
        # Anzahl der Sub-Plots pro Plotdatei
        maxNoPlots = 1
        # Anzahl der zu plottenden Sensoren auslesen
        noSensors = len(self.ui.sensors)
        # Bezeichnungen der Daten auslesen
        label1 = self.configReader.config.get("Names", "Title_File_1_short")
        label2 = self.configReader.config.get("Names", "Title_File_2_short")

        # Anzahl der Spalten des Plots bestimmen
        noPlotCols = 0
        if noSensors < maxNoPlotCols:
            noPlotCols = noSensors
        else:
            noPlotCols = maxNoPlotCols

        # Anzahl der Zeilen des Plots bestimmen
        noPlotRows = 1
        counter = 0
        lastGroup = self.sensorDict.getSensorByCol(self.ui.sensors[0]).group
        for sensor in range(noSensors):
            newGroup = self.sensorDict.getSensorByCol(
                self.ui.sensors[sensor]).group
            if newGroup != lastGroup:
                noPlotRows += 1
                counter = 1
            else:
                counter += 1
                if counter > maxNoPlotCols:
                    noPlotRows += 1
                    counter = 1
            lastGroup = self.sensorDict.getSensorByCol(
                self.ui.sensors[sensor]).group

        # Anzahl der Hauptplots bestimmen
        noPlots = math.ceil(noPlotRows / maxNoPlots)

        # PDF-Anhang Seite hinzufügen
        self.pdf.add_page()

        # Iteration beginnen
        counterPlot = 0
        remainingPlotRows = noPlotRows
        axisCounter = 0
        counterSubPlots = 0
        sensor = self.ui.sensors[counterSubPlots]
        lastGroup1 = ""
        for plotNumber in range(noPlots):
            # Plot anlegen
            fig, ax = plot.subplots(
                nrows=min(remainingPlotRows, maxNoPlots),
                ncols=noPlotCols,
                facecolor="white",
                figsize=(8, 2.5 * min(remainingPlotRows, maxNoPlots)))

            counterCell = 0
            # Überschriften in PDF-Anhang schreiben
            sensor = self.ui.sensors[counterSubPlots]
            newGroup1 = self.sensorDict.getSensorByCol(sensor).group
            if lastGroup1 != newGroup1:
                lastGroup1 = self.sensorDict.getSensorByCol(sensor).group
                sensorGroupName = self.sensorDict.sensorGroupNames.get(
                    self.sensorDict.getSensorByCol(sensor).group)
                self.pdf.printNewGroup(
                    self.configReader.config.get("Names", "Title_Timeline_Peak"
                                                 ) + " - " + sensorGroupName)

            while counterSubPlots < len(
                    self.ui.sensors
            ) and counterCell < maxNoPlotCols * maxNoPlots:
                # Auf neue Sensorgruppe prüfen (ggf. neuer Sub-Plot)
                lastGroup = self.sensorDict.getSensorByCol(sensor).group
                sensor = self.ui.sensors[counterSubPlots]
                newGroup = self.sensorDict.getSensorByCol(sensor).group
                if lastGroup != newGroup:
                    break

                # Bestimmen, welcher Sub-Plot gefüllen werden soll
                tempX = math.floor(counterCell / noPlotCols)
                tempY = counterCell % noPlotCols

                # Fallunterscheidung
                if min(remainingPlotRows, maxNoPlots) == 1 and noPlotCols == 1:
                    # Plotten von nur einem Sensor
                    ax.plot(
                        axisList[axisCounter][0],
                        axisList[axisCounter][1],
                        "-",
                        label=label1,
                        linewidth=1.0)
                    ax.plot(
                        axisList[axisCounter][0][peakList[axisCounter]],
                        axisList[axisCounter][1][peakList[axisCounter]],
                        'r.',
                        ms=5,
                        mew=2)
                    xyText = "(" + str(
                        int(axisList[axisCounter][0]
                            [peakList[axisCounter]])) + ", " + str(
                                int(axisList[axisCounter][1]
                                    [peakList[axisCounter]])) + ")"
                    ax.annotate(
                        xyText,
                        xy=(axisList[axisCounter][0][peakList[axisCounter]],
                            axisList[axisCounter][1][peakList[axisCounter]]))
                elif min(remainingPlotRows, maxNoPlots) == 1:
                    # Plotten von weniger Sensoren, 
                    # als maximal zulässig pro Zeile
                    ax[tempY].plot(
                        axisList[axisCounter][0],
                        axisList[axisCounter][1],
                        "-",
                        label=label1,
                        linewidth=1.0)
                    ax[tempY].plot(
                        axisList[axisCounter][0][peakList[axisCounter]],
                        axisList[axisCounter][1][peakList[axisCounter]],
                        'r.',
                        ms=5,
                        mew=2)
                    xyText = "(" + str(
                        int(axisList[axisCounter][0]
                            [peakList[axisCounter]])) + ", " + str(
                                int(axisList[axisCounter][1]
                                    [peakList[axisCounter]])) + ")"
                    ax[tempY].annotate(
                        xyText,
                        xy=(axisList[axisCounter][0][peakList[axisCounter]],
                            axisList[axisCounter][1][peakList[axisCounter]]))
                else:
                    # Plotten von mehreren Zeilen und Spalten an Sub-Plots
                    ax[tempX, tempY].plot(
                        axisList[axisCounter][0],
                        axisList[axisCounter][1],
                        "-",
                        label=label1,
                        linewidth=1.0)
                    ax[tempX, tempY].plot(
                        axisList[axisCounter][0][peakList[axisCounter]],
                        axisList[axisCounter][1][peakList[axisCounter]],
                        'r.',
                        ms=5,
                        mew=2)
                    xyText = "(" + str(
                        int(axisList[axisCounter][0]
                            [peakList[axisCounter]])) + ", " + str(
                                int(axisList[axisCounter][1]
                                    [peakList[axisCounter]])) + ")"
                    ax[tempX, tempY].annotate(
                        xyText,
                        xy=(axisList[axisCounter][0][peakList[axisCounter]],
                            axisList[axisCounter][1][peakList[axisCounter]]))
                axisCounter += 1

                if self.ui.processBothDatas == True:
                    # Es werden Simulations- und Referenzdaten verglichen
                    if min(remainingPlotRows,
                           maxNoPlots) == 1 and noPlotCols == 1:
                        ax.plot(
                            axisList[axisCounter][0],
                            axisList[axisCounter][1],
                            "--",
                            label=label2,
                            linewidth=1.0)
                        ax.plot(
                            axisList[axisCounter][0][peakList[axisCounter]],
                            axisList[axisCounter][1][peakList[axisCounter]],
                            'r.',
                            ms=5,
                            mew=2)
                        xyText = "(" + str(
                            int(axisList[axisCounter][0]
                                [peakList[axisCounter]])) + ", " + str(
                                    int(axisList[axisCounter][1]
                                        [peakList[axisCounter]])) + ")"
                        ax.annotate(
                            xyText,
                            xy=(axisList[axisCounter][0][peakList[
                                axisCounter]],
                                axisList[axisCounter][1][peakList[axisCounter]]
                                ))
                    elif min(remainingPlotRows, maxNoPlots) == 1:
                        ax[tempY].plot(
                            axisList[axisCounter][0],
                            axisList[axisCounter][1],
                            "--",
                            label=label2,
                            linewidth=1.0)
                        ax[tempY].plot(
                            axisList[axisCounter][0][peakList[axisCounter]],
                            axisList[axisCounter][1][peakList[axisCounter]],
                            'r.',
                            ms=5,
                            mew=2)
                        xyText = "(" + str(
                            int(axisList[axisCounter][0]
                                [peakList[axisCounter]])) + ", " + str(
                                    int(axisList[axisCounter][1]
                                        [peakList[axisCounter]])) + ")"
                        ax[tempY].annotate(
                            xyText,
                            xy=(axisList[axisCounter][0][peakList[
                                axisCounter]],
                                axisList[axisCounter][1][peakList[axisCounter]]
                                ))
                    else:
                        ax[tempX, tempY].plot(
                            axisList[axisCounter][0],
                            axisList[axisCounter][1],
                            "--",
                            label=label2,
                            linewidth=1.0)
                        ax[tempX, tempY].plot(
                            axisList[axisCounter][0][peakList[axisCounter]],
                            axisList[axisCounter][1][peakList[axisCounter]],
                            'r.',
                            ms=5,
                            mew=2)
                        xyText = "(" + str(
                            int(axisList[axisCounter][0]
                                [peakList[axisCounter]])) + ", " + str(
                                    int(axisList[axisCounter][1]
                                        [peakList[axisCounter]])) + ")"
                        ax[tempX, tempY].annotate(
                            xyText,
                            xy=(axisList[axisCounter][0][peakList[
                                axisCounter]],
                                axisList[axisCounter][1][peakList[axisCounter]]
                                ))
                    axisCounter += 1

                # Setzen von allgemeinen Parametern (erneut Fallunterscheidung)
                if min(remainingPlotRows, maxNoPlots) == 1 and noPlotCols == 1:
                    # Titel des Sub-Plots setzen
                    ax.set_title(
                        self.ui.sensorDict.getSensorByCol(sensor).originalName)
                    # Legende einblenden
                    ax.legend(loc=0)
                    # Raster einblenden im Hintergrund
                    ax.grid(True)
                    # Achsenbeschriftungen setzen
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax.set_xlabel("Zeit [s]")
                    if tempY == 0:
                        ax.set_ylabel(self.getYAxisLabelSingle(sensor))
                elif min(remainingPlotRows, maxNoPlots) == 1:
                    ax[tempY].set_title(
                        self.sensorDict.getSensorByCol(sensor).originalName)
                    ax[tempY].legend(loc=0)
                    ax[tempY].grid(True)
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax[tempY].set_xlabel("Zeit [s]")
                    if tempY == 0:
                        ax[tempY].set_ylabel(self.getYAxisLabelSingle(sensor))
                else:
                    ax[tempX, tempY].set_title(
                        self.sensorDict.getSensorByCol(sensor).originalName)
                    ax[tempX, tempY].legend(loc=0)
                    ax[tempX, tempY].grid(True)
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax[tempX, tempY].set_xlabel("Zeit [s]")
                    if tempY == 0:
                        ax[tempX, tempY].set_ylabel(
                            self.getYAxisLabelSingle(sensor))

                counterCell += 1
                counterSubPlots += 1

            counterPlot += 1
            remainingPlotRows -= min(remainingPlotRows, maxNoPlots)
            # Plot darstellen
            fig.tight_layout()
            self.plotShow(
                self.configReader.config.get("Names", "Title_Timeline_Peak") +
                " " + self.sensorDict.getSensorByCol(
                    self.ui.sensors[counterSubPlots - 1]).group + " " +
                str(counterPlot))

    def plotPeakPeak(self, peaksValueList, positionList, sensorGroupList,
                     peakValue1Dict, peakValue2Dict, justPrintResults):
        # Ergebnisse mit Boxplots darstellen
        if justPrintResults == False:
            # Plot-Titel sestzen
            plot.title(
                self.configReader.config.get("Names", "Title_PEAK_PEAK") +
                " Boxplot")
            # Y-Achsenbeschriftung setzen
            plot.ylabel("PEAK")
            # PDF-Anhang Seite hinzufügen
            self.pdf.add_page()
            self.pdf.printNewGroup(
                self.configReader.config.get("Names", "Title_PEAK_PEAK"))
            # Plotten der Boxplots
            bpDict = 0
            if len(positionList) > 5:
                ax1 = plot.gca()
                bpDict = ax1.boxplot(
                    peaksValueList,
                    0,
                    ".r",
                    positions=positionList,
                    labels=sensorGroupList,
                    showfliers=False)
                ax1.set_xticklabels(
                    ax1.xaxis.get_majorticklabels(), rotation=-45)
            else:
                bpDict = plot.boxplot(
                    peaksValueList,
                    0,
                    ".r",
                    positions=positionList,
                    labels=sensorGroupList,
                    showfliers=False)

            # X-Achse für Boxplots
            plot.xlabel("")
            #Grid einblenden
            plot.grid(True)
            #Kennzeichnung des Medians
            ax = plot.gca()
            for line in bpDict['medians']:
                x, y = line.get_xydata()[1]
                ax.annotate("%.3f" % y, xy=(x, y))
            self.plotShow(
                self.configReader.config.get("Names", "Title_PEAK_PEAK") +
                " Boxplot")

        # Plotten der PEAK-PEAK Verteilung
        for group in peakValue1Dict:
            if justPrintResults == False:
                plot.plot(
                    peakValue1Dict.get(group),
                    peakValue2Dict.get(group),
                    "b.",
                    fillstyle="none",
                    label=group)

            # Peaks hinsichtlich Unsicherheitsbereich auswerten
            greaterUcwCounter = 0
            ucw = float(self.ui.sensorDict.sensorGroupUcwPeak.get(group)) / 100
            for peak in range(len(peakValue1Dict.get(group))):
                # Abweichung ausrechnen
                div = 1
                if peakValue2Dict.get(group)[peak] == 0:
                    div = 1
                else:
                    div = peakValue1Dict.get(group)[peak] / peakValue2Dict.get(
                        group)[peak]
                if div < 1 - ucw or div > 1 + ucw:
                    greaterUcwCounter += 1
            # Anteil in % der Peaks im Vertrauensbereich berechnen
            divTotal = (
                1 - greaterUcwCounter / len(peakValue1Dict.get(group))) * 100
            if justPrintResults == True:
                self.pdf.resultDictPeak[group] = divTotal
                continue
            maxValue = max(
                max(peakValue1Dict.get(group)), max(peakValue2Dict.get(group)))

            # Text im Plot darstellen
            plot.annotate(
                "Ergebnis: " + str(round(divTotal, 1)) + "%",
                xy=(0.5 * maxValue, 0.07 * maxValue),
                color="black")
            plot.annotate(
                "(PEAKS im Vertrauensbereich)",
                xy=(0.5 * maxValue, 0.02 * maxValue),
                color="black")

            # Ergebnis als Punkt-Plot darstellen
            # Plot-Titel sestzen
            plot.title("PEAK/PEAK - " + group)
            # X und Y-Achsenbeschriftung setzen
            unit = self.getYAxisLabelSingle(
                self.ui.sensorDict.getFirstSensorFromGroup(group).col)
            plot.xlabel(unit + " " + self.configReader.config.get(
                "Names", "Title_File_1"))
            plot.ylabel(unit + " " + self.configReader.config.get(
                "Names", "Title_File_2"))

            # Orientierungs-Gerade plotten
            plot.plot([0, maxValue], [0, maxValue], "k-", linewidth=0.5)
            plot.xlim(0, maxValue)
            plot.ylim(0, maxValue)
            # Unsicherheitsbereich auslesen und plotten
            plot.plot(
                [0, maxValue], [0, maxValue * (1 + ucw)], "g--", linewidth=0.5)
            plot.plot(
                [0, maxValue], [0, maxValue * (1 - ucw)], "g--", linewidth=0.5)
            axis = plot.gca()
            axis.fill_between(
                [0, maxValue], [0, maxValue * (1 - ucw)],
                [0, maxValue * (1 + ucw)],
                facecolor='green',
                alpha=0.2)
            plot.annotate(
                "+" + str(int(ucw * 100)) + "%",
                xy=(0.9 * maxValue - 0.1 * maxValue, 0.9 * maxValue),
                color="green")
            plot.annotate(
                "+" + str(int(ucw * 100)) + "%",
                xy=(0.9 * maxValue - 0.03 * maxValue,
                    0.9 * maxValue - 0.1 * maxValue),
                color="green")

            self.plotShow(
                self.configReader.config.get("Names", "Title_PEAK_PEAK") + " "
                + group)

    def plotPeakPeacock(self, peakValueList, peacockValueList, positionList,
                        sensorGroupList, justPrintResults):
        # Ergebnisse mit Boxplots darstellen
        if justPrintResults == False:
            # Plot-Titel sestzen
            plot.title(
                self.configReader.config.get("Names", "Title_PEAK_PEACOCK") +
                " Boxplot")
            # Y-Achsenbeschriftung setzen
            plot.ylabel("PEACOCK")
            # X-Achse für Boxplots
            plot.xlabel("")

            # PDF-Anhang Seite hinzufügen
            self.pdf.add_page()
            self.pdf.printNewGroup(
                self.configReader.config.get("Names", "Title_PEAK_PEACOCK"))

            # Plotten der Boxplots
            bpDict = 0
            if len(positionList) > 5:
                ax1 = plot.gca()
                bpDict = ax1.boxplot(
                    peacockValueList,
                    0,
                    ".r",
                    positions=positionList,
                    labels=sensorGroupList,
                    showfliers=False)
                ax1.set_xticklabels(
                    ax1.xaxis.get_majorticklabels(), rotation=-45)
            else:
                bpDict = plot.boxplot(
                    peacockValueList,
                    0,
                    ".r",
                    positions=positionList,
                    labels=sensorGroupList,
                    showfliers=False)

            #Grid einblenden
            plot.grid(True)
            #Kennzeichnung des Medians
            ax = plot.gca()
            for line in bpDict['medians']:
                x, y = line.get_xydata()[1]
                ax.annotate("%.3f" % y, xy=(x, y))
            self.plotShow(
                self.configReader.config.get("Names", "Title_PEAK_PEACOCK") +
                " Boxplot")

        # Ergebnis als Punkt-Plot darstellen
        groupCounter = 0
        for group in sensorGroupList:
            if justPrintResults == False:
                # Orientierungs-Gerade plotten
                plot.plot([0, 1], [0, 0], "k-", linewidth=0.5)
                #Begrenzung der Plots
                plot.xlim(0, 1)
                plot.ylim(-1, 1)
                # Unsicherheitsbereich auslesen und plotten
                ucwPeak = self.ui.sensorDict.sensorGroupUcwPeak.get(group)
                plot.plot(
                    [0, 1], [float(ucwPeak) / 100,
                             float(ucwPeak) / 100],
                    "g--",
                    linewidth=0.5)
                plot.plot(
                    [0, 1], [-float(ucwPeak) / 100, -float(ucwPeak) / 100],
                    "g--",
                    linewidth=0.5)
                axis = plot.gca()
                axis.fill_between(
                    [0, 1], [-float(ucwPeak) / 100, -float(ucwPeak) / 100],
                    [float(ucwPeak) / 100,
                     float(ucwPeak) / 100],
                    facecolor='green',
                    alpha=0.2)
                plot.annotate(
                    "+" + ucwPeak + "%",
                    xy=(0.9, float(ucwPeak) / 100 + 0.02),
                    color="green")
                plot.annotate(
                    "+" + ucwPeak + "%",
                    xy=(0.9, -float(ucwPeak) / 100 - 0.08),
                    color="green")
                ucwPeacock = self.ui.sensorDict.sensorGroupUcwPeacock.get(
                    group)
                plot.plot(
                    [float(ucwPeacock) / 100,
                     float(ucwPeacock) / 100], [-1, 1],
                    "r--",
                    linewidth=0.5)
                axis.fill_between(
                    [0, float(ucwPeacock) / 100], [-1, -1], [1, 1],
                    facecolor='red',
                    alpha=0.2)
                plot.annotate(
                    "+" + ucwPeacock + "%",
                    xy=(float(ucwPeacock) / 100 + 0.01, 0.9),
                    color="red")
                # Plot-Titel sestzen
                plot.title("PEAK/PEACOCK - " + group)
                # X und Y-Achsenbeschriftung setzen
                plot.xlabel("PEACOCK")
                plot.ylabel("PEAK")

                #Punkte plotten
                plot.plot(
                    peacockValueList[groupCounter],
                    peakValueList[groupCounter],
                    "b.",
                    fillstyle="none",
                    label=group)

            # Peaks hinsichtlich Unsicherheitsbereich auswerten
            ucwCounter = 0
            ucwCounter2 = 0
            ucwPeak = float(
                self.ui.sensorDict.sensorGroupUcwPeak.get(group)) / 100
            ucwPeacock = float(
                self.ui.sensorDict.sensorGroupUcwPeacock.get(group)) / 100
            for peak in range(len(peakValueList[groupCounter])):
                if (peakValueList[groupCounter][peak] <= ucwPeak and 
                peakValueList[groupCounter][peak] >= ucwPeak * -1):
                    ucwCounter += 1
                    if peacockValueList[groupCounter][peak] <= ucwPeacock:
                        ucwCounter2 += 1
            # Anteil in % der Peaks im Vertrauensbereich berechnen
            divTotal = (ucwCounter / len(peakValueList[groupCounter])) * 100
            divTotal2 = (
                ucwCounter2 / len(peacockValueList[groupCounter])) * 100

            groupCounter += 1
            if justPrintResults == True:
                self.pdf.resultDictPeacock[group] = divTotal
                self.pdf.resultDictPeakPeacock[group] = divTotal2
                continue

            # Text im Plot darstellen
            ax1 = plot.gca()
            plot.annotate(
                "Ergebnis: " + str(round(divTotal, 1)) + "%",
                xy=(0.35, 0.65 * ax1.get_ylim()[0]),
                color="black")
            plot.annotate(
                "(PEAKCOCKS im Vertrauensbereich)",
                xy=(0.35, 0.75 * ax1.get_ylim()[0]),
                color="black")
            plot.annotate(
                "Ergebnis: " + str(round(divTotal2, 1)) + "%",
                xy=(0.35, 0.85 * ax1.get_ylim()[0]),
                color="black")
            plot.annotate(
                "(PEAK/PEAKCOCKS im Vertrauensbereich)",
                xy=(0.35, 0.95 * ax1.get_ylim()[0]),
                color="black")

            self.plotShow(
                self.configReader.config.get("Names", "Title_PEAK_PEACOCK") +
                " " + group)

    def plotSensorFrequency(self, groupCount, sensorGroupDict):
        # Liste für die Beschriftungspositionen des Plots
        positions = np.arange(groupCount)
        width = 0.5

        # Listen für die Erstellung des Plots anlegen 
        # (Namen und Anzahl der Messgrößen)
        labels = []
        sensorAmount = []
        for group in sensorGroupDict:
            sensorAmount.append(sensorGroupDict.get(group))
            labels.append(group)

        # Beschriftungen der verschiedenen Balken setzen
        ax = plot.gca()
        bars = ax.bar(positions, sensorAmount, width)
        ax.set_xticks(positions)
        if len(positions) > 5:
            ax.set_xticklabels(labels, rotation=-45)
        else:
            ax.set_xticklabels(labels)

        # Titel und Achsenbeschriftung setzen
        plot.title(self.configReader.config.get("Names", "Title_Frequency"))
        plot.xlabel("")
        plot.ylabel("Häufigkeit")

        # Anzeigen der Werte über den Balken
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                str(int(height)),
                ha='center',
                va='bottom')

        self.pdf.add_page()
        self.pdf.printNewGroup(
            self.configReader.config.get("Names", "Title_Frequency"))
        self.plotShow(self.configReader.config.get("Names", "Title_Frequency"))

    def plotTimelineBoxplots(self, dataList):
        # Anzahl der Sub-Plots pro Zeile in der Plot-Ausgabe
        maxNoPlotCols = 3
        # Anzahl der Zeilen pro Plotdatei
        maxNoPlots = 1
        # Anzahl der zu plottenden Sensoren auslesen
        noSensors = len(self.ui.sensors)
        # Bezeichnungen der Daten auslesen
        label1 = self.configReader.config.get("Names", "Title_File_1_short")
        label2 = self.configReader.config.get("Names", "Title_File_2_short")
        labelList = [label1, label2]
        positionList = [1, 2]

        # Anzahl der Spalten des Plots bestimmen
        noPlotCols = 0
        if noSensors < maxNoPlotCols:
            noPlotCols = noSensors
        else:
            noPlotCols = maxNoPlotCols

        # Anzahl der Zeilen des Plots bestimmen
        noPlotRows = 1
        counter = 0
        lastGroup = self.sensorDict.getSensorByCol(self.ui.sensors[0]).group
        for sensor in range(noSensors):
            newGroup = self.sensorDict.getSensorByCol(
                self.ui.sensors[sensor]).group
            if newGroup != lastGroup:
                noPlotRows += 1
                counter = 1
            else:
                counter += 1
                if counter > maxNoPlotCols:
                    noPlotRows += 1
                    counter = 1
            lastGroup = self.sensorDict.getSensorByCol(
                self.ui.sensors[sensor]).group

        # Anzahl der Hauptplots bestimmen
        noPlots = math.ceil(noPlotRows / maxNoPlots)

        # PDF-Anhang Seite hinzufügen
        self.pdf.add_page()

        # Iteration beginnen
        counterPlot = 0
        remainingPlotRows = noPlotRows
        axisCounter = 0
        counterSubPlots = 0
        sensor = self.ui.sensors[counterSubPlots]
        lastGroup1 = ""
        for plotNumber in range(noPlots):
            # Plot anlegen
            fig, ax = plot.subplots(
                nrows=min(remainingPlotRows, maxNoPlots),
                ncols=noPlotCols,
                facecolor="white",
                figsize=(8,
                         2.5 * min(remainingPlotRows,
                                   maxNoPlots)))  # , sharex=True, sharey=True

            counterCell = 0
            # Überschriften in PDF-Anhang schreiben
            sensor = self.ui.sensors[counterSubPlots]
            newGroup1 = self.sensorDict.getSensorByCol(sensor).group
            if lastGroup1 != newGroup1:
                lastGroup1 = self.sensorDict.getSensorByCol(sensor).group
                sensorGroupName = self.sensorDict.sensorGroupNames.get(
                    self.sensorDict.getSensorByCol(sensor).group)
                self.pdf.printNewGroup(
                    self.configReader.config.get(
                        "Names", "Title_Timeline_Boxplot") + " - " +
                    sensorGroupName)

            while counterSubPlots < len(
                    self.ui.sensors
            ) and counterCell < maxNoPlotCols * maxNoPlots:
                # Auf neue Sensorgruppe prüfen (ggf. neuer Sub-Plot)
                lastGroup = self.sensorDict.getSensorByCol(sensor).group
                sensor = self.ui.sensors[counterSubPlots]
                newGroup = self.sensorDict.getSensorByCol(sensor).group
                if lastGroup != newGroup:
                    break

                # Bestimmen, welcher Sub-Plot gefüllen werden soll
                tempX = math.floor(counterCell / noPlotCols)
                tempY = counterCell % noPlotCols

                # Fallunterscheidung
                bpDict = 0
                if min(remainingPlotRows, maxNoPlots) == 1 and noPlotCols == 1:
                    # Plotten von nur einem Sensor
                    bpDict = ax.boxplot(
                        dataList[axisCounter],
                        0,
                        ".r",
                        positions=positionList,
                        labels=labelList)
                    #Kennzeichnung des Medians
                    for line in bpDict['medians']:
                        x, y = line.get_xydata()[1]
                        ax.annotate("%.1f" % y, xy=(x, y))
                elif min(remainingPlotRows, maxNoPlots) == 1:
                    # Plotten von weniger Sensoren, 
                    #als maximal zulässig pro Zeile
                    bpDict = ax[tempY].boxplot(
                        dataList[axisCounter],
                        0,
                        ".r",
                        positions=positionList,
                        labels=labelList)
                    #Kennzeichnung des Medians
                    for line in bpDict['medians']:
                        x, y = line.get_xydata()[1]
                        ax[tempY].annotate("%.1f" % y, xy=(x, y))
                else:
                    # Plotten von mehreren Zeilen und Spalten an Sub-Plots
                    bpDict = ax[tempX, tempY].boxplot(
                        dataList[axisCounter],
                        0,
                        ".r",
                        positions=positionList,
                        labels=labelList)
                    #Kennzeichnung des Medians
                    for line in bpDict['medians']:
                        x, y = line.get_xydata()[1]
                        ax[tempX, tempY].annotate("%.1f" % y, xy=(x, y))
                axisCounter += 1

                # Setzen von allgemeinen Parametern (erneut Fallunterscheidung)
                if min(remainingPlotRows, maxNoPlots) == 1 and noPlotCols == 1:
                    # Titel des Sub-Plots setzen
                    ax.set_title(
                        self.ui.sensorDict.getSensorByCol(sensor).originalName)
                    # Legende einblenden
                    ax.legend(loc=0)
                    # Raster einblenden im Hintergrund
                    ax.grid(True)
                    # Achsenbeschriftungen setzen
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax.set_xlabel("")
                    if tempY == 0:
                        ax.set_ylabel(self.getYAxisLabelSingle(sensor))
                elif min(remainingPlotRows, maxNoPlots) == 1:
                    ax[tempY].set_title(
                        self.sensorDict.getSensorByCol(sensor).originalName)
                    ax[tempY].legend(loc=0)
                    ax[tempY].grid(True)
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax[tempY].set_xlabel("")
                    if tempY == 0:
                        ax[tempY].set_ylabel(self.getYAxisLabelSingle(sensor))
                else:
                    ax[tempX, tempY].set_title(
                        self.sensorDict.getSensorByCol(sensor).originalName)
                    ax[tempX, tempY].legend(loc=0)
                    ax[tempX, tempY].grid(True)
                    if (tempX + 1) + (counterPlot) * maxNoPlots == noPlotRows:
                        ax[tempX, tempY].set_xlabel("")
                    if tempY == 0:
                        ax[tempX, tempY].set_ylabel(
                            self.getYAxisLabelSingle(sensor))

                counterCell += 1
                counterSubPlots += 1

            counterPlot += 1
            remainingPlotRows -= min(remainingPlotRows, maxNoPlots)
            # Plot darstellen
            fig.tight_layout()
            self.plotShow(
                self.configReader.config.get("Names", "Title_Timeline_Boxplot")
                + " " + self.sensorDict.getSensorByCol(
                    self.ui.sensors[counterSubPlots - 1]).group + " " +
                str(counterPlot))

    def plotShow(self, namePlot):
        # Plotfigur auslesen, um sie extern abspeichern zu können
        figure = plot.gcf()
        # Plot abschließend darstellen
        plot.tight_layout()
        plot.show()

        # Speichern des Plots als externe Bilddatei
        if self.configReader.config.get("Export", "Plot_Export") == "1":
            self.__savePlot2File__(figure, namePlot)
            self.pdf.image("Plots/" + namePlot + ".png", w=175)

    def __savePlot2File__(self, figure, namePlot):
        # Plot als externe Datei unter dem gegebenen Namen speichern
        if not os.path.exists("Plots\\"):
            # Ordner "Plots" erstellen, falls er noch nicht existiert
            os.makedirs("Plots\\")
        # Namen festlegen
        plotFileName = "Plots\\" + namePlot + ".png"
        # Plot speichern
        figure.savefig(
            plotFileName,
            dpi=int(self.configReader.config.get("Export", "Plot_Resolution")))


# # Klasse: ProcessData
# Bevor die Daten und Ergebnisse der Vergleichs-Operationen dargestellt werden können, müssen sie zunächst formatiert und berechnet werden. Die Klasse "ProcessData" übernimmt diese Aufgaben, sowie kleinere Unterstützungs-Aufgaben. Sie verarbeitet die eingelesenen und strukturierten Daten aus der Klasse "CompareData" und konvertiert mit Hilfe der Methode "convertData" die einzelnen Werte der Zeitreihen in "float"-Datentypen (d. h. in Fließkommazahlen). Dieser Schritt ist notwendig, da die Daten in der ".csv"-Datei teilweise in der wissenschaftlichen Notation (z. B. "10E-5") vorliegen können. Diese werden von der Maschine jedoch zunächst nur als Zeichenkette wahrgenommen und nicht als wirkliche Zahlen.
# 
# Das weitere Vorgehen ist abhängig von der Art der Vergleichs-Operation. Die Bestimmung der Zeitreihen-Werte ist dabei das einfachste Vorgehen, da die Daten lediglich strukturiert an die jeweilige "plot"-Methode der Klasse "PlotResults" übergeben werden müssen. Bei der Bestimmung der gemittelten Zeitreihen-Werte, werden die Daten zunächst über ein bestimmtes Zeitintervall "dt" gemittelt und formatiert und dann an die betreffende "plot"-Methode weitergeleitet. Das Zeitintervall wird im Allgemeinen auf 60 Sekunden festgelegt, kann aber auch frei vom Benutzer in der Konfigurationsdatei eingestellt werden.
# 
# Für die Bestimmung der Peak-Werte, beispielsweise bei dem Vergleich der Zeitreihen mit Peak-Markierung, wird ebenfalls auf die Konfigurationsdatei zurückgegriffen, um die Art der Peak-Bestimmung auszulesen. Bei der Bestimmung des Peaks der Gastemperatur wird zum Beispiel der maximale Wert benötigt. Bei der Bestimmung des Peaks der Strömungsgeschwindigkeit hingegen der absolut maximale Wert und im Hinblick auf die Sauerstoff-Konzentration der minimale Wert. Die resultierenden Peaks werden dann entweder direkt für die Darstellung oder für die weitere Verarbeitung (z. B. für den PEAK-Vergleich) weitergegeben.
# 
# Die Berechnung der PEACOCK- und PEAK-Werte erfolgt in beiden Fällen nach einem ähnlichen Muster. Es werden jeweils die betreffenden Wertepaare aus beiden Dateien (Simulationsdaten und Referenzdaten) aufeinander bezogen, um den jeweiligen Wert zu berechnen. Beim PEACOCK-Vergleich müssen die Wertepaare jedoch auf der gleichen Zeitachse basieren, um verglichen werden zu können. Dazu kalkuliert die Methode "adjustTimelines" die maßgebliche Zeitspanne für den Vergleich (die geringere Zeitspanne beider Datensätze) und passt den zeitlich längeren Datensatz an diese neue "Endzeit" an. Zusätzlich müssen beide Datensätze auf den gleichen Zeitschritten basieren, um den PEACOCK-Vergleich durchführen zu können. Aus diesem Grund wird erneut der Datensatz mit der ursprünglich längeren Zeit angepasst und die Werte, bezogen auf die neuen Zeitschritte, werden linear interpoliert. Der PEACOCK-Vergleich ist aufgrund dieser zusätzlich nötigen Anpassung rechnerisch am aufwendigsten im Gegensatz zu den anderen Vergleichs-Operationen.

# In[50]:


class ProcessData:
    compareData = CompareData
    plotResults = PlotResults
    ui = UserInterface
    configReader = ConfigReader
    resultTable = ExportResultTable

    def __init__(self, ui, compareData, plotResults, 
                 configReader, resultTable):
        self.ui = ui
        self.compareData = compareData
        self.plotResults = plotResults
        self.configReader = configReader
        self.resultTable = resultTable

    def __calculateNumberOfRows__(self, data):
        # Berechnung der maximal benötigten Zeilen für die 
        # Iterationen (=Anzahl der X- und Y-Werte)
        noRowsNeeded = 0
        for row in range(len(data)):
            try:
                float(data[row][0])
                noRowsNeeded += 1
            except ValueError:
                # Eine Zelle mit Text soll nicht gezählt werden
                pass

        return noRowsNeeded

    def __convertData__(self, data, col):
        # Konvertierung der Daten aus wissenschaftlicher 
        # Notation z.B. 10E-5 in Fließkommazahlen

        # Initialisierung des Achsen-Arrays
        axis = [0] * self.__calculateNumberOfRows__(data)
        # Ziel-Index in neuer Speicherstruktur
        destRow = 0

        # Auslesen der Werte aus den Dateien
        for row in range(len(data)):
            try:
                # Schreiben und konvertieren der Daten 
                # (aus wissenschaftlicher Notation z.B. 10E-5)
                axis[destRow] = float(data[row][col])
                destRow += 1
            except ValueError:
                pass

        return axis

    def passTimelinesToExportTable(self):
        # Ergebnis-Tabelle mit Fühlern und Zeitreihen füllen

        # Maßgebliche Zeit der beiden Dateien ermitteln (kürzere Zeit)
        xAxis1 = self.__convertData__(self.compareData.getData("1"), 0)
        xAxis2 = self.__convertData__(self.compareData.getData("2"), 0)
        maxTime = int(min(xAxis1[len(xAxis1) - 1], xAxis2[len(xAxis2) - 1]))

        for sensor in self.ui.sensors:
            # Sensornamen auslesen
            sensorName = self.ui.sensorDict.getSensorByCol(sensor).originalName
            # Zeitreihen-Werte auslesen
            yAxis1 = self.__convertData__(
                self.compareData.getData("1"), sensor)
            yAxis2 = self.__convertData__(
                self.compareData.getData("2"), sensor)
            # Zeitreihen aneinander anpassen und "maxTime" berücksichtigen
            yAxis1Short = []
            yAxis2Short = []
            for value in range(len(xAxis1)):
                if xAxis1[value] >= maxTime:
                    break
                yAxis1Short.append(yAxis1[value])
            for value in range(len(xAxis2)):
                if xAxis2[value] >= maxTime:
                    break
                yAxis2Short.append(yAxis2[value])

            # Werte übergeben an die Ergebnis-Tabelle
            self.resultTable.appendMedian(sensorName, yAxis1Short, yAxis2Short)

    def __calculateTimelineValues__(self, plotData):
        # Berechnung der Zeitreihen-Werte

        axisList = []
        if self.ui.processBothDatas == True:
            # Vergleichsgraphen aus beiden Import-Dateien plotten
            for sensor in self.ui.sensors:
                returnAxis = self.__calculateTimelineValuesHelper__(
                    "1", sensor)
                axisList.append(returnAxis)

                returnAxis = self.__calculateTimelineValuesHelper__(
                    "2", sensor)
                axisList.append(returnAxis)
        else:
            # Nur Daten aus einer Datei plotten
            for sensor in self.ui.sensors:
                returnAxis = self.__calculateTimelineValuesHelper__(
                    self.ui.linesToPlot, sensor)
                axisList.append(returnAxis)

        if plotData == True:
            self.plotResults.plotTimeline(axisList, "")

        return axisList

    def __calculateTimelineValuesHelper__(self, dataFileNumber, sensor):
        # Hilfs-Methode zur Ermittlung der Zeitreihen-Werte

        # X-Achsen-Wertebereich ermitteln für die Anlegung eines Plots
        xAxis = self.__convertData__(
            self.compareData.getData(dataFileNumber), 0)
        # Y-Achsenwerte ermitteln
        yAxis = self.__convertData__(
            self.compareData.getData(dataFileNumber), sensor)

        # Rückgabewert erstellen
        returnAxis = [np.asarray(xAxis), np.asarray(yAxis)]

        return returnAxis

    def __calculateTimelineMeanValues__(self, plotData, writeData):
        # Berechnung der gemittelten Zeitreihen-Werte

        axisList = []
        if self.ui.processBothDatas == True:
            # Vergleichsgraphen aus beiden Import-Dateien plotten
            for sensor in self.ui.sensors:
                returnAxis = self.__calculateTimelineMeanValuesHelper__(
                    "1", sensor, writeData)
                axisList.append(returnAxis)

                returnAxis = self.__calculateTimelineMeanValuesHelper__(
                    "2", sensor, writeData)
                axisList.append(returnAxis)
        else:
            # Nur Daten aus einer Datei plotten
            for sensor in self.ui.sensors:
                returnAxis = self.__calculateTimelineMeanValuesHelper__(
                    self.ui.linesToPlot, sensor, writeData)
                axisList.append(returnAxis)

        if plotData == True:
            self.plotResults.plotTimeline(axisList, "mean")

        if (self.configReader.config.get("Export", "Export") == "1" and 
            writeData == True):
            self.compareData.writeDataCSVFilesMean(self.ui.linesToPlot)

        return axisList

    def __calculateTimelineMeanValuesHelper__(self, dataFileNumber, sensor,
                                              writeData):
        # Hilfs-Methode zur Ermittlung der gemittelten Zeitreihen-Werte

        currentTime = 0
        lastTime = 0
        dataSum = 0
        counterTime = 0
        counterData = 0
        meanTimeValues = []
        meanDataValues = []
        timeline = self.__convertData__(
            self.compareData.getData(dataFileNumber), 0)
        dataline = self.__convertData__(
            self.compareData.getData(dataFileNumber), sensor)
        dt = int(self.configReader.config.get("Variables", "dt"))

        # Startwerte übertragen
        meanTimeValues.append(timeline[0])
        meanDataValues.append(dataline[0])

        # Iteration über Zeitachse der Daten
        for timestep in range(len(timeline)):
            # Zeitschritt auslesen
            currentTime = timeline[timestep]
            # Werte aufsummieren
            dataSum += dataline[timestep]
            # Anzahl der summierten Werte zählen zur späteren Mittelung
            counterData += 1

            # Zeit seit letzter Mittlung berechnen und mit 
            # Zeitschritt aus der .ini-Datei vergleichen
            if (currentTime - lastTime >=
                    dt) or (timestep == len(timeline) - 1):
                counterTime += 1
                # Neuen Werte in Listen speichern
                meanTimeValues.append(counterTime * 60 - 30)
                meanDataValues.append(dataSum / max(counterData, 1))
                # Aktuellen Zeitschritt speichern
                lastTime = currentTime
                # Variablen zurücksetzen und neu beginnen
                dataSum = 0
                counterData = 0

        # Konvertierung der Listen zu Numpy-Arrays
        meanTimeValues = np.asarray(meanTimeValues)
        meanDataValues = np.asarray(meanDataValues)

        # X-Achsenwerte speichern
        meanTimeValuesMinMax = np.linspace(meanTimeValues.min(),
                                           meanTimeValues.max(), 300)
        # Y-Achsenwerte interpolieren aus berechneten Y-Werten
        meanDataValuesSpline = spline(meanTimeValues, meanDataValues,
                                      meanTimeValuesMinMax)

        # Rückgabewerte erstellen
        returnAxis = [meanTimeValuesMinMax, meanDataValuesSpline]

        if self.configReader.config.get("Export",
                                        "Export") == "1" and writeData == True:
            self.compareData.appendDataCSVFilesMean(returnAxis, dataFileNumber,
                                                    sensor)

        return returnAxis

    def __calculateTimelineComparison__(self):
        axisList = self.__calculateTimelineValues__(False)
        axisListMean = self.__calculateTimelineMeanValues__(False, False)

        self.plotResults.plotTimelineComparison(axisList, axisListMean)

    def __calculateTimlinePeaks__(self, plotPeaks):
        # Ermittlung der Peaks

        # Ermitteln der Zeitreihen-Werte
        axisList = []
        if plotPeaks == True:
            axisList = self.__calculateTimelineMeanValues__(False, False)
        else:
            axisList = self.__calculateTimelineValues__(False)

        # Iteration über die Sensoren um die Peaks zu ermitteln
        peakList = []
        peakIndexList = []
        for sensorAxis in range(len(axisList)):
            # Auslesen der Messgröße und der damit verbundenen Peak-Art
            group = self.ui.sensorDict.getSensorByCol(
                self.ui.sensors[int(sensorAxis / 2)]).group
            peakType = self.ui.sensorDict.sensorGroupPeakTypes.get(group)
            peakIndex = 0

            # Konvertierung
            axisList[sensorAxis][1] = axisList[sensorAxis][1].tolist()

            # Max-Peak
            if peakType.lower() == "max":
                peakIndex = axisList[sensorAxis][1].index(
                    max(axisList[sensorAxis][1]))
            # Max-Peak
            elif peakType.lower() == "min":
                peakIndex = axisList[sensorAxis][1].index(
                    min(axisList[sensorAxis][1]))
            # Absoluter-Peak
            elif peakType.lower() == "abs":
                absMaxList = []
                for i in axisList[sensorAxis][1]:
                    absMaxList.append(abs(i))
                peakIndex = absMaxList.index(max(absMaxList))

            # peakList - Parameter: X,Y
            peakList.append([
                axisList[sensorAxis][0][peakIndex],
                axisList[sensorAxis][1][peakIndex]
            ])
            peakIndexList.append(peakIndex)
        if plotPeaks == True:
            self.plotResults.plotTimelinePeaks(axisList, peakIndexList)
        return peakList

    def __getPEAKS__(self):
        # Peaks ermitteln
        peakList = self.__calculateTimlinePeaks__(False)

        # Iteration über alle Peaks (im Zweierschritt, da jeweils zwei 
        # Peaks zu einem Messfühler aus beiden Dateien gehört)
        sensorCounter = 0
        peakGroupDict = dict()
        sensorGroupList = []
        for peak in range(0, len(peakList), 2):
            sensor = self.ui.sensors[sensorCounter]
            sensorCounter += 1

            # Berechnung des PEAKS
            peakValue = (
                peakList[peak + 1][1] - peakList[peak][1]) / peakList[peak][1]

            # Gruppieren der PEAKS und Sensoren nach Untersuchungsgrößen
            group = self.ui.sensorDict.getSensorByCol(sensor).group
            if group in sensorGroupList:
                # Untersuchungsgröße befindet sich bereits im Dictionary
                peakGroupDict[group].append(peakValue)

            else:
                # Untersuchungsgröße befindet sich noch nicht im Dictionary
                sensorGroupList.append(group)
                peakGroupDict[group] = [peakValue]

        # Export und Zusammenführung der PEAKS in einer großen Liste 
        # für die Darstellung mittels Boxplots
        peaksValueList = []
        for group in peakGroupDict:
            peaksValueList.append(peakGroupDict.get(group))

        return peaksValueList

    def __calculatePeakPeak__(self, justPrintResults):
        # Verwendung beider Dateien für einen Vergleich
        self.ui.processBothDatas = True
        self.ui.linesToPlot = "xxx"

        # Peaks ermitteln
        peakList = self.__calculateTimlinePeaks__(False)

        # Liste und Dictionaries mit den untersuchten Größen für die 
        # Beschriftung und Zuordnung der Boxplots
        sensorGroupList = []
        peakValue1Dict = dict()
        peakValue2Dict = dict()
        peakGroupDict = dict()
        # Anzahl der unterschiedlichen Messgrößen
        positionList = []
        # Laufvariablen für die weitere Verarbeitung
        sensorCounter = 0
        positionCounter = 0

        # Iteration über alle Peaks (im Zweierschritt, da jeweils zwei 
        # Peaks zu einem Messfühler aus beiden Dateien gehört)
        for peak in range(0, len(peakList), 2):
            sensor = self.ui.sensors[sensorCounter]
            sensorCounter += 1

            # Berechnung des PEAKS
            peakValue = (
                peakList[peak + 1][1] - peakList[peak][1]) / peakList[peak][1]

            # Gruppieren der PEAKS und Sensoren nach Untersuchungsgrößen
            group = self.ui.sensorDict.getSensorByCol(sensor).group
            if group in sensorGroupList:
                # Untersuchungsgröße befindet sich bereits im Dictionary
                peakGroupDict[group].append(peakValue)
                peakValue1Dict[group].append(peakList[peak][1])
                peakValue2Dict[group].append(peakList[peak + 1][1])
            else:
                # Untersuchungsgröße befindet sich noch nicht im Dictionary
                sensorGroupList.append(group)
                peakGroupDict[group] = [peakValue]
                positionCounter += 1
                positionList.append(positionCounter)
                peakValue1Dict[group] = [peakList[peak][1]]
                peakValue2Dict[group] = [peakList[peak + 1][1]]

            # Hinzufügen des PEAKS zur Export-Tabelle
            sensorName = self.ui.sensorDict.getSensorByCol(sensor).originalName
            self.resultTable.appendPeak(sensorName, peakValue)

        # Export und Zusammenführung der PEAKS in einer großen Liste 
        # für die Darstellung mittels Boxplots
        peaksValueList = []
        for group in peakGroupDict:
            peaksValueList.append(peakGroupDict.get(group))

        # Plotten der PEAKS
        self.plotResults.plotPeakPeak(peaksValueList, positionList,
                                      sensorGroupList, peakValue1Dict,
                                      peakValue2Dict, justPrintResults)

    def __adjustTimelines__(self, axisList, maxTime):
        # Zeitreihen aneinander anpassen (interpolieren), damit sie 
        # sich gleiche X-Werte teilen und verglichen werden können

        yAxisReturnList = []

        # Listen mit den Achswerten anpassen und Zeitachse 
        # auf gleichen Maximalwert kürzen
        for sensor in range(len(self.ui.sensors)):
            # X-Achse anpassen
            xAxisListShort = []
            xCorr = 0
            xLast = -99
            for x in axisList[sensor][0]:
                # Nur bis zum Zeit-Maximalwert die Werte übertragen
                if x <= maxTime + 1:
                    # Korrektur für Interpolierungs-Routine
                    if x == xLast:
                        xCorr += 0.0000001
                    xAxisListShort.append(x + xCorr)
                    xLast = x

            # Y-Achse anpassen
            yAxisListShort = []
            # In Abhängigkeit der Anzahl der X-Werte, Y-Werte übertragen
            for yValue in range(len(xAxisListShort)):
                yAxisListShort.append(axisList[sensor][1][yValue])

            # Interpolations-Funktion berechnen
            f = interpolate.interp1d(
                xAxisListShort, yAxisListShort, kind='linear')

            # Neue gleichmäßige X-Achse festlegen
            xAxisNew = np.linspace(0, maxTime - 1, maxTime)
            # Werte der Y-Achse neu interpolieren
            yAxisNew = f(xAxisNew)

            # Rückgabe-Liste füllen
            yAxisReturnList.append(yAxisNew)

        return yAxisReturnList

    def __calculatePeakPeacock__(self, justPrintResults):
        # Verwendung beider Dateien für einen Vergleich
        self.ui.processBothDatas = True
        self.ui.linesToPlot = "xxx"

        # Daten aufbereiten
        axisList1 = []
        axisList2 = []
        for sensor in self.ui.sensors:
            axisList1.append(
                self.__calculateTimelineValuesHelper__("1", sensor))
            axisList2.append(
                self.__calculateTimelineValuesHelper__("2", sensor))

        # Ermitteln, welche Datei eine kürzere Zeitbetrachtung 
        # hat und diese maßgebend setzen
        maxTime = int(
            min(axisList1[0][0][len(axisList1[0][0]) - 1], axisList2[0][0][
                len(axisList2[0][0]) - 1]))

        # Y-Achse interpolieren anhand neuer einheitlichen X-Achse
        # Referenzwert(Versuch)
        yAxisList1 = self.__adjustTimelines__(axisList1, maxTime)
        # Simulationswert
        yAxisList2 = self.__adjustTimelines__(axisList2, maxTime)

        # Liste und Dictionary mit den untersuchten Größen für die 
        # Beschriftung und Zuordnung der Boxplots
        sensorGroupList = []
        peakGroupDict = dict()
        # Anzahl der unterschiedlichen Messgrößen
        positionList = []
        # Laufvariable für die weitere Verarbeitung
        positionCounter = 0

        for sensor in range(len(self.ui.sensors)):
            sumTop = 0
            sumBot = 0
            # Berechnung der PEACOCK-Werte
            for yValue in range(len(yAxisList1[0])):
                sumTop += math.pow(
                    yAxisList1[sensor][yValue] - yAxisList2[sensor][yValue], 2)
                sumBot += math.pow(yAxisList1[sensor][yValue], 2)
            peacockValue = math.sqrt(sumTop / sumBot)

            # Gruppieren der Sensoren nach Untersuchungsgrößen
            group = self.ui.sensorDict.getSensorByCol(
                self.ui.sensors[sensor]).group
            if group in sensorGroupList:
                peakGroupDict[group].append(peacockValue)
            else:
                sensorGroupList.append(group)
                peakGroupDict[group] = [peacockValue]
                positionCounter += 1
                positionList.append(positionCounter)

            # Hinzufügen des PEACOCKS zur Export-Tabelle
            sensorCol = self.ui.sensors[sensor]
            sensorName = self.ui.sensorDict.getSensorByCol(
                sensorCol).originalName
            self.resultTable.appendPeacock(sensorName, peacockValue)

        # Export und Zusammenführung der PEAKS in einer großen 
        # Liste für die Darstellung mittels Boxplots
        peacockValueList = []
        for group in peakGroupDict:
            peacockValueList.append(peakGroupDict.get(group))

        peakValueList = self.__getPEAKS__()
        self.plotResults.plotPeakPeacock(peakValueList, peacockValueList,
                                         positionList, sensorGroupList,
                                         justPrintResults)

    def __calculateTimelineBoxplots__(self):
        self.ui.processBothDatas = True
        self.ui.linesToPlot = "xxx"

        axisList = self.__calculateTimelineMeanValues__(False, False)
        axisArray = np.asarray(axisList)
        dataList = []

        # Maßgebliche Zeit der beiden Dateien ermitteln (kürzere Zeit)
        maxTime = int(
            min(axisArray[0][0][len(axisArray[0][0]) - 1], axisArray[1][0][
                len(axisArray[0][0]) - 1]))

        for sensorAxis in range(0, len(axisArray), 2):
            # Daten auslesen
            axisArrayShort1 = []
            axisArrayShort2 = []
            for value in range(len(axisArray[sensorAxis][1])):
                if axisArray[sensorAxis][0][value] >= maxTime:
                    break
                axisArrayShort1.append(axisArray[sensorAxis][1][value])
            for value in range(len(axisArray[sensorAxis + 1][1])):
                if axisArray[sensorAxis + 1][0][value] >= maxTime:
                    break
                axisArrayShort2.append(axisArray[sensorAxis + 1][1][value])
            dataList.append([axisArrayShort1, axisArrayShort2])

        self.plotResults.plotTimelineBoxplots(dataList)

    def __calculateSensorFrequency__(self):
        # Häufigkeit der Messgrößen darstellen als Balkendiagramm

        # Anzahl der unterschiedlichen Messgrößen zählen
        sensorGroupDict = dict()
        groupCount = 0
        for sensor in self.ui.sensorDict.sensorList:
            if sensor.group in sensorGroupDict:
                sensorGroupDict[
                    sensor.group] = sensorGroupDict.get(sensor.group) + 1
            else:
                sensorGroupDict[sensor.group] = 1
                groupCount += 1

        self.plotResults.plotSensorFrequency(groupCount, sensorGroupDict)

    def startProcessing(self):
        # Aufruf der vom Benutzer ausgewählten Verarbeitungsart der Daten
        # Festlegung der Reihenfolge der Operationen
        if self.ui.plotType.lower() == "verteilung":
            self.__calculateSensorFrequency__()

        if self.ui.plotType.lower() == "zeitreihe":
            self.__calculateTimelineValues__(True)

        if self.ui.plotType.lower() == "zeitreihe gemittelt":
            self.__calculateTimelineMeanValues__(True, False)

        if self.ui.plotType.lower() == "zeitreihen vergleich":
            self.__calculateTimelineComparison__()

        if self.ui.plotType.lower() == "peak-peak":
            self.__calculatePeakPeak__(False)

        if self.ui.plotType.lower() == "zeitreihen peak":
            self.__calculateTimlinePeaks__(True)

        if self.ui.plotType.lower() == "boxplot zeitreihen":
            self.__calculateTimelineBoxplots__()

        if self.ui.plotType.lower() == "peak-peacock":
            self.__calculatePeakPeacock__(False)


# # Klasse: Controller
# Die Klasse "Controller" ist die Steuereinheit der Software. Sie ist der Einstiegspunkt des Programms und initialisiert zu Beginn die verschiedenen Objekte der zuvor erläuterten Klassen. Ihre Aufgabe ist die Vorhaltung der Referenzen auf die erzeugten Objekte und die Steuerung des Programmablaufs. Zu Beginn wird die Haupt-Konfigurationsdatei eingelesen und es werden die Anzahl und Speicherorte der Validierungen festgelegt. Für jede Validierung läuft im Anschluss der gleiche allgemeine Ablauf ab, der sich in folgende Punkte unterteilen lässt:
# 
# - Einlesen der Konfigurationsdatei "config.ini" und Instanziierung der Klasse "ConfigReader"
# - Anlegen des noch leeren Messfühler-Verzeichnisses ("SensorDictionary")
# - Initialisierung der Export-Tabelle ("ExportResultTable") für die Validierungs-Ergebnisse
# - Initialisierung des PDF-Anhangs ("PDFAttachment")
# - Einlesen und strukturieren der Daten ("ImportData" und "CompareData")
# - Verarbeiten der Benutzereingaben über die Konfigurationsdatei oder Konsole ("UserInterface")
# - Berechnungs- und Darstellungsklassen instanziieren ("ProcessData" und "PlotResults")
# - Starten und Steuern der Vergleichs-Operationen
# - Ausgabe der Daten und Ergebnisse in der Konsole
# - Exportieren der Daten und Ergebnisse als ".csv"-Dateien
# - PDF-Anhang exportieren

# In[51]:


class Controller:
    startTime = 0
    configReader = ConfigReader
    sensorDict = SensorDictionary
    ui = UserInterface
    compareData = CompareData
    plotResults = PlotResults
    processData = ProcessData
    pdf = PDFAttachment

    def __init__(self):
        # Einlesen der Hauptkonfigurationsdatei
        # ermitteln welche Validierungsordner verarbeitet werden sollen
        configMainReader = ConfigReader("config_main.ini")
        configFolders = configMainReader.config.get(
            "Setup", "Validation_Folders").split(",")
        mainPath = os.getcwd()

        # Starten der Validierungen
        for configCounter in range(len(configFolders)):

            # Pfad wechseln auf den in der 
            # Hauptkonfigurationsdatei angegebenen Pfad
            os.chdir(mainPath)
            os.chdir(configFolders[configCounter])

            # Einlesen der Konfigurationsdatei
            self.configReader = ConfigReader("config.ini")

            # Gruppieren der Sensoren (Messfühler) in einem Dictionary
            self.sensorDict = SensorDictionary(self.configReader)
            
            # Anlegen der Export-Tabelle für die Ergebnisse
            resultTable = ExportResultTable(self.configReader)

            # PDF-Anhang erstellen
            self.pdf = PDFAttachment()
            self.pdf.setParams(self.configReader, self.sensorDict)

            # Dateien vergleichen
            self.compareData = CompareData(self.configReader, self.sensorDict)

            # Initialisierung der Eingabe
            self.ui = UserInterface(self.sensorDict)

            # Initialisierung des Plotters
            self.plotResults = PlotResults(self.configReader, self.sensorDict,
                                           self.ui, self.pdf)

            # Initialisierung der Berechnungsklasse
            self.processData = ProcessData(self.ui, self.compareData,
                                           self.plotResults, self.configReader,
                                           resultTable)

            # Hauptroutinen starten
            self.__startExecution__()

            # Zeitreihen an Export-Tabelle übergeben
            self.processData.passTimelinesToExportTable()

            if self.configReader.config.get("Export", "Plot_Export") == "1":
                # CSV-Exportdatei der Ergebnis-Tabelle schreiben
                resultTable.exportData()
                # CSV-Exportdatei der gemittelten Zeitreihen schreiben
                self.processData.__calculateTimelineMeanValues__(False, True)
                # PDF-Anhang schreiben
                self.pdf.printResultTable(resultTable)
                self.pdf.output(
                    self.configReader.config.get("Names", "Title_Project") +
                    ".pdf", 'F')

            # Verzeichnis wieder auf Hauptpfad wechseln für nächsten Lauf
            os.chdir(mainPath)

    def __startExecution__(self):
        # Steuerung des Programm-Ablaufs über Konsole
        if self.configReader.config.get("Input", "User_Input") == "1":
            inputContinue = "j"
            while inputContinue == "j":
                # Auslesen oder Eingabe der Berechnungs-Anweisungen
                self.ui.startInput()

                # Berechnung starten und Daten verarbeiten
                self.processData.startProcessing()

                # Abfrage, ob noch weitere Routinen gestartet werden sollen
                inputContinue = input(
                    "Sollen weitere Vergleiche angestellt werden? (j/n)\n")
        else:
            # Steuerung des Programm-Ablaufs über Konfigurations-Datei
            self.__startWithoutUserInput__()

    def __startWithoutUserInput__(self):
        # Parameter einlesen (betrachtete Messfühler und Dateinummer)
        self.ui.setInputParams(
            self.configReader.config.get("Control", "Sensors"),
            self.configReader.config.get("Control", "Data_File_Number"))

        #PDF-Anhang erweitern
        # Maßgebliche Zeit der beiden Dateien ermitteln (kürzere Zeit)
        xAxis1 = self.processData.__convertData__(
            self.compareData.getData("1"), 0)
        xAxis2 = self.processData.__convertData__(
            self.compareData.getData("2"), 0)
        maxTime = int(min(xAxis1[len(xAxis1) - 1], xAxis2[len(xAxis2) - 1]))
        self.pdf.printMaxTime(maxTime)
        self.pdf.printOperations()

        # Auslesen der zu auszuführenden Routinen
        self.__printOutput__()

    def __printOutput__(self):
        self.__printText__(
            self.configReader.config.get("Names", "Title_Project"))
        print("")
        print("Verwendete Daten:")
        print("")
        print("1. Datei:",
              self.configReader.config.get("Names", "Title_File_1"),
              "(Kurzbezeichnung:",
              self.configReader.config.get("Names", "Title_File_1_short"), ")")
        print("2. Datei:",
              self.configReader.config.get("Names", "Title_File_2"),
              "(Kurzbezeichnung:",
              self.configReader.config.get("Names", "Title_File_2_short"), ")")

        # Auslesen der auszuführenden Routinen
        if self.configReader.config.get("Control", "Plot_Frequency") == "1":
            self.__printText__(
                self.configReader.config.get("Names", "Title_Frequency"))
            self.ui.plotType = "Verteilung"
            self.__updateParams__()

        # Füllen des PDF-Anhangs mit der zusammenfassenden 
        # Tabelle aus PEAK und PEACOCK
        self.processData.__calculatePeakPeak__(True)
        self.processData.__calculatePeakPeacock__(True)
        self.pdf.printPeakPeacock()

        if self.configReader.config.get("Control", "Plot_Timeline") == "1":
            self.__printText__(
                self.configReader.config.get("Names", "Title_Timeline"))
            self.ui.plotType = "Zeitreihe"
            self.__updateParams__()
        if self.configReader.config.get("Control",
                                        "Plot_Mean_Timeline") == "1":
            self.__printText__(
                self.configReader.config.get("Names", "Title_Mean_Timeline"))
            self.ui.plotType = "Zeitreihe gemittelt"
            self.__updateParams__()
        if self.configReader.config.get("Control",
                                        "Plot_Timeline_Comparison") == "1":
            self.__printText__(
                self.configReader.config.get("Names",
                                             "Title_Timeline_Comparison"))
            self.ui.plotType = "Zeitreihen Vergleich"
            self.__updateParams__()
        if self.configReader.config.get("Control",
                                        "Plot_Timeline_Peak") == "1":
            self.__printText__(
                self.configReader.config.get("Names", "Title_Timeline_Peak"))
            self.ui.plotType = "Zeitreihen Peak"
            self.__updateParams__()
        if self.configReader.config.get("Control", "Plot_PEAK_PEAK") == "1":
            self.__printText__(
                self.configReader.config.get("Names", "Title_PEAK_PEAK"))
            self.ui.plotType = "PEAK-PEAK"
            self.__updateParams__()
        if self.configReader.config.get("Control", "Plot_PEAK_PEACOCK") == "1":
            self.__printText__(
                self.configReader.config.get("Names", "Title_PEAK_PEACOCK"))
            self.ui.plotType = "PEAK-PEACOCK"
            self.__updateParams__()
        if self.configReader.config.get("Control",
                                        "Plot_Timeline_Boxplot") == "1":
            self.__printText__(
                self.configReader.config.get("Names",
                                             "Title_Timeline_Boxplot"))
            self.ui.plotType = "Boxplot Zeitreihen"
            self.__updateParams__()

    def __printText__(self, operation):
        self.__printLine__()
        print("")
        print(operation)
        self.__printLine__()

    def __printLine__(self):
        print(
            "_____________________________________________________________")

    def __updateParams__(self):
        # Parameter aktualisieren 
        # (da sie teilweise neu gesetzt werden im Laufe der Routinen)
        self.ui.setInputParams(
            self.configReader.config.get("Control", "Sensors"),
            self.configReader.config.get("Control", "Data_File_Number"))
        self.processData.startProcessing()

    def __startTime__(self):
        # Zeitmessung starten
        self.startTime = time.clock()

    def __endTime__(self, printText):
        endTime = time.clock() - self.startTime
        print(printText, round(endTime, 2), "Sekunden")


# # Programmstart
# Die folgende Zeile ist der Einstiegspunkt für das gesamte Programm. Sie instanziiert die Klasse "Controller" und startet damit die Validierung. Die weitere Steuerung des Ablaufs übernimmt die Klasse selbst.

# In[52]:


#Programmablauf starten und steuern
controller = Controller()


# # PDF-Anhang
# Auf den folgenden Seiten befindet sich der automatisch generierte PDF-Anhang für eine exemplarisch durchgeführte Validierung. Die Randbedingungen für die Validierung werden auf der nächsten Seite erläutert.
