from django.urls import path
from .views import cart,store,checkout,update_cart,processorder
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('store/',store,name='store'),
    path('checkout/',checkout,name='checkout'),
    path('cart/',cart,name='cart'),
    path('update-cart/',update_cart,name='update-cart'),
    path('process-order/',processorder,name='process-order'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




