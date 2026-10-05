import json
import os
import queue
import re
import shutil
import subprocess
import threading
import tempfile
import uuid
import webbrowser
import xml.sax.saxutils as saxutils
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_NAME = "msiBuilder"
APP_VERSION = "1.11.0"
APP_DEVELOPER = "Fachlehrer-DEV"
PROJECT_GITHUB_URL = "https://github.com/fachlehrer-dev/msiBuilder"
PROJECT_INFO_URL = "https://fachlehrer.dev/msiBuilder"
PROJECT_CONTACT = "fred@fachlehrer.dev"
PROJECT_AUTHOR = "Fred Maier"
PROJECT_PUBLISHER = "IFL Bayreuth"
DOTNET_DOWNLOAD_URL = "https://dotnet.microsoft.com/download"
WIX_INFO_URL = "https://docs.firegiant.com/wix/using-wix/"
WIX_EULA_URL = "https://docs.firegiant.com/wix/osmf/"
MIN_DOTNET_SDK = (6, 0, 0)
MIN_DOTNET_SDK_TEXT = "6.0"

APP_ICON_PNG_BASE64 = "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"

TRANSLATIONS = {
    "en": {
        "subtitle": "Select an EXE · Build an MSI with WiX · Prepare software deployment",
        "info": "Info", "recheck": "Check again", "ready": "Ready for MSI build and software deployment.",
        "build_msi": "Build MSI", "build_msi_now": "Create MSI now", "open_output": "Open output folder",
        "tab_project": "Project", "tab_filetypes": "File types", "tab_deploy": "Deployment", "tab_log": "Build log",
        "filetypes_title": "File associations", "filetypes_help": "Register one or more file extensions for the installed application. Windows will list the application under Open with / Default apps. Existing user defaults cannot be overwritten silently on Windows 10/11.",
        "filetype_extension": "Extension", "filetype_description": "Description", "filetype_add": "Add / update", "filetype_remove": "Remove selected", "filetype_example": "Examples: .csv, .md, .myfile", "filetype_target": "Files are opened with the installed application and passed as the first argument (\"%1\").",
        "filetype_invalid": "Please enter a valid file extension, for example .csv.", "filetype_default_desc": "{ext} file",
        "source_output": "Source file & output", "program_exe": "Application EXE", "output_folder": "Output folder", "keep_source": "Save source and build data in the source folder",
        "browse": "Browse…", "product_data": "Product data", "product_name": "Product name", "manufacturer": "Manufacturer",
        "version": "Version", "architecture": "Architecture", "installer_options": "Installer options",
        "start_menu": "Create Start menu shortcut", "desktop": "Create desktop shortcut",
        "upgrade_code": "UpgradeCode (keep unchanged for future updates)", "new": "New",
        "upgrade_help": "Keep the same UpgradeCode for later versions of the same product.",
        "visibility": "Installation visibility", "visibility_help": "How much should the user see during installation?",
        "automatic_behavior": "Automatic behavior", "no_restart": "Prevent automatic restart",
        "no_restart_help": "/norestart – the installer will not restart the PC itself. Exit code 3010 can still report that a restart is required.",
        "logging": "Write a verbose installation log", "logging_help": "/L*V – useful for managed deployment and troubleshooting.",
        "logfile": "Log file", "scripts": "Generate install.cmd and uninstall.cmd",
        "advanced": "Advanced MSI parameters", "advanced_help": "Only use this if your deployment system needs additional public MSI properties.",
        "examples": "Examples:  REBOOT=ReallySuppress   PROPERTY=Value",
        "per_machine": "Note: The generated MSI is already configured as a per-machine installation.",
        "deploy_command": "Deployment command", "deploy_command_help": "Use this command in software deployment, GPO, RMM or your own scripts.",
        "copy": "Copy command", "recommended": "Recommended deployment", "recommended_help": "Recommended: silent + no automatic restart + log",
        "language": "Language", "settings_saved": "Language is saved in your AppData settings.",
        "checking": "checking…", "not_found": "not found ✗", "installing": "installing…", "install_failed": "installation failed ✗",
        "log_ready": "Ready. Checking prerequisites…",
        "select_exe": "Select application EXE", "windows_apps": "Windows applications", "all_files": "All files", "select_output": "Select output folder",
        "sdk_missing_title": "Missing prerequisite", "sdk_missing": "No .NET SDK was found.\n\nPlease install a current .NET SDK first, then choose ‘Check again’.\n\nWithout the .NET SDK, WiX cannot be installed automatically.",
        "wix_missing_title": "WiX Toolset is missing", "wix_missing": "WiX was not found.\n\nWould you like to install WiX automatically using the .NET SDK?\n\nThe following command will be run:\ndotnet tool install --global wix\n\nNote: WiX is an external project and is subject to its own license/EULA and, where applicable, maintenance-fee terms.",
        "wix_installed_title": "WiX installed", "wix_installed": "WiX has been installed. msiBuilder is now testing whether WiX can actually build an MSI and whether the required EULA has already been accepted.",
        "wix_test_running": "testing…", "wix_test_ok": "ready ✓", "wix_test_title": "WiX functional test",
        "wix_test_success": "WiX is fully ready. A temporary test MSI was built successfully.",
        "wix_test_eula": "WiX is installed correctly, but WiX 7 still requires explicit EULA acceptance before MSI packages can be built. Would you like to accept it now?",
        "wix_test_failed": "WiX is installed, but the functional test failed. See the build log for details.",
        "wix_install_failed": "WiX installation failed (exit code {rc}).\n\nSee the build log for details.",
        "exe_required": "Please select an existing EXE file.", "meta_required": "Product name and manufacturer must not be empty.",
        "guid_invalid": "The UpgradeCode is not a valid GUID.", "sdk_build_missing": "No compatible .NET SDK was found. WiX requires .NET SDK 6.0 or newer.",
        "sdk_build_too_old": "The installed .NET SDK is too old for WiX.\n\nInstalled: {installed}\nRequired: .NET SDK {required} or newer.",
        "wix_build_missing": "WiX was not found. Would you like to install it now using ‘dotnet tool install --global wix’?",
        "wix_cannot_start": "WiX was found but could not be started.",
        "build_success": "MSI successfully created:\n{path}", "build_failed": "WiX build failed (exit code {rc}). See the build log for details.",
        "wix_not_found": "WiX was not found. Please check the prerequisites again.",
        "about_title": "About this project", "close": "Close",
        "about_license": "This project/application is published on GitHub under the MIT License.",
        "download": "Download:", "more_info": "More information:", "developed_by": "Developed by {name}",
        "published_by": "Published by {name}", "contact": "Contact:", "wix_note_title": "Note about WiX Toolset",
        "wix_note": "WiX is not part of this MIT-licensed project. It is installed separately and called as an external command-line tool. WiX is subject to its own license and usage terms.",
        "wix_info": "Open WiX information",
        "mode_qn": "Fully silent – /qn (recommended)", "mode_qn_help": "No windows and no prompts. Ideal for Intune, GPO, RMM, software deployment or scripts.",
        "mode_quiet": "Fully silent – /quiet", "mode_quiet_help": "Also runs without a user interface. For msiexec this is effectively a silent installation.",
        "mode_passive": "Progress only – /passive", "mode_passive_help": "Shows progress only. The user cannot control or cancel the installation.",
        "mode_qb": "Basic interface – /qb", "mode_qb_help": "Shows a reduced Windows Installer interface. Usually unnecessary for fully automated deployment.",
        "mode_normal": "Normal installation", "mode_normal_help": "No UI reduction. Windows Installer uses its normal interface.",
    },
    "de": {
        "subtitle": "EXE auswählen · MSI mit WiX bauen · Softwareverteilung vorbereiten",
        "info": "Info", "recheck": "Neu prüfen", "ready": "Bereit für MSI-Build und Softwareverteilung.",
        "build_msi": "MSI erstellen", "build_msi_now": "MSI jetzt erstellen", "open_output": "Projektordner öffnen",
        "tab_project": "Projekt", "tab_deploy": "Verteilung", "tab_log": "Build-Log",
        "source_output": "Quelldatei & Ausgabe", "program_exe": "Programm-EXE", "output_folder": "Ausgabeordner", "keep_source": "Quelldateien und Build-Daten im Ordner source speichern",
        "browse": "Auswählen…", "product_data": "Produktdaten", "product_name": "Produktname", "manufacturer": "Hersteller",
        "version": "Version", "architecture": "Architektur", "installer_options": "Installer-Optionen",
        "start_menu": "Startmenü-Verknüpfung erstellen", "desktop": "Desktop-Verknüpfung erstellen",
        "upgrade_code": "UpgradeCode (für spätere Updates konstant halten)", "new": "Neu",
        "upgrade_help": "Für dasselbe Produkt den UpgradeCode bei späteren Versionen beibehalten.",
        "visibility": "Sichtbarkeit der Installation", "visibility_help": "Wie viel soll der Benutzer während der Installation sehen?",
        "automatic_behavior": "Automatisches Verhalten", "no_restart": "Automatischen Neustart verhindern",
        "no_restart_help": "/norestart – der Installer startet den PC nicht selbst neu. Ein Rückgabecode 3010 kann trotzdem „Neustart erforderlich“ melden.",
        "logging": "Ausführliches Installations-Log schreiben", "logging_help": "/L*V – hilfreich bei zentraler Verteilung und Fehlersuche.",
        "logfile": "Logdatei", "scripts": "install.cmd und uninstall.cmd erzeugen",
        "advanced": "Erweiterte MSI-Parameter", "advanced_help": "Nur verwenden, wenn deine Softwareverteilung zusätzliche öffentliche MSI-Properties benötigt.",
        "examples": "Beispiele:  REBOOT=ReallySuppress   PROPERTY=Wert",
        "per_machine": "Hinweis: Das erzeugte MSI ist bereits als Installation für den Computer (per-machine) konfiguriert.",
        "deploy_command": "Fertiger Deployment-Befehl", "deploy_command_help": "Diesen Befehl kannst du z. B. in Softwareverteilung, GPO, RMM oder einem eigenen Skript verwenden.",
        "copy": "Befehl kopieren", "recommended": "Empfohlene Verteilung", "recommended_help": "Empfohlen: still + kein automatischer Neustart + Log",
        "language": "Sprache", "settings_saved": "Die Sprache wird in den AppData-Einstellungen gespeichert.",
        "checking": "prüfe…", "not_found": "nicht gefunden ✗", "installing": "wird installiert…", "install_failed": "Installation fehlgeschlagen ✗",
        "log_ready": "Bereit. Voraussetzungen werden geprüft…",
        "select_exe": "Programm-EXE auswählen", "windows_apps": "Windows-Programme", "all_files": "Alle Dateien", "select_output": "Ausgabeordner auswählen",
        "sdk_missing_title": "Voraussetzung fehlt", "sdk_missing": "Es wurde kein .NET SDK gefunden.\n\nBitte installieren Sie zuerst .NET SDK 6.0 oder neuer. Danach ‘Neu prüfen’ wählen.\n\nOhne kompatibles .NET SDK kann WiX nicht automatisch installiert werden.",
        "sdk_too_old_title": ".NET SDK ist zu alt", "sdk_too_old": "Ein .NET SDK ist installiert, aber für WiX zu alt.\n\nInstalliert: {installed}\nErforderlich: .NET SDK {required} oder neuer\n\nBitte installieren Sie ein aktuelles .NET SDK und wählen Sie danach ‘Neu prüfen’.",
        "sdk_too_old_status": "{version} – zu alt ✗",
        "wix_missing_title": "WiX Toolset fehlt", "wix_missing": "WiX wurde nicht gefunden.\n\nMöchten Sie WiX jetzt automatisch über das .NET SDK installieren?\n\nAusgeführt wird:\ndotnet tool install --global wix\n\nHinweis: WiX ist ein externes Projekt. Es gelten die eigenen WiX-Lizenz-/EULA- und ggf. Maintenance-Fee-Bedingungen.",
        "wix_installed_title": "WiX installiert", "wix_installed": "WiX wurde installiert. msiBuilder prüft jetzt automatisch, ob WiX tatsächlich ein MSI bauen kann und ob der erforderlichen EULA bereits zugestimmt wurde.",
        "wix_test_running": "wird getestet…", "wix_test_ok": "einsatzbereit ✓", "wix_test_title": "WiX-Funktionstest",
        "wix_test_success": "WiX ist vollständig einsatzbereit. Ein temporäres Test-MSI wurde erfolgreich erstellt.",
        "wix_test_eula": "WiX ist korrekt installiert, aber WiX 7 verlangt vor dem Erstellen von MSI-Paketen noch die ausdrückliche Zustimmung zur EULA. Jetzt zustimmen?",
        "wix_test_failed": "WiX ist installiert, aber der Funktionstest ist fehlgeschlagen. Details stehen im Build-Log.",
        "wix_install_failed": "Die WiX-Installation ist fehlgeschlagen (Exitcode {rc}).\n\nDetails stehen im Build-Log.",
        "exe_required": "Bitte eine vorhandene EXE auswählen.", "meta_required": "Produktname und Hersteller dürfen nicht leer sein.",
        "guid_invalid": "Der UpgradeCode ist keine gültige GUID.", "sdk_build_missing": "Kein kompatibles .NET SDK gefunden. WiX benötigt .NET SDK 6.0 oder neuer.",
        "sdk_build_too_old": "Das installierte .NET SDK ist für WiX zu alt.\n\nInstalliert: {installed}\nErforderlich: .NET SDK {required} oder neuer.",
        "wix_build_missing": "WiX wurde nicht gefunden. Möchten Sie es jetzt über ‘dotnet tool install --global wix’ installieren?",
        "wix_cannot_start": "WiX wurde gefunden, konnte aber nicht gestartet werden.",
        "build_success": "MSI erfolgreich erstellt:\n{path}", "build_failed": "WiX-Build fehlgeschlagen (Exitcode {rc}). Details stehen im Build-Log.",
        "wix_not_found": "WiX wurde nicht gefunden. Bitte Voraussetzungen erneut prüfen.",
        "about_title": "Über dieses Projekt", "close": "Schließen",
        "about_license": "Dieses Projekt/Programm wurde unter der MIT-Lizenz auf GitHub veröffentlicht.",
        "download": "Download:", "more_info": "Weitere Informationen:", "developed_by": "Entwickelt von {name}",
        "published_by": "Herausgegeben von {name}", "contact": "Kontakt:", "wix_note_title": "Hinweis zu WiX Toolset",
        "wix_note": "WiX ist nicht Bestandteil dieses MIT-lizenzierten Projekts. Es wird als externes Kommandozeilenwerkzeug separat installiert und aufgerufen. Für WiX gelten die eigenen Lizenz- und Nutzungsbedingungen.",
        "wix_info": "Informationen zu WiX öffnen",
        "mode_qn": "Vollständig still – /qn (empfohlen)", "mode_qn_help": "Keine Fenster, keine Rückfragen. Ideal für Intune, GPO, RMM, Softwareverteilung oder Skripte.",
        "mode_quiet": "Vollständig still – /quiet", "mode_quiet_help": "Ebenfalls vollständig ohne Benutzeroberfläche. Entspricht bei msiexec praktisch der stillen Installation.",
        "mode_passive": "Nur Fortschritt – /passive", "mode_passive_help": "Zeigt nur den Fortschritt. Der Benutzer kann die Installation nicht steuern oder abbrechen.",
        "mode_qb": "Einfache Oberfläche – /qb", "mode_qb_help": "Zeigt eine reduzierte Windows-Installer-Oberfläche. Für vollautomatische Verteilung meist nicht nötig.",
        "mode_normal": "Normale Installation", "mode_normal_help": "Keine UI-Reduzierung. Windows Installer zeigt die normale Benutzeroberfläche.",
    }
}


