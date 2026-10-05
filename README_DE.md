# msiBuilder 1.11.2

Eine moderne Windows-Oberfläche zum Erstellen von MSI-Installern aus EXE-Dateien mit WiX – inklusive wiederöffnbarer Projektdatei, Update-festem UpgradeCode und automatischer Prüfung der Voraussetzungen.


## Neu in 1.11.2

### Dateitypen mit der installierten Anwendung verknüpfen

Im neuen Reiter **Dateitypen** können eine oder mehrere Dateiendungen hinterlegt werden, die von der installierten EXE geöffnet werden sollen, zum Beispiel:

- `.csv` – CSV-Datei
- `.md` – Markdown-Datei
- `.myfile` – eigenes Dateiformat

msiBuilder erzeugt dafür automatisch die erforderlichen WiX-`ProgId`-/`Extension`-Einträge, registriert die Anwendung unter **Öffnen mit** und in den Windows-**Standard-Apps** und übergibt die geöffnete Datei als `"%1"` an die EXE. Die Dateitypen werden in der `.wix`-Projektdatei gespeichert und beim erneuten Öffnen des Projekts wiederhergestellt.

> **Wichtig für Windows 10/11:** Ein Installer darf bestehende benutzerspezifische Standardprogramme nicht still überschreiben. msiBuilder registriert die Anwendung korrekt als verfügbaren Handler. Falls bereits ein anderes Standardprogramm gesetzt ist, muss der Benutzer die Auswahl einmal über **Öffnen mit** bzw. **Einstellungen → Apps → Standard-Apps** bestätigen.

## Neu in 1.9.2

- Scrollleisten werden nur noch angezeigt, wenn der Inhalt tatsächlich gescrollt werden muss.
- Die Überschrift „WiX-Quellcode“ hat jetzt den Hintergrund des Reiters statt einer weißen Hinterlegung.

## Neu in 1.9.0

- Im Ausgabeordner entstehen standardmäßig nur die fertige **MSI-Datei** und eine wiederöffnbare **`.wix`-Projektdatei**.
- Die `.wix`-Datei ist die msiBuilder-Projektdatei und speichert alle relevanten Einstellungen, insbesondere den **UpgradeCode** für spätere Updates.
- Optional kann **„Quelldateien und Build-Daten im Ordner source speichern“** aktiviert werden. Dann enthält `source` die Programm-EXE, `installer.wxs`, `install.cmd` und `uninstall.cmd`.
- Die von WiX erzeugte `.wixpdb` wird nach erfolgreichem Build entfernt; sie wird für den normalen msiBuilder-Workflow nicht benötigt.
- Build-Zwischendateien entstehen in einem temporären Verzeichnis und werden automatisch gelöscht.
- Der zusätzliche Leerraum oberhalb von **„Quelldatei & Ausgabe“** im Reiter **Projekt** wurde entfernt.

## Zielstruktur

Ohne Source-Archivierung:

```text
Ausgabeordner\
├── MeinProgramm-1.0.0.msi
└── MeinProgramm.wix
```

Mit aktivierter Source-Archivierung:

```text
Ausgabeordner\
├── MeinProgramm-1.0.0.msi
├── MeinProgramm.wix
└── source\
    ├── MeinProgramm.exe
    ├── installer.wxs
    ├── install.cmd
    └── uninstall.cmd
```

Die `.wix`-Projektdatei verweist bei archivierten Quelldaten relativ auf `source\MeinProgramm.exe`. Dadurch lässt sich der gesamte Ausgabeordner verschieben und später wieder öffnen.

## Projektdatei und Updates

Beim erstmaligen Projekt wird ein UpgradeCode erzeugt. Dieser wird in der `.wix`-Projektdatei gespeichert und beim erneuten Öffnen wiederhergestellt. Für neue Versionen desselben Produkts bleibt dieser UpgradeCode erhalten, damit Windows Installer die neue MSI als Update derselben Produktfamilie erkennen kann.

Die Projektdatei speichert unter anderem:

- Produktname
- Hersteller
- Version
- Architektur
- UpgradeCode
- EXE-Pfad bzw. relativen Source-Pfad
- Startmenü-/Desktop-Verknüpfung
- Deployment-Einstellungen
- Source-Archivierungsoption
- optional individuell bearbeiteten WiX-Quellcode

## Voraussetzungen

msiBuilder prüft automatisch:

1. **.NET SDK 6.0 oder neuer**
2. das **WiX Toolset**

Nach einer WiX-Installation wird automatisch ein echtes temporäres Test-MSI gebaut. So wird geprüft, ob WiX tatsächlich funktioniert und – bei WiX 7 – ob die erforderliche EULA-Zustimmung erfolgt ist. Falls nötig, wird die Zustimmung angeboten und der Test danach automatisch wiederholt.

## Bedienung

- **Ctrl+O** – Programm-EXE auswählen
- **Ctrl+L** – msiBuilder-Projekt (`.wix`) öffnen
- **Ctrl+S** – msiBuilder-Projekt (`.wix`) speichern
- **Ctrl+Shift+O** – Ausgabeordner öffnen
- **F5** – MSI jetzt erstellen
- **F6** – Voraussetzungen prüfen
- **F1** – Über msiBuilder

WiX-Quellcode (`.wxs`) kann weiterhin über das Datei-Menü separat importiert oder exportiert werden.

## One-File-EXE bauen

```cmd
build_onefile.bat
```

Das Buildskript erzeugt `dist\msiBuilder.exe` mit dem integrierten Programmsymbol.

## Lizenz

msiBuilder steht unter der MIT License. WiX ist eine externe Abhängigkeit und besitzt eigene Lizenz-/Nutzungsbedingungen.

- Layout: Der obere Abstand der Box „Quelldatei & Ausgabe“ entspricht jetzt dem linken und rechten Innenabstand des Projekt-Tabs.

### Individueller MSI-Dateiname

Der erzeugte MSI-Dateiname kann optional um ein **Präfix** und/oder **Suffix** ergänzt werden. Die Trennung per Unterstrich übernimmt msiBuilder automatisch. Eine Live-Vorschau zeigt jederzeit den endgültigen Namen.

Beispiele:

- `MeinProgramm-1.0.0.msi`
- `Setup_MeinProgramm-1.0.0.msi`
- `MeinProgramm-1.0.0_x64.msi`
- `Setup_MeinProgramm-1.0.0_x64.msi`

Präfix und Suffix werden zusammen mit dem Projekt in der `.wix`-Datei gespeichert.

### Dateizuordnungen und ProgID

Bei Dateizuordnungen gibt der Benutzer nur die Dateiendung (z. B. `.csv`) und eine Beschreibung an. Die **ProgID ist nicht die Dateiendung**, sondern eine technische Windows-Kennung für den registrierten Dateityp. msiBuilder erzeugt diese automatisch und stabil aus Produktname, Endung und Projektkennung.


## Projektdateien direkt öffnen

Wenn `.wix`-Projektdateien in Windows mit msiBuilder verknüpft sind, öffnet ein Doppelklick die Datei direkt im msiBuilder und stellt alle gespeicherten Projekteinstellungen wieder her.
