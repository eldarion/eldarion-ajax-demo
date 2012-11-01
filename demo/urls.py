from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns("",
    url(r"^$", "demo.views.home", name="home"),
    url(r"^tasks/(?P<pk>\d+)/done/$", "demo.views.mark_done", name="task_mark_done"),
    url(r"^tasks/(?P<pk>\d+)/undone/$", "demo.views.mark_undone", name="task_mark_undone"),
    url(r"^tasks/completed/$", "demo.views.complete_count_fragment", name="task_complete_count_fragment"),
    url(r"^tasks/add/$", "demo.views.add", name="task_add"),
    url(r"^tasks/(?P<pk>\d+)/delete/$", "demo.views.delete", name="task_delete"),
    
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
