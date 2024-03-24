from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from core import views
from core.views import index, upload, add_client_info, search_client

app_name = 'core'

urlpatterns = [
    path('', core_views.index, name='index'),
    path('contact/', core_views.contact, name='contact'),
    path('upload/', core_views.upload, name='upload'),
    path('success/', core_views.success_view, name='success'),
    path('generate/', core_views.generate, name='generate'),
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('search_client/', search_client, name='search_client'),
    path('add-client-info/<int:account_number>/', views.add_client_info, name='add_client_info'),
    path('search_client/core/add_client_info.html/<slug:account_number>/', views.add_client_info, name='add_client_info'),
    path('<page_slug>-<page_id>/add_client_info/', views.add_client_info, name='add_client_info'),
    #path('my_view/<int:client_account_id>/', views.my_view, name='my_view'),

    
]

"""path('loan_form/', core_views.populate_excel_view, name='populate_excel')"""
