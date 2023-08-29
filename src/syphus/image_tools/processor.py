from PIL import Image

import io
import os
import cv2
import base64


def image_to_bytes(image: Image.Image) -> bytes:
    image_stream = io.BytesIO()
    image.save(image_stream, format="PNG")
    image_bytes = image_stream.getvalue()
    image_stream.close()
    return image_bytes


def resize_image(img: bytes, target_size: tuple[int, int] = (224, 224)) -> bytes:
    with Image.open(io.BytesIO(img)) as image:
        if image.size != target_size:
            resized_image = image.resize(target_size, Image.LANCZOS)
            image.close()
            image = resized_image
        resized_image_bytes = image_to_bytes(image)
    return resized_image_bytes


def process_image(image: bytes, target_size=(224, 224)) -> bytes:
    with Image.open(io.BytesIO(image)) as img:
        if img.size != target_size:
            resized_img = img.resize(target_size, Image.LANCZOS)
            img.close()
            img = resized_img
        if img.mode != "RGB":
            converted_img = img.convert("RGB")
            img.close()
            img = converted_img
        processed_image = image_to_bytes(img)
    return processed_image


def get_b64_data(image: bytes) -> str:
    return base64.b64encode(image).decode("utf-8")


def frame_video(video_file: str, fps: int = 1) -> list[bytes]:
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
            # Check if the frame resolution is not 224x224 and resize if necessary
            if frame.shape[0] != 224 or frame.shape[1] != 224:
                frame = cv2.resize(frame, (224, 224))

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