TRANSLATIONS["en"].update({
    "wix_file_menu_hint": "WiX source import/export is available from the File menu",
    "open_project": "Open msiBuilder project", "save_project": "Save msiBuilder project", "project_files": "msiBuilder projects", "project_invalid": "This is not a valid msiBuilder project file.", "project_loaded": "Project loaded successfully.", "project_load_failed": "The project could not be loaded: {error}",
    "menu_file": "File", "menu_open_exe": "Open application EXE…", "menu_open_project": "Open project…", "menu_save_project": "Save project…", "menu_load_wix": "Load WiX code…",
    "menu_save_wix": "Save WiX code…", "menu_close_wix": "Close loaded WiX code", "menu_exit": "Exit",
    "menu_build": "Build", "menu_build_msi": "Build MSI", "menu_open_output": "Open output folder",
    "menu_tools": "Tools", "menu_check": "Check prerequisites", "menu_install_wix": "Install WiX…",
    "menu_language": "Language", "menu_help": "Help", "menu_about": "About msiBuilder",
    "tab_wix": "WiX Code", "wix_editor_title": "WiX source code",
    "wix_editor_help": "The MSI build uses the code shown here. You can edit it directly, save it as .wxs and load it again later.",
    "wix_regenerate": "Regenerate from project data", "wix_generated": "Generated from project data",
    "wix_custom": "Custom / loaded WiX code", "wix_saved": "WiX code saved.", "wix_loaded": "WiX code loaded.",
    "wix_closed": "Loaded WiX code closed. Automatic generation is active again.",
    "select_wix": "Select WiX source file", "save_wix": "Save WiX source file", "wix_files": "WiX source files",
    "arch_hint": "Target architecture",
    "menu_wix_eula": "Accept WiX EULA…",
    "wix_eula_title": "WiX 7 EULA acceptance required",
    "wix_eula_prompt": "WiX 7 requires an explicit acceptance of its OSMF EULA before it can build an MSI.\n\nPlease read the WiX terms first. If you choose ‘Yes’, msiBuilder will run:\n\nwix eula accept wix7\n\nAcceptance is stored by WiX for the current user on this computer. Continue?",
    "wix_eula_open": "Open WiX EULA / OSMF terms",
    "wix_eula_accepting": "Accepting WiX EULA…",
    "wix_eula_ok": "The WiX 7 EULA was accepted successfully. You can now build MSI packages.",
    "wix_eula_failed": "WiX EULA acceptance failed (exit code {rc}). See the build log for details.",
})
TRANSLATIONS["de"].update({
    "wix_file_menu_hint": "WiX-Quellcode kann über das Datei-Menü importiert/exportiert werden",
    "open_project": "msiBuilder-Projekt öffnen", "save_project": "msiBuilder-Projekt speichern", "project_files": "msiBuilder-Projekte", "project_invalid": "Dies ist keine gültige msiBuilder-Projektdatei.", "project_loaded": "Projekt wurde erfolgreich geladen.", "project_load_failed": "Das Projekt konnte nicht geladen werden: {error}",
    "menu_file": "Datei", "menu_open_exe": "Programm-EXE öffnen…", "menu_open_project": "Projekt öffnen…", "menu_save_project": "Projekt speichern…", "menu_load_wix": "WiX-Code laden…",
    "menu_save_wix": "WiX-Code speichern…", "menu_close_wix": "Geladenen WiX-Code schließen", "menu_exit": "Beenden",
    "menu_build": "Erstellen", "menu_build_msi": "MSI erstellen", "menu_open_output": "Ausgabeordner öffnen",
    "menu_tools": "Werkzeuge", "menu_check": "Voraussetzungen prüfen", "menu_install_wix": "WiX installieren…",
    "menu_language": "Sprache", "menu_help": "Hilfe", "menu_about": "Über msiBuilder",
    "tab_wix": "WiX-Code", "wix_editor_title": "WiX-Quellcode",
    "wix_editor_help": "Für den MSI-Build wird der hier angezeigte Code verwendet. Du kannst ihn direkt bearbeiten, als .wxs speichern und später wieder laden.",
    "wix_regenerate": "Aus Projektdaten neu erzeugen", "wix_generated": "Aus Projektdaten erzeugt",
    "wix_custom": "Eigener / geladener WiX-Code", "wix_saved": "WiX-Code gespeichert.", "wix_loaded": "WiX-Code geladen.",
    "wix_closed": "Geladener WiX-Code geschlossen. Die automatische Erzeugung ist wieder aktiv.",
    "select_wix": "WiX-Quelldatei auswählen", "save_wix": "WiX-Quelldatei speichern", "wix_files": "WiX-Quelldateien",
    "arch_hint": "Zielarchitektur",
    "menu_wix_eula": "WiX-EULA zustimmen…",
    "wix_eula_title": "Zustimmung zur WiX-7-EULA erforderlich",
    "wix_eula_prompt": "WiX 7 verlangt vor dem Erstellen einer MSI eine ausdrückliche Zustimmung zur OSMF-EULA.\n\nBitte lesen Sie zuerst die WiX-Bedingungen. Wenn Sie ‘Ja’ wählen, führt msiBuilder folgenden Befehl aus:\n\nwix eula accept wix7\n\nDie Zustimmung wird von WiX für den aktuellen Benutzer auf diesem Computer gespeichert. Fortfahren?",
    "wix_eula_open": "WiX-EULA / OSMF-Bedingungen öffnen",
    "wix_eula_accepting": "WiX-EULA wird bestätigt…",
    "wix_eula_ok": "Der WiX-7-EULA wurde erfolgreich zugestimmt. MSI-Pakete können jetzt erstellt werden.",
    "wix_eula_failed": "Die Zustimmung zur WiX-EULA ist fehlgeschlagen (Exitcode {rc}). Details stehen im Build-Log.",
})

TRANSLATIONS["en"].update({
    "filename_options": "MSI file name",
    "filename_prefix": "Prefix",
    "filename_suffix": "Suffix",
    "filename_preview": "File name preview",
    "filename_optional": "optional",
    "filename_help": "Prefix and suffix are optional. msiBuilder inserts the underscore automatically.",
    "filetype_progid_hint": "ProgID is generated automatically for each extension and normally does not need to be edited.",
})
TRANSLATIONS["de"].update({
    "filename_options": "MSI-Dateiname",
    "filename_prefix": "Präfix",
    "filename_suffix": "Suffix",
    "filename_preview": "Dateinamenvorschau",
    "filename_optional": "optional",
    "filename_help": "Präfix und Suffix sind optional. Den Unterstrich setzt msiBuilder automatisch.",
    "filetype_progid_hint": "Die ProgID wird für jede Dateiendung automatisch erzeugt und muss normalerweise nicht bearbeitet werden.",
})

MODE_FLAGS = {"qn": "/qn", "quiet": "/quiet", "passive": "/passive", "qb": "/qb", "normal": ""}
MODE_ORDER = ["qn", "quiet", "passive", "qb", "normal"]


def settings_path():
    base = Path(os.environ.get("APPDATA") or (Path.home() / "AppData" / "Roaming"))
    return base / APP_NAME / "settings.json"


