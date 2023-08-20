import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageSequenceClip

def video_clip_to_numpy_array(video_clip):
    frames = [frame for frame in video_clip.iter_frames()]
    return np.array(frames)

def resize_video_array(video_np, new_width, new_height):
    return np.array([cv2.resize(frame, (new_width, new_height)) for frame in video_np])

def create_zap(directory_path, transition_video_path, output_path="output.mp4"):
    video_files = [f for f in os.listdir(directory_path) if f.endswith('.mp4') and f != os.path.basename(transition_video_path)]
    video_files = sorted(video_files)  # Optionnel, cela trie les vidéos par nom

    clips = []

    for video_file in video_files:
        video_path = os.path.join(directory_path, video_file)
        video_clip = VideoFileClip(video_path)

        original_width, original_height = video_clip.size
        new_height = int(video_clip.size[1])
        new_width = int(new_height * 9 / 16)

        video_np = video_clip_to_numpy_array(video_clip)
        if original_width != new_width or original_height != new_height:
            video_np_resized = resize_video_array(video_np, new_width, new_height)
        else:
            video_np_resized = video_np

        video_clip_resized = ImageSequenceClip(list(video_np_resized), fps=video_clip.fps)
        
        transition_clip = VideoFileClip(transition_video_path)
        transition_np = video_clip_to_numpy_array(transition_clip)
        
        transition_original_width, transition_original_height = transition_clip.size
        if transition_original_width != new_width or transition_original_height != new_height:
            transition_np_resized = resize_video_array(transition_np, new_width, new_height)
        else:
            transition_np_resized = transition_np

        transition_clip_resized = ImageSequenceClip(list(transition_np_resized), fps=transition_clip.fps)

        clips.extend([video_clip_resized, transition_clip_resized])

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, codec="libx264")

if __name__ == "__main__":
    directory = "videozap"
    transition = "transition.mp4"
    
    create_zap(directory, transition)
