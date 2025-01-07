from django import forms

from law.models import Contact


class ContactsViewModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}))