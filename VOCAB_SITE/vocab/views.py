from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect, HttpResponse
from .forms import LoginForm


@require_http_methods(["GET"])
def home(request):
    return render(request, 'home.html')

@require_http_methods(["GET"])
def createURI(request):
    return render(request, 'createURI.html')

@require_http_methods(["GET"])
def createUser(request):
    return render(request, 'createUser.html')

@require_http_methods(["GET"])
def createVocab(request):
    return render(request, 'createVocab.html')

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
