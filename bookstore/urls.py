
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Language switching
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('accounts', include('books.urls')),
    path('accounts/', include('books.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # Includes all auth URLs
)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('books.urls')),
#     path('accounts', include('books.urls')),
#     path('accounts/', include('books.urls')),
#     path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
#     path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('accounts/', include('django.contrib.auth.urls')),  # Includes all auth URLs
# ]