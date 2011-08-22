from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=120,
            widget=forms.TextInput(attrs={'size':32}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'size':32}))
    website = forms.URLField()
    message = forms.CharField(
            widget=forms.Textarea(attrs={'rows':8, 'cols':32}))
