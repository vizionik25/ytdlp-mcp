import yt_dlp
import os
import re

# this is where you will write the logic code for the different fastapi app endpoints for the yt-dlp functions

def search_youtube(search_term: str, max_results: int = 10):
    """
    Search YouTube for a search term and return the top URLs.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    
    search_query = f"ytsearch{max_results}:{search_term}"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(search_query, download=False)
        
        if 'entries' not in result:
            return []
            
        urls = []
        for entry in result['entries']:
            if entry.get('url'):
                urls.append(entry['url'])
            elif entry.get('id'):
                urls.append(f"https://www.youtube.com/watch?v={entry['id']}")
                
        return urls[:max_results]

def format_filename(title: str):
    """
    Format title: first 5 words, no spaces (e.g., thisWouldBeAcceptableName.mp4 or this-would-be-acceptable-name.mp4)
    I'll use camelCase as suggested in example.
    """
    # Remove non-alphanumeric except spaces
    clean_title = re.sub(r'[^\w\s]', '', title)
    words = clean_title.split()
    first_5_words = words[:5]
    
    if not first_5_words:
        return "video"
        
    # camelCase formatting
    formatted = first_5_words[0].lower() + "".join(word.capitalize() for word in first_5_words[1:])
    return formatted

def download_video(url: str, output_dir: str = "downloads"):
    """
    Download video in highest quality mp4 format.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    def get_filename(info):
        title = info.get('title', 'video')
        formatted = format_filename(title)
        return f"{formatted}.mp4"

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_dir}/%(title).50s.%(ext)s', # Placeholder template
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }
    
    # We need to get info first to name it correctly or use a hook
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filename = get_filename(info)
        
        # Update template with our formatted filename
        ydl_opts['outtmpl'] = os.path.join(output_dir, filename)
        
    # Now download with the correct filename
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        return os.path.join(output_dir, filename)
