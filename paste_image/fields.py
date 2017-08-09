from django.db.models.fields.files import ImageFileDescriptor, ImageField
from django.core.files.uploadhandler import TemporaryFileUploadHandler

from .forms import PasteImageFormField


class PasteImageFileDescriptor(ImageFileDescriptor):
    """Image descriptor that can be set with image bytes as the value."""
    def __set__(self, instance, value):
        if isinstance(value, bytes):
            # Get the data
            if b"base64," in value:
                value = value.split(b"base64,")[-1]

            # value = File(io.BytesIO(base64.b64decode(value)))
            # value.name = self.field.name + ".png"

            # Manually upload the file data as if a file input was given
            handler = TemporaryFileUploadHandler()
            handler.new_file(self.field.name, self.field.name + ".jpeg", "image/jpeg", len(value))
            handler.receive_data_chunk(value, 0)
            value = handler.file_complete(len(value))
        super(PasteImageFileDescriptor, self).__set__(instance, value)


class PasteImageField(ImageField):
    """Field for the PasteImageWidget"""
    descriptor_class = PasteImageFileDescriptor

    def formfield(self, **kwargs):
        defaults = {'form_class': PasteImageFormField}
        defaults.update(kwargs)
        return super(PasteImageField, self).formfield(**defaults)
