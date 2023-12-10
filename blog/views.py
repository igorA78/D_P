from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import BlogForm
from blog.models import Blog


def is_author_or_manager(request):
    pk = int(request.path.split('/')[-1])
    is_author = Blog.objects.get(pk=pk).owner == request.user
    is_content_manager = request.user.has_perm('blog.content_manager')
    return is_author or is_content_manager


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm

    def get_form(self, form_class=None):
        form = super().get_form()
        if not self.request.user.has_perm('blog.content_manager'):
            form.fields['is_published'].disabled = True
        return form

    def get_success_url(self, *args, **kwargs):
        return reverse('blog:detail', args={self.object.pk})

    def form_valid(self, form):
        if form.is_valid:
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.title)
            new_blog.owner = self.request.user
            new_blog.save()

        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        elif not self.request.user.has_perm('blog.content_manager'):
            queryset = queryset.filter(is_published=True) | queryset.filter(owner=self.request.user)
        queryset = queryset.order_by('-created_at', )
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        if self.object.views_count == 100:
            send_mail(
                '100 просмотров',
                f'Статья ({self.object.pk})"{self.object.title}" набрала 100 просмотров.',
                settings.EMAIL_HOST_USER,
                ['a.kolmychek@gmail.com']
            )
        return self.object


class BlogUpdateView(UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm

    def test_func(self):
        return is_author_or_manager(self.request)

    def get_form(self, form_class=None):
        form = super().get_form()
        if not self.request.user.has_perm('blog.content_manager'):
            form.fields['is_published'].disabled = True
        return form

    def get_success_url(self):
        return reverse('blog:detail', args=[self.kwargs['pk']])


class BlogDeleteView(UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')

    def test_func(self):
        return is_author_or_manager(self.request)
