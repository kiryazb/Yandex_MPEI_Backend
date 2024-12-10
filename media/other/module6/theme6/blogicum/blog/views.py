from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView, DeleteView,
)
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .forms import CommentForm, PostForm, ProfileEditForm
from .models import Post, Category, User, Comment


class BasePostQueryMixin:

    def get_base_post_queryset(self):
        return Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        ).select_related(
            'author', 'location', 'category'
        ).prefetch_related('comment_set').all()


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'blog/create.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={
                'username': self.request.user.username,
            },
        )


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={
                'username': self.request.user.username,
            },
        )


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.author != request.user:
            return redirect('blog:post_detail', kwargs['pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=kwargs['pk'])

        if post.author != user and not user.is_superuser:
            return redirect('blog:post_detail', kwargs['pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={
                'username': self.request.user.username,
            },
        )


@method_decorator(login_required, name='dispatch')
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={
                'pk': self.kwargs['post_id'],
            },
        )


@method_decorator(login_required, name='dispatch')
class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        if comment.author != request.user:
            return redirect('blog:post_detail', kwargs['post_id'])

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={
                'pk': self.kwargs['post_id'],
            },
        )


@method_decorator(login_required, name='dispatch')
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        comment = get_object_or_404(Comment, pk=kwargs['pk'])

        if comment.author != user and not user.is_superuser:
            return redirect('blog:post_detail', kwargs['pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={
                'pk': self.kwargs['post_id'],
            },
        )


class PostListView(BasePostQueryMixin, ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        return self.get_base_post_queryset()


class PostDetailView(BasePostQueryMixin, DetailView):
    model = Post
    paginate_comments_by = 10

    def get_queryset(self):
        user = self.request.user
        base_queryset = self.get_base_post_queryset()

        if user.is_authenticated:
            author_posts = Post.objects.filter(author=user).select_related(
                'author', 'location', 'category'
            ).prefetch_related('comment_set')
            return (base_queryset | author_posts).distinct()

        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.filter(
            post=self.get_object(),
            is_published=True
        ).select_related('author')
        context['comments'] = comments

        context['form'] = CommentForm()

        return context


class CategoryDetailView(DetailView):
    model = Category
    paginate_posts_by = 10

    def get_queryset(self):
        return self.model.objects.filter(
            is_published=True
        ).prefetch_related('post_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = self.object.post_set.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
        ).select_related('author', 'location', 'category')
        paginator = Paginator(posts, self.paginate_posts_by)

        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        return context


class ProfileDetailView(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'blog/profile.html'
    paginate_posts_by = 10

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = self.object.post_set.all().select_related(
            'author', 'location', 'category').prefetch_related('comment_set')
        paginator = Paginator(posts, self.paginate_posts_by)

        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        return context

