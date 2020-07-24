from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from .models import Post
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
# Create your views here.


def home(request):

    return redirect('register')

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5


class UserPostListView(ListView):
    html_file = get_template('blog/activation.html')
    html_content = html_file.render()
    sub = 'Activate your Account'
    from_email = 'sushpalikhe85@gmail.com'
    to = ['sushmipalikhe97@gmail.com', ]
    msg = EmailMultiAlternatives(subject=sub, from_email=from_email, to=to)

    msg.attach_alternative(html_content, 'text/html')
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
