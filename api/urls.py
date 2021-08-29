from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import visited_domains, visited_links

urlpatterns = {
    path('visited_links', visited_links, name='visited-links'),
    path('visited_domains', visited_domains, name='visited-domains'),
}
urlpatterns = format_suffix_patterns(urlpatterns)
