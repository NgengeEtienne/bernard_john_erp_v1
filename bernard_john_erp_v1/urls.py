
from django.contrib import admin
from django.urls import path, include
from .settings import BASE_DIR
from user import views
from django.conf.urls.static import static
from django.conf import settings
#from user.utils import login_required_patterns
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('user.urls')),
    path('admin/', admin.site.urls),
    path('login/', RedirectView.as_view(url='/accounts/login/')),  # Redirect to Django's default login
    path('', RedirectView.as_view(url='/login/')),
    
    path('invoice/', include("invoice.urls", namespace='invoice')),
    path('customer/', include('customer.urls', namespace='customer')),
    path('purchases/', include('purchases.urls', namespace='purchases')),
    path('supplier/', include('supplier.urls', namespace='supplier')),
    path('task/', include('task.urls', namespace='task')),
    path("__reload__/", include("django_browser_reload.urls")),

    path('bar/', include("bar.urls", namespace='bar')),
    path('bakery/', include("bakery.urls", namespace='bakery')),
    path('boulangerie/', include("boulangerie.urls", namespace='boulangerie')),
    path('supermarket/', include("supermarket.urls", namespace='supermarket')),
    path('wholesale/', include("wholesale.urls", namespace='wholesale')),
    path('accounting/', include("accounting.urls", namespace='accounting')),
]
#urlpatterns = login_required_patterns(urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=BASE_DIR / 'static')
    urlpatterns += static('/app-assets/', document_root=BASE_DIR / 'app-assets')
