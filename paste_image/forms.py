import os
from django import forms
from django.core.files import File
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .widgets import PasteImageWidget


class PasteImageFormField(forms.ImageField):
    widget = PasteImageWidget
    default_error_messages = {
        'invalid_file': _(
            "Upload a valid image. The file you uploaded was either not an "
            "image or a corrupted image."
        ),
        'invalid_image': _(
            "Upload a valid image. The file you uploaded did not have an extension with "
            ".jpg, .jpeg, .png, or .gif."
        ),
        'invalid': _("No file was submitted. Check the encoding type on the form."),
    }

    VALID_IMAGE_EXTENSIONS = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
    ]

    def __init__(self, multiple=False, *args, **kwargs):
        self.multiple = multiple
        super(PasteImageFormField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        """
        Checks that the file-upload field data contains a valid image (GIF, JPG,
        PNG, possibly others -- whatever the Python Imaging Library supports).
        """
        ret = []
        data = data or []
        for item in data:
            img = super(PasteImageFormField, self).to_python(item)
            if img:
                ret.append(img)
        if not self.multiple and len(ret) > 0:
            return ret[-1]
        return ret

    def validate(self, data):
        super(PasteImageFormField, self).validate(data)

        if not isinstance(data, list):
            if data is None or data == "":
                num_files = 0
            else:
                num_files = 1
            data = [data]
        else:
            num_files = len(data)

        if not self.required and num_files == 0:
            return

        if self.multiple and num_files == 0:
            raise ValidationError(self.error_messages["invalid"])

        for img in data:
            if not isinstance(img, File):
                raise ValidationError(self.error_messages["invalid_file"])
            if os.path.splitext(img.name)[-1] not in self.VALID_IMAGE_EXTENSIONS:
                raise ValidationError(self.error_messages["invalid_image"])