def load_settings():
    try:
        data = json.loads(settings_path().read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_settings(data):
    try:
        path = settings_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def esc(value):
    return saxutils.escape(value or "", {'"': '&quot;'})


def safe_filename(value):
    value = re.sub(r'[<>:"/\\|?*]+', '_', value.strip())
    value = re.sub(r'\s+', '_', value)
    return value or "Setup"


def normalize_version(value):
    parts = re.findall(r'\d+', value or '')[:4]
    if not parts:
        return "1.0.0"
    while len(parts) < 3:
        parts.append('0')
    return '.'.join(str(int(p)) for p in parts)


def no_window_flag():
    return subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0


def run_capture(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace', creationflags=no_window_flag())
        return p.returncode, (p.stdout or '').strip(), (p.stderr or '').strip()
    except FileNotFoundError:
        return 127, '', 'not found'
    except Exception as exc:
        return 1, '', str(exc)


def parse_dotnet_sdks(output):
    """Return installed SDKs as [(version_tuple, raw_version), ...]."""
    sdks = []
    for line in (output or '').splitlines():
        raw = line.strip().split()[0] if line.strip() else ''
        m = re.match(r'^(\d+)\.(\d+)(?:\.(\d+))?', raw)
        if not m:
            continue
        version = (int(m.group(1)), int(m.group(2)), int(m.group(3) or 0))
        sdks.append((version, raw))
    return sdks


def dotnet_sdk_status():
    """Return (compatible, best_raw_version, all_sdks, command_ok)."""
    rc, out, _ = run_capture(['dotnet', '--list-sdks'])
    if rc != 0:
        return False, '', [], False
    sdks = parse_dotnet_sdks(out)
    if not sdks:
        return False, '', [], True
    sdks.sort(key=lambda item: item[0])
    compatible = [item for item in sdks if item[0] >= MIN_DOTNET_SDK]
    best = (compatible[-1] if compatible else sdks[-1])[1]
    return bool(compatible), best, sdks, True


def find_wix_executable():
    found = shutil.which('wix') or shutil.which('wix.exe')
    if found:
        return found
    candidate = Path.home() / '.dotnet' / 'tools' / ('wix.exe' if os.name == 'nt' else 'wix')
    return str(candidate) if candidate.is_file() else None


class ModernStyle:
    BG = '#f4f7fb'; CARD = '#ffffff'; TEXT = '#172033'; MUTED = '#687386'; ACCENT = '#0891b2'; ACCENT_HOVER = '#0e7490'
    BORDER = '#cbd5e1'; SOFT = '#e8f7fb'; DARK = '#0f172a'

    @classmethod
    def apply(cls, root):
        root.configure(bg=cls.BG)
        style = ttk.Style(root)
        try: style.theme_use('clam')
        except tk.TclError: pass
        style.configure('.', font=('Segoe UI', 10), background=cls.BG, foreground=cls.TEXT)
        style.configure('TFrame', background=cls.BG); style.configure('Card.TFrame', background=cls.CARD)
        style.configure('Title.TLabel', background=cls.BG, foreground=cls.TEXT, font=('Segoe UI Semibold', 20))
        style.configure('Subtitle.TLabel', background=cls.BG, foreground=cls.MUTED, font=('Segoe UI', 10))
        style.configure('CardTitle.TLabel', background=cls.CARD, foreground=cls.TEXT, font=('Segoe UI Semibold', 11))
        style.configure('SectionTitle.TLabel', background=cls.BG, foreground=cls.TEXT, font=('Segoe UI Semibold', 11))
        style.configure('CardText.TLabel', background=cls.CARD, foreground=cls.TEXT)
        style.configure('Muted.TLabel', background=cls.CARD, foreground=cls.MUTED, font=('Segoe UI', 9))
        style.configure('Info.TLabel', background=cls.SOFT, foreground=cls.TEXT, font=('Segoe UI', 9))
        style.configure('Status.TLabel', background=cls.BG, foreground=cls.MUTED, font=('Segoe UI', 9))
        style.configure('Accent.TButton', background=cls.ACCENT, foreground='white', borderwidth=1, relief='solid', bordercolor=cls.ACCENT_HOVER, padding=(14, 9), font=('Segoe UI Semibold', 10))
        style.map('Accent.TButton', background=[('active', cls.ACCENT_HOVER), ('disabled', '#9ca3af')])
        style.configure('Secondary.TButton', background='#f8fafc', foreground=cls.TEXT, borderwidth=1, relief='solid', bordercolor=cls.BORDER, padding=(12, 8))
        style.map('Secondary.TButton', background=[('active', '#eaf0f6')], bordercolor=[('active', '#94a3b8')])
        style.configure('TEntry', fieldbackground='white', bordercolor=cls.BORDER, padding=7)
        style.configure('Segment.TButton', background='#f8fafc', foreground=cls.TEXT, borderwidth=1, relief='solid', bordercolor=cls.BORDER, padding=(12, 7))
        style.map('Segment.TButton', background=[('active', '#eaf0f6')], bordercolor=[('active', '#94a3b8')])
        style.configure('SegmentSelected.TButton', background=cls.SOFT, foreground=cls.ACCENT_HOVER, borderwidth=1, relief='solid', bordercolor=cls.ACCENT, padding=(12, 7), font=('Segoe UI Semibold', 10))
        style.map('SegmentSelected.TButton', background=[('active', '#d9f2f8')])
        style.configure('Choice.TRadiobutton', background=cls.CARD, foreground=cls.TEXT, padding=(4,4))
        style.map('Choice.TRadiobutton', background=[('active', cls.CARD)])
        style.configure('TCheckbutton', background=cls.CARD, foreground=cls.TEXT)
        style.map('TCheckbutton', background=[('active', cls.CARD)])
        style.configure('TNotebook', background=cls.BG, borderwidth=0)
        style.configure('TNotebook.Tab', padding=(22, 9), background='#e8eef5', foreground=cls.MUTED, borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', cls.CARD), ('active', '#eef3f8')], foreground=[('selected', cls.TEXT)], padding=[('selected', (22, 9)), ('!selected', (22, 9))])


class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, *, padding=(0,0,0,0)):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg=ModernStyle.BG, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas, padding=padding)
        self.window_id = self.canvas.create_window((0,0), window=self.inner, anchor='nw')
        self._scrollbar_visible = False
        self.canvas.configure(yscrollcommand=self._on_scroll)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.inner.bind('<Configure>', self._refresh_scrollregion)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.canvas.bind('<Enter>', lambda e: self.canvas.bind_all('<MouseWheel>', self._wheel))
        self.canvas.bind('<Leave>', lambda e: self.canvas.unbind_all('<MouseWheel>'))

    def _refresh_scrollregion(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.after_idle(self._update_scrollbar_visibility)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)
        self.after_idle(self._update_scrollbar_visibility)

    def _on_scroll(self, first, last):
        self.scrollbar.set(first, last)
        needs_scrollbar = float(first) > 0.0 or float(last) < 1.0
        if needs_scrollbar and not self._scrollbar_visible:
            self.scrollbar.pack(side='right', fill='y')
            self._scrollbar_visible = True
        elif not needs_scrollbar and self._scrollbar_visible:
            self.scrollbar.pack_forget()
            self._scrollbar_visible = False

    def _update_scrollbar_visibility(self):
        bbox = self.canvas.bbox('all')
        if not bbox:
            return
        content_height = bbox[3] - bbox[1]
        viewport_height = self.canvas.winfo_height()
        needs_scrollbar = content_height > viewport_height + 1
        if needs_scrollbar and not self._scrollbar_visible:
            self.scrollbar.pack(side='right', fill='y')
            self._scrollbar_visible = True
        elif not needs_scrollbar and self._scrollbar_visible:
            self.scrollbar.pack_forget()
            self._scrollbar_visible = False
            self.canvas.yview_moveto(0)

    def _wheel(self, event):
        if self._scrollbar_visible:
            self.canvas.yview_scroll(int(-event.delta/120), 'units')


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.language = self.settings.get('language', 'en') if self.settings.get('language') in ('en','de') else 'en'
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry('1040x760'); self.minsize(800, 560)
        self._app_icon = None
        self._apply_app_icon(self)
        ModernStyle.apply(self)
        self.msgq = queue.Queue(); self.wix_executable = None; self.sdk_available = False; self.sdk_version = ""; self.wix_available = False
        self._sdk_warning_shown = False; self._wix_question_shown = False; self._installing_wix = False; self._testing_wix = False; self._pending_build = False; self._building = False
        self.wix_custom = False; self.wix_loaded_path = None; self._ignore_wix_modified = False
        self._init_vars(); self._build_ui(); self._bind_shortcuts()
        self.after(150, self._poll_messages); self.after(700, lambda: self.refresh_environment(interactive=True))


    def _apply_app_icon(self, window):
        """Apply the embedded application icon without reading a runtime file."""
        try:
            if self._app_icon is None:
                self._app_icon = tk.PhotoImage(data=APP_ICON_PNG_BASE64)
            window.iconphoto(True, self._app_icon)
        except Exception:
            # Icon failure must never delay or prevent application startup.
            pass

    def t(self, key, **kwargs):
        text = TRANSLATIONS.get(self.language, TRANSLATIONS['en']).get(key, key)
        return text.format(**kwargs) if kwargs else text

    def _init_vars(self):
        self.exe_path = tk.StringVar(); self.out_dir = tk.StringVar(value=str(Path.home() / 'Desktop'))
        self.product_name = tk.StringVar(value='My Application' if self.language == 'en' else 'Meine Anwendung')
        self.manufacturer = tk.StringVar(value='M. Maier'); self.version = tk.StringVar(value='1.0.0'); self.arch = tk.StringVar(value='x64')
        self.start_menu = tk.BooleanVar(value=True); self.desktop_shortcut = tk.BooleanVar(value=False); self.keep_source = tk.BooleanVar(value=False); self.upgrade_code = tk.StringVar(value=str(uuid.uuid4()).upper())
        self.filename_prefix = tk.StringVar(); self.filename_suffix = tk.StringVar(); self.filename_preview = tk.StringVar()
        self.file_associations = []
        self.filetype_ext = tk.StringVar(); self.filetype_desc = tk.StringVar()
        self.ui_mode_key = 'qn'; self.ui_mode_display = tk.StringVar(); self.ui_mode_help = tk.StringVar()
        self.no_restart = tk.BooleanVar(value=True); self.logging = tk.BooleanVar(value=True); self.log_name = tk.StringVar(value='install.log'); self.generate_cmd = tk.BooleanVar(value=False); self.extra_props = tk.StringVar()
        self.dotnet_status = tk.StringVar(value=self.t('checking')); self.wix_status = tk.StringVar(value=self.t('checking')); self.command_preview = tk.StringVar()
        self.language_display = tk.StringVar(value='English' if self.language == 'en' else 'Deutsch')
        self.wix_code_status = tk.StringVar(value=self.t('wix_generated'))
        for var in (self.no_restart, self.logging, self.log_name, self.extra_props, self.product_name, self.version, self.filename_prefix, self.filename_suffix):
            var.trace_add('write', lambda *_: self._refresh_filename_dependent_previews())
        self._refresh_filename_dependent_previews()

    def _filename_token(self, value):
        value = (value or '').strip()
        value = re.sub(r'[<>:\"/\\|?*]+', '-', value)
        value = re.sub(r'\s+', ' ', value).strip(' ._-')
        return safe_filename(value).strip(' ._-') if value else ''

    def msi_filename(self):
        base = safe_filename(self.product_name.get().strip() or 'Application') + '-' + normalize_version(self.version.get())
        prefix = self._filename_token(self.filename_prefix.get())
        suffix = self._filename_token(self.filename_suffix.get())
        if prefix:
            base = prefix + '_' + base
        if suffix:
            base = base + '_' + suffix
        return base + '.msi'

    def _refresh_filename_dependent_previews(self):
        if hasattr(self, 'filename_preview'):
            self.filename_preview.set(self.msi_filename())
        if hasattr(self, 'command_preview'):
            self.update_command_preview()

    def _mode_label(self, key): return self.t('mode_' + key)
    def _mode_help(self, key): return self.t('mode_' + key + '_help')

    def _card(self, parent, title, row, column, columnspan=1, padx=8, pady=8):
        outer = tk.Frame(parent, bg=ModernStyle.BORDER, bd=0)
        outer.grid(row=row, column=column, columnspan=columnspan, sticky='nsew', padx=padx, pady=pady)
        inner = ttk.Frame(outer, style='Card.TFrame', padding=16); inner.pack(fill='both', expand=True, padx=1, pady=1)
        ttk.Label(inner, text=title, style='CardTitle.TLabel').pack(anchor='w', pady=(0,10)); return inner

    def _build_menu(self):
        menubar = tk.Menu(self, tearoff=False)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label=self.t('menu_open_exe'), command=self.choose_exe, accelerator='Ctrl+O', underline=0)
        file_menu.add_separator()
        file_menu.add_command(label=self.t('menu_open_project'), command=self.open_project, accelerator='Ctrl+L')
        file_menu.add_command(label=self.t('menu_save_project'), command=self.save_project, accelerator='Ctrl+S')
        file_menu.add_separator()
        file_menu.add_command(label=self.t('menu_load_wix'), command=self.load_wix_code)
        file_menu.add_command(label=self.t('menu_save_wix'), command=self.save_wix_code)
        file_menu.add_command(label=self.t('menu_close_wix'), command=self.close_wix_code)
        file_menu.add_separator()
        file_menu.add_command(label=self.t('menu_exit'), command=self.destroy, accelerator='Alt+F4')
        menubar.add_cascade(label=self.t('menu_file'), menu=file_menu, underline=0)

        build_menu = tk.Menu(menubar, tearoff=False)
        build_menu.add_command(label=self.t('menu_build_msi'), command=self.start_build, accelerator='F5')
        build_menu.add_command(label=self.t('menu_open_output'), command=self.open_output, accelerator='Ctrl+Shift+O')
        menubar.add_cascade(label=self.t('menu_build'), menu=build_menu, underline=0)

        tools_menu = tk.Menu(menubar, tearoff=False)
        tools_menu.add_command(label=self.t('menu_check'), command=lambda: self.refresh_environment(interactive=True, reset_prompts=True), accelerator='F6')
        tools_menu.add_command(label=self.t('menu_install_wix'), command=self.install_wix)
        tools_menu.add_command(label=self.t('menu_wix_eula'), command=self.accept_wix_eula)
        menubar.add_cascade(label=self.t('menu_tools'), menu=tools_menu, underline=0)

        lang_menu = tk.Menu(menubar, tearoff=False)
        self.menu_language_var = tk.StringVar(value=self.language)
        lang_menu.add_radiobutton(label='English', value='en', variable=self.menu_language_var, command=lambda: self._set_language('en'))
        lang_menu.add_radiobutton(label='Deutsch', value='de', variable=self.menu_language_var, command=lambda: self._set_language('de'))
        menubar.add_cascade(label=self.t('menu_language'), menu=lang_menu, underline=0)

        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label=self.t('menu_about'), command=self.show_about, accelerator='F1')
        help_menu.add_command(label=self.t('wix_info'), command=lambda: self._open_link(WIX_INFO_URL))
        menubar.add_cascade(label=self.t('menu_help'), menu=help_menu, underline=0)
        self.config(menu=menubar)

    def _bind_shortcuts(self):
        self.bind_all('<Control-o>', lambda e: self.choose_exe())
        self.bind_all('<Control-l>', lambda e: self.open_project())
        self.bind_all('<Control-s>', lambda e: self.save_project())
        self.bind_all('<F5>', lambda e: self.start_build())
        self.bind_all('<F6>', lambda e: self.refresh_environment(interactive=True, reset_prompts=True))
        self.bind_all('<F1>', lambda e: self.show_about())
        self.bind_all('<Control-Shift-O>', lambda e: self.open_output())

    def _build_ui(self):
        self.ui_mode_display.set(self._mode_label(self.ui_mode_key)); self.ui_mode_help.set(self._mode_help(self.ui_mode_key))
        self._build_menu()
        header = ttk.Frame(self, padding=(22,18,22,6)); header.pack(fill='x')
        left = ttk.Frame(header); left.pack(side='left', fill='x', expand=True)
        ttk.Label(left, text=APP_NAME, style='Title.TLabel').pack(anchor='w')
        ttk.Label(left, text=self.t('subtitle'), style='Subtitle.TLabel').pack(anchor='w', pady=(2,0))
        self.build_now_button = ttk.Button(header, text=self.t('build_msi_now'), style='Accent.TButton', command=self.start_build)
        self.build_now_button.pack(side='right', padx=(18,0), pady=(2,0), ipadx=12, ipady=6)

        env = ttk.Frame(self, padding=(22,4,22,4)); env.pack(fill='x')
        ttk.Label(env, text='.NET SDK:', style='Status.TLabel').pack(side='left'); ttk.Label(env, textvariable=self.dotnet_status, style='Status.TLabel').pack(side='left', padx=(5,20))
        ttk.Label(env, text='WiX:', style='Status.TLabel').pack(side='left'); ttk.Label(env, textvariable=self.wix_status, style='Status.TLabel').pack(side='left', padx=(5,8))

        footer = ttk.Frame(self, padding=(22,6,22,12)); footer.pack(side='bottom', fill='x')
        ttk.Label(footer, text=self.t('ready'), style='Status.TLabel').pack(side='left')
        ttk.Label(footer, text='F5  ' + self.t('build_msi') + '   ·   F6  ' + self.t('recheck'), style='Status.TLabel').pack(side='right')

        self.notebook = ttk.Notebook(self); self.notebook.pack(fill='both', expand=True, padx=22, pady=(8,8))
        self.tab_project = ttk.Frame(self.notebook); self.tab_filetypes = ttk.Frame(self.notebook, padding=8); self.tab_deploy = ttk.Frame(self.notebook); self.tab_wix = ttk.Frame(self.notebook, padding=8); self.tab_log = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(self.tab_project, text='  '+self.t('tab_project')+'  '); self.notebook.add(self.tab_filetypes, text='  '+self.t('tab_filetypes')+'  '); self.notebook.add(self.tab_deploy, text='  '+self.t('tab_deploy')+'  '); self.notebook.add(self.tab_wix, text='  '+self.t('tab_wix')+'  '); self.notebook.add(self.tab_log, text='  '+self.t('tab_log')+'  ')
        self.project_scroll = ScrollableFrame(self.tab_project, padding=(8,8,8,8)); self.project_scroll.pack(fill='both', expand=True); self.project_content = self.project_scroll.inner
        self.deploy_scroll = ScrollableFrame(self.tab_deploy, padding=8); self.deploy_scroll.pack(fill='both', expand=True); self.deploy_content = self.deploy_scroll.inner
        self._build_project_tab(); self._build_filetypes_tab(); self._build_deploy_tab(); self._build_wix_tab(); self._build_log_tab(); self._refresh_filename_dependent_previews()

    def _set_language(self, new_lang):
        if new_lang not in ('en','de') or new_lang == self.language:
            return
        self.language = new_lang; self.settings['language'] = new_lang; save_settings(self.settings)
        self.language_display.set('English' if new_lang == 'en' else 'Deutsch')
        old_code = self.wix_editor.get('1.0','end-1c') if hasattr(self, 'wix_editor') else None
        old_custom = self.wix_custom
        for child in list(self.winfo_children()): child.destroy()
        self._build_ui()
        if old_code is not None and old_custom:
            self._set_wix_editor_text(old_code, custom=True)
        self.update_command_preview()

    def _change_language(self, _event=None):
        self._set_language('de' if self.language_display.get() == 'Deutsch' else 'en')

    def _build_project_tab(self):
        t = self.project_content; t.columnconfigure(0, weight=1); t.columnconfigure(1, weight=1)
        source = self._card(t, self.t('source_output'), 0,0,2,pady=(0,8)); grid=ttk.Frame(source, style='Card.TFrame'); grid.pack(fill='x'); grid.columnconfigure(1,weight=1)
        ttk.Label(grid,text=self.t('program_exe'),style='CardText.TLabel').grid(row=0,column=0,sticky='w',padx=(0,12),pady=5); ttk.Entry(grid,textvariable=self.exe_path).grid(row=0,column=1,sticky='ew',pady=5); ttk.Button(grid,text=self.t('browse'),style='Secondary.TButton',command=self.choose_exe).grid(row=0,column=2,padx=(8,0),pady=5)
        ttk.Label(grid,text=self.t('output_folder'),style='CardText.TLabel').grid(row=1,column=0,sticky='w',padx=(0,12),pady=5); ttk.Entry(grid,textvariable=self.out_dir).grid(row=1,column=1,sticky='ew',pady=5); ttk.Button(grid,text=self.t('browse'),style='Secondary.TButton',command=self.choose_out).grid(row=1,column=2,padx=(8,0),pady=5)
        ttk.Checkbutton(grid,text=self.t('keep_source'),variable=self.keep_source).grid(row=2,column=1,columnspan=2,sticky='w',pady=(7,2))

        fname=self._card(t,self.t('filename_options'),1,0,2); fg=ttk.Frame(fname,style='Card.TFrame'); fg.pack(fill='x'); fg.columnconfigure(1,weight=1); fg.columnconfigure(3,weight=1)
        ttk.Label(fg,text=self.t('filename_prefix'),style='CardText.TLabel').grid(row=0,column=0,sticky='w',padx=(0,8),pady=5)
        ttk.Entry(fg,textvariable=self.filename_prefix).grid(row=0,column=1,sticky='ew',padx=(0,18),pady=5)
        ttk.Label(fg,text=self.t('filename_suffix'),style='CardText.TLabel').grid(row=0,column=2,sticky='w',padx=(0,8),pady=5)
        ttk.Entry(fg,textvariable=self.filename_suffix).grid(row=0,column=3,sticky='ew',pady=5)
        ttk.Label(fg,text=self.t('filename_preview')+':',style='Muted.TLabel').grid(row=1,column=0,sticky='w',padx=(0,8),pady=(7,2))
        ttk.Label(fg,textvariable=self.filename_preview,style='CardText.TLabel').grid(row=1,column=1,columnspan=3,sticky='w',pady=(7,2))
        ttk.Label(fg,text=self.t('filename_help'),style='Muted.TLabel').grid(row=2,column=0,columnspan=4,sticky='w',pady=(5,0))

        meta=self._card(t,self.t('product_data'),2,0); mg=ttk.Frame(meta,style='Card.TFrame'); mg.pack(fill='both',expand=True); mg.columnconfigure(1,weight=1)
        for r,(label,var) in enumerate([(self.t('product_name'),self.product_name),(self.t('manufacturer'),self.manufacturer),(self.t('version'),self.version)]): ttk.Label(mg,text=label,style='CardText.TLabel').grid(row=r,column=0,sticky='w',padx=(0,10),pady=6); ttk.Entry(mg,textvariable=var).grid(row=r,column=1,sticky='ew',pady=6)
        ttk.Label(mg,text=self.t('architecture'),style='CardText.TLabel').grid(row=3,column=0,sticky='w',padx=(0,10),pady=6)
        arch_frame=ttk.Frame(mg,style='Card.TFrame'); arch_frame.grid(row=3,column=1,sticky='w',pady=6)
        self.arch_buttons={}
        for i,value in enumerate(('x64','x86','arm64')):
            btn=ttk.Button(arch_frame,text=value,command=lambda v=value:self._set_arch(v))
            btn.grid(row=0,column=i,padx=(0 if i==0 else 5,0))
            self.arch_buttons[value]=btn
        self._refresh_arch_buttons()
        opts=self._card(t,self.t('installer_options'),2,1); ttk.Checkbutton(opts,text=self.t('start_menu'),variable=self.start_menu).pack(anchor='w',pady=5); ttk.Checkbutton(opts,text=self.t('desktop'),variable=self.desktop_shortcut).pack(anchor='w',pady=5)
        ttk.Label(opts,text=self.t('upgrade_code'),style='Muted.TLabel').pack(anchor='w',pady=(12,4)); row=ttk.Frame(opts,style='Card.TFrame'); row.pack(fill='x'); ttk.Entry(row,textvariable=self.upgrade_code).pack(side='left',fill='x',expand=True); ttk.Button(row,text=self.t('new'),style='Secondary.TButton',command=lambda:self.upgrade_code.set(str(uuid.uuid4()).upper())).pack(side='left',padx=(8,0)); ttk.Label(opts,text=self.t('upgrade_help'),style='Muted.TLabel',wraplength=390).pack(anchor='w',pady=(10,0))

    def _normalize_extension(self, value):
        value=(value or '').strip().lower()
        if not value:
            return ''
        if not value.startswith('.'):
            value='.'+value
        if not re.fullmatch(r'\.[a-z0-9][a-z0-9_+.-]{0,31}', value):
            return ''
        return value

    def _build_filetypes_tab(self):
        outer=ttk.Frame(self.tab_filetypes, padding=(8,8,8,8)); outer.pack(fill='both',expand=True)
        card=tk.Frame(outer,bg=ModernStyle.BORDER,bd=0); card.pack(fill='both',expand=True)
        inner=ttk.Frame(card,style='Card.TFrame',padding=16); inner.pack(fill='both',expand=True,padx=1,pady=1)
        ttk.Label(inner,text=self.t('filetypes_title'),style='CardTitle.TLabel').pack(anchor='w')
        ttk.Label(inner,text=self.t('filetypes_help'),style='Muted.TLabel',wraplength=900).pack(anchor='w',pady=(4,4))
        ttk.Label(inner,text=self.t('filetype_progid_hint'),style='Muted.TLabel',wraplength=900).pack(anchor='w',pady=(0,12))

        form=ttk.Frame(inner,style='Card.TFrame'); form.pack(fill='x'); form.columnconfigure(1,weight=1); form.columnconfigure(3,weight=3)
        ttk.Label(form,text=self.t('filetype_extension'),style='CardText.TLabel').grid(row=0,column=0,sticky='w',padx=(0,8))
        ext_entry=ttk.Entry(form,textvariable=self.filetype_ext,width=18); ext_entry.grid(row=0,column=1,sticky='ew',padx=(0,16))
        ttk.Label(form,text=self.t('filetype_description'),style='CardText.TLabel').grid(row=0,column=2,sticky='w',padx=(0,8))
        desc_entry=ttk.Entry(form,textvariable=self.filetype_desc); desc_entry.grid(row=0,column=3,sticky='ew')
        ttk.Label(form,text=self.t('filetype_example'),style='Muted.TLabel').grid(row=1,column=0,columnspan=2,sticky='w',pady=(4,0))

        actions=ttk.Frame(inner,style='Card.TFrame'); actions.pack(fill='x',pady=(10,10))
        ttk.Button(actions,text=self.t('filetype_add'),style='Accent.TButton',command=self._add_or_update_filetype).pack(side='left')
        ttk.Button(actions,text=self.t('filetype_remove'),style='Secondary.TButton',command=self._remove_filetype).pack(side='left',padx=(8,0))
        ttk.Label(actions,text=self.t('filetype_target'),style='Muted.TLabel').pack(side='right')

        table_frame=tk.Frame(inner,bg=ModernStyle.BORDER,bd=0); table_frame.pack(fill='both',expand=True)
        self.filetype_tree=ttk.Treeview(table_frame,columns=('extension','description'),show='headings',selectmode='browse',height=9)
        self.filetype_tree.heading('extension',text=self.t('filetype_extension')); self.filetype_tree.heading('description',text=self.t('filetype_description'))
        self.filetype_tree.column('extension',width=160,stretch=False,anchor='w'); self.filetype_tree.column('description',width=650,stretch=True,anchor='w')
        vs=ttk.Scrollbar(table_frame,orient='vertical',command=self.filetype_tree.yview)
        def _set_scroll(first,last):
            vs.set(first,last)
            if float(first)<=0.0 and float(last)>=1.0: vs.grid_remove()
            else: vs.grid()
        self.filetype_tree.configure(yscrollcommand=_set_scroll)
        self.filetype_tree.grid(row=0,column=0,sticky='nsew',padx=(1,0),pady=1); vs.grid(row=0,column=1,sticky='ns',pady=1); vs.grid_remove()
        table_frame.grid_rowconfigure(0,weight=1); table_frame.grid_columnconfigure(0,weight=1)
        self.filetype_tree.bind('<<TreeviewSelect>>',self._on_filetype_select)
        self.filetype_tree.bind('<Double-1>',self._on_filetype_select)
        ext_entry.bind('<Return>',lambda e:self._add_or_update_filetype())
        desc_entry.bind('<Return>',lambda e:self._add_or_update_filetype())
        self._refresh_filetype_tree()

    def _refresh_filetype_tree(self):
        if not hasattr(self,'filetype_tree'):
            return
        for item in self.filetype_tree.get_children(): self.filetype_tree.delete(item)
        for assoc in sorted(self.file_associations,key=lambda x:x.get('extension','')):
            self.filetype_tree.insert('', 'end', values=(assoc.get('extension',''), assoc.get('description','')))

    def _on_filetype_select(self, _event=None):
        if not hasattr(self,'filetype_tree'):
            return
        sel=self.filetype_tree.selection()
        if not sel:
            return
        vals=self.filetype_tree.item(sel[0],'values')
        if vals:
            self.filetype_ext.set(vals[0]); self.filetype_desc.set(vals[1] if len(vals)>1 else '')

    def _add_or_update_filetype(self):
        ext=self._normalize_extension(self.filetype_ext.get())
        if not ext:
            messagebox.showerror(APP_NAME,self.t('filetype_invalid'),parent=self); return
        desc=self.filetype_desc.get().strip() or self.t('filetype_default_desc',ext=ext)
        updated=False
        for assoc in self.file_associations:
            if assoc.get('extension','').lower()==ext:
                assoc['extension']=ext; assoc['description']=desc; updated=True; break
        if not updated:
            self.file_associations.append({'extension':ext,'description':desc})
        self.filetype_ext.set(''); self.filetype_desc.set(''); self._refresh_filetype_tree()
        if hasattr(self,'wix_editor') and not self.wix_custom: self.regenerate_wix_code(mark_custom=False)

    def _remove_filetype(self):
        if not hasattr(self,'filetype_tree'):
            return
        sel=self.filetype_tree.selection()
        if not sel:
            return
        vals=self.filetype_tree.item(sel[0],'values'); ext=vals[0] if vals else ''
        self.file_associations=[a for a in self.file_associations if a.get('extension')!=ext]
        self.filetype_ext.set(''); self.filetype_desc.set(''); self._refresh_filetype_tree()
        if hasattr(self,'wix_editor') and not self.wix_custom: self.regenerate_wix_code(mark_custom=False)

    def _set_arch(self, value):
        self.arch.set(value)
        self._refresh_arch_buttons()

    def _refresh_arch_buttons(self):
        if not hasattr(self, 'arch_buttons'):
            return
        for value, btn in self.arch_buttons.items():
            btn.configure(style='SegmentSelected.TButton' if self.arch.get()==value else 'Segment.TButton')

    def _build_deploy_tab(self):
        t=self.deploy_content; t.columnconfigure(0,weight=1); t.columnconfigure(1,weight=1)
        mode=self._card(t,self.t('visibility'),0,0); ttk.Label(mode,text=self.t('visibility_help'),style='Muted.TLabel').pack(anchor='w',pady=(0,7))
        self.mode_var=tk.StringVar(value=self.ui_mode_key)
        for key in MODE_ORDER:
            rb=ttk.Radiobutton(mode,text=self._mode_label(key),value=key,variable=self.mode_var,style='Choice.TRadiobutton',command=self._on_ui_mode_radio)
            rb.pack(anchor='w',fill='x',pady=1)
        hf=tk.Frame(mode,bg=ModernStyle.SOFT,bd=0); hf.pack(fill='x',pady=(11,0)); ttk.Label(hf,textvariable=self.ui_mode_help,style='Info.TLabel',wraplength=420,padding=(10,8)).pack(fill='x')
        behavior=self._card(t,self.t('automatic_behavior'),0,1); ttk.Checkbutton(behavior,text=self.t('no_restart'),variable=self.no_restart).pack(anchor='w',pady=(2,0)); ttk.Label(behavior,text=self.t('no_restart_help'),style='Muted.TLabel',wraplength=420).pack(anchor='w',padx=(24,0),pady=(2,9)); ttk.Checkbutton(behavior,text=self.t('logging'),variable=self.logging).pack(anchor='w',pady=(2,0)); ttk.Label(behavior,text=self.t('logging_help'),style='Muted.TLabel',wraplength=420).pack(anchor='w',padx=(24,0),pady=(2,7))
        lf=ttk.Frame(behavior,style='Card.TFrame'); lf.pack(fill='x'); ttk.Label(lf,text=self.t('logfile'),style='CardText.TLabel').pack(side='left'); ttk.Entry(lf,textvariable=self.log_name,width=28).pack(side='right',fill='x',expand=True,padx=(10,0))
        props=self._card(t,self.t('advanced'),1,0,2); ttk.Label(props,text=self.t('advanced_help'),style='Muted.TLabel').pack(anchor='w'); ttk.Label(props,text=self.t('examples'),style='Muted.TLabel').pack(anchor='w',pady=(2,6)); ttk.Entry(props,textvariable=self.extra_props).pack(fill='x'); ttk.Label(props,text=self.t('per_machine'),style='Muted.TLabel').pack(anchor='w',pady=(7,0))
        preview=self._card(t,self.t('deploy_command'),2,0,2); ttk.Label(preview,text=self.t('deploy_command_help'),style='Muted.TLabel').pack(anchor='w',pady=(0,7)); self.preview_box=tk.Text(preview,height=4,wrap='word',bg=ModernStyle.DARK,fg='#e5edf5',insertbackground='white',relief='flat',font=('Consolas',10),padx=12,pady=10); self.preview_box.pack(fill='x')
        btns=ttk.Frame(preview,style='Card.TFrame'); btns.pack(fill='x',pady=(10,0)); ttk.Button(btns,text=self.t('copy'),style='Secondary.TButton',command=self.copy_command).pack(side='left'); ttk.Button(btns,text=self.t('recommended'),style='Secondary.TButton',command=self.apply_deploy_defaults).pack(side='left',padx=(8,0)); ttk.Label(btns,text=self.t('recommended_help'),style='Muted.TLabel').pack(side='right'); self.update_command_preview()

    def _build_wix_tab(self):
        top=ttk.Frame(self.tab_wix); top.pack(fill='x',pady=(0,8))
        left=ttk.Frame(top); left.pack(side='left',fill='x',expand=True)
        ttk.Label(left,text=self.t('wix_editor_title'),style='SectionTitle.TLabel').pack(anchor='w')
        ttk.Label(left,text=self.t('wix_editor_help'),style='Status.TLabel',wraplength=760).pack(anchor='w',pady=(2,0))
        ttk.Button(top,text=self.t('wix_regenerate'),style='Secondary.TButton',command=self.regenerate_wix_code).pack(side='right')

        body=tk.Frame(self.tab_wix,bg=ModernStyle.BORDER,bd=0); body.pack(fill='both',expand=True)
        self.wix_editor=tk.Text(body,wrap='none',undo=True,bg='#0f172a',fg='#e5edf5',insertbackground='white',selectbackground='#155e75',relief='flat',font=('Consolas',10),padx=12,pady=12)
        vs=ttk.Scrollbar(body,orient='vertical',command=self.wix_editor.yview); hs=ttk.Scrollbar(body,orient='horizontal',command=self.wix_editor.xview)
        def _set_vscroll(first,last):
            vs.set(first,last)
            if float(first) <= 0.0 and float(last) >= 1.0:
                vs.grid_remove()
            else:
                vs.grid()
        def _set_hscroll(first,last):
            hs.set(first,last)
            if float(first) <= 0.0 and float(last) >= 1.0:
                hs.grid_remove()
            else:
                hs.grid()
        self.wix_editor.configure(yscrollcommand=_set_vscroll,xscrollcommand=_set_hscroll)
        self.wix_editor.grid(row=0,column=0,sticky='nsew',padx=(1,0),pady=(1,0)); vs.grid(row=0,column=1,sticky='ns',pady=(1,0)); hs.grid(row=1,column=0,sticky='ew',padx=(1,0),pady=(0,1))
        vs.grid_remove(); hs.grid_remove()
        body.grid_rowconfigure(0,weight=1); body.grid_columnconfigure(0,weight=1)
        self.wix_editor.bind('<<Modified>>',self._on_wix_modified)
        status=ttk.Frame(self.tab_wix,padding=(0,7,0,0)); status.pack(fill='x')
        ttk.Label(status,textvariable=self.wix_code_status,style='Status.TLabel').pack(side='left')
        ttk.Label(status,text=self.t('wix_file_menu_hint'),style='Status.TLabel').pack(side='right')
        self.regenerate_wix_code(mark_custom=False)

    def _on_wix_modified(self, _event=None):
        if not hasattr(self,'wix_editor'):
            return
        if self.wix_editor.edit_modified():
            if not self._ignore_wix_modified:
                self.wix_custom=True; self.wix_code_status.set(self.t('wix_custom'))
            self.wix_editor.edit_modified(False)

    def _set_wix_editor_text(self, text, custom=False):
        if not hasattr(self,'wix_editor'):
            return
        self._ignore_wix_modified=True
        self.wix_editor.delete('1.0','end'); self.wix_editor.insert('1.0',text); self.wix_editor.edit_modified(False)
        self._ignore_wix_modified=False
        self.wix_custom=custom; self.wix_code_status.set(self.t('wix_custom') if custom else self.t('wix_generated'))

    def regenerate_wix_code(self, mark_custom=False):
        exe_name=Path(self.exe_path.get().strip()).name or 'application.exe'
        self.wix_loaded_path=None
        self._set_wix_editor_text(self.wix_source(exe_name),custom=mark_custom)

    def _project_data(self, source_relative=None):
        data = {
            "format": "msiBuilder-project", "format_version": 1, "msibuilder_version": APP_VERSION,
            "product_name": self.product_name.get(), "manufacturer": self.manufacturer.get(),
            "version": self.version.get(), "architecture": self.arch.get(),
            "upgrade_code": self.upgrade_code.get().strip().strip('{}').upper(),
            "source_exe": source_relative if source_relative is not None else self.exe_path.get(),
            "output_folder": self.out_dir.get(), "start_menu": bool(self.start_menu.get()),
            "desktop_shortcut": bool(self.desktop_shortcut.get()), "keep_source": bool(self.keep_source.get()),
            "filename_prefix": self.filename_prefix.get().strip(), "filename_suffix": self.filename_suffix.get().strip(),
            "file_associations": [dict(x) for x in self.file_associations],
            "ui_mode": self.ui_mode_key, "no_restart": bool(self.no_restart.get()),
            "logging": bool(self.logging.get()), "log_name": self.log_name.get(),
            "extra_properties": self.extra_props.get(),
            "custom_wix": bool(self.wix_custom),
            "wix_source": self.wix_editor.get('1.0','end-1c') if self.wix_custom and hasattr(self,'wix_editor') else None
        }
        return data

    def save_project(self, path=None, source_relative=None):
        if path is None:
            initial=safe_filename(self.product_name.get().strip() or 'project')+'.wix'
            chosen=filedialog.asksaveasfilename(title=self.t('save_project'),defaultextension='.wix',initialfile=initial,filetypes=[(self.t('project_files'),'*.wix'),(self.t('all_files'),'*.*')])
            if not chosen: return None
            path=Path(chosen)
        else:
            path=Path(path)
        path.write_text(json.dumps(self._project_data(source_relative),ensure_ascii=False,indent=2),encoding='utf-8')
        return path

    def open_project(self):
        chosen=filedialog.askopenfilename(title=self.t('open_project'),filetypes=[(self.t('project_files'),'*.wix'),(self.t('all_files'),'*.*')])
        if not chosen: return
        path=Path(chosen)
        try:
            data=json.loads(path.read_text(encoding='utf-8'))
            if data.get('format')!='msiBuilder-project': raise ValueError(self.t('project_invalid'))
            src=data.get('source_exe','')
            if src and not Path(src).is_absolute(): src=str((path.parent/src).resolve())
            self.exe_path.set(src); self.out_dir.set(str(path.parent))
            self.product_name.set(data.get('product_name','')); self.manufacturer.set(data.get('manufacturer',''))
            self.version.set(data.get('version','1.0.0')); self.arch.set(data.get('architecture','x64')); self._refresh_arch_buttons()
            self.upgrade_code.set(data.get('upgrade_code',str(uuid.uuid4()).upper()))
            self.start_menu.set(bool(data.get('start_menu',True))); self.desktop_shortcut.set(bool(data.get('desktop_shortcut',False))); self.keep_source.set(bool(data.get('keep_source',False)))
            self.filename_prefix.set(data.get('filename_prefix','')); self.filename_suffix.set(data.get('filename_suffix',''))
            self.file_associations=[]
            for item in data.get('file_associations',[]):
                if isinstance(item,dict):
                    ext=self._normalize_extension(item.get('extension',''))
                    if ext: self.file_associations.append({'extension':ext,'description':str(item.get('description','')).strip() or self.t('filetype_default_desc',ext=ext)})
            self._refresh_filetype_tree()
            self.ui_mode_key=data.get('ui_mode','qn'); self.no_restart.set(bool(data.get('no_restart',True))); self.logging.set(bool(data.get('logging',True))); self.log_name.set(data.get('log_name','install.log')); self.extra_props.set(data.get('extra_properties',''))
            if data.get('custom_wix') and data.get('wix_source'):
                self._set_wix_editor_text(data['wix_source'],custom=True)
            else:
                self.regenerate_wix_code(mark_custom=False)
            self.update_command_preview()
            messagebox.showinfo(APP_NAME,self.t('project_loaded'),parent=self)
        except Exception as exc:
            messagebox.showerror(APP_NAME,self.t('project_load_failed',error=str(exc)),parent=self)

    def load_wix_code(self):
        path=filedialog.askopenfilename(title=self.t('select_wix'),filetypes=[(self.t('wix_files'),'*.wxs'),(self.t('all_files'),'*.*')])
        if not path:
            return
        try:
            text=Path(path).read_text(encoding='utf-8-sig')
        except Exception as exc:
            messagebox.showerror(APP_NAME,str(exc),parent=self); return
        self.wix_loaded_path=Path(path)
        self._set_wix_editor_text(text,custom=True)
        self.notebook.select(self.tab_wix)
        self.log(self.t('wix_loaded')+' '+str(path))

    def save_wix_code(self):
        if not hasattr(self,'wix_editor'):
            return
        initial=(safe_filename(self.product_name.get()) or 'installer')+'.wxs'
        path=filedialog.asksaveasfilename(title=self.t('save_wix'),defaultextension='.wxs',initialfile=initial,filetypes=[(self.t('wix_files'),'*.wxs'),(self.t('all_files'),'*.*')])
        if not path:
            return
        try:
            Path(path).write_text(self.wix_editor.get('1.0','end-1c'),encoding='utf-8')
        except Exception as exc:
            messagebox.showerror(APP_NAME,str(exc),parent=self); return
        self.wix_loaded_path=Path(path)
        self.log(self.t('wix_saved')+' '+str(path))

    def close_wix_code(self):
        self.wix_loaded_path=None; self.regenerate_wix_code(mark_custom=False)
        self.log(self.t('wix_closed'))

    def current_wix_source(self, exe_name):
        if self.wix_custom and hasattr(self,'wix_editor'):
            text=self.wix_editor.get('1.0','end-1c')
            if text.strip():
                return text
        return self.wix_source(exe_name)

    def _build_log_tab(self):
        self.logbox=tk.Text(self.tab_log,wrap='word',bg=ModernStyle.DARK,fg='#dbeafe',insertbackground='white',relief='flat',font=('Consolas',10),padx=12,pady=12); self.logbox.pack(fill='both',expand=True); self.log(self.t('log_ready'))

    def _on_ui_mode_radio(self):
        self.ui_mode_key=self.mode_var.get() if hasattr(self,'mode_var') else self.ui_mode_key
        self.ui_mode_display.set(self._mode_label(self.ui_mode_key)); self.ui_mode_help.set(self._mode_help(self.ui_mode_key)); self.update_command_preview()

    def _on_ui_mode_changed(self, _event=None):
        self._on_ui_mode_radio()

    def choose_exe(self):
        path=filedialog.askopenfilename(title=self.t('select_exe'),filetypes=[(self.t('windows_apps'),'*.exe'),(self.t('all_files'),'*.*')])
        if path:
            self.exe_path.set(path); stem=Path(path).stem
            if self.product_name.get() in ('My Application','Meine Anwendung'): self.product_name.set(stem)
            if hasattr(self,'wix_editor') and not self.wix_custom: self.regenerate_wix_code(mark_custom=False)

    def choose_out(self):
        path=filedialog.askdirectory(title=self.t('select_output'))
        if path: self.out_dir.set(path)

    def open_output(self):
        path=Path(self.out_dir.get()).expanduser(); path.mkdir(parents=True,exist_ok=True)
        if os.name=='nt': os.startfile(str(path))
        else: messagebox.showinfo(APP_NAME,str(path))

    def _open_link(self,url): webbrowser.open(url)
    def _link_label(self,parent,text,url,bg=ModernStyle.CARD):
        label=tk.Label(parent,text=text,bg=bg,fg=ModernStyle.ACCENT_HOVER,font=('Segoe UI',10,'underline'),cursor='hand2'); label.bind('<Button-1>',lambda e:self._open_link(url)); return label

    def show_about(self):
        win=tk.Toplevel(self); self._apply_app_icon(win); win.title(self.t('about_title')); win.geometry('620x560'); win.minsize(480,380); win.resizable(True,True); win.configure(bg=ModernStyle.BG); win.transient(self); win.grab_set()
        footer=ttk.Frame(win,padding=(16,8,16,14)); footer.pack(side='bottom',fill='x'); ttk.Button(footer,text=self.t('close'),style='Accent.TButton',command=win.destroy).pack(side='right')
        scroll=ScrollableFrame(win,padding=(16,14,16,12)); scroll.pack(fill='both',expand=True); frame=scroll.inner; outer=tk.Frame(frame,bg=ModernStyle.BORDER); outer.pack(fill='x',expand=True); inner=tk.Frame(outer,bg=ModernStyle.CARD,padx=24,pady=24); inner.pack(fill='both',expand=True,padx=1,pady=1)
        tk.Label(inner,text='GitHub',bg=ModernStyle.CARD,fg='#111827',font=('Segoe UI Semibold',18)).pack(pady=(0,12)); tk.Label(inner,text=APP_NAME,bg=ModernStyle.CARD,fg=ModernStyle.TEXT,font=('Segoe UI Semibold',15)).pack(); tk.Label(inner,text=f'Version {APP_VERSION}',bg=ModernStyle.CARD,fg=ModernStyle.MUTED,font=('Segoe UI',9)).pack(pady=(2,12)); tk.Label(inner,text=self.t('about_license'),bg=ModernStyle.CARD,fg=ModernStyle.TEXT,font=('Segoe UI',10),wraplength=500,justify='center').pack(pady=(0,12))
        for label,url in [(self.t('download'),PROJECT_GITHUB_URL),(self.t('more_info'),PROJECT_INFO_URL)]:
            row=tk.Frame(inner,bg=ModernStyle.CARD); row.pack(pady=3); tk.Label(row,text=label+' ',bg=ModernStyle.CARD,fg=ModernStyle.TEXT,font=('Segoe UI',10)).pack(side='left'); self._link_label(row,url,url).pack(side='left')
        ttk.Separator(inner,orient='horizontal').pack(fill='x',pady=18); tk.Label(inner,text=self.t('developed_by',name=PROJECT_AUTHOR),bg=ModernStyle.CARD,fg=ModernStyle.TEXT,font=('Segoe UI',10)).pack(pady=3); tk.Label(inner,text=self.t('published_by',name=PROJECT_PUBLISHER),bg=ModernStyle.CARD,fg=ModernStyle.TEXT,font=('Segoe UI',10)).pack(pady=3)
        row=tk.Frame(inner,bg=ModernStyle.CARD); row.pack(pady=3); tk.Label(row,text=self.t('contact')+' ',bg=ModernStyle.CARD,fg=ModernStyle.TEXT,font=('Segoe UI',10)).pack(side='left'); self._link_label(row,PROJECT_CONTACT,'mailto:'+PROJECT_CONTACT).pack(side='left')
        ttk.Separator(inner,orient='horizontal').pack(fill='x',pady=18); tk.Label(inner,text=self.t('wix_note_title'),bg=ModernStyle.CARD,fg=ModernStyle.TEXT,font=('Segoe UI Semibold',10)).pack(); tk.Label(inner,text=self.t('wix_note'),bg=ModernStyle.CARD,fg=ModernStyle.MUTED,font=('Segoe UI',9),wraplength=500,justify='center').pack(pady=(5,8)); self._link_label(inner,self.t('wix_info'),WIX_INFO_URL).pack()

    def refresh_environment(self, interactive=False, reset_prompts=False):
        if reset_prompts: self._sdk_warning_shown=False; self._wix_question_shown=False
        self.dotnet_status.set(self.t('checking')); self.wix_status.set(self.t('checking'))
        def worker():
            sdk_ok, sdk_version, sdks, command_ok = dotnet_sdk_status()
            if sdk_ok:
                sdk_text = sdk_version + ' ✓'
            elif sdks:
                sdk_text = self.t('sdk_too_old_status', version=sdk_version)
            else:
                sdk_text = self.t('not_found')
            self.msgq.put(('status_dotnet',(sdk_ok, sdk_text, sdk_version)))

            # Only try to execute WiX if a compatible SDK is available.
            wix_path=find_wix_executable(); wix_ok=False; wix_version=''
            if sdk_ok and wix_path:
                rc2,out2,_=run_capture([wix_path,'--version']); wix_ok=rc2==0 and bool(out2.strip()); wix_version=out2.splitlines()[0] if wix_ok else ''
            self.msgq.put(('status_wix',(wix_ok,(wix_version+' ✓') if wix_ok else self.t('not_found'),wix_path)))
            if interactive:
                if not sdks:
                    self.msgq.put(('sdk_missing',None))
                elif not sdk_ok:
                    self.msgq.put(('sdk_too_old',(sdk_version, MIN_DOTNET_SDK_TEXT)))
                elif not wix_ok:
                    self.msgq.put(('wix_missing',None))
        threading.Thread(target=worker,daemon=True).start()

    def install_wix(self):
        if self._installing_wix:return
        sdk_ok, sdk_version, sdks, _ = dotnet_sdk_status()
        if not sdks:
            messagebox.showwarning(self.t('sdk_missing_title'), self.t('sdk_missing'), parent=self)
            return
        if not sdk_ok:
            messagebox.showwarning(self.t('sdk_too_old_title'), self.t('sdk_too_old', installed=sdk_version, required=MIN_DOTNET_SDK_TEXT), parent=self)
            return
        self._installing_wix=True; self.wix_status.set(self.t('installing')); self.notebook.select(self.tab_log); self.log(''); self.log('dotnet tool install --global wix')
        def worker():
            try:
                p=subprocess.Popen(['dotnet','tool','install','--global','wix'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',creationflags=no_window_flag())
                for line in p.stdout:self.msgq.put(('log',line.rstrip()))
                self.msgq.put(('wix_install_done',p.wait()))
            except Exception as exc:self.msgq.put(('wix_install_error',str(exc)))
        threading.Thread(target=worker,daemon=True).start()

    def test_wix_installation(self, build_after=False):
        # Build a tiny temporary MSI to prove WiX is usable and EULA-ready.
        if self._testing_wix:
            return
        wix = self.wix_executable or find_wix_executable()
        if not wix:
            self._pending_build=False
            messagebox.showerror(self.t('wix_missing_title'), self.t('wix_not_found'), parent=self)
            return
        self._testing_wix=True
        self.wix_status.set(self.t('wix_test_running'))
        self.notebook.select(self.tab_log)
        self.log('')
        self.log('WiX functional test: temporary MSI build')
        def worker():
            version=''
            try:
                rc_v, out_v, err_v = run_capture([wix, '--version'])
                if rc_v != 0:
                    details=(out_v or '')+'\n'+(err_v or '')
                    self.msgq.put(('wix_test_result',(False,False,details.strip(),build_after,wix,version)))
                    return
                version=(out_v or '').strip().splitlines()[0] if (out_v or '').strip() else ''
                with tempfile.TemporaryDirectory(prefix='msibuilder_wix_test_') as td:
                    td=Path(td)
                    payload=td/'probe.txt'; payload.write_text('msiBuilder WiX functional test',encoding='utf-8')
                    test_wxs=td/'probe.wxs'
                    test_wxs.write_text(f'''<?xml version="1.0" encoding="utf-8"?>
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
  <Package Name="msiBuilder WiX Test" Manufacturer="IFL Bayreuth" Version="1.0.0" UpgradeCode="{str(uuid.uuid4()).upper()}" Scope="perMachine">
    <MediaTemplate EmbedCab="yes" />
    <StandardDirectory Id="ProgramFiles6432Folder">
      <Directory Id="INSTALLFOLDER" Name="msiBuilderWiXTest" />
    </StandardDirectory>
    <Component Id="ProbeComponent" Directory="INSTALLFOLDER" Guid="*">
      <File Id="ProbeFile" Source="probe.txt" KeyPath="yes" />
    </Component>
    <Feature Id="MainFeature" Title="Test" Level="1">
      <ComponentRef Id="ProbeComponent" />
    </Feature>
  </Package>
</Wix>
''',encoding='utf-8')
                    cmd=[wix,'build',str(test_wxs),'-o',str(td/'probe.msi')]
                    p=subprocess.run(cmd,cwd=str(td),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',creationflags=no_window_flag())
                    details=(p.stdout or '').strip()
                    if p.returncode==0 and (td/'probe.msi').is_file():
                        self.msgq.put(('wix_test_result',(True,False,details,build_after,wix,version)))
                        return
                    low=details.lower()
                    eula_required=('eula' in low and ('accept' in low or 'wix7' in low or 'license' in low))
                    self.msgq.put(('wix_test_result',(False,eula_required,details,build_after,wix,version)))
            except Exception as exc:
                self.msgq.put(('wix_test_result',(False,False,str(exc),build_after,wix,version)))
        threading.Thread(target=worker,daemon=True).start()

    def accept_wix_eula(self, build_after=False):
        wix = self.wix_executable or find_wix_executable()
        if not wix:
            messagebox.showerror(self.t('wix_missing_title'), self.t('wix_not_found'), parent=self)
            return False
        # WiX v6 and older do not use the WiX 7 EULA command.
        rc, out, _ = run_capture([wix, '--version'])
        try:
            major = int(re.match(r'\s*(\d+)', out or '').group(1)) if rc == 0 and re.match(r'\s*(\d+)', out or '') else 0
        except Exception:
            major = 0
        if major and major < 7:
            if build_after:
                self._launch_build_thread()
            return True
        if not messagebox.askyesno(self.t('wix_eula_title'), self.t('wix_eula_prompt'), parent=self):
            return False
        self._open_link(WIX_EULA_URL)
        self.notebook.select(self.tab_log)
        self.log('')
        self.log('wix eula accept wix7')
        def worker():
            try:
                p = subprocess.Popen([wix, 'eula', 'accept', 'wix7'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', creationflags=no_window_flag())
                for line in p.stdout:
                    self.msgq.put(('log', line.rstrip()))
                self.msgq.put(('wix_eula_done', (p.wait(), build_after)))
            except Exception as exc:
                self.msgq.put(('wix_eula_error', str(exc)))
        threading.Thread(target=worker, daemon=True).start()
        return False

    def apply_deploy_defaults(self):
        self.ui_mode_key='qn'; self.ui_mode_display.set(self._mode_label('qn')); self.ui_mode_help.set(self._mode_help('qn'));
        if hasattr(self,'mode_var'): self.mode_var.set('qn')
        self.no_restart.set(True); self.logging.set(True); self.generate_cmd.set(False); self.update_command_preview()

    def deployment_flags(self):
        flags=[]; mf=MODE_FLAGS.get(self.ui_mode_key,'')
        if mf: flags.append(mf)
        if self.no_restart.get(): flags.append('/norestart')
        if self.logging.get(): flags.extend(['/L*V',f'"%TEMP%\\{self.log_name.get().strip() or "install.log"}"'])
        if self.extra_props.get().strip(): flags.append(self.extra_props.get().strip())
        return ' '.join(flags)

    def update_command_preview(self):
        if not hasattr(self,'preview_box'): return
        msi=self.msi_filename(); cmd=f'msiexec.exe /i "{msi}"'; flags=self.deployment_flags(); cmd += (' '+flags) if flags else ''; self.command_preview.set(cmd); self.preview_box.configure(state='normal'); self.preview_box.delete('1.0','end'); self.preview_box.insert('1.0',cmd); self.preview_box.configure(state='disabled')
    def copy_command(self): self.clipboard_clear(); self.clipboard_append(self.command_preview.get()); self.update()
    def log(self,text):
        if hasattr(self,'logbox'): self.logbox.insert('end',text.rstrip()+'\n'); self.logbox.see('end')

    def _poll_messages(self):
        try:
            while True:
                kind,payload=self.msgq.get_nowait()
                if kind=='log': self.log(payload)
                elif kind=='status_dotnet': self.sdk_available,text,self.sdk_version=payload; self.dotnet_status.set(text)
                elif kind=='status_wix': self.wix_available,text,path=payload; self.wix_status.set(text); self.wix_executable=(path or find_wix_executable()) if self.wix_available else None
                elif kind=='sdk_missing' and not self._sdk_warning_shown:
                    self._sdk_warning_shown=True; messagebox.showwarning(self.t('sdk_missing_title'),self.t('sdk_missing'),parent=self)
                elif kind=='sdk_too_old' and not self._sdk_warning_shown:
                    self._sdk_warning_shown=True; installed,required=payload; messagebox.showwarning(self.t('sdk_too_old_title'),self.t('sdk_too_old',installed=installed,required=required),parent=self)
                elif kind=='wix_missing' and not self._wix_question_shown and not self._installing_wix:
                    self._wix_question_shown=True
                    if messagebox.askyesno(self.t('wix_missing_title'),self.t('wix_missing'),parent=self): self.install_wix()
                elif kind=='wix_install_done':
                    self._installing_wix=False; rc=payload
                    if rc==0:
                        self._wix_question_shown=False
                        self.log(self.t('wix_installed'))
                        self.test_wix_installation(build_after=self._pending_build)
                    else:
                        self._pending_build=False
                        self.wix_status.set(self.t('install_failed')); messagebox.showerror(self.t('wix_missing_title'),self.t('wix_install_failed',rc=rc),parent=self)
                elif kind=='wix_install_error': self._installing_wix=False; self.wix_status.set(self.t('install_failed')); messagebox.showerror(self.t('wix_missing_title'),payload,parent=self)
                elif kind=='wix_test_result':
                    self._testing_wix=False
                    ok, eula_required, details, build_after, wix_path, version = payload
                    if ok:
                        self.wix_available=True; self.wix_executable=wix_path
                        self.wix_status.set((version + ' · ' if version else '') + self.t('wix_test_ok'))
                        self.settings['wix7_eula_accepted'] = True; save_settings(self.settings)
                        self.log(self.t('wix_test_success'))
                        if build_after:
                            self._pending_build=False
                            self._launch_build_thread()
                        else:
                            messagebox.showinfo(self.t('wix_test_title'), self.t('wix_test_success'), parent=self)
                    elif eula_required:
                        self.wix_status.set((version + ' · EULA') if version else 'EULA')
                        self.log(details)
                        if messagebox.askyesno(self.t('wix_eula_title'), self.t('wix_test_eula'), parent=self):
                            self.accept_wix_eula(build_after=build_after)
                        else:
                            self._pending_build=False
                    else:
                        self._pending_build=False
                        self.wix_status.set(self.t('install_failed'))
                        if details: self.log(details)
                        messagebox.showerror(self.t('wix_test_title'), self.t('wix_test_failed'), parent=self)
                elif kind=='wix_eula_done':
                    rc, build_after = payload
                    if rc == 0:
                        self.settings['wix7_eula_accepted'] = True; save_settings(self.settings)
                        self.log(self.t('wix_eula_ok'))
                        self.test_wix_installation(build_after=build_after)
                    else:
                        self._pending_build=False
                        messagebox.showerror(self.t('wix_eula_title'), self.t('wix_eula_failed',rc=rc), parent=self)
                elif kind=='wix_eula_error': messagebox.showerror(self.t('wix_eula_title'), payload, parent=self)
                elif kind=='done':
                    self._building=False
                    if hasattr(self,'build_now_button'): self.build_now_button.configure(state='normal')
                    messagebox.showinfo(APP_NAME,payload,parent=self)
                elif kind=='error':
                    self._building=False; self._pending_build=False
                    if hasattr(self,'build_now_button'): self.build_now_button.configure(state='normal')
                    messagebox.showerror(APP_NAME,payload,parent=self)
        except queue.Empty: pass
        self.after(150,self._poll_messages)

    def validate(self):
        exe=Path(self.exe_path.get().strip())
        if not exe.is_file() or exe.suffix.lower()!='.exe': messagebox.showerror(APP_NAME,self.t('exe_required'),parent=self); return False
        if not self.product_name.get().strip() or not self.manufacturer.get().strip(): messagebox.showerror(APP_NAME,self.t('meta_required'),parent=self); return False
        try: uuid.UUID(self.upgrade_code.get().strip().strip('{}'))
        except Exception: messagebox.showerror(APP_NAME,self.t('guid_invalid'),parent=self); return False
        sdk_ok, sdk_version, sdks, _ = dotnet_sdk_status()
        if not sdks:
            messagebox.showerror(APP_NAME,self.t('sdk_build_missing'),parent=self); return False
        if not sdk_ok:
            messagebox.showerror(APP_NAME,self.t('sdk_build_too_old',installed=sdk_version,required=MIN_DOTNET_SDK_TEXT),parent=self); return False
        wix=find_wix_executable()
        if not wix:
            if messagebox.askyesno(self.t('wix_missing_title'),self.t('wix_build_missing'),parent=self):
                self._pending_build=True; self.install_wix()
            return False
        rc,_,_=run_capture([wix,'--version'])
        if rc!=0: messagebox.showerror(APP_NAME,self.t('wix_cannot_start'),parent=self); return False
        self.wix_executable=wix; return True

    def wix_source(self,exe_name):
        product=esc(self.product_name.get().strip()); manufacturer=esc(self.manufacturer.get().strip()); version=normalize_version(self.version.get()); upgrade=self.upgrade_code.get().strip().strip('{}').upper(); install_dir=product
        shortcut_nodes=[]; std_dirs=[]; refs=['MainExeComponent']; reg=f'Software\\{manufacturer}\\{product}'
        if self.start_menu.get(): std_dirs.append(f'    <StandardDirectory Id="ProgramMenuFolder">\n      <Directory Id="AppProgramsFolder" Name="{install_dir}" />\n    </StandardDirectory>'); shortcut_nodes.append(f'    <Component Id="StartMenuShortcutComponent" Directory="AppProgramsFolder" Guid="*">\n      <Shortcut Id="StartMenuShortcut" Name="{product}" Target="[#MainExeFile]" WorkingDirectory="INSTALLFOLDER" />\n      <RemoveFolder Id="RemoveAppProgramsFolder" On="uninstall" />\n      <RegistryValue Root="HKLM" Key="{reg}" Name="StartMenuShortcut" Type="integer" Value="1" KeyPath="yes" />\n    </Component>'); refs.append('StartMenuShortcutComponent')
        if self.desktop_shortcut.get(): std_dirs.append('    <StandardDirectory Id="DesktopFolder" />'); shortcut_nodes.append(f'    <Component Id="DesktopShortcutComponent" Directory="DesktopFolder" Guid="*">\n      <Shortcut Id="DesktopShortcut" Name="{product}" Target="[#MainExeFile]" WorkingDirectory="INSTALLFOLDER" />\n      <RegistryValue Root="HKLM" Key="{reg}" Name="DesktopShortcut" Type="integer" Value="1" KeyPath="yes" />\n    </Component>'); refs.append('DesktopShortcutComponent')

        # File associations: register the EXE as a supported handler. Modern Windows
        # protects an existing per-user default; the user can choose the app in
        # Open with / Default apps after installation.
        assoc_nodes=[]; capability_nodes=[]
        clean_product=re.sub(r'[^A-Za-z0-9]+','',self.product_name.get().strip()) or 'Application'
        suffix=re.sub(r'[^A-Fa-f0-9]','',upgrade)[:8] or 'App'
        cap_key=f'Software\\{manufacturer}\\{product}\\Capabilities'
        if self.file_associations:
            capability_nodes.append(f'      <RegistryValue Root="HKLM" Key="{cap_key}" Name="ApplicationName" Type="string" Value="{product}" />')
            capability_nodes.append(f'      <RegistryValue Root="HKLM" Key="{cap_key}" Name="ApplicationDescription" Type="string" Value="{product}" />')
            capability_nodes.append(f'      <RegistryValue Root="HKLM" Key="Software\\RegisteredApplications" Name="{product}" Type="string" Value="{cap_key}" />')
        seen=set()
        for assoc in self.file_associations:
            dotted=self._normalize_extension(assoc.get('extension',''))
            if not dotted or dotted in seen: continue
            seen.add(dotted); ext=dotted[1:]
            desc=esc(assoc.get('description','').strip() or self.t('filetype_default_desc',ext=dotted))
            progid=f'{clean_product}.{ext}.{suffix}'
            assoc_nodes.append(f'      <ProgId Id="{esc(progid)}" Description="{desc}" Icon="MainExeFile">\n        <Extension Id="{esc(ext)}">\n          <Verb Id="open" Command="Open" TargetFile="MainExeFile" Argument="&quot;%1&quot;" />\n        </Extension>\n      </ProgId>')
            capability_nodes.append(f'      <RegistryValue Root="HKLM" Key="{cap_key}\\FileAssociations" Name="{esc(dotted)}" Type="string" Value="{esc(progid)}" />')
        assoc_xml=('\n'+'\n'.join(assoc_nodes+capability_nodes)) if (assoc_nodes or capability_nodes) else ''

        return f"""<?xml version="1.0" encoding="utf-8"?>\n<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">\n  <Package Name="{product}" Manufacturer="{manufacturer}" Version="{version}" UpgradeCode="{upgrade}" Scope="perMachine">\n    <MajorUpgrade DowngradeErrorMessage="A newer version of {product} is already installed." />\n    <MediaTemplate EmbedCab="yes" />\n    <StandardDirectory Id="ProgramFiles6432Folder">\n      <Directory Id="INSTALLFOLDER" Name="{install_dir}" />\n    </StandardDirectory>\n{chr(10).join(std_dirs)}\n    <Component Id="MainExeComponent" Directory="INSTALLFOLDER" Guid="*">\n      <File Id="MainExeFile" Source="{esc(exe_name)}" KeyPath="yes" />{assoc_xml}\n    </Component>\n{chr(10).join(shortcut_nodes)}\n    <Feature Id="MainFeature" Title="{product}" Level="1">\n{chr(10).join('      <ComponentRef Id="'+r+'" />' for r in refs)}\n    </Feature>\n  </Package>\n</Wix>\n"""

    def start_build(self):
        if self._building or self._testing_wix or self._installing_wix:
            return
        self._pending_build = True
        if not self.validate():
            if not self._installing_wix:
                self._pending_build=False
            return
        self.test_wix_installation(build_after=True)

    def _launch_build_thread(self):
        if self._building: return
        self._building=True
        if hasattr(self,'build_now_button'): self.build_now_button.configure(state='disabled')
        self.notebook.select(self.tab_log)
        threading.Thread(target=self._build_worker, daemon=True).start()

    def _build_worker(self):
        try:
            exe=Path(self.exe_path.get()).resolve(); out=Path(self.out_dir.get()).expanduser().resolve(); out.mkdir(parents=True,exist_ok=True)
            base=safe_filename(self.product_name.get())
            msi_name=self.msi_filename(); msi_path=out/msi_name
            project_path=out/(base+'.wix')
            wix=self.wix_executable or find_wix_executable() or 'wix'
            with tempfile.TemporaryDirectory(prefix='msibuilder_') as tmp:
                builddir=Path(tmp); local_exe=builddir/exe.name; shutil.copy2(exe,local_exe)
                wxs=builddir/'installer.wxs'; wxs.write_text(self.current_wix_source(exe.name),encoding='utf-8')
                self.msgq.put(('log',f'Temporary build directory: {builddir}'))
                cmd=[wix,'build',str(wxs),'-arch',self.arch.get(),'-o',str(msi_path)]
                self.msgq.put(('log','Build: '+' '.join(f'"{x}"' if ' ' in x else x for x in cmd)))
                p=subprocess.Popen(cmd,cwd=str(builddir),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',creationflags=no_window_flag())
                for line in p.stdout:self.msgq.put(('log',line.rstrip()))
                rc=p.wait()
                if rc!=0: raise RuntimeError(self.t('build_failed',rc=rc))
                # WiX debug database is not needed for normal use.
                for candidate in (msi_path.with_suffix('.wixpdb'), builddir/(msi_path.stem+'.wixpdb')):
                    try:
                        if candidate.exists(): candidate.unlink()
                    except OSError: pass
                source_relative=None
                if self.keep_source.get():
                    source_dir=out/'source'; source_dir.mkdir(parents=True,exist_ok=True)
                    shutil.copy2(exe,source_dir/exe.name); shutil.copy2(wxs,source_dir/'installer.wxs')
                    install_cmd=f'@echo off\r\nmsiexec /i "..\\{msi_name}"\r\n'
                    uninstall_cmd=f'@echo off\r\nmsiexec /x "..\\{msi_name}"\r\n'
                    (source_dir/'install.cmd').write_text(install_cmd,encoding='utf-8')
                    (source_dir/'uninstall.cmd').write_text(uninstall_cmd,encoding='utf-8')
                    source_relative=str(Path('source')/exe.name)
                    self.msgq.put(('log','Source archive: '+str(source_dir)))
                self.save_project(project_path, source_relative=source_relative)
            self.msgq.put(('log','Project file: '+str(project_path)))
            self.msgq.put(('done',self.t('build_success',path=msi_path)))
        except FileNotFoundError:self.msgq.put(('error',self.t('wix_not_found')))
        except Exception as exc:self.msgq.put(('error',str(exc))); self.msgq.put(('log','ERROR: '+str(exc)))



if __name__=='__main__':
    if os.name!='nt': print('Note: msiBuilder is intended for Windows.')
    App().mainloop()
