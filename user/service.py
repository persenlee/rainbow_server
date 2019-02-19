
from user.models import UserModel, CollectImagesModel
from image_browser.ImageService import ImageService


class UserService:
    @staticmethod
    def request_user_info(user_id):
        if user_id is None:
            return None
        user = UserModel.objects.filter(id=user_id).first()
        return user

    @staticmethod
    def collect_image(user_id, image_id, collect):
        if user_id is None:
            return False
        user = UserModel.objects.filter(id=user_id).first()
        if user and ImageService.image_is_exist(image_id):
            image = ImageService.request_image(image_id)
            if collect and collect != '0' and collect != 'false':
             collect_model = CollectImagesModel()
             collect_model.user = user
             collect_model.image = image
             collect_model.save()
             return True
            else:
                collect_model = CollectImagesModel.objects.filter(user=user, image=image).first()
                if collect_model:
                    collect_model.delete()
                    return True
        return False

    @staticmethod
    def request_image_like_count(image_id):
        if image_id is None:
            return 0
        queryset = CollectImagesModel().objects.filter(image=image_id)
        return count(queryset)

    @staticmethod
    def request_has_collect_image(user_id,image_id):
        if user_id and image_id:
            user = UserModel.objects.filter(id=user_id).first()
            image = ImageService.request_image(image_id)
            if user and image:
                collect_model = CollectImagesModel.objects.filter(user=user, image=image).first()
                if collect_model:
                    return True
        return False
