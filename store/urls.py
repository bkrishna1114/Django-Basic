from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter,SimpleRouter

router = DefaultRouter()
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)


urlpatterns = [
    path('',include(router.urls)),
    # path('products/',views.ProductList.as_view(),name='products'),
    # path('products/<int:id>',views.ProductDetails.as_view(),name='products_details'),
    # path('collections/',views.CollectionDetails.as_view(),name='collections'),
    # path('collections/<int:id>',views.CollectionDetails.as_view(),name='collection-detail'),
]