from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.core.urlresolvers import reverse
from wordpress.models import Post


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post.html'


class PostList(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-modified'
    paginate_by = 5


class PostFeed(Feed):
    title = "Fss Open Tech Club News"
    link = "/blog/"

    def items(self):
        return Post.objects.order_by('-post_date')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('blog:post', kwargs={"pk": item.pk})

    def item_pubdate(self, item):
        return item.post_date

    def item_author_name(self, item):
        return item.author.name
