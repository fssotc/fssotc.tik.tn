from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from wordpress.models import Post

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post.html'

class PostList(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-modified'
    paginate_by = 5
