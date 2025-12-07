"""
YouTube Video Downloader - GUI Version
A user-friendly graphical interface for downloading YouTube videos.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import sys
import webbrowser
import shutil
import yt_dlp
from pathlib import Path
import traceback
import urllib.request
import io


class YouTubeDownloader:
    """
    A YouTube video downloader that handles age-restricted content.
    Uses yt-dlp library for robust video downloading.
    """
    
    def __init__(self, output_path='downloads'):
        """
        Initialize the downloader.
        
        Args:
            output_path (str): Directory where videos will be saved
        """
        self.output_path = output_path
        Path(output_path).mkdir(parents=True, exist_ok=True)
    
    def download_video(self, url, quality='best', format_type='mp4', use_cookies=True, proxy=None, progress_hook=None):
        """
        Download a YouTube video, including age-restricted content.
        
        Args:
            url (str): YouTube video URL
            quality (str): Video quality ('best', 'worst', or specific height like '720')
            format_type (str): Output format ('mp4', 'mkv', 'webm', etc.)
            use_cookies (bool): Whether to attempt using cookies
            proxy (str): Proxy server URL (optional)
            progress_hook (callable): Callback function for download progress
        
        Returns:
            dict: Download information including success status and file path
        """
        try:
            # Configure yt-dlp options
            ydl_opts = {
                'format': f'bestvideo[ext={format_type}]+bestaudio[ext=m4a]/best[ext={format_type}]/best',
                'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'no_warnings': False,
                'quiet': False,
                'merge_output_format': format_type,
                # Critical for age-restricted videos
                'age_limit': None,  # No age limit
            }
            
            # Add progress hook if provided
            if progress_hook:
                ydl_opts['progress_hooks'] = [progress_hook]
            
            # Add proxy if provided
            if proxy:
                ydl_opts['proxy'] = proxy
            
            # Try to add cookies if available and requested
            if use_cookies:
                cookies_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
                if os.path.exists(cookies_file):
                    ydl_opts['cookiefile'] = cookies_file
                    print("Using cookies.txt file for authentication")
                else:
                    # Try browser cookies but don't fail if it doesn't work
                    try:
                        ydl_opts['cookiesfrombrowser'] = ('chrome',)
                    except:
                        pass  # Continue without browser cookies
            
            # Adjust quality settings
            if quality != 'best':
                if quality == 'worst':
                    ydl_opts['format'] = 'worst'
                elif quality.isdigit():
                    ydl_opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'
            
            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading video from: {url}")
                info = ydl.extract_info(url, download=True)
                
                # Get the downloaded file path
                filename = ydl.prepare_filename(info)
                
                return {
                    'success': True,
                    'title': info.get('title', 'Unknown'),
                    'file_path': filename,
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def download_audio_only(self, url, format_type='mp3', use_cookies=True, proxy=None, progress_hook=None):
        """
        Download only the audio from a YouTube video.
        
        Args:
            url (str): YouTube video URL
            format_type (str): Audio format ('mp3', 'wav', 'm4a', etc.)
            use_cookies (bool): Whether to attempt using cookies
            proxy (str): Proxy server URL (optional)
            progress_hook (callable): Callback function for download progress
        
        Returns:
            dict: Download information
        """
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': format_type,
                    'preferredquality': '192',
                }],
                'nocheckcertificate': True,
                'age_limit': None,
            }
            
            # Add progress hook if provided
            if progress_hook:
                ydl_opts['progress_hooks'] = [progress_hook]
            
            # Add proxy if provided
            if proxy:
                ydl_opts['proxy'] = proxy
            
            # Try to add cookies if available and requested
            if use_cookies:
                cookies_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
                if os.path.exists(cookies_file):
                    ydl_opts['cookiefile'] = cookies_file
                    print("Using cookies.txt file for authentication")
                else:
                    try:
                        ydl_opts['cookiesfrombrowser'] = ('chrome',)
                    except:
                        pass
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading audio from: {url}")
                info = ydl.extract_info(url, download=True)
                
                return {
                    'success': True,
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0)
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_video_info(self, url, use_cookies=True, proxy=None):
        """
        Get information about a video without downloading it.
        
        Args:
            url (str): YouTube video URL
            use_cookies (bool): Whether to attempt using cookies
            proxy (str): Proxy server URL (optional)
        
        Returns:
            dict: Video information
        """
        try:
            ydl_opts = {
                'nocheckcertificate': True,
                'age_limit': None,
            }
            
            # Add proxy if provided
            if proxy:
                ydl_opts['proxy'] = proxy
            
            # Try to add cookies if available and requested
            if use_cookies:
                cookies_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
                if os.path.exists(cookies_file):
                    ydl_opts['cookiefile'] = cookies_file
                    print("Using cookies.txt file for authentication")
                else:
                    try:
                        ydl_opts['cookiesfrombrowser'] = ('chrome',)
                    except:
                        pass  # Continue without browser cookies
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'success': True,
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'views': info.get('view_count', 0),
                    'description': info.get('description', ''),
                    'age_restricted': info.get('age_limit', 0) > 0
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_videos(self, query, max_results=10):
        """
        Search for YouTube videos.
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results
        
        Returns:
            dict: Search results with success status and video list
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_url = f"ytsearch{max_results}:{query}"
                result = ydl.extract_info(search_url, download=False)
                
                videos = []
                for entry in result.get('entries', []):
                    if entry:
                        # Extract video ID from URL or id field
                        video_id = entry.get('id', '')
                        video_url = entry.get('url', '')
                        
                        # Get thumbnail - try multiple sources
                        thumbnail = entry.get('thumbnail', '')
                        
                        # If no thumbnail but we have video ID, construct YouTube thumbnail URL
                        if not thumbnail and video_id:
                            thumbnail = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
                        
                        # If we have thumbnails array, get the best one
                        thumbnails = entry.get('thumbnails', [])
                        if thumbnails and isinstance(thumbnails, list):
                            # Get the last (usually highest quality) thumbnail
                            thumbnail = thumbnails[-1].get('url', thumbnail)
                        
                        videos.append({
                            'title': entry.get('title', 'Unknown'),
                            'url': video_url,
                            'id': video_id,
                            'duration': entry.get('duration', 0),
                            'views': entry.get('view_count', 0),
                            'channel': entry.get('uploader', 'Unknown'),
                            'thumbnail': thumbnail
                        })
                
                return {
                    'success': True,
                    'videos': videos
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'videos': []
            }


