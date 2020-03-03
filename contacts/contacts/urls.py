from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('app.urls')),
    path('admin/', admin.site.urls),
    path('',include('django.contrib.auth.urls'))
    # IDEA: to use these we need to make a folder in our templates DIR
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# Coustomizing admin site
admin.site.site_header = "Contacts"
admin.site.index_title = "Welcome to project"
admin.site.site_title = "Contol Panel"
