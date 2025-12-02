from django.urls import path
from hardware.views import *

urlpatterns = [
    path('create_collection_api/', create_collection),
    path('get_collection_list_api/', get_collection_list),
    path('delete_collection_api/', delete_collection),
]

