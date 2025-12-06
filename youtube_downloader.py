import yt_dlp
import os
from pathlib import Path


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
    
    def download_video(self, url, quality='best', format_type='mp4', use_cookies=True):
        """
        Download a YouTube video, including age-restricted content.
        
        Args:
            url (str): YouTube video URL
            quality (str): Video quality ('best', 'worst', or specific height like '720')
            format_type (str): Output format ('mp4', 'mkv', 'webm', etc.)
            use_cookies (bool): Whether to attempt using cookies
        
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
    
    def download_audio_only(self, url, format_type='mp3', use_cookies=True):
        """
        Download only the audio from a YouTube video.
        
        Args:
            url (str): YouTube video URL
            format_type (str): Audio format ('mp3', 'wav', 'm4a', etc.)
            use_cookies (bool): Whether to attempt using cookies
        
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
    
    def get_video_info(self, url, use_cookies=True):
        """
        Get information about a video without downloading it.
        
        Args:
            url (str): YouTube video URL
            use_cookies (bool): Whether to attempt using cookies
        
        Returns:
            dict: Video information
        """
        try:
            ydl_opts = {
                'nocheckcertificate': True,
                'age_limit': None,
            }
            
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


def main():
    """
    Example usage of the YouTubeDownloader class.
    """
    print("=== YouTube Video Downloader ===")
    print("This tool can download age-restricted videos.\n")
    
    # Create downloader instance
    downloader = YouTubeDownloader(output_path='downloads')
    
    # Get video URL from user
    url = input("Enter YouTube video URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return
    
    # Get video info first
    print("\nFetching video information...")
    info = downloader.get_video_info(url)
    
    if info['success']:
        print(f"\nTitle: {info['title']}")
        print(f"Uploader: {info['uploader']}")
        print(f"Duration: {info['duration']} seconds")
        print(f"Views: {info['views']}")
        print(f"Age Restricted: {'Yes' if info['age_restricted'] else 'No'}")
        
        # Ask user for download type
        print("\nDownload options:")
        print("1. Video (best quality)")
        print("2. Audio only (MP3)")
        print("3. Video (720p)")
        print("4. Cancel")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\nDownloading video...")
            result = downloader.download_video(url)
            if result['success']:
                print(f"\n✓ Download complete!")
                print(f"File saved to: {result['file_path']}")
            else:
                print(f"\n✗ Download failed: {result['error']}")
        
        elif choice == '2':
            print("\nDownloading audio...")
            result = downloader.download_audio_only(url)
            if result['success']:
                print(f"\n✓ Download complete!")
                print(f"Audio saved to downloads folder")
            else:
                print(f"\n✗ Download failed: {result['error']}")
        
        elif choice == '3':
            print("\nDownloading video (720p)...")
            result = downloader.download_video(url, quality='720')
            if result['success']:
                print(f"\n✓ Download complete!")
                print(f"File saved to: {result['file_path']}")
            else:
                print(f"\n✗ Download failed: {result['error']}")
        
        else:
            print("Download cancelled.")
    
    else:
        print(f"\n✗ Failed to get video info: {info['error']}")


if __name__ == '__main__':
    main()
