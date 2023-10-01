from django.contrib.auth import views as auth_view
from django.urls import path

from . import views

# app_name = 'core'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.index, name='home'),
    path('products/', views.products, name='products'),
    path('detail/<str:pk>/', views.detail, name='detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new-item/', views.new, name='new'),
    path('edit-item/<str:pk>/', views.edit, name='edit'),
    path('delete-item/<str:pk>/', views.delete, name='delete'),
    path('contact/', views.contact, name='contact'),
    path('profile/<str:pk>', views.userProfile, name='profile'),
    path('rate_and_comment/<str:pk>', views.rate_and_comment, name='rate-comment'),
    path('edit-profile/', views.updateUser, name='edit-profile'),
    # path('login/', auth_view.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    # path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('inbox/', views.inbox, name='inbox'),
    path('messages/<str:pk>/', views.messageDetail, name='convo-detail'),
    path('new-convo/<int:item_pk>/', views.new_conversation, name='new-convo'),
    path('about/', views.about, name='about'),
    path('delete-comment/<str:pk>', views.deleteComment, name='delete-comment')
]