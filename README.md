# YouTube Video Downloader with GUI

A powerful Python-based video downloader with a beautiful GUI that supports YouTube, Mediaset, and 1000+ other video platforms. Features include age-restricted video support, YouTube search, proxy settings, and more.

**Author:** Roberto Raimondo - IS Senior Systems Engineer II

## ✨ Features

### Core Features
- 📹 **Download videos in best quality** (automatic selection)
- 🎵 **Extract audio only** (MP3 format)
- 🔍 **YouTube search** directly in the app
- 🍪 **Age-restricted video support** using browser cookies
- 🌍 **Proxy support** for geo-blocked content
- 📁 **Flexible download location** (choose per download)
- 🔄 **Auto-reset** after each download

### GUI Features
- 🎨 Beautiful, modern interface with YouTube red theme (opens maximized)
- 📊 Real-time video information display
- 🔘 Smart single-button interface (Fetch → Download)
- ⚡ Progress bar with status updates
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

### Easy Launch
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

1. **Launch the GUI** (double-click `start_gui.bat`)
2. **Paste a YouTube URL** or use the search feature
3. **Click "Fetch Video Info"** to see video details
4. **Choose Video or Audio Only**
5. **Click "Download"** (choose folder when prompted)
6. **Done!** The interface auto-resets for the next download

### YouTube Search Feature

1. **Type keywords** in the URL field
2. **Click the 🔍 Search button**
3. **Browse results** in the popup window
4. **Click a video** to select it
5. **Download normally**

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
├── youtube_downloader_gui.py   # Main GUI application
├── youtube_downloader.py       # Core downloader class
├── export_cookies.py          # Cookie export helper
├── proxy_list.txt            # Working proxy list
├── cookies.txt               # Your exported cookies
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── TROUBLESHOOTING.md        # Detailed troubleshooting
```

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




