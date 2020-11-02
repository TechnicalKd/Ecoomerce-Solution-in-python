from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('App_login.urls')),
    path('Shop',include('App_Shop.urls')),
    path('App_Cart/',include('App_Cart.urls')),
    path('App_payment/',include('App_payment.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)