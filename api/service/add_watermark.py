import io
import math
from datetime import datetime

import cv2
import numpy
from PIL import Image
from api.models import ProfilePhoto
from django.core.files.base import ContentFile


def decode_image(start_image):
    image_array = cv2.imdecode(numpy.frombuffer(start_image.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    return Image.fromarray(image_rgb)


def add_watermark(image):
    def resize_images(image):
        width, height = image.size

        resize = max(width/1000,height/1500)
        if resize>1:
            image = image.resize((math.floor(width/resize), math.floor(height/resize)), Image.ANTIALIAS)
        else:
            image = image.resize((math.floor(width/resize),math.floor(height/resize)), Image.ANTIALIAS)
        watermark = Image.open("api/service/watermark.png")
        return image, watermark

    def union_image_with_watermark(image, watermark):
        width, height = image.size
        processed_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        processed_image.paste(image, (0, 0))
        processed_image.paste(watermark, (0, 0), mask=watermark)
        return processed_image

    resized_image, watermark = resize_images(image)

    return union_image_with_watermark(resized_image, watermark)


def image_saving(image_with_mark, user):
    def time_now():
        time = datetime.now()
        time = datetime.strftime(time, "%Y-%m-%d-%H")
        return time

    add_new_photo = ProfilePhoto(profile=user)

    flow = io.BytesIO()
    try:
        image_with_mark.save(flow, format='png')
        add_new_photo.photo.save(f"{user.username}/photo-{time_now()}.png", ContentFile(flow.getvalue()))
    finally:
        flow.close()


def image_changing(data, user):
    start_image = data.get("img")

    decoded_image = decode_image(start_image)

    image_with_mark = add_watermark(decoded_image)

    image_saving(image_with_mark, user)
