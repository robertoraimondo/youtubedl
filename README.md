# YouTube Video Downloader with GUI

A powerful Python-based video downloader with a beautiful GUI that supports YouTube, Mediaset, and 1000+ other video platforms. Features include YouTube search with thumbnail preview, real-time download progress, age-restricted video support, proxy settings, and more.

**Author:** Roberto Raimondo - IS Senior Systems Engineer II

## ✨ Features

### Core Features
- 📹 **Download videos in best quality** (automatic selection)
- 🎵 **Extract audio only** (MP3 format)
- 🔍 **YouTube search** with 50+ results and thumbnail previews
- 👁️ **Video preview panel** - view thumbnails before downloading
- 📊 **Real-time download progress** - percentage, speed (MB/s), and ETA
- 🍪 **Age-restricted video support** using browser cookies
- 🌍 **Proxy support** for geo-blocked content
- 📁 **Flexible download location** (choose per download)
- 🔄 **Auto-reset** after each download

### GUI Features
- 🎨 Beautiful, modern interface with YouTube red theme (opens maximized)
- 🖼️ **Two-panel search results** - list view + preview panel
- 📺 **Thumbnail preview** - see video image before downloading
- ▶️ **Play in Browser** button for quick video watching
- 📊 Real-time video information display
- 🔘 Smart single-button interface (Fetch → Download)
- ⚡ Advanced progress tracking with speed and time remaining
- 🍪 Cookie setup wizard with browser extension links
- 🌐 Proxy manager with saved proxy list
- 📋 Load saved proxies feature
- 📖 Help button with comprehensive documentation
- ❌ Safe exit with confirmation

### Supported Platforms
- ✅ YouTube (including age-restricted)
- ✅ Vimeo
- ✅ Dailymotion
- ✅ Mediaset Infinity (requires VPN)
- ✅ 1000+ other video sites (via yt-dlp)

## 🚀 Quick Start

### Executable (No Python Required!)
1. Download `YouTube_Downloader.exe` from the `dist` folder
2. **Double-click to run** - no installation needed!
3. Paste a video URL or search YouTube
4. Download with real-time progress tracking

### Python Version (For Developers)
Simply double-click `start_gui.bat` to launch the application!

Or run:
```powershell
python youtube_downloader_gui.py
```

## 📋 Prerequisites

1. **Python 3.7+** installed on your system
2. **FFmpeg** installed (required for audio extraction and format conversion)
   - Windows: Download from https://ffmpeg.org/download.html or use `winget install ffmpeg`
   - Add FFmpeg to your system PATH

## 💻 Installation

1. Install required Python packages:
```powershell
pip install -r requirements.txt
```

2. Launch the GUI:
```powershell
python youtube_downloader_gui.py
```

## 📖 How to Use

### Basic Usage (YouTube)

1. **Launch the GUI** (double-click `YouTube_Downloader.exe` or `start_gui.bat`)
2. **Paste a YouTube URL** or use the search feature
3. **Click "Fetch Video Info"** to see video details
4. **Choose Video or Audio Only**
5. **Click "Download"** (choose folder when prompted)
6. **Watch real-time progress** - percentage, speed (MB/s), and ETA displayed
7. **Done!** The interface auto-resets for the next download

### YouTube Search Feature

1. **Type keywords** in the URL field
2. **Click the 🔍 Search button**
3. **Browse 50 results** in a two-panel window:
   - **Left panel**: Video list with titles, channels, views, duration
   - **Right panel**: Preview with thumbnail and details
4. **Click any video** to see thumbnail preview
5. **Click "▶ Play in Browser"** to watch the video
6. **Click "✓ SELECT THIS VIDEO FOR DOWNLOAD"** to download
7. **Download normally** with progress tracking

### Video Preview Features

When viewing search results or previewing videos:
- **Thumbnail display** - see video image before downloading
- **Video information** - channel, duration, views, URL
- **Play in Browser** - watch video without downloading
- **Quick select** - one-click selection for download

Note: In-app video streaming is not available due to YouTube's bot detection. Use "Play in Browser" to watch full videos.

### Age-Restricted Videos (Cookie Setup)

For age-restricted YouTube videos, you need to export your browser cookies:

#### Method 1: Cookie Setup Wizard (Recommended)

1. **Click "🍪 Setup Cookies"** button in the GUI
2. **Follow the 3-step wizard:**
   - Step 1: Install browser extension (Chrome/Firefox/Edge)
   - Step 2: Export cookies from YouTube
   - Step 3: Import cookies.txt file
3. **Done!** The app will use your cookies automatically

#### Method 2: Manual Cookie Export

1. Install **"Get cookies.txt LOCALLY"** extension:
   - Chrome: https://chrome.google.com/webstore
   - Firefox: https://addons.mozilla.org/firefox
   
