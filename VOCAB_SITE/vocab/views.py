from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, ContactForm, IRIForm, SearchForm
from .models import RegisteredIRI

@require_http_methods(["GET"])
def home(request):
    return render(request, 'home.html')

@login_required
@require_http_methods(["GET", "POST"])
def createIRI(request):
    IRIFormset = formset_factory(IRIForm)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset = IRIFormset(request.POST)
        # check whether it's valid:
        if formset.is_valid():
            # process the data in form.cleaned_data as required
            for form in formset:
                if form.is_valid():
                    vocabulary = form.cleaned_data['vocabulary']
                    termType = form.cleaned_data['termType']
                    term = form.cleaned_data['term']
                    newiri = 'https://w3id.org/xapi/' + vocabulary + '/' + termType + '/' + term + '/'
                    print(newiri)
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('iriCreationResults'), {'newiri': newiri, 'data': form.cleaned_data})

    # if a GET (or any other method) we'll create a blank form
    else:
        formset = IRIFormset()

    return render(request, 'createIRI.html', {'formset': formset})

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
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IRIForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # domain = form.cleaned_data['domain']
            # resourceType = form.cleaned_data['resourceType']
            vocabulary = form.cleaned_data['vocabulary']
            termType = form.cleaned_data['termType']
            term = form.cleaned_data['term']
            # redirect to a new URL:
            return HttpResponseRedirect('vocabReceived', form.cleaned_data)

    # if a GET (or any other method) we'll create a blank form
    # starting at the vocab portion of the iri
    else:
        form = IRIForm()

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

@login_required()
@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required()
@require_http_methods(["GET"])
def iriCreationResults(request):
    return render(request, 'iriCreationResults.html')
