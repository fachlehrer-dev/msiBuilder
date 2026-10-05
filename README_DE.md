# msiBuilder

> **Moderne Windows-GUI zum Erstellen von MSI-Installern aus EXE-Dateien mit WiX – inklusive Silent-Deployment, wiederöffnbaren Projekten und automatischer Prüfung der Voraussetzungen.**

[English version](README.md)

---

## Was ist msiBuilder?

**msiBuilder** ist eine grafische Windows-Anwendung, mit der sich aus einer vorhandenen Windows-EXE ein sauberer **MSI-Installer** erstellen lässt – ohne WiX-Dateien von Hand schreiben oder lange Kommandozeilenbefehle zusammensetzen zu müssen.

Die Anwendung richtet sich an Administratoren, Entwickler, Schulen, kleine IT-Abteilungen und alle, die Programme als MSI paketieren oder zentral verteilen möchten.

msiBuilder übernimmt dabei nicht nur den eigentlichen Build, sondern unterstützt den gesamten Ablauf:

- EXE auswählen
- Produktdaten und Installationsoptionen festlegen
- UpgradeCode für spätere Updates verwalten
- Startmenü- und Desktop-Verknüpfungen konfigurieren
- Silent-Deployment-Befehle erzeugen
- WiX-Quellcode automatisch erzeugen und bei Bedarf bearbeiten
- .NET SDK und WiX automatisch prüfen
- WiX bei Bedarf installieren und anschließend mit einem echten Test-Build verifizieren
- Projekte als `.wix` speichern und später wieder vollständig öffnen

Das Ziel ist bewusst einfach:

> **EXE auswählen → Einstellungen festlegen → „MSI jetzt erstellen“ → fertig.**

---

## Highlights

### MSI aus EXE – ohne WiX-Handarbeit

msiBuilder erzeugt den benötigten WiX-Quellcode automatisch aus deinen Projekteinstellungen und startet den WiX-Build im Hintergrund.

### Wiederöffnbare Projekte

Jedes Projekt kann als **`.wix`-Projektdatei** gespeichert werden. Diese Datei enthält die relevanten msiBuilder-Einstellungen und kann später wieder geöffnet werden.

**Wichtig:** Die `.wix`-Datei ist eine **msiBuilder-Projektdatei** und **keine WiX-XML-Datei**. Der technische WiX-Quellcode verwendet weiterhin die Endung `.wxs`.

### Update-fähig durch stabilen UpgradeCode

Beim Erstellen eines neuen Projekts erzeugt msiBuilder einen **UpgradeCode**. Dieser wird in der `.wix`-Projektdatei gespeichert und bei späteren Versionen desselben Programms wiederverwendet.

Damit kann Windows Installer eine neue MSI als Update derselben Produktfamilie erkennen.

### Für Softwareverteilung vorbereitet

Der Reiter **Deployment** erzeugt passende `msiexec`-Befehle für z. B.:

- Microsoft Intune
- Gruppenrichtlinien / GPO
- RMM-Systeme
- Softwareverteilung
- eigene Batch-/PowerShell-Skripte

Unterstützt werden unter anderem:

- `/qn` – vollständig still
- `/quiet` – vollständig still
- `/passive` – nur Fortschritt
- `/qb` – reduzierte Oberfläche
- normale Installation
- `/norestart`
- ausführliches MSI-Logging mit `/L*V`
- zusätzliche öffentliche MSI-Properties

### Automatische Voraussetzungen-Prüfung

msiBuilder prüft automatisch:

1. ob ein **.NET SDK 6.0 oder neuer** installiert ist,
2. ob das **WiX Toolset** verfügbar ist,
3. ob WiX tatsächlich ein MSI bauen kann,
4. und – falls erforderlich – ob der **WiX-EULA** zugestimmt wurde.

Nach einer WiX-Installation wird nicht einfach nur `wix --version` geprüft. msiBuilder erstellt zusätzlich ein kleines temporäres Test-MSI. Erst wenn dieser Test erfolgreich ist, gilt WiX als einsatzbereit.

---

## Schnellstart

### 1. msiBuilder starten

Starte `msiBuilder.exe`.

Beim Programmstart werden die Voraussetzungen im Hintergrund geprüft. Die Oberfläche bleibt dabei direkt verfügbar.

### 2. EXE auswählen

Im Reiter **Projekt** bei **Programm-EXE** die Anwendung auswählen, aus der ein MSI erstellt werden soll.

### 3. Ausgabeordner festlegen

Wähle den Ordner, in dem die fertige MSI und die Projektdatei gespeichert werden sollen.

### 4. Produktdaten eintragen

Im Bereich **Produktdaten** werden unter anderem festgelegt:

- Produktname
- Hersteller
- Version
- Architektur
- UpgradeCode

Den **UpgradeCode bei späteren Versionen desselben Produkts nicht ändern**.

