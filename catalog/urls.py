from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, UserQuestionCreateView, \
    ProductUpdateView, HarvestCreateView, HarvestUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contact/', UserQuestionCreateView.as_view(), name='contact'),
    path('view/<int:pk>', ProductDetailView.as_view(), name='view'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update'),
    path('create_harvest/<int:product_pk>', HarvestCreateView.as_view(), name='create_harvest'),
    path('update_harvest/<int:pk>', HarvestUpdateView.as_view(), name='update_harvest'),
]
