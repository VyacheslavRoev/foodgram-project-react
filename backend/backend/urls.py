from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# api = [
#     path('', include('recipes.urls', namespace='recipes')),
#     path('', include('users.urls', namespace='users')),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recipes.urls', namespace='recipes')),
    path('api/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
