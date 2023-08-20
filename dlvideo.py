import requests
import os

CLIENT_ID = 'be9b625a673e79c'
HEADERS = {
    'Authorization': f'Client-ID {CLIENT_ID}'
}

IMGUR_API_URL = 'https://api.imgur.com/3/gallery/top/viral/0?showViral=true&mature=true&album_previews=true'
DOWNLOAD_FOLDER = 'videozap'  # Changement du chemin

def download_file(url, filename):
    print(f"Downloading from {url} to {filename}")
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(filename, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)

def get_video_from_album(album_id):
    url = f"https://api.imgur.com/3/album/{album_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    
    if not data['success']:
        print(f'Failed to retrieve data for album {album_id}.')
        return None
    
    album_data = data['data']
    videos = [image for image in album_data['images'] if 'type' in image and image['type'].startswith('video/')]
    
    if videos:
        return videos[0]  # Retourne la première vidéo trouvée dans l'album
    return None

def get_top_50_imgur_videos():
    response = requests.get(IMGUR_API_URL, headers=HEADERS)
    data = response.json()

    if not data['success']:
        print('Failed to retrieve data from Imgur.')
        return []

    videos = []

    for item in data['data']:
        # Si c'est une vidéo directe
        if 'type' in item and item['type'].startswith('video/'):
            videos.append(item)
        # Si c'est un album qui contient une vidéo
        elif item.get('is_album') and 'images' in item:
            for image in item['images']:
                if image['type'].startswith('video/'):
                    videos.append(image)
    
    print(f"Found {len(videos)} videos.")
    return videos

def main():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    videos = get_top_50_imgur_videos()

    for video in videos:
        filename = os.path.join(DOWNLOAD_FOLDER, video['id'] + '.mp4')  # Assuming all videos are mp4 format
        download_file(video['link'], filename)

if __name__ == "__main__":
    main()
