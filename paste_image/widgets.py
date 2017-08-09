import os
import base64
from django.templatetags.static import static
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.forms.widgets import FileInput
from django.template import loader, TemplateDoesNotExist, Template, Context
from django.utils.safestring import mark_safe


# ========== Library Files (Don't need to incude paste_image in INSTALLED_APPS for a few static files) ==========
DIRECTORY = os.path.dirname(__file__)
SINGLE_TEMPLATE_PATH = os.path.join(DIRECTORY, "templates/paste_image/widgets/paste_image.html")
TEMPLATE_MULTIPLE_PATH = os.path.join(DIRECTORY, "templates/paste_image/widgets/paste_image_multiple.html")

with open(os.path.join(DIRECTORY, 'static/paste_image/paste_image.css')) as file:
    LIBRARY_CSS = mark_safe(file.read())

with open(os.path.join(DIRECTORY, 'static/paste_image/jquery.js')) as file:
    LIBRARY_JQUERY = mark_safe(file.read())


class StaticTemplate(Template):
    def __init__(self, template_string, origin=None, name=None, engine=None):
        if isinstance(template_string, str) and os.path.exists(template_string):
            with open(template_string, "r") as file:
                template_string = file.read()
        super(StaticTemplate, self).__init__(template_string, origin, name, engine)

    def render(self, context):
        context["library_css"] = LIBRARY_CSS
        context["library_jquery"] = LIBRARY_JQUERY
        return super(StaticTemplate, self).render(Context(context))


SINGLE_TEMPLATE = StaticTemplate(SINGLE_TEMPLATE_PATH)
TEMPLATE_MULTIPLE = StaticTemplate(TEMPLATE_MULTIPLE_PATH)
# ========== End Library Files ==========


class PasteImageWidget(FileInput):
    """This widget accepts any kind of image file with the ability to copy and paste onto the web page.

    Note:
        Call with PasteImageWidget(attrs={"multiple": True}) to allow multiple images.
    """

    template_name = "paste_image/widgets/paste_image.html"
    temmplate_name_multiple = "paste_image/widgets/paste_image_multiple.html"
    input_type = "file"
    needs_multipart_form = True

    class Media:
        css = {
            "all": ("paste_image/paste_image.css",)
        }

    def value_omitted_from_data(self, data, files, name):
        for key in data:
            if (key == name and data[key] != "") or key.startswith("pasted_image_"+name):
                return False
        return name not in files

    def value_from_datadict(self, data, files, name):
        """File widgets take data from FILES, not POST"""
        pasted_images = {key: data[key] for key in data
                         if (key == name and data[key] != "") or key.startswith("pasted_image_"+name)}
        if len(pasted_images) == 0 and name not in files:
            return None

        try:
            myfiles = files.getlist(name)
        except AttributeError:
            myfiles = []

        handler = TemporaryFileUploadHandler()

        for key in pasted_images:
            img = pasted_images[key]
            content_type = "image/jpeg"
            if "base64," in img:
                pre, img = img.split("base64,")
                content_type = pre[5:-1]  # Skip "data:" and remove the ; ("data:image/png;")

            # img = File(io.BytesIO(base64.b64decode(img)))
            # img.name = key + ".jpeg"
            imgdata = base64.b64decode(img)
            file_name = key + "." + content_type.split("/")[-1]

            handler.new_file(name, file_name, content_type, len(imgdata))
            handler.receive_data_chunk(imgdata, 0)
            file = handler.file_complete(len(imgdata))
            myfiles.append(file)
        return myfiles

    def get_context(self, name, value, attrs=None):
        url = ""
        if value is not None:
            try:
                url = value.url
            except (AttributeError, ValueError):
                pass

        widget_vars = {"name": name, "value": url}
        if attrs:
            widget_vars.update(self.attrs)  # div_style
        return {"widget": widget_vars}

    def render(self, name, value, attrs=None):
        template = self.template_name
        static_template = SINGLE_TEMPLATE
        try:
            if attrs and attrs.get("multiple", False):
                template = self.temmplate_name_multiple
                static_template = TEMPLATE_MULTIPLE
        except (AttributeError, ValueError, TypeError):
            pass

        context = self.get_context(name, value, attrs)

        # Try to get a custom template or just load the library template if paste_image is not in INSTALLED_APPS
        try:
            template = loader.get_template(template)
        except TemplateDoesNotExist:
            template = static_template

        return mark_safe(template.render(context))
