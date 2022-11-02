from django.urls import path

from .views import *

urlpatterns = [
    path('', AnnouncementList.as_view(), name='ann_list'),
    path('<int:pk>/', AnnouncementDetail.as_view(), name='ann_detail'),
    path('category/<int:pk>/', AnnCategoryList.as_view(), name='category'),
    path('create/', AnnouncementCreate.as_view(), name='ann_create'),
    path('about/', about_us, name='about'),
    path('myanns/', MyAnnouncement.as_view(), name='my_anns'),
    path('myanndetail/<int:pk>/', my_ann_detail, name='my_ann_detail'),
    path('delete/<int:pk>/', AnnounceDelete.as_view(), name='ann_delete'),
    path('update/<int:pk>/', AnnounceUpdate.as_view(), name='ann_update'),
    path('respond/<int:pk>/', RespondStatus.as_view(), name='res_status'),
    path('respond/<int:pk>/accept', respond_accept, name='res_accept'),
    path('respond/<int:pk>/remove/', respond_remove, name='res_remove'),
]
