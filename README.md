# msiBuilder 1.11.2

A modern Windows GUI for creating MSI installers from EXE files with WiX, including reopenable project files, stable UpgradeCodes for future updates, and automatic prerequisite checks.


## New in 1.11.2

### File type associations

The new **File types** tab lets you register one or more extensions for the installed EXE, for example `.csv`, `.md` or a custom format. msiBuilder generates the required WiX `ProgId` / `Extension` entries, registers the application for **Open with** and Windows **Default apps**, and passes the selected file to the EXE as `"%1"`. Associations are stored in the `.wix` project file.

> **Windows 10/11 note:** Installers are not allowed to silently replace an existing per-user default application. msiBuilder registers the application as a supported handler; if another default is already selected, Windows requires the user to confirm the new default through system UI.

## New in 1.9.2

- Scrollbars are now only shown when the content actually requires scrolling.
- The “WiX source code” heading now blends into the tab background instead of appearing on a white label.

## New in 1.9.0

- The output folder normally contains only the finished **MSI** and an reopenable **`.wix` msiBuilder project file**.
- The project file stores all important settings including the persistent **UpgradeCode**.
- Optional source archiving creates a `source` folder containing the EXE, `installer.wxs`, `install.cmd`, and `uninstall.cmd`.
- WiX `.wixpdb` debug output is removed after a successful normal build.
- Intermediate build files are created in a temporary directory and removed automatically.
- The extra top spacing before **Source file & output** on the Project tab has been removed.

## Output layout

Default:

```text
Output\
├── MyApplication-1.0.0.msi
└── MyApplication.wix
```

With source archiving enabled:

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

The `.wix` file is an msiBuilder project file, not WiX XML. It stores product metadata, architecture, UpgradeCode, source location, shortcut settings, deployment settings, and optional custom WiX source.

## Shortcuts

- **Ctrl+O** – choose application EXE
- **Ctrl+L** – open `.wix` msiBuilder project
- **Ctrl+S** – save `.wix` msiBuilder project
- **Ctrl+Shift+O** – open output folder
- **F5** – build MSI
- **F6** – check prerequisites
- **F1** – About

WiX `.wxs` source can still be imported/exported separately from the File menu.

## Requirements

msiBuilder requires a compatible **.NET SDK 6.0+** and WiX to build MSI packages. After WiX installation it performs an actual temporary test build, including the WiX 7 EULA check where applicable.

## Building msiBuilder

Run `build_onefile.bat` to create `dist\msiBuilder.exe` with the integrated application icon.

## License

msiBuilder is MIT licensed. WiX is an external dependency with its own license and usage terms.

- Layout: The top spacing of the “Source file & output” card now matches the left and right tab padding.

### Custom MSI file names

Optional prefix/suffix fields can be added to the generated MSI file name. msiBuilder inserts `_` separators automatically and shows a live preview, e.g. `Setup_MyApp-1.0.0_x64.msi`. These values are stored in the `.wix` project file.

For file associations, users enter only the extension and description. The Windows **ProgID is generated automatically**; it is not the file extension itself.


## Opening project files directly

If `.wix` project files are associated with msiBuilder in Windows, double-clicking a project opens it directly and restores all saved project settings.
