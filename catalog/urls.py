from django.urls import path

from . import views
from .views import marks_filter

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<id>/<slug>/', views.product_detail, name='product_detail'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('marks_filter/', marks_filter, name='marks_filter'),

]
