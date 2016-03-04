from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect, HttpResponse
from .forms import LoginForm, ContactForm, TermForm, VocabForm
from django.core.mail import send_mail

@require_http_methods(["GET"])
def home(request):
    return render(request, 'home.html')

@require_http_methods(["GET", "POST"])
def createURI(request):
    # return render(request, 'login.html')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TermForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            domain = form.cleaned_data['domain']
            resourceType = form.cleaned_data['resourceType']
            vocabulary = form.cleaned_data['vocabulary']
            termType = form.cleaned_data['termType']
            term = form.cleaned_data['term']
            newuri = 'https://' + domain + '/' + resourceType + '/' + vocabulary + '/' + termType + '/' + term
            # redirect to a new URL:
            return HttpResponse('you did not create a term, but we did trick this info out of you: <br> %s' % newuri)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TermForm()

    return render(request, 'createURI.html', {'form': form})

@require_http_methods(["GET", "POST"])
def createUser(request):
    # return render(request, 'createUser.html')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # return HttpResponse('baby step get on the elevator <br> %s' % form.cleaned_data['subject'])
            return HttpResponseRedirect('/')
            #above are two options to respond simply
            #below is an example from documentation, let's see what happens
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['andrew.creighton.ctr@adlnet.gov']
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/')
            #this does not send and email, but since that's not what we really want here anyway - i think we're alright

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'createUser.html', {'form': form})

@require_http_methods(["GET", "POST"])
def createVocab(request):
    # return render(request, 'login.html')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VocabForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            domain = form.cleaned_data['domain']
            resourceType = form.cleaned_data['resourceType']
            vocabulary = form.cleaned_data['vocabulary']
            termType = form.cleaned_data['termType']
            term = form.cleaned_data['term']
            # redirect to a new URL:
            return HttpResponse("that's a lot of words are you finished now? <br> %s" % vocabulary)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VocabForm()

    return render(request, 'createVocab.html', {'form': form})

@require_http_methods(["GET"])
def userProfile(request):
    return render(request, 'userProfile.html')

@require_http_methods(["GET"])
def searchResults(request):
    return render(request, 'searchResults.html')

@require_http_methods(["GET", "POST"])
def login(request):
    # return render(request, 'login.html')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse('thank you please drive through <br> %s' % form.cleaned_data['userName'])

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
