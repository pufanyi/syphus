from typing import List, Tuple
from PIL import Image
import io
import os
import cv2
import base64


def convert_pil_image_to_bytes(image: Image.Image) -> bytes:
    """
    Convert a PIL Image object into bytes.

    Args:
        image (PIL.Image.Image): The input PIL Image object.

    Returns:
        bytes: The image data in bytes.
    """
    image_stream = io.BytesIO()
    image.save(image_stream, format="PNG")
    image_bytes = image_stream.getvalue()
    image_stream.close()
    return image_bytes


def resize_image(img_bytes: bytes, target_size: Tuple[int, int] = (224, 224)) -> bytes:
    """
    Resize an image in bytes format to the specified target size.

    Args:
        img_bytes (bytes): The input image data in bytes.
        target_size (Tuple[int, int], optional): The target size (width, height). Defaults to (224, 224).

    Returns:
        bytes: The resized image data in bytes.
    """
    with Image.open(io.BytesIO(img_bytes)) as image:
        if image.size != target_size:
            resized_image = image.resize(target_size, Image.LANCZOS)
            image.close()
            image = resized_image
        resized_image_bytes = convert_pil_image_to_bytes(image)
    return resized_image_bytes


def process_image(img_bytes: bytes, target_size: Tuple[int, int] = (224, 224)) -> bytes:
    """
    Process an image in bytes format by resizing and converting it to RGB mode.

    Args:
        img_bytes (bytes): The input image data in bytes.
        target_size (Tuple[int, int], optional): The target size (width, height). Defaults to (224, 224).

    Returns:
        bytes: The processed image data in bytes.
    """
    with Image.open(io.BytesIO(img_bytes)) as img:
        if img.size != target_size:
            resized_img = img.resize(target_size, Image.LANCZOS)
            img.close()
            img = resized_img
        if img.mode != "RGB":
            converted_img = img.convert("RGB")
            img.close()
            img = converted_img
        processed_image = convert_pil_image_to_bytes(img)
    return processed_image


def convert_image_to_base64(img_bytes: bytes) -> str:
    """
    Convert image data in bytes format to a base64-encoded string.

    Args:
        img_bytes (bytes): The input image data in bytes.

    Returns:
        str: The base64-encoded image data as a string.
    """
    return base64.b64encode(img_bytes).decode("utf-8")


def extract_and_process_frames(
    video_file: str, fps: int = 1, target_size: Tuple[int, int] = (224, 224)
) -> List[bytes]:
    """
    Extract and process frames from a video file.

    Args:
        video_file (str): The path to the video file.
        fps (int, optional): The frame rate at which to extract frames. Defaults to 1.
        target_size (Tuple[int, int], optional): The target size (width, height) for frames. Defaults to (224, 224).

    Returns:
        List[bytes]: A list of processed frame images in bytes format.
    """
    if not os.path.exists(video_file):
        raise FileNotFoundError(f"Video file {video_file} does not exist.")

    cap = cv2.VideoCapture(video_file)
    video_fps = int(cap.get(cv2.CAP_PROP_FPS))

    frame_count = 0
    saved_frame_count = 0
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % (video_fps // fps) == 0:
            if frame.shape[0] != target_size[0] or frame.shape[1] != target_size[1]:
                frame = cv2.resize(frame, target_size)

            success, buffer = cv2.imencode(".png", frame)
            if not success:
                print(f"Failed to encode frame {frame_count} of video {video_file}.")
            frames.append(process_image(buffer))
            saved_frame_count += 1

            del buffer

        frame_count += 1

        del frame

    cap.release()
    return frames
