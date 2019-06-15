from django.urls import path

from.import views

urlpatterns = [
    path('',views.index,name='index'),
    path('foodie/',views.foodie,name='foodie'),
    path('foods_detail/<int:id>/<slug:slug>/post_delete/',views.post_delete,name='post_delete'),
    path('foods_detail/<int:id>/<slug:slug>/',views.foods_detail,name='foods_detail'),
    path('like/', views.image_like, name='like'),
]