2. Visit **YouTube.com** (make sure you're logged in)
3. Click the extension icon and export cookies
4. Save the file as `cookies.txt` in the project folder
5. Click **"Import Cookies"** button in the GUI

### Geo-Blocked Content (Proxy/VPN)

For content like Mediaset that's geo-blocked:

#### Option 1: Use VPN (Recommended)
1. Install **ProtonVPN** (free): https://protonvpn.com
2. Connect to the appropriate country server (e.g., Italy for Mediaset)
3. Use the downloader normally (leave proxy field empty)

#### Option 2: Use Proxy
1. Click **"📋 Load Saved"** button to see verified proxies
2. Select a proxy from the list
3. Or manually enter: `socks5://IP:PORT`
4. Download normally

**Note:** Free proxies may not work reliably for video streaming. VPN is recommended.

## ⚙️ Advanced Usage

### Programmatic Usage

```python
from youtube_downloader import YouTubeDownloader

# Create downloader instance
downloader = YouTubeDownloader(output_path='my_videos')

# Download a video
result = downloader.download_video(
    url='https://www.youtube.com/watch?v=VIDEO_ID',
    quality='best',
    use_cookies=True,
    proxy='socks5://IP:PORT'  # Optional
)

if result['success']:
    print(f"Downloaded: {result['title']}")
    print(f"Saved to: {result['file_path']}")

# Download audio only
result = downloader.download_audio_only(
    url='https://www.youtube.com/watch?v=VIDEO_ID',
    format_type='mp3',
    use_cookies=True
)

# Get video info
info = downloader.get_video_info(
    url='https://www.youtube.com/watch?v=VIDEO_ID',
    use_cookies=False
)
print(f"Title: {info['title']}")
print(f"Duration: {info['duration']} seconds")
print(f"Views: {info.get('views', 'N/A')}")
print(f"Age Restricted: {info.get('age_restricted', False)}")

# Search YouTube
results = downloader.search_videos('search query', max_results=10)
if results['success']:
    for video in results['videos']:
        print(f"{video['title']} - {video['url']}")
```

## 🔧 Troubleshooting

### Common Issues

#### "Could not copy Chrome cookie database"
**Solution:** Use the Cookie Setup Wizard in the GUI
- Click "🍪 Setup Cookies" button
- Follow the step-by-step instructions
- Export cookies manually using browser extension

#### "This video is age-restricted"
**Solution:** Export your YouTube cookies
1. Make sure you're logged into YouTube
2. Use the Cookie Setup Wizard
3. Or manually export cookies.txt

#### "Sign in to confirm you're not a bot"
**Solution:** This is YouTube's bot detection
- Video preview in-app is not available due to this restriction
- Use **"▶ Play in Browser"** button to watch videos
- Download still works normally with cookies

#### Progress bar shows "Processing (merging video/audio)"
**Normal behavior:** yt-dlp is combining video and audio streams
- This happens when downloading best quality
- Progress bar shows indeterminate mode during merge
- Wait for completion

#### "This content is not available in your location"
**Solution:** Use a VPN
- Install ProtonVPN (free tier available)
- Connect to the appropriate country
- For Mediaset: Connect to Italy

**Note:** Free proxies don't work reliably for video streaming platforms.

#### "ffmpeg not found"
**Solution:** Install FFmpeg
- Download from https://ffmpeg.org/download.html
- Add to system PATH
- Restart your terminal/computer

#### "Unable to extract video data"
**Solution:** Update yt-dlp
```powershell
pip install --upgrade yt-dlp
```

### Getting Help

1. Check `TROUBLESHOOTING.md` for detailed solutions
2. Click the **"📖 Help"** button in the GUI
3. Check proxy help with **"🌍 Find Proxies"** button

## 📁 Project Structure

```
youtubedl/
├── youtube_downloader_gui.py   # Main GUI application (single file)
├── export_cookies.py          # Cookie export helper
├── proxy_list.txt            # Working proxy list
├── cookies.txt               # Your exported cookies (after setup)
├── requirements.txt          # Python dependencies
├── start_gui.bat            # Easy launcher for Windows
├── build_executable.bat     # Build .exe file
├── README.md                # This file
├── TROUBLESHOOTING.md       # Detailed troubleshooting
├── dist/                    # Compiled executable
│   └── YouTube_Downloader.exe  # Standalone application
└── downloads/               # Default download folder
```

## 🏗️ Building Executable

To build the standalone executable:

```powershell
# Install PyInstaller if needed
pip install pyinstaller

# Build executable
python -m PyInstaller --onefile --windowed --name "YouTube_Downloader" --icon="Youtube-icon.ico" --add-data "proxy_list.txt;." youtube_downloader_gui.py

# Or use the batch file
build_executable.bat
```

The executable will be created in the `dist` folder.

## 📦 Output

Downloaded videos will be saved to:
- Custom: Choose location for each download (dialog appears before download)

Files are saved with the video title as the filename.

## ⚠️ Legal Notice

This tool is for educational purposes only. Please respect:
- YouTube's Terms of Service
- Copyright laws
- Content creators' rights
- Only download videos you have permission to download
- Do not redistribute copyrighted content

## 🙏 Credits

- **yt-dlp**: https://github.com/yt-dlp/yt-dlp
- **FFmpeg**: https://ffmpeg.org/
- **tkinter**: Python's standard GUI library

## 📄 License

MIT License - Feel free to use and modify as needed.

**Author:** Roberto Raimondo - IS Senior Systems Engineer II




