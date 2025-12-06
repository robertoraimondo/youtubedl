"""
YouTube Video Downloader - GUI Version
A user-friendly graphical interface for downloading YouTube videos.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
from youtube_downloader import YouTubeDownloader
import sys
import webbrowser
import shutil


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
        proxy = self.proxy_entry.get()
        if proxy and "proxy.example.com" not in proxy and "127.0.0.1:1080" not in proxy:
            return proxy
        return None
    
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
            
            result = self.downloader.search_videos(query, max_results=10)
            
            if result['success'] and result['videos']:
                self.root.after(0, lambda: self.show_search_results(result['videos']))
                self.root.after(0, lambda: self.progress_bar.stop())
                self.root.after(0, lambda: self.progress_label.config(text="Search complete - Select a video", fg="green"))
            else:
                error_msg = result.get('error', 'No videos found')
                self.root.after(0, lambda: self.progress_bar.stop())
                self.root.after(0, lambda: self.progress_label.config(text="Search failed", fg="red"))
                self.root.after(0, lambda: messagebox.showerror("Search Failed", f"Could not find videos: {error_msg}"))
        
        except Exception as e:
            self.root.after(0, lambda: self.progress_bar.stop())
            self.root.after(0, lambda: self.progress_label.config(text="Search failed", fg="red"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Search error: {str(e)}"))
    
    def show_search_results(self, videos):
        """Show search results in a popup window."""
        results_window = tk.Toplevel(self.root)
        results_window.title("Search Results")
        results_window.geometry("800x500")
        
        # Title
        title = tk.Label(
            results_window,
            text="🔍 Search Results - Click on a video to select",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            pady=10
        )
        title.pack(fill=tk.X)
        
        # Scrollable frame
        canvas = tk.Canvas(results_window)
        scrollbar = tk.Scrollbar(results_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add video entries
        for i, video in enumerate(videos):
            video_frame = tk.Frame(scrollable_frame, relief=tk.RAISED, bd=2, padx=10, pady=10)
            video_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Video info
            title_label = tk.Label(
                video_frame,
                text=f"🎬 {video['title']}",
                font=("Arial", 11, "bold"),
                wraplength=700,
                justify=tk.LEFT
            )
            title_label.pack(anchor="w")
            
            # Format duration and views safely
            duration = int(video.get('duration', 0)) if video.get('duration') else 0
            views = int(video.get('views', 0)) if video.get('views') else 0
            duration_str = f"{duration//60}:{duration%60:02d}" if duration > 0 else "N/A"
            views_str = f"{views:,}" if views > 0 else "N/A"
            
            info_label = tk.Label(
                video_frame,
                text=f"📺 {video['channel']} | 👁️ {views_str} views | ⏱️ {duration_str}",
                font=("Arial", 9),
                fg="gray"
            )
            info_label.pack(anchor="w")
            
            # Select button
            select_btn = tk.Button(
                video_frame,
                text="✓ Select This Video",
                command=lambda url=video['url'], win=results_window: self.select_video_from_search(url, win),
                font=("Arial", 9, "bold"),
                bg="#4CAF50",
                fg="white",
                cursor="hand2",
                padx=15,
                pady=5
            )
            select_btn.pack(anchor="e", pady=(5, 0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def select_video_from_search(self, url, window):
        """Select a video from search results."""
        # Set URL in entry
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        self.url_entry.config(fg="black")
        
        # Close search window
        window.destroy()
        
        # Automatically fetch video info
        messagebox.showinfo("Video Selected", "Video selected! Fetching information...")
        self.fetch_video_info()
    
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
            command=lambda: open_proxy_site("https://www.proxy-list.download/HTTPS"),
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
        
        # Update progress label
        self.progress_label.config(text="Ready to download another video", fg="green")
    
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
                # Format info text
                info_text = f"""
Title: {info['title']}
Uploader: {info['uploader']}
Duration: {info['duration']} seconds ({info['duration']//60} min {info['duration']%60} sec)
Views: {info.get('views', 'N/A'):,}
Age Restricted: {'Yes ⚠️' if info.get('age_restricted', False) else 'No ✓'}

Description:
{info.get('description', 'N/A')[:200]}...
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
            
            if download_type == "video":
                result = self.downloader.download_video(url, quality=quality, use_cookies=use_cookies, proxy=proxy)
            else:
                result = self.downloader.download_audio_only(url, use_cookies=use_cookies, proxy=proxy)
            
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
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            self.root.after(0, lambda: self.progress_bar.stop())


def main():
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
