from django.contrib import admin
from django.urls import include, path 
from .views import train_list, cases_list, case_detail

app_name = 'train'
urlpatterns = [
    path('', train_list, name='train_list'),
    path('train/<int:train_id>/', cases_list, name='cases_list'),
    path('case/<int:case_id>/', case_detail, name='case_detail'),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    # path('group/<slug:slug>/', group_posts, name='group_list'),
    # path('profile/<str:username>/', views.profile, name='profile'),
    # path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # path('create/', views.post_create, name='post_create'),
    # path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    # path('posts/<int:post_id>/comment/',
    #      views.add_comment, name='add_comment'),
    # path('follow/', views.follow_index, name='follow_index'),
    # path('profile/<str:username>/follow/',
    #      views.profile_follow,
    #      name='profile_follow'),
    # path('profile/<str:username>/unfollow/',
    #      views.profile_unfollow,
    #      name='profile_unfollow'),
]