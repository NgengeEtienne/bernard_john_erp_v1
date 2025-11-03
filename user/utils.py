# user/utils.py
from django.contrib.auth.decorators import login_required
from django.urls import URLPattern, URLResolver

def login_required_patterns(urlpatterns):
    secured_urlpatterns = []
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            secured_urlpatterns.append(URLPattern(pattern.pattern, login_required(pattern.callback), name=pattern.name))
        elif isinstance(pattern, URLResolver):
            secured_urlpatterns.append(URLResolver(pattern.pattern, login_required_patterns(pattern.url_patterns), namespace=pattern.namespace))
        else:
            secured_urlpatterns.append(pattern)
    return secured_urlpatterns
