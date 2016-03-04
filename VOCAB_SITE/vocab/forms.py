from django import forms

class LoginForm(forms.Form):
    userName = forms.CharField(label='User name', max_length=10)

class ContactForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class TermForm(forms.Form):
    domain = forms.CharField(label='Domain:', max_length=40)
    resourceType = forms.CharField(label='Resource Type:', max_length=10)
    vocabulary = forms.CharField(label='Vocabulary/Profile', max_length=40)
    termType = forms.ChoiceField(label='Term Type', initial='Activity Type', choices=(('verb', 'Verb'), ('activityType', 'Activity Type')))
    term = forms.CharField(label='Term', max_length=40)

class VocabForm(forms.Form):
    # this is quite repetitive at the moment, will simplify later
    domain = forms.CharField(label='Domain:', max_length=40)
    resourceType = forms.CharField(label='Resource Type:', max_length=10)
    vocabulary = forms.CharField(label='Vocabulary/Profile', max_length=40)
    termType = forms.CharField(label='Term Type', max_length=40)
    term = forms.CharField(label='Term', max_length=40)
