# Building the Executable

## Quick Build

The project includes a build script to create the executable automatically:

```powershell
.\build_executable.bat
```

This will create `YouTube_Downloader.exe` in the `dist` folder.

## Manual Build

If you prefer to build manually:

```powershell
pyinstaller --onefile --windowed --name "YouTube_Downloader" --icon="Youtube-icon.ico" --add-data "proxy_list.txt;." youtube_downloader_gui.py
```

## Important Notes

### Required Files
The executable needs these files in the same directory:
- **cookies.txt** - Your browser cookies (export using the cookie wizard)
- **proxy_list.txt** - Saved proxy list (included automatically)
- **FFmpeg** - Must be installed and in PATH for audio extraction

### First Run
1. Copy the executable from `dist/YouTube_Downloader.exe` to your desired location
2. Make sure FFmpeg is installed on your system
3. Run the executable - it will open maximized
4. Use the cookie wizard to export your browser cookies if needed

### Distribution
When sharing the executable:
- Include `proxy_list.txt` in the same folder
- Remind users to install FFmpeg
- Provide instructions for exporting cookies.txt

### File Sizes
- The executable is approximately 45-50 MB due to bundled libraries
- This is normal for PyInstaller packages with yt-dlp

## Troubleshooting

### "FFmpeg not found" error
Install FFmpeg and add it to your system PATH

### "cookies.txt not found" error
Use the cookie wizard in the app to export your browser cookies

### Antivirus warnings
Some antivirus software may flag PyInstaller executables as false positives. Add an exception if needed.
