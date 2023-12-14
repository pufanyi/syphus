import io
from PIL import Image as PILImage

import syphus.utils.image_processor as image_processor


class Image(object):
    def __init__(self, image_id, *, image_path=None, image_data=None):
        self.image_id = image_id
        if image_path is not None and image_data is not None:
            raise ValueError("Cannot specify both image_path and image_data.")
        if image_path is None and image_data is None:
            self.image = None
        elif image_path is not None:
            self.image = PILImage.open(image_path)
        elif image_data is None:
            self.image = None
        elif isinstance(image_data, PILImage.Image):
            self.image = image_data
        elif isinstance(image_data, bytes):
            self.image = image_processor.convert_bytes_to_pil_image(image_data)
        elif isinstance(image_data, str):
            self.image = image_processor.convert_base64_to_pil_image(image_data)
        else:
            raise TypeError("image_data should be bytes, str, or PIL.Image.Image")

    def to_base64(self):
        return image_processor.convert_pil_image_to_base64(self.image)

    def to_bytes(self):
        return image_processor.convert_pil_image_to_bytes(self.image)

    def to_pil_image(self):
        return self.image

    def from_path(self, image_path):
        self.image = PILImage.open(image_path)

    def from_base64(self, image_base64):
        self.image = image_processor.convert_base64_to_pil_image(image_base64)

    def from_bytes(self, image_bytes):
        self.image = image_processor.convert_bytes_to_pil_image(image_bytes)
