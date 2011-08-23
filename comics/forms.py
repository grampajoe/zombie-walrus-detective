from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(max_length=120,
            widget=forms.TextInput(attrs={'size':32}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'size':32}))
    website = forms.URLField(widget=forms.TextInput(attrs={'size':32}))
    message = forms.CharField(
            widget=forms.Textarea(attrs={'rows':8, 'cols':42}))

    required_css_class = 'required'
