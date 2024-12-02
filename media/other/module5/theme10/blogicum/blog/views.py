from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Post, Category


class BasePostQueryMixin:

    def get_base_post_queryset(self):
        return Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        ).select_related('author', 'location', 'category')


class PostListView(BasePostQueryMixin, ListView):
    model = Post

    def get_queryset(self):
        return self.get_base_post_queryset()[:5]


class PostDetailView(BasePostQueryMixin, DetailView):
    model = Post

    def get_queryset(self):
        return self.get_base_post_queryset()


class CategoryDetailView(DetailView):
    model = Category

    def get_queryset(self):
        return self.model.objects.filter(
            is_published=True
        ).prefetch_related('post_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post_list'] = self.object.post_set.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
        ).order_by(
            '-pub_date'
        ).select_related('author', 'location', 'category')

        return context
