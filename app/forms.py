from django import forms
from .models import Product,Comment


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()

class FormModelComment(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ()