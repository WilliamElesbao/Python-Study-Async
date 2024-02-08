from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('flashcard/', include('flashcard.urls')),
    path('books/', include('books.urls')),
    path('', lambda requests: redirect('/flashcard/new_flashcard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
