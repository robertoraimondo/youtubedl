# Troubleshooting Guide

## Chrome Cookie Database Error

**Error Message:**
```
ERROR: Could not copy Chrome cookie database
```

### Why This Happens
- Chrome locks its cookie database while running
- Windows file system prevents copying locked files
- This is a known limitation when trying to extract cookies from a running browser

### Solution: Export Cookies Manually (RECOMMENDED)

This is the **most reliable** way to handle age-restricted videos:

#### Step 1: Install Browser Extension

**For Chrome/Edge:**
1. Visit: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
2. Click "Add to Chrome"
3. Accept permissions

**For Firefox:**
1. Visit: https://addons.mozilla.org/firefox/addon/cookies-txt/
2. Click "Add to Firefox"

#### Step 2: Export Cookies

1. **Log into YouTube** in your browser (if not already logged in)
2. **Visit any YouTube page** (youtube.com)
3. **Click the extension icon** in your toolbar
4. **Click "Export" or "Get cookies.txt"**
5. **Save the file** as `cookies.txt`

#### Step 3: Place Cookie File

Save the `cookies.txt` file in your project folder:
```
D:\MyProject\youtubedl\cookies.txt
```

#### Step 4: Verify

Run the program again - the status bar should show:
```
✅ cookies.txt found - Age-restricted videos supported
```

---

## Other Common Issues

### Issue: "This video is age-restricted"

**Cause:** Video requires authentication

**Solution:**
- Follow the cookie export steps above
- Make sure you're logged into YouTube when exporting cookies
- Verify cookies.txt is in the correct location

---

### Issue: "FFmpeg not found"

**Cause:** FFmpeg is required for audio extraction and format conversion

**Solution for Windows:**
```powershell
# Using winget (Windows 10/11)
winget install ffmpeg

# Or download manually from:
https://ffmpeg.org/download.html
```

After installation:
1. Add FFmpeg to your system PATH
2. Restart your terminal/PowerShell
3. Verify: `ffmpeg -version`

---

### Issue: "Unable to extract video data"

**Possible Causes:**
- Video is private or deleted
- URL is incorrect
- yt-dlp needs updating

**Solutions:**
```powershell
# Update yt-dlp
pip install --upgrade yt-dlp

# Verify URL format
# Should be: https://www.youtube.com/watch?v=VIDEO_ID
```

---

### Issue: Video downloads but can't convert to MP3

**Cause:** FFmpeg is not installed or not in PATH

**Solution:**
1. Install FFmpeg (see above)
2. Make sure it's in your system PATH
3. Restart the program

---

### Issue: Downloads are very slow

**Possible Solutions:**
- Check your internet connection
- Try a different quality (lower quality = faster)
- Close other downloads/streaming apps
- Try at a different time (YouTube may throttle)

---

## Testing Without Age-Restricted Videos

If you just want to test the downloader with public videos (no age restriction):

1. Use any public YouTube video
2. No cookies needed
3. Should work immediately

**Example public videos to test:**
- Music videos from official channels
- Educational content
- Public vlogs

---

## Still Having Issues?

### Quick Diagnostic Steps:

1. **Check Python version:**
   ```powershell
   python --version
   ```
   Should be 3.7 or higher

2. **Check yt-dlp installation:**
   ```powershell
   pip show yt-dlp
   ```

3. **Test yt-dlp directly:**
   ```powershell
   yt-dlp --version
   ```

4. **Check FFmpeg:**
   ```powershell
   ffmpeg -version
   ```

5. **Try a simple public video:**
   ```powershell
   python quick_download.py https://www.youtube.com/watch?v=jNQXAC9IVRw
   ```
   (This is the "Me at the zoo" video - first ever YouTube video)

---

## Getting Help

If you've tried everything above and still have issues:

1. **Check the error message carefully** - it often tells you exactly what's wrong
2. **Update everything:**
   ```powershell
   pip install --upgrade yt-dlp ffmpeg-python
   ```
3. **Try the command-line version** to see detailed errors:
   ```powershell
   python youtube_downloader.py
   ```
4. **Check yt-dlp issues:** https://github.com/yt-dlp/yt-dlp/issues

---

## Summary: Age-Restricted Videos

✅ **What Works:**
- Using cookies.txt exported from browser extension
- Being logged into YouTube when exporting cookies
- Keeping cookies.txt updated (re-export if login expires)

❌ **What Doesn't Work:**
- Trying to copy Chrome cookies while Chrome is running
- Not being logged into YouTube
- Using expired cookies

💡 **Best Practice:**
- Export cookies.txt once
- Keep it in your project folder
- Re-export if you log out of YouTube