### 5. Installationsoptionen festlegen

Optional können Verknüpfungen erzeugt werden:

- Startmenü
- Desktop

### 6. MSI erstellen

Klicke auf **„MSI jetzt erstellen“** oder drücke **F5**.

Fehlt WiX, führt msiBuilder durch die notwendige Installation und Prüfung. Nach erfolgreicher Einrichtung kann der ursprünglich gestartete Build automatisch fortgesetzt werden.

---

## Die Oberfläche

### Reiter „Projekt“

Hier wird das eigentliche MSI-Projekt definiert:

- Programm-EXE
- Ausgabeordner
- Produktname
- Hersteller
- Version
- Architektur
- UpgradeCode
- Startmenü-Verknüpfung
- Desktop-Verknüpfung
- optionales Source-Archiv

### Reiter „Deployment“

Hier stellst du ein, wie das fertige MSI später verteilt oder automatisiert installiert werden soll.

msiBuilder zeigt daraus direkt einen fertigen `msiexec`-Befehl an, der kopiert und beispielsweise in GPO, RMM oder Skripten verwendet werden kann.

### Reiter „WiX-Code“

Der von msiBuilder erzeugte WiX-Quellcode kann hier eingesehen und direkt bearbeitet werden.

Du kannst:

- automatisch erzeugten Code prüfen,
- ihn manuell anpassen,
- `.wxs`-Dateien importieren,
- WiX-Code separat als `.wxs` speichern,
- oder den Code jederzeit erneut aus den Projektdaten erzeugen.

Wird eigener WiX-Code verwendet, kann dieser zusammen mit dem Projekt gespeichert werden.

### Reiter „Build-Log“

Hier erscheinen:

- Prüfungen der Voraussetzungen
- WiX-Ausgaben
- Installationsstatus
- Build-Ausgaben
- Fehlermeldungen

Wenn ein MSI-Build fehlschlägt, ist dies die erste Stelle für die Fehlersuche.

---

## Projektdateien und Ausgabe

Standardmäßig bleibt der Zielordner bewusst sauber:

```text
Ausgabeordner\
├── MeinProgramm-1.0.0.msi
└── MeinProgramm.wix
```

Dabei ist:

- `MeinProgramm-1.0.0.msi` → der fertige Installer
- `MeinProgramm.wix` → die wiederöffnbare msiBuilder-Projektdatei

Die von WiX erzeugte `.wixpdb` wird für den normalen Workflow nicht benötigt und nach erfolgreichem Build entfernt.

### Optional: vollständige Quelldaten archivieren

Aktivierst du:

**„Quelldateien und Build-Daten im Ordner source speichern“**

entsteht zusätzlich:

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

Damit kann ein Projekt inklusive der verwendeten Programmdatei und der technischen Build-Daten archiviert werden.

Bei aktivierter Source-Archivierung speichert die `.wix`-Projektdatei den Pfad zur EXE relativ. Dadurch lässt sich der gesamte Projektordner verschieben oder sichern und später wieder öffnen.

---

## Updates für ein bestehendes Programm erstellen

Für ein Update sollte nicht jedes Mal ein neues Projekt begonnen werden.

Empfohlener Ablauf:

1. vorhandene `.wix`-Projektdatei öffnen,
2. neue EXE auswählen bzw. die archivierte EXE ersetzen,
3. Versionsnummer erhöhen,
4. **UpgradeCode unverändert lassen**,
5. neues MSI erstellen.

Beispiel:

```text
Version 1.0.0
UpgradeCode: {ABCDEF12-3456-7890-ABCD-EF1234567890}

Version 1.1.0
UpgradeCode: {ABCDEF12-3456-7890-ABCD-EF1234567890}
```

Der UpgradeCode identifiziert die Produktfamilie. Genau deshalb wird er dauerhaft in der `.wix`-Projektdatei gespeichert.

---

## Voraussetzungen

### Windows

msiBuilder ist für Windows ausgelegt. Das erzeugte MSI verwendet Windows Installer.

### .NET SDK

Für WiX wird mindestens benötigt:

```text
.NET SDK 6.0 oder neuer
```

msiBuilder prüft nicht nur, ob `dotnet` vorhanden ist, sondern wertet die tatsächlich installierten SDK-Versionen aus.

Beispiel:

```text
2.1.202
```

ist **zu alt**.

Sind mehrere SDKs installiert, reicht mindestens eine kompatible Version, z. B.:

```text
2.1.202
8.0.414
```

→ **einsatzbereit**.

### WiX Toolset

WiX wird extern verwendet und ist nicht Bestandteil von msiBuilder.

Falls WiX fehlt, kann msiBuilder die Installation über das .NET SDK anstoßen:

```cmd
dotnet tool install --global wix
```

Nach der Installation folgt automatisch ein echter Funktionstest.