class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.state('zoomed')  # Open maximized on Windows
        self.root.resizable(True, True)
        
        # Set icon color scheme
        self.bg_color = "#f0f0f0"
        self.accent_color = "#FF0000"  # YouTube red
        self.root.configure(bg=self.bg_color)
        
        # Initialize downloader
        self.downloader = None
        self.download_path = os.path.join(os.getcwd(), "downloads")
        
        self.create_widgets()
        self.check_cookies()
        
        # Check VLC installation
        vlc_installed, vlc_path = self.check_vlc_installed()
        if not vlc_installed:
            # Show VLC download prompt after GUI is ready
            self.root.after(1000, self.show_vlc_download_prompt)
        
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # Title
        title_frame = tk.Frame(self.root, bg=self.accent_color, height=60)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        # Title inner frame for layout
        title_inner = tk.Frame(title_frame, bg=self.accent_color)
        title_inner.pack(fill=tk.BOTH, expand=True, padx=10)
        
        title_label = tk.Label(
            title_inner, 
            text="🎬 YouTube Video Downloader",
            font=("Arial", 20, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        title_label.pack(side=tk.LEFT, pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # URL Input Section
        url_frame = tk.LabelFrame(
            main_frame, 
            text="Video URL or YouTube Search",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=10
        )
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Info label about supported sites
        supported_label = tk.Label(
            url_frame,
            text="✓ Supports YouTube, Mediaset, Vimeo, and 1000+ other sites",
            font=("Arial", 8),
            bg=self.bg_color,
            fg="#2196F3"
        )
        supported_label.pack(anchor="w", pady=(0, 5))
        
        # Search or URL input
        input_row = tk.Frame(url_frame, bg=self.bg_color)
        input_row.pack(fill=tk.X, pady=5)
        
        self.url_entry = tk.Entry(
            input_row,
            font=("Arial", 11),
            relief=tk.SOLID,
            bd=1
        )
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5)
        self.url_entry.insert(0, "Paste video URL or search YouTube...")
        self.url_entry.bind("<FocusIn>", self.clear_placeholder)
        self.url_entry.bind("<FocusOut>", self.restore_placeholder)
        self.url_entry.config(fg="gray")
        
        # Search button
        search_btn = tk.Button(
            input_row,
            text="🔍",
            command=self.search_videos,
            font=("Arial", 14),
            bg="#2196F3",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10
        )
        search_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Smart button that changes from Fetch to Download
        self.action_btn = tk.Button(
            url_frame,
            text="📥 FETCH VIDEO INFO",
            command=self.smart_button_action,
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED,
            bd=4,
            padx=40,
            pady=15,
            cursor="hand2"
        )
        self.action_btn.pack(pady=10, fill=tk.X)
        
        # Cookie buttons frame
        cookie_frame = tk.Frame(url_frame, bg=self.bg_color)
        cookie_frame.pack(pady=5, fill=tk.X)
        
        self.cookie_wizard_btn = tk.Button(
            cookie_frame,
            text="🍪 Setup Cookies for Age-Restricted Videos",
            command=self.cookie_setup_wizard,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.cookie_wizard_btn.pack(side=tk.LEFT, expand=True, padx=2)
        
        # Upload cookie file button
        self.upload_cookie_btn = tk.Button(
            cookie_frame,
            text="📂 Upload cookies.txt",
            command=self.import_cookies_file,
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="white",
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.upload_cookie_btn.pack(side=tk.LEFT, expand=True, padx=2)
        
        # Proxy Settings Section
        proxy_frame = tk.LabelFrame(
            main_frame,
            text="Proxy Settings (for geo-blocked content)",
            font=("Arial", 9),
            bg=self.bg_color,
            padx=10,
            pady=5
        )
        proxy_frame.pack(fill=tk.X, pady=(5, 10))
        
        proxy_input_frame = tk.Frame(proxy_frame, bg=self.bg_color)
        proxy_input_frame.pack(fill=tk.X)
        
        tk.Label(
            proxy_input_frame,
            text="Proxy URL:",
            font=("Arial", 9),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.proxy_entry = tk.Entry(
            proxy_input_frame,
            font=("Arial", 10),
            width=50
        )
        self.proxy_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.proxy_entry.insert(0, "http://proxy.example.com:8080 or socks5://127.0.0.1:1080")
        self.proxy_entry.bind("<FocusIn>", self.clear_proxy_placeholder)
        self.proxy_entry.bind("<FocusOut>", self.restore_proxy_placeholder)
        self.proxy_entry.config(fg="gray")
        
        # Proxy help button
        proxy_help_btn = tk.Button(
            proxy_input_frame,
            text="🌍 Find Proxies",
            command=self.show_proxy_help,
            font=("Arial", 9, "bold"),
            bg="#2196F3",
            fg="white",
            relief=tk.RAISED,
            cursor="hand2",
            padx=10,
            pady=5,
            bd=2
        )
        proxy_help_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Load proxy button
        load_proxy_btn = tk.Button(
            proxy_input_frame,
            text="📋 Load Saved",
            command=self.load_proxy_from_file,
            font=("Arial", 9, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED,
            cursor="hand2",
            padx=10,
            pady=5,
            bd=2
        )
        load_proxy_btn.pack(side=tk.LEFT)
        
        tk.Label(
            proxy_frame,
            text="💡 Tip: For Mediaset/Italian content, use an Italian proxy or VPN",
            font=("Arial", 8),
            bg=self.bg_color,
            fg="#FF9800"
        ).pack(anchor="w", pady=(2, 0))
        
        # Browser extension links frame
        extensions_frame = tk.LabelFrame(
            url_frame,
            text="Install Cookie Extension (Required for Age-Restricted Videos)",
            font=("Arial", 8, "bold"),
            bg=self.bg_color,
            fg="#FF0000",
            padx=5,
            pady=5
        )
        extensions_frame.pack(pady=5, fill=tk.X)
        
        # Chrome link
        chrome_link = tk.Label(
            extensions_frame,
            text="🔗 Chrome Extension",
            font=("Arial", 9, "underline"),
            bg=self.bg_color,
            fg="blue",
            cursor="hand2"
        )
        chrome_link.pack(side=tk.LEFT, padx=10)
        chrome_link.bind("<Button-1>", lambda e: self.open_browser_link(
            "https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc"
        ))
        
        # Firefox link
        firefox_link = tk.Label(
            extensions_frame,
            text="🔗 Firefox Extension",
            font=("Arial", 9, "underline"),
            bg=self.bg_color,
            fg="blue",
            cursor="hand2"
        )
        firefox_link.pack(side=tk.LEFT, padx=10)
        firefox_link.bind("<Button-1>", lambda e: self.open_browser_link(
            "https://addons.mozilla.org/firefox/addon/cookies-txt/"
        ))
        
        # Edge link
        edge_link = tk.Label(
            extensions_frame,
            text="🔗 Edge Extension",
            font=("Arial", 9, "underline"),
            bg=self.bg_color,
            fg="blue",
            cursor="hand2"
        )
        edge_link.pack(side=tk.LEFT, padx=10)
        edge_link.bind("<Button-1>", lambda e: self.open_browser_link(
            "https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc"
        ))
        
        # Track the current mode
        self.button_mode = "fetch"  # can be "fetch" or "download"
        
        # Video Info Section
        info_frame = tk.LabelFrame(
            main_frame,
            text="Video Information",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=10
        )
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Info text widget
        self.info_text = tk.Text(
            info_frame,
            height=8,
            font=("Courier New", 9),
            relief=tk.SOLID,
            bd=1,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Download type selection (Video or Audio) - always best quality
        type_frame = tk.LabelFrame(
            main_frame,
            text="Download Type (Always Best Quality)",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=10
        )
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        type_row = tk.Frame(type_frame, bg=self.bg_color)
        type_row.pack(fill=tk.X, pady=5)
        
        self.download_type = tk.StringVar(value="video")
        
        tk.Radiobutton(
            type_row,
            text="🎥 Video (MP4) - Best Quality",
            variable=self.download_type,
            value="video",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            cursor="hand2",
            selectcolor="#4CAF50"
        ).pack(side=tk.LEFT, padx=15, pady=5)
        
        tk.Radiobutton(
            type_row,
            text="🎵 Audio Only (MP3) - Best Quality",
            variable=self.download_type,
            value="audio",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            cursor="hand2",
            selectcolor="#4CAF50"
        ).pack(side=tk.LEFT, padx=15, pady=5)
        
        # Default Download Path Section
        path_frame = tk.LabelFrame(
            main_frame,
            text="Default Download Location (You can change it when downloading)",
            font=("Arial", 9, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=5
        )
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        path_row = tk.Frame(path_frame, bg=self.bg_color)
        path_row.pack(fill=tk.X, pady=5)
        
        self.path_label = tk.Label(
            path_row,
            text=self.download_path,
            font=("Arial", 9),
            bg="white",
            relief=tk.SOLID,
            bd=1,
            anchor="w",
            padx=5,
            pady=5
        )
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = tk.Button(
            path_row,
            text="📁 Change Default",
            command=self.browse_folder,
            font=("Arial", 9),
            bg="#2196F3",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=5
        )
        browse_btn.pack(side=tk.LEFT)
        
        # Progress Section
        progress_frame = tk.Frame(main_frame, bg=self.bg_color)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready to download",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="gray"
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=400
        )
        self.progress_bar.pack(pady=5)
        
        # Status bar at bottom
        status_frame = tk.Frame(self.root, bg="#e0e0e0", height=50)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        status_inner = tk.Frame(status_frame, bg="#e0e0e0")
        status_inner.pack(fill=tk.BOTH, expand=True, padx=5, pady=8)
        
        self.status_label = tk.Label(
            status_inner,
            text="⚠️ Cookie status: Checking...",
            font=("Arial", 9),
            bg="#e0e0e0",
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add exit button - Make it very visible
        exit_btn = tk.Button(
            status_inner,
            text="❌ EXIT",
            command=self.exit_application,
            font=("Arial", 10, "bold"),
            bg="#f44336",
            fg="white",
            relief=tk.RAISED,
            cursor="hand2",
            padx=20,
            pady=5,
            bd=3
        )
        exit_btn.pack(side=tk.RIGHT, padx=5)
        
        # Add help button for cookies
        help_btn = tk.Button(
            status_inner,
            text="📖 Help",
            command=self.show_cookie_help,
            font=("Arial", 9),
            bg="#FFA500",
            fg="white",
            relief=tk.RAISED,
            cursor="hand2",
            padx=10,
            pady=5,
            bd=2
        )
        help_btn.pack(side=tk.RIGHT, padx=(5, 0))
    
    def clear_placeholder(self, event):
        """Clear placeholder text on focus."""
        current_text = self.url_entry.get()
        if current_text in ["https://www.youtube.com/watch?v=...", "Paste URL or type search query...", "Paste video URL or search YouTube..."]:
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg="black")
    
    def exit_application(self):
        """Exit the application with confirmation."""
        result = messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to exit?\n\nAny downloads in progress will be cancelled."
        )
        if result:
            self.root.quit()
            self.root.destroy()
    
    def restore_placeholder(self, event):
        """Restore placeholder if empty."""
        if not self.url_entry.get():
            self.url_entry.insert(0, "Paste URL or type search query...")
            self.url_entry.config(fg="gray")
    
    def clear_proxy_placeholder(self, event):
        """Clear proxy placeholder text on focus."""
        current_text = self.proxy_entry.get()
        if "proxy.example.com" in current_text or "127.0.0.1:1080" in current_text:
            self.proxy_entry.delete(0, tk.END)
            self.proxy_entry.config(fg="black")
    
    def restore_proxy_placeholder(self, event):
        """Restore proxy placeholder if empty."""
        if not self.proxy_entry.get():
            self.proxy_entry.insert(0, "http://proxy.example.com:8080 or socks5://127.0.0.1:1080")
            self.proxy_entry.config(fg="gray")
    
    def get_proxy(self):
        """Get proxy URL if provided."""
        proxy = self.proxy_entry.get().strip()
        # Return None if empty or contains placeholder text
        if not proxy or "proxy.example.com" in proxy or "127.0.0.1:1080" in proxy or proxy == "":
            return None
        return proxy
    
    def search_videos(self):
        """Search for YouTube videos."""
        query = self.url_entry.get()
        
        if not query or query == "Paste video URL or search YouTube...":
            messagebox.showwarning("Invalid Query", "Please enter a search query or video URL")
            return
        
        # Check if it's already a URL
        if query.startswith("http"):
            messagebox.showinfo("URL Detected", "This looks like a URL. Click 'Fetch Video Info' instead to download from any supported site.")
            return
        
        # Show searching message
        self.progress_label.config(text="Searching YouTube...", fg="blue")
        self.progress_bar.start(10)
        
        # Run search in thread
        thread = threading.Thread(target=self._search_thread, args=(query,))
        thread.daemon = True
        thread.start()
    
    def _search_thread(self, query):
        """Thread function to search videos."""
        try:
            if not self.downloader:
                self.downloader = YouTubeDownloader(output_path=self.download_path)
            
            result = self.downloader.search_videos(query, max_results=50)
            
            if result['success']:
                if result['videos']:
                    self.root.after(0, lambda: self.show_search_results(result['videos']))
                    self.root.after(0, lambda: self.progress_bar.stop())
                    self.root.after(0, lambda: self.progress_label.config(text="Search complete - Select a video", fg="green"))
                else:
                    # No results found
                    self.root.after(0, lambda: self.progress_bar.stop())
                    self.root.after(0, lambda: self.progress_label.config(text="No results found", fg="orange"))
                    self.root.after(0, lambda: messagebox.showinfo("No Results", "No videos found for your search query. Try different keywords."))
            else:
                error_msg = result.get('error', 'Search failed')
                self.root.after(0, lambda: self.progress_bar.stop())
                self.root.after(0, lambda: self.progress_label.config(text="Search failed", fg="red"))
                self.root.after(0, lambda: messagebox.showerror("Search Failed", f"Could not search videos: {error_msg}"))
        
        except Exception as e:
            self.root.after(0, lambda: self.progress_bar.stop())
            self.root.after(0, lambda: self.progress_label.config(text="Search failed", fg="red"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Search error: {str(e)}"))
    
    def show_search_results(self, videos):
        """Show search results in a popup window with preview panel."""
        results_window = tk.Toplevel(self.root)
        results_window.title("Search Results")
        results_window.state('zoomed')  # Open maximized
        
        # Title
        title = tk.Label(
            results_window,
            text="🔍 Search Results - Click on a video to preview or select",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            pady=10
        )
        title.pack(fill=tk.X)
        
        # Main container with two panels
        main_container = tk.Frame(results_window)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Search results list
        left_panel = tk.Frame(main_container, width=600)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollable frame for results
        canvas = tk.Canvas(left_panel)
        scrollbar = tk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        # Ensure 'canvas' is defined before configuring yscrollcommand
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Make scrollable_frame accessible in this scope
        # This ensures scrollable_frame is defined before use below

        # Enable mouse wheel scrolling for left panel
        def _on_mousewheel_left(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel_left)
        
        # Right panel - Video preview
        right_panel = tk.Frame(main_container, width=600, bg="#f5f5f5", relief=tk.SUNKEN, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_panel.pack_propagate(False)
        
        # Preview header
        preview_header = tk.Label(
            right_panel,
            text="📺 Video Preview",
            font=("Arial", 14, "bold"),
            bg="#FF0000",
            fg="white",
            pady=10
        )
        preview_header.pack(fill=tk.X)
        
        # Preview content area (scrollable)
        preview_canvas = tk.Canvas(right_panel, bg="#f5f5f5")
        preview_scrollbar = tk.Scrollbar(right_panel, orient="vertical", command=preview_canvas.yview)
        preview_content = tk.Frame(preview_canvas, bg="#f5f5f5")
        
        preview_content.bind(
            "<Configure>",
            lambda e: preview_canvas.configure(scrollregion=preview_canvas.bbox("all"))
        )
        
        preview_canvas.create_window((0, 0), window=preview_content, anchor="nw")
        preview_canvas.configure(yscrollcommand=preview_scrollbar.set)
        
        # Enable mouse wheel scrolling for right panel
        def _on_mousewheel_right(event):
            preview_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        preview_canvas.bind("<MouseWheel>", _on_mousewheel_right)
        
        # Default preview message
        default_msg = tk.Label(
            preview_content,
            text="👈 Click on a video from the list\nto see detailed preview here",
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="gray",
            pady=100
        )
        default_msg.pack(expand=True)
        
        preview_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Function to show video preview
        def show_preview(video):
            print(f"DEBUG: show_preview called for: {video.get('title', 'Unknown')}")
            
            # Stop any existing VLC player before clearing
            if hasattr(preview_content, 'vlc_player'):
                try:
                    preview_content.vlc_player.stop()
                    preview_content.vlc_player.release()
                    print("DEBUG: Stopped previous VLC player")
                except:
                    pass
                delattr(preview_content, 'vlc_player')
            if hasattr(preview_content, 'vlc_instance'):
                try:
                    preview_content.vlc_instance.release()
                except:
                    pass
                delattr(preview_content, 'vlc_instance')
            
            # Clear preview content
            for widget in preview_content.winfo_children():
                widget.destroy()
            
            # Video title at top
            title_label = tk.Label(
                preview_content,
                text=video.get('title', 'Unknown Title'),
                font=("Arial", 12, "bold"),
                wraplength=550,
                justify=tk.LEFT,
                bg="#f5f5f5",
                padx=10,
                pady=10
            )
            title_label.pack(anchor="w", fill=tk.X)
            
            # Embedded video player frame
            player_frame = tk.Frame(preview_content, bg="black", width=560, height=315)
            player_frame.pack(pady=10)
            player_frame.pack_propagate(False)
            player_frame.update()
            
            # Initialize VLC variables
            vlc_player = None
            vlc_instance = None
            temp_video_file = None
            
            # Try to download preview clip for VLC playback
            print("DEBUG: Attempting preview clip download for VLC playback")
            vlc_success = False
            
            # Show downloading progress message
            download_label = tk.Label(
                player_frame,
                text="⏳ Downloading 30-second preview...\nPlease wait, this may take a moment.",
                font=("Arial", 12, "bold"),
                bg="black",
                fg="yellow",
                justify=tk.CENTER
            )
            download_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            player_frame.update()
            
            try:
                import vlc
                import tempfile
                
                # Create temp directory for preview
                temp_dir = tempfile.gettempdir()
                temp_video_file = os.path.join(temp_dir, f"yt_preview_{video.get('id', 'temp')}.mp4")
                
                print(f"DEBUG: Downloading 30-second preview to: {temp_video_file}")
                
                # Download first 30 seconds as preview
                ydl_opts = {
                    'format': 'best[height<=480]',  # Lower quality for faster preview
                    'quiet': False,
                    'no_warnings': False,
                    'outtmpl': temp_video_file,
                    'external_downloader': 'ffmpeg',
                    'external_downloader_args': ['-t', '30'],  # Download only 30 seconds
                }
                
                # Add cookies if available
                cookies_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
                if os.path.exists(cookies_file):
                    ydl_opts['cookiefile'] = cookies_file
                    print(f"DEBUG: Using cookies file: {cookies_file}")
                
                # Update progress message
                download_label.config(text="⏳ Processing preview...\nAlmost ready!")
                player_frame.update()
                
                # Try to download preview clip
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    print("DEBUG: Starting preview download...")
                    ydl.download([video['url']])
                    
                # Check if file was created
                if os.path.exists(temp_video_file) and os.path.getsize(temp_video_file) > 0:
                    print(f"DEBUG: Preview file downloaded successfully: {os.path.getsize(temp_video_file)} bytes")
                    
                    # Remove download progress label
                    download_label.destroy()
                    
                    # Create VLC instance and player
                    vlc_instance = vlc.Instance('--no-xlib')
                    vlc_player = vlc_instance.media_player_new()
                    
                    # Store references to prevent garbage collection
                    preview_content.vlc_instance = vlc_instance
                    preview_content.vlc_player = vlc_player
                    
                    # Create media from file
                    media = vlc_instance.media_new(temp_video_file)
                    vlc_player.set_media(media)
                    
                    # Embed VLC in tkinter frame
                    if sys.platform.startswith('win'):
                        vlc_player.set_hwnd(player_frame.winfo_id())
                    else:
                        vlc_player.set_xwindow(player_frame.winfo_id())
                    
                    vlc_success = True
                    print("DEBUG: VLC player initialized with preview clip successfully")
                else:
                    print("DEBUG: Preview file not created or empty")
                    download_label.destroy()
                    vlc_success = False
                    
            except Exception as e:
                print(f"DEBUG: Preview clip download failed: {e}")
                traceback.print_exc()
                # Remove download progress label on error
                try:
                    download_label.destroy()
                except:
                    pass
                vlc_success = False
                # Clean up failed download
                if temp_video_file and os.path.exists(temp_video_file):
                    try:
                        os.remove(temp_video_file)
                    except:
                        pass
            
            # If VLC failed, show thumbnail
            if not vlc_success:
                print("DEBUG: Falling back to thumbnail preview")
                self._show_thumbnail_in_frame(video, player_frame)
            
            # Add status label
            if vlc_success:
                status_label = tk.Label(
                    preview_content,
                    text="🎬 30-second preview loaded! Click Play to watch",
                    font=("Arial", 9, "italic"),
                    bg="#f5f5f5",
                    fg="#4CAF50",
                    pady=5
                )
            else:
                status_label = tk.Label(
                    preview_content,
                    text="⚠️ Preview download unavailable. Showing thumbnail (you can still download full video).",
                    font=("Arial", 9, "italic"),
                    bg="#f5f5f5",
                    fg="#FF6600",
                    pady=5
                )
            status_label.pack()
            
            # DEBUG: Print button creation status
            print(f"DEBUG: VLC Success Status = {vlc_success}")
            print(f"DEBUG: Creating control buttons...")
            
            # Control buttons frame (ALWAYS show)
            controls_frame = tk.Frame(preview_content, bg="#f5f5f5")
            controls_frame.pack(fill=tk.X, pady=10)
            
            # Play button (works for both VLC and non-VLC)
            def play_video():
                if vlc_success and hasattr(preview_content, 'vlc_player'):
                    preview_content.vlc_player.play()
                    print("DEBUG: Playing video with VLC")
                else:
                    # Open in browser if VLC not available
                    webbrowser.open(video['url'])
                    print("DEBUG: Opening in browser (VLC not available)")
            
            play_btn = tk.Button(
                controls_frame,
                text="▶ Play",
                command=play_video,
                font=("Arial", 10, "bold"),
                bg="#4CAF50",
                fg="white",
                cursor="hand2",
                padx=15,
                pady=5
            )
            play_btn.pack(side=tk.LEFT, padx=2)
            print("DEBUG: Play button created")
            
            # Pause button (only functional with VLC)
            def pause_video():
                if vlc_success and hasattr(preview_content, 'vlc_player'):
                    preview_content.vlc_player.pause()
                    print("DEBUG: Paused video")
                else:
                    messagebox.showinfo("VLC Not Available", "Pause control requires VLC player.\n\nFor YouTube videos, use the browser player controls.")
            
            pause_btn = tk.Button(
                controls_frame,
                text="⏸ Pause",
                command=pause_video,
                font=("Arial", 10, "bold"),
                bg="#FF9800" if vlc_success else "#CCCCCC",
                fg="white",
                cursor="hand2" if vlc_success else "arrow",
                padx=15,
                pady=5,
                state=tk.NORMAL if vlc_success else tk.DISABLED
            )
            pause_btn.pack(side=tk.LEFT, padx=2)
            print("DEBUG: Pause button created")
            
            # Stop button (only functional with VLC)
            def stop_video():
                if vlc_success and hasattr(preview_content, 'vlc_player'):
                    preview_content.vlc_player.stop()
                    print("DEBUG: Stopped video")
                else:
                    messagebox.showinfo("VLC Not Available", "Stop control requires VLC player.\n\nFor YouTube videos, use the browser player controls.")
            
            stop_btn = tk.Button(
                controls_frame,
                text="⏹ Stop",
                command=stop_video,
                font=("Arial", 10, "bold"),
                bg="#f44336" if vlc_success else "#CCCCCC",
                fg="white",
                cursor="hand2" if vlc_success else "arrow",
                padx=15,
                pady=5,
                state=tk.NORMAL if vlc_success else tk.DISABLED
            )
            stop_btn.pack(side=tk.LEFT, padx=2)
            print("DEBUG: Stop button created")
            
            # Volume control (only functional with VLC)
            if vlc_success:
                volume_frame = tk.Frame(controls_frame, bg="#f5f5f5")
                volume_frame.pack(side=tk.LEFT, padx=10)
                
                tk.Label(volume_frame, text="🔊", bg="#f5f5f5", font=("Arial", 10)).pack(side=tk.LEFT)
                
                def set_volume(val):
                    if hasattr(preview_content, 'vlc_player'):
                        preview_content.vlc_player.audio_set_volume(int(float(val)))
                
                volume_slider = tk.Scale(
                    volume_frame,
                    from_=0,
                    to=100,
                    orient=tk.HORIZONTAL,
                    command=set_volume,
                    length=100,
                    showvalue=False
                )
                volume_slider.set(80)
                volume_slider.pack(side=tk.LEFT)
                print("DEBUG: Volume slider created")
            
            # Open in Browser button (always available as fallback)
            def play_in_browser():
                webbrowser.open(video['url'])
                print("DEBUG: Opened video in browser")
            
            play_browser_btn = tk.Button(
                controls_frame,
                text="🌐 Open in Browser",
                command=play_in_browser,
                font=("Arial", 10, "bold"),
                bg="#2196F3",
                fg="white",
                cursor="hand2",
                padx=15,
                pady=5
            )
            play_browser_btn.pack(side=tk.LEFT, padx=2)
            print("DEBUG: Open in Browser button created")
            
            # Close button
            def close_preview():
                if vlc_player:
                    vlc_player.stop()
                    vlc_player.release()
                if vlc_instance:
                    vlc_instance.release()
                # Clean up temporary file if exists
                if temp_video_file and os.path.exists(temp_video_file):
                    try:
                        os.remove(temp_video_file)
                    except:
                        pass
                results_window.destroy()
            
            close_btn = tk.Button(
                controls_frame,
                text="✕ Close",
                command=close_preview,
                font=("Arial", 10, "bold"),
                bg="#555555",
                fg="white",
                cursor="hand2",
                padx=15,
                pady=5
            )
            close_btn.pack(side=tk.RIGHT, padx=5)
            print("DEBUG: Close button created")
            print("DEBUG: All buttons created successfully!")
            
            # Video information below controls
            info_section = tk.Frame(preview_content, bg="#f5f5f5")
            info_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Channel
            channel_label = tk.Label(
                info_section,
                text=f"📺 Channel: {video.get('channel', 'Unknown')}",
                font=("Arial", 10),
                bg="#f5f5f5",
                fg="#333",
                anchor="w"
            )
            channel_label.pack(anchor="w", pady=2)
            
            # Duration
            duration = int(video.get('duration', 0)) if video.get('duration') else 0
            duration_str = f"{duration//60}:{duration%60:02d}" if duration > 0 else "N/A"
            duration_label = tk.Label(
                info_section,
                text=f"⏱️ Duration: {duration_str}",
                font=("Arial", 10),
                bg="#f5f5f5",
                fg="#333",
                anchor="w"
            )
            duration_label.pack(anchor="w", pady=2)
            
            # Views
            views = int(video.get('views', 0)) if video.get('views') else 0
            views_str = f"{views:,}" if views > 0 else "N/A"
            views_label = tk.Label(
                info_section,
                text=f"👁️ Views: {views_str}",
                font=("Arial", 10),
                bg="#f5f5f5",
                fg="#333",
                anchor="w"
            )
            views_label.pack(anchor="w", pady=2)
            
            # Video URL
            tk.Label(
                info_section,
                text="🔗 URL:",
                font=("Arial", 10, "bold"),
                bg="#f5f5f5",
                anchor="w"
            ).pack(anchor="w", pady=(10, 2))
            
            url_text = tk.Text(info_section, height=2, wrap=tk.WORD, font=("Courier", 8))
            url_text.insert(1.0, video['url'])
            url_text.config(state=tk.DISABLED, bg="white")
            url_text.pack(fill=tk.X, pady=2)
            
            # Select button
            select_btn = tk.Button(
                info_section,
                text="✓ SELECT THIS VIDEO FOR DOWNLOAD",
                command=lambda: self.select_video_from_search(video['url'], results_window),
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                cursor="hand2",
                padx=30,
                pady=12
            )
            select_btn.pack(pady=15)

        # Add video entries
        for i, video in enumerate(videos):
            video_frame = tk.Frame(scrollable_frame, relief=tk.RAISED, bd=2, padx=10, pady=10, cursor="hand2", bg="white")
            video_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Video info
            title_label = tk.Label(
                video_frame,
                text=f"🎬 {video.get('title', 'Unknown Title')}",
                font=("Arial", 11, "bold"),
                wraplength=500,
                justify=tk.LEFT,
                cursor="hand2",
                bg="white"
            )
            title_label.pack(anchor="w")
            
            # Format duration and views safely
            duration = int(video.get('duration', 0)) if video.get('duration') else 0
            views = int(video.get('views', 0)) if video.get('views') else 0
            duration_str = f"{duration//60}:{duration%60:02d}" if duration > 0 else "N/A"
            views_str = f"{views:,}" if views > 0 else "N/A"
            
            info_label = tk.Label(
                video_frame,
                text=f"📺 {video.get('channel', 'Unknown')} | 👁️ {views_str} views | ⏱️ {duration_str}",
                font=("Arial", 9),
                fg="gray",
                cursor="hand2",
                bg="white"
            )
            info_label.pack(anchor="w")
            
            # Button frame for actions
            btn_frame = tk.Frame(video_frame, bg="white")
            btn_frame.pack(anchor="e", pady=(5, 0))
            
            # Preview button
            preview_btn = tk.Button(
                btn_frame,
                text="👁️ Preview",
                command=lambda v=video: show_preview(v),
                font=("Arial", 9, "bold"),
                bg="#2196F3",
                fg="white",
                cursor="hand2",
                padx=10,
                pady=3
            )
            preview_btn.pack(side=tk.LEFT, padx=(0, 5))
            
            # Select button
            select_btn = tk.Button(
                btn_frame,
                text="✓ Select",
                command=lambda url=video['url'], win=results_window: self.select_video_from_search(url, win),
                font=("Arial", 9, "bold"),
                bg="#4CAF50",
                fg="white",
                cursor="hand2",
                padx=10,
                pady=3
            )
            select_btn.pack(side=tk.LEFT)
            
            # Bind click events to all widgets in the frame (except buttons)
            def bind_click(widget, vid=video):
                if not isinstance(widget, tk.Button):
                    widget.bind("<Button-1>", lambda e: show_preview(vid))
                for child in widget.winfo_children():
                    bind_click(child, vid)
            
            bind_click(video_frame, video)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
    
    def _show_thumbnail_in_frame(self, video, player_frame):
        """Show thumbnail in the player frame when VLC fails."""
        print(f"DEBUG: _show_thumbnail_in_frame called")
        print(f"DEBUG: Video data: {video}")
        
        # Show loading message first
        loading_label = tk.Label(
            player_frame,
            text="⏳ Loading preview...",
            font=("Arial", 12),
            bg="black",
            fg="white"
        )
        loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        player_frame.update()
        
        thumbnail_url = video.get('thumbnail', '').strip()
        video_id = video.get('id', '').strip()
        print(f"DEBUG: Thumbnail URL: {thumbnail_url}")
        print(f"DEBUG: Video ID: {video_id}")
        
        # If no thumbnail URL but we have video ID, construct one
        if not thumbnail_url and video_id:
            thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
            print(f"DEBUG: Constructed thumbnail URL from video ID: {thumbnail_url}")
        
        if thumbnail_url:
            try:
                from PIL import Image, ImageTk
                
                print(f"DEBUG: Loading thumbnail from: {thumbnail_url}")
                
                # Try to get the highest quality thumbnail
                # For YouTube, try to get maxresdefault (1280x720) or hq720
                if 'youtube.com' in thumbnail_url or 'ytimg.com' in thumbnail_url:
                    video_id = video.get('id', '')
                    print(f"DEBUG: YouTube video ID: {video_id}")
                    
                    if video_id:
                        # Try different quality options in order
                        quality_options = [
                            f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
                            f"https://i.ytimg.com/vi/{video_id}/hq720.jpg",
                            f"https://i.ytimg.com/vi/{video_id}/sddefault.jpg",
                            f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
                            thumbnail_url  # fallback to original
                        ]
                        
                        # Try each quality until one works
                        image_data = None
                        for url in quality_options:
                            try:
                                print(f"DEBUG: Trying thumbnail URL: {url}")
                                with urllib.request.urlopen(url, timeout=5) as response:
                                    image_data = response.read()
                                    thumbnail_url = url
                                    print(f"DEBUG: Successfully loaded from: {url}")
                                    break
                            except Exception as e:
                                print(f"DEBUG: Failed to load {url}: {e}")
                                continue
                        
                        if not image_data:
                            raise Exception("Could not load any thumbnail quality")
                    else:
                        # No video ID, use original thumbnail
                        print(f"DEBUG: No video ID, using original thumbnail")
                        with urllib.request.urlopen(thumbnail_url, timeout=5) as response:
                            image_data = response.read()
                else:
                    # Not YouTube, use original thumbnail
                    print(f"DEBUG: Not YouTube, using original thumbnail")
                    with urllib.request.urlopen(thumbnail_url, timeout=5) as response:
                        image_data = response.read()
                
                # Open and resize image
                image = Image.open(io.BytesIO(image_data))
                print(f"DEBUG: Image loaded, size: {image.size}")
                
                # Calculate size to fit in 560x315 frame while maintaining aspect ratio
                frame_width, frame_height = 560, 315
                img_width, img_height = image.size
                
                # Calculate scaling factor
                scale = min(frame_width / img_width, frame_height / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                
                # Resize image
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"DEBUG: Image resized to: {new_width}x{new_height}")
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Remove loading message
                loading_label.destroy()
                
                # Display thumbnail
                thumbnail_label = tk.Label(player_frame, image=photo, bg="black")
                thumbnail_label.image = photo  # Keep a reference!
                thumbnail_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                
                print("DEBUG: Thumbnail displayed successfully")
                
            except Exception as e:
                print(f"DEBUG: Error loading thumbnail: {e}")
                traceback.print_exc()
                
                # Remove loading message and show error
                try:
                    loading_label.destroy()
                except:
                    pass
                
                # Show error message in frame
                error_label = tk.Label(
                    player_frame,
                    text="⚠️ Thumbnail preview not available\n\nYou can still:\n• Play in Browser\n• Download the video",
                    font=("Arial", 11),
                    bg="black",
                    fg="white",
                    justify=tk.CENTER
                )
                error_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            # No thumbnail available
            print("DEBUG: No thumbnail URL provided")
            try:
                loading_label.destroy()
            except:
                pass
            no_thumb_label = tk.Label(
                player_frame,
                text="📹 No thumbnail available\n\nYou can still:\n• Play in Browser\n• Download the video",
                font=("Arial", 11),
                bg="black",
                fg="white",
                justify=tk.CENTER
            )
            no_thumb_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def _show_thumbnail_preview(self, video, player_frame, preview_content, results_window):
        """Show thumbnail with play button as fallback."""
        if video.get('thumbnail'):
            try:
                import urllib.request
                from PIL import Image, ImageTk
                import io
                
                print(f"DEBUG: Downloading thumbnail from: {video['thumbnail']}")
                # Download thumbnail
                with urllib.request.urlopen(video['thumbnail']) as url:
                    image_data = url.read()
                
                # Open and resize image
                image = Image.open(io.BytesIO(image_data))
                # Resize to fit player frame
                ratio = 560 / image.width
                new_height = int(image.height * ratio)
                image = image.resize((560, new_height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Display thumbnail
                thumbnail_label = tk.Label(player_frame, image=photo, bg="black")
                thumbnail_label.image = photo  # Keep a reference!
                thumbnail_label.pack()
                
                # Play button overlay - opens in browser
                play_overlay = tk.Label(
                    player_frame,
                    text="▶",
                    font=("Arial", 64, "bold"),
                    bg="black",
                    fg="white",
                    cursor="hand2"
                )
                play_overlay.place(relx=0.5, rely=0.5, anchor="center")
                play_overlay.bind("<Button-1>", lambda e: self.open_video_in_browser(video['url']))
                thumbnail_label.bind("<Button-1>", lambda e: self.open_video_in_browser(video['url']))
                thumbnail_label.config(cursor="hand2")
                
                print("DEBUG: Thumbnail displayed with play button")
            except Exception as e:
                print(f"DEBUG: Thumbnail error: {e}")
                tk.Label(
                    player_frame,
                    text="▶ Click to Watch Video",
                    font=("Arial", 14, "bold"),
                    bg="black",
                    fg="white",
                    cursor="hand2"
                ).pack(expand=True)
                player_frame.bind("<Button-1>", lambda e: self.open_video_in_browser(video['url']))
        else:
            tk.Label(
                player_frame,
                text="▶ Click to Watch Video",
                font=("Arial", 14, "bold"),
                bg="black",
                fg="white",
                cursor="hand2"
            ).pack(expand=True)
            player_frame.bind("<Button-1>", lambda e: self.open_video_in_browser(video['url']))
            
            # Watch in browser button
            watch_btn = tk.Button(
                preview_content,
                text="▶ Watch in Browser",
                command=lambda: self.open_video_in_browser(video['url']),
                font=("Arial", 11, "bold"),
                bg="#FF0000",
                fg="white",
                cursor="hand2",
                padx=20,
                pady=8
            )
            watch_btn.pack(pady=10)
            
            # Video URL
            url_frame = tk.Frame(preview_content, bg="#f5f5f5", padx=10)
            url_frame.pack(anchor="w", fill=tk.X, pady=5)
            
            tk.Label(url_frame, text="🔗 URL:", font=("Arial", 10, "bold"), bg="#f5f5f5").pack(anchor="w")
            url_text = tk.Text(url_frame, height=2, wrap=tk.WORD, font=("Courier", 8))
            url_text.insert(1.0, video['url'])
            url_text.config(state=tk.DISABLED, bg="white")
            url_text.pack(fill=tk.X, pady=2)
            
            # Channel
            channel_label = tk.Label(
                preview_content,
                text=f"📺 Channel: {video.get('channel', 'Unknown')}",
                font=("Arial", 10),
                bg="#f5f5f5",
                fg="#333",
                padx=10
            )
            channel_label.pack(anchor="w", pady=2)
            
            # Duration
            duration = int(video.get('duration', 0)) if video.get('duration') else 0
            duration_str = f"{duration//60}:{duration%60:02d}" if duration > 0 else "N/A"
            duration_label = tk.Label(
                preview_content,
                text=f"⏱️ Duration: {duration_str}",
                font=("Arial", 10),
                bg="#f5f5f5",
                fg="#333",
                padx=10
            )
            duration_label.pack(anchor="w", pady=2)
            
            # Views
            views = int(video.get('views', 0)) if video.get('views') else 0
            views_str = f"{views:,}" if views > 0 else "N/A"
            views_label = tk.Label(
                preview_content,
                text=f"👁️ Views: {views_str}",
                font=("Arial", 10),
                bg="#f5f5f5",
                fg="#333",
                padx=10
            )
            views_label.pack(anchor="w", pady=2)
            
            # Large select button
            select_btn = tk.Button(
                preview_content,
                text="✓ SELECT THIS VIDEO",
                command=lambda: self.select_video_from_search(video['url'], results_window),
                font=("Arial", 14, "bold"),
                bg="#4CAF50",
                fg="white",
                cursor="hand2",
                padx=30,
                pady=15
            )
            select_btn.pack(pady=20)
    
    def select_video_from_search(self, url, window):
        """Select a video from search results."""
        # Stop VLC player if it's running
        # Find the preview_content widget in the window
        for widget in window.winfo_children():
            for child in widget.winfo_children():
                for subchild in child.winfo_children():
                    if hasattr(subchild, 'winfo_children'):
                        for content in subchild.winfo_children():
                            if hasattr(content, 'vlc_player'):
                                try:
                                    content.vlc_player.stop()
                                    content.vlc_player.release()
                                except:
                                    pass
                            if hasattr(content, 'vlc_instance'):
                                try:
                                    content.vlc_instance.release()
                                except:
                                    pass
        
        # Set URL in entry
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        self.url_entry.config(fg="black")
        
        # Close search window
        window.destroy()
        
        # Automatically fetch video info
        messagebox.showinfo("Video Selected", "Video selected! Fetching information...")
        self.fetch_video_info()
    
    def open_video_in_browser(self, url):
        """Open video in default web browser."""
        import webbrowser
        webbrowser.open(url)
    
    def preview_video_embedded(self, video):
        """Open embedded video preview in a new window using VLC."""
        preview_win = tk.Toplevel(self.root)
        preview_win.title(f"Preview: {video.get('title', 'Unknown Title')}")
        preview_win.geometry("900x600")
        preview_win.configure(bg="#000000")
        
        # Header with video title
        header = tk.Frame(preview_win, bg="#FF0000")
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=video.get('title', 'Unknown Title'),
            font=("Arial", 12, "bold"),
            bg="#FF0000",
            fg="white",
            wraplength=850,
            pady=10,
            padx=10
        ).pack()
        
        # Video player frame
        player_frame = tk.Frame(preview_win, bg="black")
        player_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Try to use VLC player
        try:
            import vlc
            
            # Create VLC instance
            instance = vlc.Instance()
            player = instance.media_player_new()
            
            # Get video URL via yt-dlp
            import yt_dlp
            ydl_opts = {'format': 'best', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video['url'], download=False)
                stream_url = info['url']
            
            # Create media
            media = instance.media_new(stream_url)
            player.set_media(media)
            
            # Embed VLC player in tkinter
            if tk.sys.platform.startswith('win'):
                player.set_hwnd(player_frame.winfo_id())
            else:
                player.set_xwindow(player_frame.winfo_id())
            
            # Play
            player.play()
            
            # Control buttons
            controls = tk.Frame(preview_win, bg="#222222")
            controls.pack(fill=tk.X)
            
            tk.Button(
                controls,
                text="⏸ Pause/Play",
                command=lambda: player.pause(),
                font=("Arial", 10),
                bg="#555555",
                fg="white",
                padx=10,
                pady=5
            ).pack(side=tk.LEFT, padx=5, pady=5)
            
            tk.Button(
                controls,
                text="⏹ Stop",
                command=lambda: player.stop(),
                font=("Arial", 10),
                bg="#555555",
                fg="white",
                padx=10,
                pady=5
            ).pack(side=tk.LEFT, padx=5, pady=5)
            
            tk.Button(
                controls,
                text="Close",
                command=lambda: [player.stop(), preview_win.destroy()],
                font=("Arial", 10),
                bg="#555555",
                fg="white",
                padx=10,
                pady=5
            ).pack(side=tk.RIGHT, padx=5, pady=5)
            
            # Cleanup on close
            preview_win.protocol("WM_DELETE_WINDOW", lambda: [player.stop(), preview_win.destroy()])
            
        except ImportError:
            # VLC not installed - show instructions
            msg_frame = tk.Frame(player_frame, bg="black")
            msg_frame.pack(expand=True)
            
            tk.Label(
                msg_frame,
                text="VLC Player Required for In-App Preview",
                font=("Arial", 16, "bold"),
                bg="black",
                fg="white"
            ).pack(pady=20)
            
            tk.Label(
                msg_frame,
                text="To watch videos inside the app, please install:\n\n"
                     "1. VLC Media Player from videolan.org\n"
                     "2. Python VLC package: pip install python-vlc\n\n"
                     "Or click below to watch in browser:",
                font=("Arial", 11),
                bg="black",
                fg="white",
                justify=tk.CENTER
            ).pack(pady=10)
            
            tk.Button(
                msg_frame,
                text="▶ Watch in Browser",
                command=lambda: [self.open_video_in_browser(video['url']), preview_win.destroy()],
                font=("Arial", 12, "bold"),
                bg="#FF0000",
                fg="white",
                padx=30,
                pady=10
            ).pack(pady=20)
            
            tk.Button(
                msg_frame,
                text="Close",
                command=preview_win.destroy,
                font=("Arial", 10),
                bg="#555555",
                fg="white",
                padx=15,
                pady=5
            ).pack(pady=5)
            
        except Exception as e:
            # Error occurred - show message
            msg_frame = tk.Frame(player_frame, bg="black")
            msg_frame.pack(expand=True)
            
            tk.Label(
                msg_frame,
                text=f"Unable to load video player\n\nError: {str(e)}",
                font=("Arial", 12),
                bg="black",
                fg="white",
                justify=tk.CENTER
            ).pack(pady=20)
            
            tk.Button(
                msg_frame,
                text="▶ Watch in Browser",
                command=lambda: [self.open_video_in_browser(video['url']), preview_win.destroy()],
                font=("Arial", 12, "bold"),
                bg="#FF0000",
                fg="white",
                padx=30,
                pady=10
            ).pack(pady=20)
    
    def restore_placeholder(self, event):
        """Restore placeholder if empty."""
        if not self.url_entry.get():
            self.url_entry.insert(0, "Paste video URL or search YouTube...")
            self.url_entry.config(fg="gray")
    
    def cookie_setup_wizard(self):
        """Step-by-step wizard to setup cookies for age-restricted videos."""
        # Check if cookies already exist
        cookies_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
        
        if os.path.exists(cookies_file):
            # Cookies already exist - offer to replace or cancel
            result = messagebox.askyesno(
                "Cookies Already Exist",
                "✅ You already have cookies.txt installed!\n\n"
                "Do you want to replace it with a new one?\n\n"
                "• Click YES to update cookies (if expired/not working)\n"
                "• Click NO to keep current cookies"
            )
            if not result:
                return
        
        # Step 1: Show instructions and offer to open extension page
        step1 = messagebox.askyesnocancel(
            "Step 1 of 3: Install Browser Extension",
            "To download age-restricted videos, you need to:\n\n"
            "1. Install the 'Get cookies.txt LOCALLY' browser extension\n"
            "2. Log into YouTube\n"
            "3. Export your cookies\n\n"
            "Would you like to open the extension installation page?\n\n"
            "• YES = Open Chrome extension\n"
            "• NO = Open Firefox extension\n"
            "• CANCEL = Exit setup"
        )
        
        if step1 is None:  # Cancel
            return
        elif step1:  # Yes - Chrome
            webbrowser.open("https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc")
        else:  # No - Firefox
            webbrowser.open("https://addons.mozilla.org/firefox/addon/cookies-txt/")
        
        # Step 2: Instructions to export
        step2 = messagebox.askokcancel(
            "Step 2 of 3: Export Cookies from YouTube",
            "After installing the extension:\n\n"
            "1. Go to YouTube.com in your browser\n"
            "2. Make sure you're LOGGED IN\n"
            "3. Click the extension icon (puzzle piece in toolbar)\n"
            "4. Click 'Export' or 'Get cookies.txt'\n"
            "5. Save the file (usually goes to Downloads folder)\n\n"
            "Click OK when you've exported the cookies.txt file.\n"
            "Click Cancel to exit setup."
        )
        
        if not step2:
            return
        
        # Step 3: Import the file
        messagebox.showinfo(
            "Step 3 of 3: Select Your cookies.txt File",
            "In the next window:\n\n"
            "1. Navigate to where you saved cookies.txt\n"
            "   (Usually in Downloads folder)\n"
            "2. Select the cookies.txt file\n"
            "3. Click Open\n\n"
            "The file will be automatically imported!"
        )
        
        # Open file dialog to select cookies.txt
        file_path = filedialog.askopenfilename(
            title="Select your cookies.txt file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir=os.path.expanduser("~/Downloads")
        )
        
        if not file_path:
            messagebox.showwarning(
                "Setup Cancelled",
                "No file selected. Setup cancelled.\n\n"
                "You can run this wizard again anytime!"
            )
            return
        
        try:
            # Copy the file to project folder
            project_folder = os.path.dirname(os.path.abspath(__file__))
            destination = os.path.join(project_folder, "cookies.txt")
            shutil.copy2(file_path, destination)
            
            # Refresh cookie status
            self.check_cookies()
            
            messagebox.showinfo(
                "🎉 Setup Complete!",
                "✅ cookies.txt has been successfully imported!\n\n"
                f"Saved to:\n{destination}\n\n"
                "You can now download age-restricted videos!\n\n"
                "Note: If cookies expire or stop working,\n"
                "just run this setup wizard again."
            )
        except Exception as e:
            messagebox.showerror(
                "Import Failed",
                f"Could not import cookies.txt:\n{e}\n\n"
                "Please try again or check the Help button."
            )
    
    def import_cookies_file(self):
        """Import cookies.txt file and save it to the project folder."""
        # Ask user to select the cookies.txt file
        file_path = filedialog.askopenfilename(
            title="Select your cookies.txt file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir=os.path.expanduser("~/Downloads")
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            # Destination path in the project folder
            project_folder = os.path.dirname(os.path.abspath(__file__))
            destination = os.path.join(project_folder, "cookies.txt")
            
            # Copy the file
            shutil.copy2(file_path, destination)
            
            # Refresh cookie status
            self.check_cookies()
            
            messagebox.showinfo(
                "Success!",
                f"✅ cookies.txt imported successfully!\n\n"
                f"Saved to:\n{destination}\n\n"
                "You can now download age-restricted videos!"
            )
        except Exception as e:
            messagebox.showerror(
                "Import Failed",
                f"Could not import cookies.txt:\n{e}\n\n"
                "Please make sure:\n"
                "1. The file is a valid cookies.txt file\n"
                "2. You have write permissions to this folder"
            )
    
    def open_browser_link(self, url):
        """Open a URL in the default web browser."""
        try:
            webbrowser.open(url)
            messagebox.showinfo(
                "Opening Browser",
                "Opening browser extension page...\n\n"
                "After installing and exporting:\n"
                "1. Log into YouTube\n"
                "2. Click the extension icon\n"
                "3. Export cookies (saves to Downloads folder)\n"
                "4. Come back here and click '📂 Import cookies.txt File'\n"
                "5. Select the cookies.txt from Downloads"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not open browser:\n{e}\n\nPlease copy this URL manually:\n{url}")
    
    def check_vlc_installed(self):
        """Check if VLC is installed on the system."""
        try:
            # Check if VLC is installed via registry (Windows)
            if sys.platform.startswith('win'):
                import winreg
                try:
                    # Check 64-bit registry
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\VideoLAN\VLC")
                    install_dir = winreg.QueryValueEx(key, "InstallDir")[0]
                    winreg.CloseKey(key)
                    return True, install_dir
                except:
                    try:
                        # Check 32-bit registry on 64-bit system
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\VideoLAN\VLC")
                        install_dir = winreg.QueryValueEx(key, "InstallDir")[0]
                        winreg.CloseKey(key)
                        return True, install_dir
                    except:
                        pass
            
            # Try importing python-vlc module
            import vlc
            return True, "VLC module found"
        except:
            return False, None
    
    def show_vlc_download_prompt(self):
        """Show prompt to download VLC if not installed."""
        result = messagebox.askyesno(
            "VLC Not Found",
            "VLC Media Player is not installed on your system.\n\n"
            "VLC is required for in-app video preview features.\n\n"
            "Would you like to download VLC now?\n\n"
            "(The download page will open in your browser)"
        )
        
        if result:
            webbrowser.open("https://www.videolan.org/vlc/download-windows.html")
            messagebox.showinfo(
                "VLC Download",
                "After installing VLC:\n\n"
                "1. Install VLC Media Player\n"
                "2. Install python-vlc: pip install python-vlc\n"
                "3. Restart this application\n\n"
                "Video preview features will then be available!"
            )
    
    def check_cookies(self):
        """Check if cookies.txt exists."""
        cookies_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
        if os.path.exists(cookies_file):
            self.status_label.config(
                text="✅ cookies.txt found - Age-restricted videos supported",
                fg="green"
            )
            # Update wizard button to show cookies are installed
            self.cookie_wizard_btn.config(
                text="✅ Cookies Installed - Click to Update",
                bg="#2196F3"
            )
        else:
            self.status_label.config(
                text="⚠️ No cookies.txt - Age-restricted videos will fail",
                fg="orange"
            )
            # Update wizard button to show setup needed
            self.cookie_wizard_btn.config(
                text="🍪 Setup Cookies for Age-Restricted Videos",
                bg="#4CAF50"
            )
    
    def run_export_cookies(self):
        """Run the export cookies script and show instructions."""
        import subprocess
        import sys
        
        try:
            # Run export_cookies.py in a new window
            script_path = os.path.join(os.path.dirname(__file__), 'export_cookies.py')
            
            if os.path.exists(script_path):
                # Open in a new terminal window
                if sys.platform == 'win32':
                    subprocess.Popen(['start', 'cmd', '/k', 'python', script_path], shell=True)
                    messagebox.showinfo(
                        "Cookie Export Tool",
                        "Opening cookie export instructions in a new window!\n\n"
                        "Follow the instructions to export your YouTube cookies.\n"
                        "This is required for age-restricted videos."
                    )
                else:
                    subprocess.Popen(['python', script_path])
            else:
                # Script not found, show instructions
                self.show_cookie_help()
        except Exception as e:
            messagebox.showerror("Error", f"Could not run export script:\n{e}\n\nShowing help instead...")
            self.show_cookie_help()
    
    def show_cookie_help(self):
        """Show cookie export help dialog."""
        help_text = """How to Download Age-Restricted Videos:

1. Install Browser Extension:
   • Chrome/Edge: "Get cookies.txt LOCALLY"
   • Firefox: "cookies.txt" addon

2. Export Your Cookies:
   • Log into YouTube in your browser
   • Visit any YouTube page
   • Click the extension icon
   • Click "Export" or "Get cookies.txt"

3. Save the File:
   • Save as "cookies.txt"
   • Place in the same folder as this program:
     """ + os.path.dirname(os.path.abspath(__file__)) + """

4. Restart the Program
   • The status bar will show ✅ when ready

Alternative: Run this command for detailed help:
   python export_cookies.py

Chrome Extension Link:
https://chrome.google.com/webstore/detail/
get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
"""
        
        # Create a custom dialog with the help text
        help_window = tk.Toplevel(self.root)
        help_window.title("Cookie Export Help")
        help_window.geometry("600x500")
        help_window.resizable(False, False)
        
        # Title
        title = tk.Label(
            help_window,
            text="🍪 How to Export Cookies",
            font=("Arial", 14, "bold"),
            bg="#FFA500",
            fg="white",
            pady=10
        )
        title.pack(fill=tk.X)
        
        # Text widget with scrollbar
        text_frame = tk.Frame(help_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(
            text_frame,
            font=("Courier New", 9),
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert(1.0, help_text)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(
            help_window,
            text="Close",
            command=help_window.destroy,
            font=("Arial", 10),
            padx=20,
            pady=5
        )
        close_btn.pack(pady=10)
    
    def show_proxy_help(self):
        """Show proxy help and resources."""
        help_window = tk.Toplevel(self.root)
        help_window.title("🌍 Proxy Setup Guide - How to Access Geo-Blocked Content")
        help_window.geometry("700x600")
        help_window.configure(bg=self.bg_color)
        
        # Text widget with scrollbar
        text_frame = tk.Frame(help_window, bg=self.bg_color)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(
            text_frame,
            font=("Courier New", 9),
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            bg="#f5f5f5"
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║     🌍 HOW TO ACCESS GEO-BLOCKED CONTENT (e.g., Mediaset)    ║
╚══════════════════════════════════════════════════════════════╝

📌 OPTION 1: USE A VPN (RECOMMENDED - EASIEST & MOST RELIABLE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Best Solution: Install a VPN and connect to Italy

FREE VPN Options:
• ProtonVPN (Free tier, no logs, good speeds)
  → https://protonvpn.com
  
• Windscribe (10GB free per month)
  → https://windscribe.com

PAID VPN Options (More reliable):
• NordVPN (Fast, many Italian servers)
• ExpressVPN (Premium speed and reliability)
• Surfshark (Affordable, unlimited devices)

How to use with VPN:
1. Install and connect VPN to Italian server
2. Run this downloader normally
3. No proxy needed - VPN routes all traffic!


📌 OPTION 2: USE A PROXY SERVER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Note: Free proxies are often slow, unreliable, or don't work.

WHERE TO FIND ITALIAN PROXIES:

1. Free Proxy Lists (Update frequently):
   • https://www.proxy-list.download/HTTPS
     → Filter by Country: Italy (IT)
   
   • https://free-proxy-list.net/
     → Look for Italian IPs
   
   • https://www.sslproxies.org/
     → Search for Italy proxies

2. Paid Proxy Services (More reliable):
   • Bright Data: https://brightdata.com
   • Smartproxy: https://smartproxy.com
   • Proxy-Seller: https://proxy-seller.com


HOW TO USE PROXY IN THIS APP:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Format: protocol://IP:PORT

Examples:
• HTTP Proxy:   http://185.123.45.67:8080
• HTTPS Proxy:  https://192.168.1.1:3128
• SOCKS5 Proxy: socks5://127.0.0.1:1080

With Authentication:
• http://username:password@proxy.com:8080


TESTING A PROXY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Before using, test if proxy works:
1. Copy proxy URL
2. Paste it in the Proxy Settings field
3. Try fetching video info
4. If it fails, try another proxy


📌 OPTION 3: BROWSER EXTENSION + COOKIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Install free VPN browser extension (Chrome/Firefox)
   • Hola VPN, Urban VPN, Touch VPN
2. Set location to Italy
3. Login to Mediaset/YouTube in browser
4. Export cookies using Cookie Setup Wizard
5. Use cookies in this downloader


⚠️ IMPORTANT NOTES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Free proxies change frequently - update regularly
• Proxies may be slow - be patient
• For best results: Use paid VPN or proxy service
• Some content may still be blocked even with proxy
• Always respect copyright and terms of service


🎯 QUICK START FOR MEDIASET:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Install ProtonVPN (free)
2. Connect to Italian server
3. Paste Mediaset URL in this app
4. Download! (No proxy field needed)

        """
        
        text_widget.insert(1.0, help_text)
        text_widget.config(state=tk.DISABLED)
        
        # Buttons frame
        btn_frame = tk.Frame(help_window, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        # Open proxy list button
        def open_proxy_site(url):
            try:
                webbrowser.open(url)
            except:
                messagebox.showinfo("URL", f"Please open manually:\n{url}")
        
        tk.Button(
            btn_frame,
            text="🔗 Free Proxy List",
            command=lambda: open_proxy_site("https://proxy5.net/free-proxy"),
            font=("Arial", 9, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="🔗 ProtonVPN (Free)",
            command=lambda: open_proxy_site("https://protonvpn.com"),
            font=("Arial", 9, "bold"),
            bg="#6D4AFF",
            fg="white",
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Close",
            command=help_window.destroy,
            font=("Arial", 9),
            padx=15,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
    
    def load_proxy_from_file(self):
        """Load working proxies from proxy_list.txt and let user choose."""
        proxy_file = os.path.join(os.path.dirname(__file__), 'proxy_list.txt')
        
        if not os.path.exists(proxy_file):
            messagebox.showerror(
                "File Not Found",
                "proxy_list.txt not found!\n\nThe file should be in the same folder as this program."
            )
            return
        
        try:
            # Read proxies from file
            with open(proxy_file, 'r') as f:
                lines = f.readlines()
            
            # Extract valid proxy URLs (skip comments and empty lines)
            proxies = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and ('http://' in line or 'socks5://' in line):
                    proxies.append(line)
            
            if not proxies:
                messagebox.showwarning(
                    "No Proxies Found",
                    "No valid proxies found in proxy_list.txt\n\n"
                    "Add proxies in format:\nhttp://IP:PORT\nor\nsocks5://IP:PORT"
                )
                return
            
            # Create selection window
            proxy_window = tk.Toplevel(self.root)
            proxy_window.title("📋 Select a Proxy")
            proxy_window.geometry("600x400")
            proxy_window.configure(bg=self.bg_color)
            
            tk.Label(
                proxy_window,
                text="✅ Verified Working Proxies",
                font=("Arial", 14, "bold"),
                bg=self.bg_color,
                fg="#4CAF50"
            ).pack(pady=10)
            
            tk.Label(
                proxy_window,
                text="Click on a proxy to use it",
                font=("Arial", 9),
                bg=self.bg_color
            ).pack()
            
            # Listbox with scrollbar
            list_frame = tk.Frame(proxy_window, bg=self.bg_color)
            list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = tk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            proxy_listbox = tk.Listbox(
                list_frame,
                font=("Courier New", 10),
                yscrollcommand=scrollbar.set,
                height=15
            )
            proxy_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=proxy_listbox.yview)
            
            # Add proxies to listbox
            for proxy in proxies:
                proxy_listbox.insert(tk.END, proxy)
            
            def use_selected_proxy():
                selection = proxy_listbox.curselection()
                if selection:
                    selected_proxy = proxy_listbox.get(selection[0])
                    self.proxy_entry.delete(0, tk.END)
                    self.proxy_entry.insert(0, selected_proxy)
                    self.proxy_entry.config(fg="black")
                    proxy_window.destroy()
                    messagebox.showinfo(
                        "Proxy Loaded",
                        f"✅ Using proxy:\n{selected_proxy}\n\n"
                        "Now paste your video URL and click 'Fetch Video Info'"
                    )
                else:
                    messagebox.showwarning("No Selection", "Please select a proxy from the list")
            
            # Buttons
            btn_frame = tk.Frame(proxy_window, bg=self.bg_color)
            btn_frame.pack(pady=10)
            
            tk.Button(
                btn_frame,
                text="✅ Use Selected Proxy",
                command=use_selected_proxy,
                font=("Arial", 10, "bold"),
                bg="#4CAF50",
                fg="white",
                padx=20,
                pady=5,
                cursor="hand2"
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                btn_frame,
                text="Cancel",
                command=proxy_window.destroy,
                font=("Arial", 10),
                padx=20,
                pady=5
            ).pack(side=tk.LEFT, padx=5)
            
            # Double-click to select
            proxy_listbox.bind('<Double-Button-1>', lambda e: use_selected_proxy())
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load proxies:\n{e}")
    
    def browse_folder(self):
        """Browse for default download folder."""
        folder = filedialog.askdirectory(
            initialdir=self.download_path,
            title="Select Default Download Folder"
        )
        if folder:
            self.download_path = folder
            self.path_label.config(text=folder)
            messagebox.showinfo("Default Folder Updated", f"Downloads will be saved to:\n{folder}\n\nYou can still choose a different folder when downloading.")
    
    def update_info_text(self, text):
        """Update the info text widget."""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)
        self.info_text.config(state=tk.DISABLED)
    
    def reset_for_new_download(self):
        """Reset the interface for a new download."""
        # Clear URL field
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, "Paste video URL or search YouTube...")
        self.url_entry.config(fg="gray")
        
        # Clear video info
        self.update_info_text("Ready to fetch a new video...")
        
        # Reset button to fetch mode
        self.button_mode = "fetch"
        self.action_btn.config(
            state=tk.NORMAL,
            bg="#4CAF50",
            fg="white",
            text="📥 FETCH VIDEO INFO",
            cursor="hand2",
            relief=tk.RAISED,
            bd=4
        )
        
        # Update progress label and reset progress bar
        self.progress_label.config(text="Ready to download another video", fg="green")
        self.progress_bar.stop()
        self.progress_bar.config(mode='indeterminate', value=0)
    
    def smart_button_action(self):
        """Smart button that switches between fetch and download."""
        if self.button_mode == "fetch":
            self.fetch_video_info()
        else:
            self.start_download()
    
    def fetch_video_info(self):
        """Fetch video information."""
        url = self.url_entry.get()
        
        if not url or url == "https://www.youtube.com/watch?v=...":
            messagebox.showwarning("Invalid URL", "Please enter a valid YouTube URL")
            return
        
        # Start progress
        self.progress_label.config(text="Fetching video information...", fg="blue")
        self.progress_bar.start(10)
        self.action_btn.config(state=tk.DISABLED)
        
        # Run in thread to avoid freezing GUI
        thread = threading.Thread(target=self._fetch_info_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _fetch_info_thread(self, url):
        """Thread function to fetch video info."""
        try:
            # Initialize downloader with current path
            self.downloader = YouTubeDownloader(output_path=self.download_path)
            
            # Get proxy if provided
            proxy = self.get_proxy()
            
            # Try without cookies first (works for most videos)
            info = self.downloader.get_video_info(url, use_cookies=False, proxy=proxy)
            
            # If it fails and we have cookies.txt, try with cookies
            if not info['success']:
                cookies_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
                if os.path.exists(cookies_file):
                    info = self.downloader.get_video_info(url, use_cookies=True, proxy=proxy)
            
            if info['success']:
                # Format info text safely
                title = info.get('title', 'Unknown')
                uploader = info.get('uploader', 'Unknown')
                duration = info.get('duration', 0)
                duration_sec = duration if duration else 0
                duration_text = f"{duration_sec} seconds ({duration_sec//60} min {duration_sec%60} sec)" if duration_sec > 0 else "N/A"
                views = info.get('views', None)
                views_text = f"{views:,}" if views is not None else "N/A"
                age_restricted = info.get('age_restricted', False)
                description = info.get('description', 'N/A')
                description_preview = description[:200] if description and description != 'N/A' else 'N/A'
                
                info_text = f"""
Title: {title}
Uploader: {uploader}
Duration: {duration_text}
Views: {views_text}
Age Restricted: {'Yes ⚠️' if age_restricted else 'No ✓'}

Description:
{description_preview}...
                """.strip()
                
                # Update GUI in main thread
                self.root.after(0, lambda: self.update_info_text(info_text))
                self.root.after(0, lambda: self.progress_label.config(text="✅ Video ready! Click the RED button to download!", fg="green"))
                self.root.after(0, lambda: self.progress_bar.stop())
                # Change button to download mode
                def switch_to_download():
                    self.button_mode = "download"
                    self.action_btn.config(
                        state=tk.NORMAL, 
                        bg="#FF0000", 
                        fg="white",
                        text="⬇️ DOWNLOAD VIDEO NOW",
                        cursor="hand2",
                        relief=tk.RAISED,
                        bd=5
                    )
                self.root.after(0, switch_to_download)
            else:
                error_msg = f"Error: {info['error']}"
                self.root.after(0, lambda: self.update_info_text(error_msg))
                self.root.after(0, lambda: self.progress_label.config(text="❌ Failed to fetch info", fg="red"))
                self.root.after(0, lambda: self.progress_bar.stop())
                
                # Re-enable button in fetch mode
                def reset_button():
                    self.action_btn.config(state=tk.NORMAL)
                self.root.after(0, reset_button)
                
                # Check if it's a cookie-related error
                if "age" in info['error'].lower() or "restricted" in info['error'].lower():
                    error_with_help = (
                        f"{info['error']}\n\n"
                        "This video is age-restricted. To download it:\n"
                        "1. Run 'python export_cookies.py' for instructions\n"
                        "2. Export cookies.txt from your browser\n"
                        "3. Place it in the same folder as this program\n"
                        "4. Try again"
                    )
                    self.root.after(0, lambda: messagebox.showerror("Age-Restricted Video", error_with_help))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", info['error']))
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.update_info_text(error_msg))
            self.root.after(0, lambda: self.progress_label.config(text="❌ Failed to fetch info", fg="red"))
            self.root.after(0, lambda: self.progress_bar.stop())
            # Re-enable button
            self.root.after(0, lambda: self.action_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
    
    def start_download(self):
        """Start the download process."""
        url = self.url_entry.get()
        
        if not url or url == "https://www.youtube.com/watch?v=...":
            messagebox.showwarning("Invalid URL", "Please enter a valid YouTube URL")
            return
        
        # Ask user to select download folder
        result = messagebox.askyesno(
            "Select Download Location",
            f"Current default folder:\n{self.download_path}\n\n"
            "Do you want to choose a different folder for this download?\n\n"
            "• Click YES to browse for a different folder\n"
            "• Click NO to use the default folder shown above"
        )
        
        if result:  # User wants to choose a different folder
            folder = filedialog.askdirectory(
                initialdir=self.download_path,
                title="Select Download Folder for This Video"
            )
            
            # If user cancels, don't download
            if not folder:
                messagebox.showinfo("Cancelled", "Download cancelled - no folder selected")
                return
            
            download_path = folder
        else:  # Use default folder
            download_path = self.download_path
        
        # Start progress
        self.progress_label.config(text=f"Downloading to: {download_path}", fg="blue")
        self.progress_bar.start(10)
        self.action_btn.config(state=tk.DISABLED, text="⏳ Downloading...")
        
        # Run in thread with the selected path
        thread = threading.Thread(target=self._download_thread, args=(url, download_path))
        thread.daemon = True
        thread.start()
    
    def _download_thread(self, url, download_path=None):
        """Thread function to download video."""
        try:
            # Initialize downloader if not already done
            if not self.downloader:
                self.downloader = YouTubeDownloader(output_path=download_path or self.download_path)
            
            # Update output path
            self.downloader.output_path = download_path or self.download_path
            
            # Always use best quality
            quality = "best"
            download_type = self.download_type.get()
            
            # Check if cookies.txt exists
            cookies_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
            use_cookies = os.path.exists(cookies_file)
            
            # Get proxy if provided
            proxy = self.get_proxy()
            
            # Define progress hook
            def progress_hook(d):
                if d['status'] == 'downloading':
                    # Get download percentage
                    if 'total_bytes' in d:
                        downloaded = d.get('downloaded_bytes', 0)
                        total = d['total_bytes']
                        percent = (downloaded / total) * 100
                        speed = d.get('speed', 0)
                        eta = d.get('eta', 0)
                        
                        # Format speed
                        if speed:
                            speed_mb = speed / (1024 * 1024)
                            speed_str = f"{speed_mb:.2f} MB/s"
                        else:
                            speed_str = "N/A"
                        
                        # Update GUI
                        status_text = f"⏬ Downloading: {percent:.1f}% | Speed: {speed_str} | ETA: {eta}s"
                        self.root.after(0, lambda: self.progress_label.config(text=status_text, fg="blue"))
                        self.root.after(0, lambda: self.progress_bar.stop())
                        self.root.after(0, lambda: self.progress_bar.config(mode='determinate', value=percent))
                    elif 'total_bytes_estimate' in d:
                        downloaded = d.get('downloaded_bytes', 0)
                        total = d['total_bytes_estimate']
                        percent = (downloaded / total) * 100
                        status_text = f"⏬ Downloading: {percent:.1f}% (estimated)"
                        self.root.after(0, lambda: self.progress_label.config(text=status_text, fg="blue"))
                        self.root.after(0, lambda: self.progress_bar.stop())
                        self.root.after(0, lambda: self.progress_bar.config(mode='determinate', value=percent))
                    else:
                        # No total bytes available, show indeterminate progress
                        downloaded = d.get('downloaded_bytes', 0)
                        downloaded_mb = downloaded / (1024 * 1024)
                        status_text = f"⏬ Downloading: {downloaded_mb:.1f} MB..."
                        self.root.after(0, lambda: self.progress_label.config(text=status_text, fg="blue"))
                elif d['status'] == 'finished':
                    self.root.after(0, lambda: self.progress_label.config(text="🔄 Processing (merging video/audio)...", fg="blue"))
                    self.root.after(0, lambda: self.progress_bar.config(mode='indeterminate'))
                    self.root.after(0, lambda: self.progress_bar.start(10))
            
            if download_type == "video":
                result = self.downloader.download_video(url, quality=quality, use_cookies=use_cookies, proxy=proxy, progress_hook=progress_hook)
            else:
                result = self.downloader.download_audio_only(url, use_cookies=use_cookies, proxy=proxy, progress_hook=progress_hook)
            
            if result['success']:
                success_msg = f"✅ Download complete!\n\n"
                if download_type == "video":
                    success_msg += f"File: {result.get('file_path', 'downloads folder')}"
                else:
                    success_msg += f"Audio saved to: {download_path or self.download_path}"
                
                self.root.after(0, lambda: self.progress_label.config(text="✅ Download complete!", fg="green"))
                self.root.after(0, lambda: messagebox.showinfo("Success", success_msg))
                
                # Reset for next download
                self.root.after(0, self.reset_for_new_download)
            else:
                error_msg = result['error']
                self.root.after(0, lambda: self.progress_label.config(text="❌ Download failed", fg="red"))
                self.root.after(0, lambda: self.progress_bar.stop())
                self.root.after(0, lambda: self.progress_bar.config(mode='indeterminate', value=0))
                
                # Check if it's a cookie-related error
                if ("age" in error_msg.lower() or "restricted" in error_msg.lower() or 
                    "cookie" in error_msg.lower() or "sign in" in error_msg.lower()):
                    error_with_help = (
                        f"{error_msg}\n\n"
                        "This video requires authentication. To fix:\n\n"
                        "1. Run: python export_cookies.py\n"
                        "2. Follow instructions to export cookies.txt\n"
                        "3. Place cookies.txt in this folder\n"
                        "4. Restart and try again\n\n"
                        "The cookies.txt file will contain your YouTube login session."
                    )
                    self.root.after(0, lambda: messagebox.showerror("Authentication Required", error_with_help))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Download Failed", error_msg))
        
        except Exception as e:
            error_msg = f"Error during download:\n{str(e)}"
            self.root.after(0, lambda: self.progress_label.config(text="❌ Download failed", fg="red"))
            self.root.after(0, lambda: self.progress_bar.stop())
            self.root.after(0, lambda: self.progress_bar.config(mode='indeterminate', value=0))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            self.root.after(0, lambda: self.progress_bar.stop())


def main():
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
