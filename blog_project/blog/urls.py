from django.urls import path,re_path
from . import views
from .views import UpdatePostView

app_name ="blog"
urlpatterns = [

    #blogs
    path('', views.blogs, name="blogs"),
    path('draft/', views.blogs_draft, name="blog_draft"),
    path('publish/<slug:slug>/', views.publish_blog, name='publish'),
    path("blog/<slug:slug>/", views.blogs_detail, name="blog_detail"),
    path("blog_add/", views.blog_add, name="blog_add"),
    path("blog_edit/<slug:slug>/", UpdatePostView.as_view(), name="blog_edit"),
    path("blog_delete/<slug:slug>/", views.blog_delete, name="blog_delete"),
    path("blog_search/", views.blog_search, name="blog_search"),
    path('recent', views.blog_random_post, name="blog_random_post"),
    path('comment/<int:comment_id>/add_reply/', views.reply_comment, name='add_reply'),
    path('love_post/<slug:slug>/', views.react_love_post, name='love_post'),
    path('blog_most_view/', views.most_view_post, name="most_view_post"),
    path('blog_most_loved/', views.most_loved_post, name="most_loved_post"),
    path('blog_most_comment/', views.most_comment_post, name="most_comment_post"),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    #user 
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("profile/<int:user_id>/", views.profile_user, name="profile"),
    path('edit_profile/', views.save_profile, name='save_profile'),
    path('user_posts/<int:user_id>/', views.user_posts, name='user_posts'),
]