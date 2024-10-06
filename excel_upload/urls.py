from django.urls import path, include
from excel_upload import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('download/', views.download_sample, name='download_sample'),
    path('companies/', views.CompanyList.as_view(), name='company-list'),
    path('filter/', views.filter_view, name='filter_view'),
    path('csv-files/', views.csv_file_list, name='csv_file_list'),
]