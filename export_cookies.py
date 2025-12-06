"""
Helper script to export YouTube cookies from your browser.
This is needed for downloading age-restricted videos.
"""

import os
import platform


def print_instructions():
    """Print instructions for exporting cookies."""
    print("=" * 60)
    print("YouTube Cookie Export Guide")
    print("=" * 60)
    print("\nTo download age-restricted videos, you need to export")
    print("your YouTube cookies from your browser.\n")
    
    print("METHOD 1: Using Browser Extension (RECOMMENDED)")
    print("-" * 60)
    print("1. Install 'Get cookies.txt LOCALLY' extension:")
    print("   Chrome: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc")
    print("   Firefox: https://addons.mozilla.org/firefox/addon/cookies-txt/")
    print("   Edge: Same as Chrome link")
    print("\n2. Log into YouTube in your browser")
    print("\n3. Go to any YouTube page")
    print("\n4. Click the extension icon")
    print("\n5. Click 'Export' or 'Get cookies.txt'")
    print("\n6. Save the file as 'cookies.txt' in this folder:")
    print(f"   {os.path.dirname(os.path.abspath(__file__))}")
    
    print("\n\nMETHOD 2: Using yt-dlp directly")
    print("-" * 60)
    print("Run this command to test if your browser cookies work:")
    print("\n   yt-dlp --cookies-from-browser firefox YOUR_VIDEO_URL")
    print("\nReplace 'firefox' with your browser: chrome, firefox, edge, etc.")
    print("If this works, you can use the browser parameter in the script.")
    
    print("\n\nMETHOD 3: Manual Cookie File")
    print("-" * 60)
    print("For Firefox:")
    print("1. Install 'cookies.txt' addon")
    print("2. Log into YouTube")
    print("3. Export cookies and save as cookies.txt in this folder")
    
    print("\n" + "=" * 60)
    print("After exporting cookies, run youtube_downloader.py again")
    print("=" * 60 + "\n")
    
    # Check if cookies.txt exists
    cookies_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies.txt')
    if os.path.exists(cookies_path):
        print(f"✓ cookies.txt found at: {cookies_path}")
        print("You're ready to download age-restricted videos!\n")
    else:
        print(f"✗ cookies.txt NOT found at: {cookies_path}")
        print("Please export your cookies using one of the methods above.\n")


def check_browser_cookies():
    """Check which browsers might have cookies available."""
    print("\nChecking for browser cookie databases...")
    print("-" * 60)
    
    system = platform.system()
    home = os.path.expanduser("~")
    
    browsers = []
    
    if system == "Windows":
        # Chrome
        chrome_path = os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
        if os.path.exists(chrome_path):
            browsers.append("Chrome")
        
        # Edge
        edge_path = os.path.join(home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Network", "Cookies")
        if os.path.exists(edge_path):
            browsers.append("Edge")
        
        # Firefox
        firefox_path = os.path.join(home, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
        if os.path.exists(firefox_path):
            browsers.append("Firefox")
    
    if browsers:
        print(f"Found cookies for: {', '.join(browsers)}")
        print("\nNote: Chrome cookies might be locked if Chrome is running.")
        print("Try closing Chrome completely or use the cookie export method.\n")
    else:
        print("No browser cookie databases found.")
        print("Please use the browser extension method to export cookies.\n")


if __name__ == "__main__":
    print_instructions()
    check_browser_cookies()
    
    input("\nPress Enter to exit...")
