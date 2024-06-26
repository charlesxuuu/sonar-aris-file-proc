import cv2
import numpy as np
import os

def load_frames(video_path):
    """ Load all frames from the video as greyscale. """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return []
    frames = []
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if ret:
            # Assuming frame is already greyscale, append directly
            frames.append(frame)
            frame_count += 1  # Increment the counter on successful read
            print(f"Loaded {frame_count} frames...")
        else:
            print("Warning: No more frames to read or end of video reached.")
            break
    cap.release()
    return frames

def denoise_frames(frames, d=3, sigmaColor=75, sigmaSpace=75):
    """ Apply bilateral filter to greyscale video frames, with debug information. """
    if not frames:
        print("Error: No frames to denoise.")
        return []
    print("Starting denoising process...")
    denoised_frames = []
    for i, frame in enumerate(frames):
        print(f"Denoising frame {i+1} of {len(frames)}")
        denoised_frame = cv2.bilateralFilter(frame, d, sigmaColor, sigmaSpace)
        denoised_frames.append(denoised_frame)
    print("Denoising completed.")
    return denoised_frames

def save_and_display_denoised_frames(frames, video_path):
    """ Save and display denoised frames. """
    base_name = os.path.basename(video_path)
    dir_name = os.path.dirname(video_path)
    new_base_name = f"denoised_{base_name}"
    new_path = os.path.join(dir_name, new_base_name)

    # Create a VideoWriter object to save denoised frames
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Modify codec if necessary
    out = cv2.VideoWriter(new_path, fourcc, 20.0, (frames[0].shape[1], frames[0].shape[0]), False)  # Last parameter is isColor=False

    for frame in frames:
        out.write(frame)  # Write frame to file
        cv2.imshow('Denoised Frame', frame)
        if cv2.waitKey(0) == 13:  # Wait for the Enter key
            continue
    out.release()
    cv2.destroyAllWindows()

# Load video frames
video_path = '../../output/Haida_2020-05-24/2020-05-24_230000_373-443.mp4'

frames = load_frames(video_path)  # Adjust number based on your video length and memory capabilities

# Denoise the frames
if frames:
    denoised_frames = denoise_frames(frames)
    if denoised_frames:
        # Save and display denoised frames
        save_and_display_denoised_frames(denoised_frames, video_path)
    else:
        print("No frames were denoised.")
else:
    print("Failed to load frames.")


