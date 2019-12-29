
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView  # new

urlpatterns = [
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
    # path('', TemplateView.as_view(template_name='index.html'), name='catalog_home'),
    path('admin/', admin.site.urls),
]


# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

# add static files directories to the path
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
