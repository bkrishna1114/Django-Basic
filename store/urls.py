from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter,SimpleRouter #we using the nested defautl router..
from rest_framework_nested import routers
from pprint import pprint

#nested routers..
router = routers.DefaultRouter()
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)

#creating chils routers..
product_router = routers.NestedDefaultRouter(parent_router=router,parent_prefix='products',lookup='product')
product_router.register('reviews',viewset=views.ReviewsViewSet,basename='product-reviews')

urlpatterns = router.urls + product_router.urls  

#normal routers.
# router = DefaultRouter()
# router.register('products',views.ProductViewSet)
# router.register('collections',views.CollectionViewSet)
# router.register('reviews',views.ReviewsViewSet)
# pprint(router.urls) #printing the urls..
#routers.urls

# urlpatterns = [
#     path('',include(router.urls)),
#     # path('products/',views.ProductList.as_view(),name='products'),
#     # path('products/<int:id>',views.ProductDetails.as_view(),name='products_details'),
#     # path('collections/',views.CollectionDetails.as_view(),name='collections'),
#     # path('collections/<int:id>',views.CollectionDetails.as_view(),name='collection-detail'),
# ]
