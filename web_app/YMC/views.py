from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Blog
from .forms import CommentForm, ImagePostForm, IdeaPostForm, VideoPostForm


class BlogListView(ListView):
    model = Blog
    template_name = "YMC/home.html" #<app>/<model>_<viewtype>.html
    context_object_name = 'blogs'
    ordering = ['-date_created']

class VideoPost(ListView):
    model = Blog
    template_name = "YMC/video_post.html" #<app>/<model>_<viewtype>.html
    context_object_name = 'videos'
    ordering = ['-date_created']

class ImagePost(ListView):
    model = Blog
    template_name = "YMC/image_post.html" #<app>/<model>_<viewtype>.html
    context_object_name = 'images'
    ordering = ['-date_created']

class IdeaPost(ListView):
    model = Blog
    template_name = "YMC/idea_post.html" #<app>/<model>_<viewtype>.html
    context_object_name = 'ideas'
    ordering = ['-date_created']


class PostDetailView(DeleteView):
    model = Blog
    template_name = 'YMC/blog_details.html'



class UserPostListView(ListView):
    model = Blog
    template_name = 'YMC/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-date_created'] 

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        
        return super().get_queryset().filter(author=user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(
            User, 
            username=self.kwargs.get('username')
        )
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    template_name = 'YMC/blog_update.html'
    fields = ['title', 'content','image_file','videos_file']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = '/'
    

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CreatePost(CreateView):
    model = Blog
    fields = ['title', 'content', 'image_file','videos_file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)
    success_url = reverse_lazy('home')


class CreateImagePost(CreateView):
    model = Blog
    fields = ['image_file',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)
    success_url = reverse_lazy('image_post')

class CreateVideoPost(CreateView):
    model = Blog
    fields = ['videos_file',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)
    success_url = reverse_lazy('video_post')

class CreateIdeaPost(CreateView):
    model = Blog
    fields = ['content',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)
    success_url = reverse_lazy('idea_post')
def blogcomment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been posted!')
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'YMC/blog_comment.html', {'form': form})







