from django import forms
from .models import Product
from django.contrib.auth.models import User

class SearchForm(forms.Form):
    query = forms.CharField(
label='検索キーワード',
        max_length=100,
        required=False,
widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入 力'})
)
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']



