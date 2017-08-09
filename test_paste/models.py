from django.db import models

import paste_image


class MyModel(models.Model):
    image = paste_image.PasteImageField(upload_to="pasted_images/", blank=True)

    def __str__(self):
        return " ".join((str(self.id), str(self.image)))
