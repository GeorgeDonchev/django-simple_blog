from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView)

# Create your views here.
from my_site.form import PostForm, CommentForm
from my_site.models import Post, Comments


class AboutView(TemplateView):
    template_name = '../templates/my_site/about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    redirect_field_name = 'my_site/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'my_site/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    # login_url = '/login'
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'my_site/post_list'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('created_date')


@login_required
def add_comment_to_post(req, pk):
    post = get_object_or_404(Post, pk=pk)
    if req.method == 'POST':
        form = CommentForm(req.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = CommentForm()
    return render(req, 'my_site/comment_form.html', {'form':form})


@login_required
def comment_approve(req, pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.approve()
    return redirect('post_detail', pk =comment.post.pk)


@login_required
def comment_remove(req, pk):
    comment = get_object_or_404(Comments, pk= pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


@login_required
def post_publish(req, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk = pk)



