from django.urls import path
from .views import CSVUploadView, UploadHistoryView

urlpatterns = [
    path('upload/', CSVUploadView.as_view(), name='csv-upload'),
    path('history/', UploadHistoryView.as_view(), name='upload-history'),
    path('report/<int:pk>/', GeneratePDFView.as_view(), name="report-pdf"),
]
