from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from wordpress.models import Post

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post.html'

def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})
