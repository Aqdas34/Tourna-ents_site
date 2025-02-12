from django.contrib import admin
from django.urls import path
from tournaments import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('',views.home_view,name="homepage"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.tournament_list, name='dashboard'),
    
    # URL to add a new tournament
    path('add/', views.add_tournament, name='add_tournament'),
    
    # URL to update an existing tournament (using its id)
    path('update/<int:tournament_id>/', views.update_tournament, name='update_tournament'),
    
    # URL to delete a tournament (using its id)
    path('delete/<int:tournament_id>/', views.delete_tournament, name='delete_tournament'),
    path('tournament/<int:tournament_id>/', views.tournament_details, name='tournament_details'),

    path('addAR/', views.add_virtual_assistant, name='add_virtual_assistant'),
    path('list/', views.virtual_assistant_list, name='virtual_assistant_list'),
    path('edit/<int:pk>/', views.edit_virtual_assistant, name='edit_virtual_assistant'),
    path('deleteAR/<int:pk>/', views.delete_virtual_assistant, name='delete_virtual_assistant'),

    
    # Banners Url 
    path('banner/', views.view_banners, name='banner_list'),
    path('add-banner/',views.add_banners,name='add_banner'),
    path('delete-banner/<int:banner_id>/', views.delete_banner, name='delete_banner'),
    # path('admin/', admin.site.urls),

    # path('tournaments/', views.tournament_list, name='tournament_list'),
    # path('register/', views.register, name='register'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
