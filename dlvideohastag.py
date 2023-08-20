import os
import requests

CLIENT_ID = 'be9b625a673e79c'
HEADERS = {
    'Authorization': f'Client-ID {CLIENT_ID}'
}

# Liste des tags pour lesquels nous voulons télécharger les vidéos
TAGS = ['memes', 'funny', 'animals', 'football','drole']  # ajoutez ou supprimez des tags selon vos besoins

SAVE_PATH = os.path.join(os.getcwd(), 'videozap')


def get_top_videos_from_tag(tag):
    url = f'https://api.imgur.com/3/gallery/t/{tag}/time/week'
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    if not data['success']:
        print(f'Failed to retrieve data for tag: {tag}.')
        return []

    videos = []

    for item in data['data']['items']:
        if 'type' in item and item['type'].startswith('video/'):
            videos.append(item)
        elif item.get('is_album') and 'images' in item:
            for image in item['images']:
                if image['type'].startswith('video/'):
                    videos.append(image)
                    
    return videos


def download_videos(videos):
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    for video in videos:
        video_url = video['link']
        response = requests.get(video_url, stream=True)

        # Save the video to the file
        with open(os.path.join(SAVE_PATH, video_url.split('/')[-1]), 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)


def main():
    all_videos = []

    for tag in TAGS:
        print(f"Fetching videos from tag: {tag}...")
        videos = get_top_videos_from_tag(tag)
        all_videos.extend(videos)

    print(f"Found a total of {len(all_videos)} videos across all tags.")
    download_videos(all_videos)
    print(f"Videos saved to {SAVE_PATH}.")


if __name__ == "__main__":
    main()