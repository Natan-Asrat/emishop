from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("emishop/admin/", admin.site.urls),
    path('emishop/api/account/', include('account.urls')),
    path('emishop/api/post/', include('post.urls')),
    path('emishop/api/transaction/', include('transaction.urls')),
    path('emishop/api/notification/', include('notification.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
