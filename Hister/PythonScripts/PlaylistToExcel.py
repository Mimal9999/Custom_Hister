import yt_dlp
import pandas as pd

def get_playlist_info(playlist_url, name):
    ydl_opts = {
        'quiet': False,
        'extract_flat': False,
        'cookiesfrombrowser': ('firefox',),
    }

    songs = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)

        for idx, entry in enumerate(info_dict['entries']):
            
            song_data = {
                'ID': idx,
                'Author': entry.get('uploader', 'No Data'),
                'Artist': entry.get('artist', 'No Data'),
                'Channel': entry.get('channel', 'No Data'),
                'Title': entry.get('title', 'No Data'),
                'Track Title': entry.get('track', 'No Data'),
                'URL': entry.get('webpage_url', 'No Data'),
                'Year': entry.get('upload_date', 'No Data')[:4] if entry.get('upload_date') else 'No Data',
                'Views': entry.get('view_count', 'No Data'),
                'Name': name,
            }
            songs.append(song_data)

    return songs

def save_to_excel(data, filename='playlist_data.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    playlist_url = input("YouTube playlist URL: ")
    name = input("Name of the playlist owner: ")

    songs_data = get_playlist_info(playlist_url, name)

    save_to_excel(songs_data)

    print("Data saved to: 'playlist_data.xlsx'.")
