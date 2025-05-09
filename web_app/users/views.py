from django.shortcuts import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import UserRegisterForm, UserUpdateForm,ProfileUpdateForm, StoryForm 
from .models import Story, EmailVerification, Relationship
from django.contrib.auth import login
from django.core.mail import *
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
import uuid
from django.urls import reverse
from django.conf import settings
#from django.db.models import Q
from django.db import models


def logout(request):
    return render(request, 'users/logout_confirm.html')

def send_verification_email(request, user):
    
    verification, created = EmailVerification.objects.get_or_create(user=user)
    
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    
    message = render_to_string('users/verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': verification.token,
    })
    
    send_mail(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,
        fail_silently=False,
    )

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        verification = EmailVerification.objects.get(user=user, token=token)
        
        if verification.is_expired():
            return render(request, 'verification_expired.html')
            
        verification.is_verified = True
        verification.save()
        
        
        user.is_active = True
        user.save()
        
       
        login(request, user)
        
        return render(request, 'verification_success.html')
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, EmailVerification.DoesNotExist):
        return render(request, 'verification_invalid.html')
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_verification_email(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account has been created ! You are now able to login")
            return redirect("login")

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method =='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form= ProfileUpdateForm(request.POST, 
                                  request.FILES,
                                  instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated !")
            return redirect("profile")
            
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form= ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def story_create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            messages.success(request, f"Your story has been created !")
            return redirect("profile")
    else:
        form = StoryForm()
    return render(request, 'users/story_form.html', {'form': form})
class Storydetails(DetailView):
    model = Story
    template_name = "users/story_details.html"
    context_object_name = 'story'


class UserDetails(DetailView):
    model = User
    template_name = 'users/user_details.html'
   
class UserListView(ListView):
    model = User
    template_name = "users/user_list.html" #<app>/<model>_<viewtype>.html
    context_object_name = 'users'
    ordering = ['date_joined']

def UserDetailView(request, user_id):
    user = get_object_or_404(User, id=user_id)
    users = {'user': user}
    return render(request, 'users/user_details.html', users)

@login_required
def follow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    
    if request.user == followed_user:
        messages.error(request, "You cannot follow yourself")
        return redirect('user_profile', username=request.user.username)
    
    Relationship.objects.get_or_create(
        follower=request.user,
        followed=followed_user
    )
    messages.success(request, f"You are now following {followed_user.username}")
    return redirect('user_profile', username=followed_user.username)


@login_required
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    Relationship.objects.filter(
        follower=request.user,
        followed=followed_user
    ).delete()
    messages.success(request, f"You have unfollowed {followed_user.username}")
    return redirect('user_profile', username=followed_user.username)
@require_POST
@login_required
def send_friend_request(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if request.user == target_user:
        messages.error(request, "You cannot send friend request to yourself")
        return redirect('user_profile', username=request.user.username)
    
    if Relationship.objects.filter(
        follower=request.user,
        followed=target_user,
        is_friends=True
    ).exists():
        messages.info(request, f"You are already friends with {target_user.username}")
        return redirect('user_profile', username=target_user.username)

    rel, created = Relationship.objects.update_or_create(
        follower=request.user,
        followed=target_user,
        defaults={'is_friends': False}
    )
    
    messages.success(request, f"Friend request sent to {target_user.username}")
    return redirect('user_profile', username=target_user.username)

@login_required
def accept_friend_request(request, user_id):
    requester = get_object_or_404(User, id=user_id)
    
    incoming_request = get_object_or_404(
        Relationship,
        follower=requester,
        followed=request.user,
        is_friends=False
    )
    
    incoming_request.is_friends = True
    incoming_request.save()
    
    Relationship.objects.get_or_create(
        follower=request.user,
        followed=requester,
        is_friends=True
    )
    
    messages.success(request, f"You are now friends with {requester.username}")
    return redirect('user_profile', username=requester.username)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    
    # Get relationship status
    is_following = Relationship.objects.filter(
        follower=request.user,
        followed=user
    ).exists()
    
    is_friends = Relationship.objects.filter(
        follower=request.user,
        followed=user,
        is_friends=True
    ).exists()
    
    friend_request_sent = Relationship.objects.filter(
        follower=request.user,
        followed=user,
        is_friends=False
    ).exists()
    

    pending_request_from_user = Relationship.objects.filter(
        follower=user,
        followed=request.user,
        is_friends=False
    ).exists()
    
    context = {
        'user': user,
        'is_following': is_following,
        'is_friends': is_friends,
        'friend_request_sent': friend_request_sent,
        'pending_request_from_user': pending_request_from_user,
        'stories': Story.objects.filter(user=user),
        'followers_count': user.followers.count(),
        'following_count': user.following.count(),
        'friends_count': Relationship.objects.filter(
            models.Q(follower=user, is_friends=True) |
            models.Q(followed=user, is_friends=True)
        ).count(),
    }
    return render(request, 'users/user_details.html', context)