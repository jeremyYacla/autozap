import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, ColorClip

def is_valid_video(video_path):
    """Verify if the video can be loaded and played without issues."""
    try:
        with VideoFileClip(video_path) as clip:
            frame = clip.get_frame(0)
            if clip.audio is None:
                print(f"{video_path} has no audio. Skipping...")
                return False
            return True
    except:
        print(f"Error validating {video_path}. Skipping...")
        return False

def process_video_clip(video_path):
    """Resizes and centers the video clip according to the final format."""
    clip = VideoFileClip(video_path)
    if clip.size[0] > clip.size[1]:  # Landscape video
        clip = clip.resize(height=1080)  # Resize it to 1080 in height
        # Now, we'll center it in a 1080x1920 frame
        background = ColorClip((1080, 1920), color=(0, 0, 0)).set_duration(clip.duration)
        clip = CompositeVideoClip([background, clip.set_position("center")])
    else:
        clip = clip.resize(width=1080)  # Portrait video
    return clip

def create_zap(directory_path, transition_video_path, output_path="output.mp4"):
    print("Starting create_zap function...")
    
    video_files = [f for f in os.listdir(directory_path) if f.endswith('.mp4') and f != os.path.basename(transition_video_path)]
    video_files = sorted(video_files)
    print(f"Found {len(video_files)} video files in the directory.")

    clips = []

    transition_clip = VideoFileClip(transition_video_path).resize(width=1080)  # Ensure the transition is also resized to 1080x1920
    print("Loaded and resized transition video.")

    for video_file in video_files:
        video_path = os.path.join(directory_path, video_file)
        if not is_valid_video(video_path):
            continue

        try:
            video_clip = process_video_clip(video_path)
            if video_clip:
                clips.append(video_clip)
                clips.append(transition_clip)
        except Exception as e:
            print(f"Error processing video {video_file}: {e}")

    try:
        if clips:
            print(f"Attempting to concatenate {len(clips)//2} videos and {len(clips)//2} transitions.")
            final_clip = concatenate_videoclips(clips[:-1], method="compose")  # We exclude the last transition
            final_clip.write_videofile(output_path, codec="libx264", audio_codec='aac')
            print("Final video written successfully.")
        else:
            print("No valid clips found to concatenate.")
    except Exception as e:
        print(f"Error during final video creation: {e}")

if __name__ == "__main__":
    directory = "videozap"
    transition = "transition.mp4"
    
    create_zap(directory, transition)
