import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def create_zap(directory_path, transition_video_path, output_path="output.mp4"):
    video_files = [f for f in os.listdir(directory_path) if f.endswith('.mp4') and f != os.path.basename(transition_video_path)]
    video_files = sorted(video_files)

    clips = []

    target_size = (1080, 1920)  # Desired video size

    for video_file in video_files:
        video_path = os.path.join(directory_path, video_file)
        video_clip = VideoFileClip(video_path)
        
        # Resizing video while keeping the audio
        video_clip_resized = video_clip.resize(target_size).set_audio(video_clip.audio)
        clips.append(video_clip_resized)

        # For transition video
        transition_clip = VideoFileClip(transition_video_path)
        transition_clip_resized = transition_clip.resize(target_size)
        clips.append(transition_clip_resized)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, codec="libx264", audio_codec='aac')

if __name__ == "__main__":
    directory = "videozap"
    transition = "transition.mp4"
    
    create_zap(directory, transition)