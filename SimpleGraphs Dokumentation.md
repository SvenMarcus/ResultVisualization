# SimpleGraphs Dokumentation

## Einleitende Worte

Für eine Weiterentwicklung der Software sollte ein grundlegendes Verständnis der objektorientierten Programmierung vorhanden sein, insbesondere mit dem Prinzip der Polymorphie. Des Weiteren wurden bei der Implementierung der Anwendung sogenannte *Entwurfsmuster* (*Design Patterns*) verwendet. Eine Kenntnis der verwendeten Muster ist daher von Vorteil.

## Aufbau der Software

### Generelle Aufteilung

Anwendungslogik und Darstellungslogik sind im Source Code getrennt. Der Ordner *ResultVisulization* enthält die Anwendungslogik, im Ordner *QtResultVisualization* enthält dagegen ausschließlich Code, der für die Konstruktion der Anwendungsfenster mit Qt und matplotlib zuständig ist. Der Vorteil dieser Vorgehensweise liegt daran, dass Anwendungslogik nicht von der Darstellung beeinflusst wird. Die Bibliotheken Qt und matplotlib können gegen andere Bibliotheken gleicher Funktionalität ausgetauscht werden, ohne dass Code aus *ResultVisualization* dafür angepasst werden muss.

### Wichtige Klassen der Kernanwendung

#### MainWindow

Beinhaltet den Code für das Hauptfenster. Hier ist ausschließlich die Logik für das Verwalten von Unteransichten in Form von GraphViews und das Hinzufügen/Entfernen von *Toolbar* und *Menubar* Einträgen implementiert. Das *MainWindow* selbst hat keinerlei Kenntnisse darüber, dass es sich um eine Anwendung zu Darstellung von Plots handelt.

#### GraphView

Beinhaltet eine Liste aller derzeit vorhandenen *Series*. Die *GraphView* Klasse verwendet nur die abstrakte Klasse *Series* und nicht die Ableitungen *LineSeries*, *BoxSeries* und *FillAreaSeries*. Die Klasse bleibt somit unabhängig von den Implementierungen und kann somit für jede Art von *Series* ohne Änderungen wiederverwendet werden.

Des Weiteren hält *GraphView* eine Instanz der Klasse *Graph*, die für das Darstellen von *Series* verantwortlich ist.

#### Graph

Zuständig für die Darstellung von *Series*. Beim Hinzufügen einer *Series* zum *Graph* reicht der *Graph* eine Instanz von *Plotter* and die *Series* weiter, die daraufhin den *Plotter* nutzt, um sich selbst auf dem *Graph* zu zeichnen.

#### Plotter

Eine Schnittstelle, die Methoden zum Darstellen verschiedener Plot-Varianten zur Verfügung stellt.

#### Series

Eine abstrakte Klasse, die als Basis für verschiedene Subtypen wie *LineSeries* oder *BoxSeries* dient.

#### SeriesFilter

*SeriesFilter* teilen einer *Series* mit, ob ein bestimmter Dateneintrag mit dargestellt werden oder herausgefiltert werden soll. Das Filtern geschieht anhand der Metadaten der *Series*. Die Filtertechnik hängt von der Implementierung des Filters ab.

#### Command

Die Schnittstelle *Command* beinhaltet lediglich eine *execute()* Methode. Der Sinn einer *Command*-Klasse ist die Kapselung eines einzelnen Verhaltens, um dieses zu einem bestimmten Zeitpunkt auszuführen. *Commands* werden in dieser Anwendung genutzt, um *Toolbar* und *Menubar* Einträgen eine Funktion mithilfe von *Actions* zuzuweisen.

#### Action

*Actions* stellen die grafische Repräsentation von *Commands* dar. Sie beinhalten Informationen über das Menü, in das die *Action* eingefügt werden soll, und welcher Text und welches Icon verwendet werden sollen.
