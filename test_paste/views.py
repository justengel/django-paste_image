from django.shortcuts import render, redirect, get_object_or_404

from django import forms
from django.forms.widgets import ClearableFileInput

from paste_image import widgets

from .models import MyModel


# Create your views here.
class ImageForm(forms.ModelForm):
    class Meta:
        model = MyModel
        exclude = []


def index(request, pk=None):
    instance = None
    if pk is not None:
        instance = get_object_or_404(MyModel, pk=pk)

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            pk = form.save().id
            return redirect("test_paste:index", pk=pk)
    else:
        form = ImageForm(instance=instance)

    return render(request, "test_paste/index.html", {"form": form, "pk": pk})
