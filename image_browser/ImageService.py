from image_browser.models import Image


class ImageService:
    @staticmethod
    def request_image(image_id):
        if image_id:
            image = Image.objects.filter(id=image_id).first()
            return image
        return None

    @staticmethod
    def image_is_exist(image_id):
        if ImageService.request_image(image_id):
            return True
        else:
            return False

