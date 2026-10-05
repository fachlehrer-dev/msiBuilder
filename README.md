# msiBuilder

> **A modern Windows GUI for building MSI installers from EXE files using WiX, with silent deployment options and automatic prerequisite checks.**

**[Ausführliches deutsches Handbuch / Full German documentation](README_DE.md)**

---

## What is msiBuilder?

**msiBuilder** is a Windows desktop application that turns an existing application EXE into an **MSI installer** using the WiX Toolset – without requiring users to write WiX XML or assemble build commands manually.

It is designed for developers, administrators, schools, small IT departments and anyone who needs clean MSI packages for manual installation, updates or centralized software deployment.

The basic workflow is intentionally simple:

> **Choose EXE → configure project → click “Build MSI now” → done.**

---

## Features

- Build MSI installers from Windows EXE files
- Modern graphical Windows interface
- Reopenable `.wix` msiBuilder project files
- Persistent **UpgradeCode** for future product updates
- x86 / x64 target architecture selection
- Start menu and desktop shortcut options
- Automatic WiX source generation
- Built-in WiX source editor with `.wxs` import/export
- Silent deployment presets for `msiexec`
- `/qn`, `/quiet`, `/passive`, `/qb` and normal UI modes
- `/norestart` and verbose MSI logging support
- Ready-to-copy deployment commands for GPO, Intune, RMM and scripts
- Automatic .NET SDK version check
- Automatic WiX detection and optional installation
- Real WiX test build after installation
- WiX EULA handling when required
- Optional `source` archive with EXE and build files
- Temporary build artifacts are cleaned automatically
- One-file Windows EXE build script included

---

## Quick start

1. Start `msiBuilder.exe`.
2. Select the application EXE on the **Project** tab.
3. Choose an output folder.
4. Enter product name, manufacturer and version.
5. Select architecture and shortcut options.
6. Click **Build MSI now** or press `F5`.

msiBuilder checks the required tooling in the background. If WiX is missing, the application can guide the user through installation and performs a real test MSI build afterwards.

---

## Requirements

For MSI creation, msiBuilder expects:

- Windows
- **.NET SDK 6.0 or newer**
- WiX Toolset

WiX is an external dependency and is not bundled with msiBuilder.

If WiX is not installed, msiBuilder can invoke:

```cmd
dotnet tool install --global wix
```

Afterwards, msiBuilder builds a temporary test MSI to verify that WiX is actually usable and that any required WiX EULA acceptance has been completed.

---

## Project files

A normal output folder stays intentionally clean:

```text
Output\
├── MyApplication-1.0.0.msi
└── MyApplication.wix
```

The `.wix` file is an **msiBuilder project file**, not WiX XML. It stores the settings required to reopen and continue the project later, including the persistent UpgradeCode.

WiX XML source continues to use the `.wxs` extension.

### Optional source archive

When **Save source and build data in the source folder** is enabled:

```text
Output\
├── MyApplication-1.0.0.msi
├── MyApplication.wix
└── source\
    ├── MyApplication.exe
    ├── installer.wxs
    ├── install.cmd
    └── uninstall.cmd
```

This makes it possible to archive the complete build input together with the project.

---

## Updating an existing application

For a new version of the same product:

1. reopen the existing `.wix` project,
2. update the EXE,
3. increase the product version,
4. **keep the UpgradeCode unchanged**,
5. build the new MSI.

The UpgradeCode identifies the product family and is therefore stored permanently in the msiBuilder project file.

---

## Deployment

The **Deployment** tab generates ready-to-use `msiexec` commands for automated rollout.

Example:

```cmd
msiexec /i "MyApplication-1.0.0.msi" /qn /norestart /L*V "MyApplication-install.log"
```

This is useful for environments such as:

- Microsoft Intune
- Group Policy / GPO
- RMM systems
- software deployment platforms
- batch or PowerShell scripts

---

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+O` | Select application EXE |
| `Ctrl+L` | Open msiBuilder project (`.wix`) |
| `Ctrl+S` | Save project |
| `Ctrl+Shift+O` | Open output folder |
| `F5` | Build MSI now |
| `F6` | Check prerequisites |
| `F1` | About msiBuilder |

---

## Build msiBuilder from source

Run:

```cmd
build_onefile.bat
```

The script installs/updates PyInstaller and creates:

```text
dist\msiBuilder.exe
```

The application icon is embedded in the executable. End users of the built EXE do not need Python installed.

---

## License

msiBuilder is released under the **MIT License**.

WiX is an external project and is subject to its own license, EULA and usage terms.

---

## Documentation

For the complete guide, detailed update workflow, prerequisite explanation, deployment options and troubleshooting, see:

### **[README_DE.md – Deutsches Handbuch](README_DE.md)**
