from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('oauth', include('social_django.urls', namespace='social')),
    path('about', views.AboutView.as_view(), name='about'),
    path('account', views.AccountView.as_view(), name='account'),
    path('account/edit', views.AccountEditView.as_view(), name='account_edit'),
    path('search', views.SearchResultsView.as_view(), name='search_results'),
    path('bookmarks', views.BookmarkView.as_view(), name='bookmarks'),
    path('register', views.RegisterView.as_view(), name='register')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

