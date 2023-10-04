"""
Module: core/urls.py

This module defines URL patterns for the core app, mapping each view to a specific URL route.

- '': Landing page displaying featured items.
- 'home/': Home page displaying recent items.
- 'products/': Page for browsing and searching products.
- 'detail/<str:pk>/': Product detail page.
- 'dashboard/': User's dashboard for managing their items.
- 'new-item/': Form for adding a new item.
- 'edit-item/<str:pk>/': Form for editing an existing item.
- 'delete-item/<str:pk>/': Confirmation page for deleting an item.
- 'profile/<str:pk>': User profile page.
- 'rate_and_comment/<str:pk>': Page for rating and commenting on a user's profile.
- 'edit-profile/': Form for editing the user's profile.
- 'delete-comment/<str:pk>': Confirmation page for deleting a comment.
- 'login/': User login page.
- 'logout/': User logout page.
- 'signup/': User registration page.
- 'inbox/': User's inbox for messages and conversations.
- 'messages/<str:pk>/': Page for viewing a conversation and sending messages.
- 'new-convo/<int:item_pk>/': Page for starting a new conversation related to an item.
- 'about/': About page providing information about the application.

Each URL pattern is mapped to a specific view from the 'core/views.py' module.
"""


from django.contrib.auth import views as auth_view
from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.index, name='home'),

    path('products/', views.products, name='products'),
    path('detail/<str:pk>/', views.detail, name='detail'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('new-item/', views.new, name='new'),
    path('edit-item/<str:pk>/', views.edit, name='edit'),
    path('delete-item/<str:pk>/', views.delete, name='delete'),

    path('profile/<str:pk>', views.userProfile, name='profile'),
    path('rate_and_comment/<str:pk>', views.rate_and_comment, name='rate-comment'),
    path('edit-profile/', views.updateUser, name='edit-profile'),
    path('delete-comment/<str:pk>', views.deleteComment, name='delete-comment'),

    # path('login/', auth_view.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    # path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    path('inbox/', views.inbox, name='inbox'),
    path('messages/<str:pk>/', views.messageDetail, name='convo-detail'),
    path('new-convo/<int:item_pk>/', views.new_conversation, name='new-convo'),

    path('about/', views.about, name='about'),
]
