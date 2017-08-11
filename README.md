# django-paste_image

This django library is intended to make copying and pasting images in the web browser easier.
 
## Uses
```python
# models.py
import paste_image  # Not needed in installed apps
 
class MyModel(models.Model):
    image = paste_image.PasteImageField(upload_to="pasted_images/", blank=True)
```

Or just use the widget
```python
# models.py
class MyModel(models.Model):
    image = models.ImageField(upload_to="pasted_images/", blank=True)

# forms.py
import paste_image
 
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        exclude = []
        widgets = {
            'image': paste_image.PasteImageWidget()
        }
```

## Advanced usage
Override `static/paste_image/paste_image.css` with the classes
  * pasted_image_style
  * remove_pasted_image
  * pasted_image_file

I've made this to work by default by loading the static file from the library folder. 
This app does not need to be put into INSTALLED_APPS.
 
### Multiple Images
**Not fully test. WIP**

For multiple images pass the `multiple` argument. This will require some work.

Note the ForeignKey relationship to another model

```python
# models.py
class MyModel(models.Model):
    name = model.CharField(max_length=255)
    
class MyImages(models.Model):
    mymodel = models.ForeignKey(MyModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="myimages/")

# forms.py
import paste_image

class MyForm(forms.ModelForm):
    images = paste_image.PasteImageFormField(multiple=True)
    
    class Meta:
        model = MyModel
        exclude = []
    
    def save(self, *args, **kwargs):
        # Save and create the main object
        obj = super(MyForm, self).save(*args, **kwargs)

        # This should be a list of TemporaryFileUpload images
        images = self.cleaned_data["images"]
        for file in images:
            MyImages.objects.create(mymodel=obj, image=file)
        return obj
```

A widget can also use the multiple keywork, but you have to handle the list of returned images.

```python
# forms.py
import paste_image
 
class MyForm(forms.ModelForm):
    image = forms.ImageField(widget=paste_image.PasteImageWidget(attrs={"multiple":True}))
    
    class Meta:
        model = MyModel
        exclude = []
```

## How it works
Custom django widget that uses the template `templates/paste_image/widgets/paste_image.html`

There are three main items to the generated html.
  * file input <input type=file id="id_{{ widget.name }}>
    * This allows a user to browse for a file
  * img tag to display the image(s)
    * For multiple images this is a div that contains and creates multiple image tags.
  * Hidden input tag.
    * This contains the data for pasted images.
    * On submit the widget runs the `value_from_datadict` function
    * Each pasted image uses it's binary data to create a `TemporaryFileUpload` 
    which is how a normal file upload works in django
