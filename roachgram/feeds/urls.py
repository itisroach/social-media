from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("" , views.home , name="home-page"),
    path("post/" , views.post , name="post"),
    path("<int:pk>/like" , views.likePost , name="like-post"),
    path("<int:pk>/bookmark" , views.bookmarkPost , name="bookmark-post")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)