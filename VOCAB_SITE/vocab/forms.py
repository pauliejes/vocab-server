from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=200, label='Name')
    email = forms.EmailField(max_length=200, label='Email')
    password = forms.CharField(label='Password', 
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label='Password Again', 
                                widget=forms.PasswordInput(render_value=False))

    def clean(self):
        cleaned = super(RegisterForm, self).clean()
        p1 = cleaned.get("password")
        p2 = cleaned.get("password2")
        if p1 and p2:
            if p1 == p2:
                return cleaned
        raise forms.ValidationError("Passwords did not match")

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

class SearchForm(forms.Form):
    search_term = forms.CharField(label='Search:', max_length=40)