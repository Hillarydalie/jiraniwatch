from django.shortcuts import render, redirect
from .models import Profile, Hood, Business, Post, Join
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import SignUpForm, NewBusinessForm, NewPostForm, EditProfile, NewHoodForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


# @login_required(login_url='/accounts/login/')
def index(request):
    '''
    View function that displays the homepage and all its contents including social ammenitits and hoods notices
    '''
    post = Post.objects.all()
    biz = Business.objects.all()
    hoods = Hood.objects.all()
    return render(request, 'all/index.html', {"post": post, "biz": biz[::-1], "hoods":hoods} )


# @login_required(login_url='/accounts/login/')
def search_results(request):
    '''
    View function that enables a user search for any listed business
    '''

    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_businesses = Business.search_by_business_name(search_term)
        message = f"{search_term}"

        return render(request, 'all/search.html', {"message": message, "searched_businesses": searched_businesses})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all/search.html', {"message": message})


def signup(request):
    '''
    View function that ensures a user is first authenticated before using/accesing the application.
    '''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/')
            user.set_password(user.password)
            user.save()
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})


# @login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.user = request.user
            post.save()
            return redirect('/')
    else:
        form = NewPostForm()
    return render(request, 'all/post.html', {"form": form})

#View function that displays one profile. That includes their image and basic information


# @login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    current_user = request.user
    profiles = Profile.objects.filter(user__id__iexact=profile_id)
    profile = Profile.objects.get(user=profile_id)
    all_profile = Profile.objects.all()
    content = {
        "profiles": profiles,
        "profile": profile,
        "user": current_user,
        "profile_id": profile_id,
        "all_profile": all_profile
    }
    return render(request, "all/profile.html", content)

#View function that allows a user to edit his/her profile


# @login_required(login_url='/accounts/login/')
def edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            current_user = request.user
            profile = form.save(    )
            profile.user = request.user
            profile.save()
            return redirect('profile/', current_user.id)
    else:
        form = EditProfile()
    return render(request, 'all/editprofile.html', {"form": form})

# View function that enables one create a business


# @login_required(login_url='/accounts/login/')
def business(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewBusinessForm(request.POST)
        if form.is_valid():
            business = form.save()
            business.user = current_user
            business.save()
            return redirect('/')
    else:
        form = NewBusinessForm()
    return render(request, 'all/business.html', {"form": form})

# @login_required(login_url='/accounts/login/')
def neighbourhood(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewHoodForm(request.POST)
        if form.is_valid():
            hood = form.save()
            hood.user = current_user
            hood.save()
            return redirect('/')
    else:
        form = NewHoodForm()
    return render(request, 'all/hood.html', {"form": form})

# View function that displays all listed businesses


# @login_required(login_url='/accounts/login/')
def bizdisplay(request):
    biz = Business.objects.all()
    return render(request, 'all/bizdisplay.html', {"biz": biz[::-1]})

# View function that displays all listed neighbourhoods


# @login_required(login_url='/accounts/login/')
def mtaadisplay(request):
    hoods = Hood.objects.all()
    return render(request, 'all/displayhood.html', {"hoods": hoods[::-1]})


def join(request, hoodId):
    '''
    This view function will enable new users join a given neighbourhood 
    '''
    neighbourhood = Hood.objects.get(pk=hoodId)
    if Join.objects.filter(user_id=request.user).exists():
        messages.success(
            request, 'Welcome. You are now a member of this Neighbourhood')
        Join.objects.filter(user_id=request.user).update(hood_id=neighbourhood)
        return redirect('/')
    else:
        messages.success(
            request, 'Welcome. You are now a member of this Neighbourhood')
        Join(user_id=request.user, hood_id=neighbourhood).save()
        return redirect('/')


def exitHood(request, hoodId):
    '''
    View function to delete a user from a neighbourhood instance in the join table
    '''
    if Join.objects.filter(user_id=request.user).exists():
        Join.objects.get(user_id=request.user).delete()

        return redirect('/')