### WiX-EULA

Bei WiX-Versionen, die eine ausdrückliche Zustimmung verlangen, erkennt msiBuilder diesen Zustand beim Funktionstest und bietet die notwendige Zustimmung an.

WiX ist ein eigenständiges Projekt. Es gelten dessen eigene Lizenz-, EULA- und gegebenenfalls Maintenance-Bedingungen.

---

## Tastenkürzel

| Tastenkürzel | Funktion |
|---|---|
| `Ctrl+O` | Programm-EXE auswählen |
| `Ctrl+L` | msiBuilder-Projekt (`.wix`) öffnen |
| `Ctrl+S` | Projekt speichern |
| `Ctrl+Shift+O` | Ausgabeordner öffnen |
| `F5` | MSI jetzt erstellen |
| `F6` | Voraussetzungen prüfen |
| `F1` | Über msiBuilder |

Zusätzlich stehen die wichtigsten Funktionen über die klassische Menüleiste zur Verfügung.

---

## Typischer Deployment-Befehl

Für eine vollständig stille Installation eignet sich beispielsweise:

```cmd
msiexec /i "MeinProgramm-1.0.0.msi" /qn /norestart /L*V "MeinProgramm-install.log"
```

Eine stille Deinstallation kann über Windows Installer ebenfalls automatisiert werden. Wenn die Source-Archivierung aktiviert ist, legt msiBuilder zusätzlich passende `install.cmd`- und `uninstall.cmd`-Hilfsdateien ab.

---

## Eigene WiX-Anpassungen

Für Standardprojekte ist kein eigener WiX-Code notwendig.

Wer mehr Kontrolle benötigt, kann den automatisch erzeugten Code im Reiter **WiX-Code** direkt bearbeiten. Dadurch lassen sich spezielle WiX-Szenarien ergänzen, ohne auf die Projektverwaltung von msiBuilder verzichten zu müssen.

Der aktuelle Code kann jederzeit wieder aus den Projektangaben neu erzeugt werden.

---

## Fehlerbehebung

### „.NET SDK ist zu alt“

Installiere ein aktuelles .NET SDK ab Version 6.0 und starte anschließend **Voraussetzungen prüfen** erneut.

### „WiX wurde nicht gefunden“

Nutze **Werkzeuge → WiX installieren** oder starte erneut **MSI jetzt erstellen**. msiBuilder kann die Installation automatisch anstoßen.

### WiX ist installiert, aber der Build funktioniert nicht

msiBuilder führt einen echten Test-Build durch. Details stehen im **Build-Log**. Bei einer noch nicht akzeptierten WiX-EULA wird die Zustimmung automatisch angeboten.

### MSI-Build schlägt bei eigenem WiX-Code fehl

Im Reiter **WiX-Code** prüfen, ob der manuell angepasste `.wxs`-Code gültig ist. Alternativ **„Aus Projektdaten neu erzeugen“** verwenden.

### Update installiert sich nicht wie erwartet

Prüfen, ob für alle Versionen derselben Anwendung derselbe **UpgradeCode** verwendet wurde. Am sichersten ist es, für Updates immer die ursprüngliche `.wix`-Projektdatei erneut zu öffnen.

---

## msiBuilder selbst aus dem Quellcode bauen

Im Repository befindet sich `build_onefile.bat`.

Voraussetzung dafür ist eine lokale Python-Installation mit dem Python Launcher `py`.

Danach:

```cmd
build_onefile.bat
```

Das Skript:

1. installiert bzw. aktualisiert PyInstaller,
2. entfernt alte Build-Artefakte,
3. erzeugt eine einzelne Windows-EXE,
4. bindet das msiBuilder-Icon ein.

Die fertige Anwendung liegt anschließend unter:

```text
dist\msiBuilder.exe
```

Für Benutzer der fertigen EXE ist keine Python-Installation notwendig.

---

## Projektstruktur

```text
msiBuilder/
├── msibuilder.py
├── msibuilder.ico
├── msibuilder_icon.png
├── build_onefile.bat
├── README.md
├── README_DE.md
└── LICENSE
```

---

## Lizenz

msiBuilder wird unter der **MIT License** veröffentlicht.

WiX ist **nicht Bestandteil** dieses Projekts und wird als externes Tool verwendet. Für WiX gelten die eigenen Lizenz- und Nutzungsbedingungen.

---

## Repository Description

> **A modern Windows GUI for building MSI installers from EXE files using WiX, with silent deployment options and automatic prerequisite checks.**

---

## Kurz gesagt

Wenn du eine EXE hast und daraus ohne unnötige Handarbeit ein vernünftiges MSI für Installation, Updates oder zentrale Softwareverteilung bauen willst, soll msiBuilder genau diesen Weg möglichst kurz machen:

**Projekt öffnen → EXE wählen → MSI erstellen.**
