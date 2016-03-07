from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm, ContactForm, TermForm, VocabForm, SearchForm
from .models import RegisteredIRI

@require_http_methods(["GET"])
def home(request):
    return render(request, 'home.html')

@login_required
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

@csrf_protect
@require_http_methods(["POST", "GET"])
def createUser(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'createUser.html', {"form": form})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            pword = form.cleaned_data['password']
            email = form.cleaned_data['email']
            # If username doesn't already exist
            if not User.objects.filter(username__exact=name).count():
                # if email doesn't already exist
                if not User.objects.filter(email__exact=email).count():
                    User.objects.create_user(name, email, pword)
                else:
                    return render(request, 'createUser.html', {"form": form, "error_message": "Email %s is already registered." % email})                    
            else:
                return render(request, 'createUser.html', {"form": form, "error_message": "User %s already exists." % name})                
            # If a user is already logged in, log them out
            if request.user.is_authenticated():
                logout(request)
            new_user = authenticate(username=name, password=pword)
            login(request, new_user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'createUser.html', {"form": form})

@login_required
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

@login_required
@require_http_methods(["GET"])
def userProfile(request):    
    return render(request, 'userProfile.html')

@require_http_methods(["GET", "POST"])
def searchResults(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid:
            search_term = form.data['search_term']
            iris = RegisteredIRI.objects.filter(address__contains=search_term)
        return render(request, 'searchResults.html', {"form":form, "iris":iris})
    else:
        form = SearchForm()
    return render(request, 'searchResults.html', {"form":form})


# @require_http_methods(["GET", "POST"])
# def login(request):
#     # return render(request, 'login.html')
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = LoginForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponse('thank you please drive through <br> %s' % form.cleaned_data['userName'])

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = RegisterForm()

#     return render(request, 'login.html', {'form': form})
@login_required()
@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))