from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from catalog.forms import ProductForm, UserQuestionForm, HarvestForm
from catalog.models import Category, Product, CompanyContact, UserQuestion, Harvest


class ProductListView(ListView):
    model = Product

    def get_context_data(self):
        data = []
        categories = Category.objects.all()
        print(self.request.user.has_perm('catalog.can_moderate'))
        for category in categories:
            products = Product.objects.filter(category=category.pk)
            if not self.request.user.is_authenticated:
                products = products.filter(is_published=True)
            elif not self.request.user.has_perm('catalog.can_moderate'):
                products = products.filter(owner=self.request.user) | products.filter(is_published=True)
            data.append({
                'category': category,
                'products': products
            })
        data = sorted(data, key=lambda item: item['category'].pk)
        return {'data': data}


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def get_form(self, form_class=None):
        form = super().get_form()
        if not self.request.user.has_perm('catalog.can_moderate'):
            form.fields['is_published'].disabled = True
        return form

    def get_success_url(self):
        return reverse('catalog:view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        new_product = form.save(commit=False)
        new_product.owner = self.request.user
        new_product.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_form(self, form_class=None):
        form = super().get_form()
        if self.request.user.has_perm('catalog.can_moderate'):
            form.fields['name'].disabled = True
            form.fields['image'].disabled = True
            form.fields['price'].disabled = True
        else:
            form.fields['is_published'].disabled = True
        return form

    def test_func(self):
        pk = int(self.request.path.split('/')[-1])
        is_author = Product.objects.get(pk=pk).owner == self.request.user
        can_moderate = self.request.user.has_perm('catalog.can_moderate')
        return is_author or can_moderate

    def get_success_url(self):
        return reverse_lazy('catalog:view', args=[self.kwargs['pk']])


class UserQuestionCreateView(CreateView):
    model = UserQuestion
    form_class = UserQuestionForm
    # company_contacts = CompanyContact.objects.all()
    # company_contacts = sorted(company_contacts, key=lambda item: item.pk)
    # extra_context = {'cont': company_contacts}
    success_url = reverse_lazy('catalog:contact')


class HarvestCreateView(CreateView):
    model = Harvest
    form_class = HarvestForm

    def get_success_url(self):
        return reverse('catalog:view', args=[self.kwargs['product_pk']])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['product'] = Product.objects.get(pk=self.kwargs['product_pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['product'] = Product.objects.get(pk=self.kwargs['product_pk'])
        return context


class HarvestUpdateView(UpdateView):
    model = Harvest
    form_class = HarvestForm

    def get_success_url(self):
        return reverse_lazy('catalog:view', args=[self.object.product.pk])
