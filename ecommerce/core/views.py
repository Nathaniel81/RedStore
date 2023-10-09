"""
Module: core/views.py

This module contains Django views for handling various functionalities of the web application, including:
- Displaying product listings and details
- User dashboard management (adding, editing, deleting items)
- User profile and authentication
- Messaging and conversations
- User ratings and comments

Each view is documented with its purpose and functionality.
"""


from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import random
from django.contrib.auth import authenticate, login, logout

from .models import User, Category, Item, Conversation, ConversationMessage, Comments, Rating
from .forms import NewItemForm, EditItemForm, SignUpForm, ConversationMessageForm, UserForm


def landing(request):
    """
    Render the landing page with random recent items and categories.
    """

    latest_items = list(Item.objects.filter(is_sold=False).order_by('-created_at')[0:9])

    random.shuffle(latest_items)

    featured = Item.objects.filter(featured=True)
    categories = Category.objects.all()

    context = {
        'items': latest_items,
        'featured': featured,
        'categories': categories
    }

    return render(request, 'core/landing.html', context)

def index(request):
    """
    Render the index page with recent items and categories.
    """

    items = Item.objects.filter(is_sold=False).order_by('-created_at')[0:6]
    featured = Item.objects.filter(featured=True)
    categories = Category.objects.all()

    context = {
	    'items':items,
	    'featured': featured,
	    'categories':categories
	}

    return render(request, 'core/index.html', context)

def products(request):
    """
    Display a list of products based on search query and category filter.
    """

    query = request.GET.get('query', '')
    items = Item.objects.filter(is_sold=False).order_by('-created_at')
    categories = Category.objects.all()
    selected_category_name = 'All Items'
    category_id = request.GET.get('category', 0)
    
    if category_id:
        items = Item.objects.filter(category_id=category_id)
        category = Category.objects.get(pk=category_id)
        selected_category_name = category.name
    if query:
        items = Item.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(created_by__username__icontains=query)
            )
    
    items_per_page = 15
    page_number = request.GET.get('page', 1)
    p = Paginator(items, items_per_page)
    
    try:
        page = p.page(page_number)
    except EmptyPage:
        page = p.page(1)

    context = {
        'items': page,
        'query': query,
        'categories': categories,
        'selected_category_name': selected_category_name,
        'category_id': category_id,
    }
    
    return render(request, 'core/products.html', context)

def detail(request, pk):
    """
    Display the details of a product and related items.
    """

    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    items = Item.objects.filter(category=item.category, is_sold=False)[4:]

    context = {
	    'item':item,
	    'related_items':related_items,
	    'items':items
	}

    return render(request, 'core/detail.html', context)

@login_required
def dashboard(request):
    """
    Display the user's dashboard with their items.
    """

    items = Item.objects.filter(created_by=request.user).order_by('-created_at')
    query = request.GET.get('query', '')
    selected_category_name = 'My Items'
    
    categories = Category.objects.all()
    category_id = request.GET.get('category', 0)
    
    if category_id:
        items = Item.objects.filter(category_id=category_id)
        category = Category.objects.get(pk=category_id)
        selected_category_name = category.name
    if query:
        items = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    items_per_page = 12
    page_number = request.GET.get('page', 1)
    p = Paginator(items, items_per_page)
    
    try:
        page = p.page(page_number)
    except EmptyPage:
        page = p.page(1)

    context = {
        'items': page,
        'query': query,
        'categories': categories,
        'selected_category_name': selected_category_name,
        'category_id': category_id,
    }

    return render(request, 'core/dashboard.html', context)

@login_required
def new(request):
    """
    Create a new item listing.
    """

    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('core:detail', pk=item.id)
    else:
        form = NewItemForm()
    
    context = {'form':form}

    return render(request, 'core/item-form.html', context)
      
@login_required
def edit(request, pk):
    """
    Edit an existing item listing.
    """
    name = 'Edit Item'
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('core:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    
    context = {'form': form, 'pk':pk, 'name': name}
    
    return render(request, 'core/item-form.html', context)

@login_required
def delete(request, pk):
    """
    Delete an item listing.
    """

    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('core:home')
    
    return render(request, 'core/confirmation.html', {'item': item})

def loginPage(request):
    """
    Render the login page and authenticate user.
    """

    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {}

    return render(request, 'core/login.html', context)

# def loginPage(request):
#     if request.user.is_authenticated:
#         return redirect('/')

#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         print(form.errors)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             password = form.cleaned_data['password']
#             # username = request.POST.get('name').lower()
#             # password = request.POST.get('password')

#             user = authenticate(request, name=name, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('index')
#             else:
#                 messages.error(request, 'Username or password is incorrect')
#         else:
#             messages.error(request, 'Invalid form data. Please check the fields.')

#     else:
#         form = LoginForm()

#     context = {'form': form}
#     return render(request, 'core/login.html', context)

def logoutUser(request):
    """
    Log out the user and redirect to the home page.
    """

    logout(request)
    return redirect('/')

def signup(request):
    """
    Handle user registration and redirect to the home page upon success.
    """

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = SignUpForm()

    context = {'form':form}

    return render(request, 'core/signup.html', context)

def userProfile(request, pk):
    """
    Display user profile and their comments.
    """

    user = User.objects.get(id=pk)
    comments = Comments.objects.filter(seller=user)
    context = {'user':user, 'comments':comments}
    
    return render(request, 'core/profile.html', context)

@login_required
def updateUser(request):
    """
    Update user profile information.
    """

    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('core:profile', pk=user.id)

    return render(request, 'core/update-user.html', {'form': form})

@login_required
def rate_and_comment(request, pk):
    """
    Allow users to rate and comment on other users profiles.
    """

    user = get_object_or_404(User, id=pk)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment_text = request.POST.get('body')
        
        if request.user == user:
            return redirect('core:profile', pk=pk)
        
        existing_rating = Rating.objects.filter(user=user, created_by=request.user).first()
        if existing_rating:
            existing_rating.rating = rating
            existing_rating.save()
        else:
            rating_instance = Rating.objects.create(user=user, rating=rating, created_by=request.user)
        
        existing_comment = Comments.objects.filter(seller=user, created_by=request.user).first()
        if existing_comment:
            existing_comment.body = comment_text
            existing_comment.save()
        else:
            comment = Comments.objects.create(seller=user, created_by=request.user, body=comment_text)
        
        user.update_total_ratings()
  
    return redirect('core:profile', pk=user.id)

@login_required
def new_conversation(request, item_pk):
    """
    Create a new conversation for an item and redirect to it.
    """

    item = get_object_or_404(Item, pk=item_pk)
    if item.created_by == request.user:
        return redirect('core:dashboard')
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('core:convo-detail', pk=conversations.first().id)
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()
            
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            conv_id = conversation_message.id

            return redirect('core:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'core/new-convo.html', {
        'form': form
    })


@login_required
def inbox(request):
    """
    Display the user's inbox with conversations.
    """

    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'core/inbox.html', {
        'conversations': conversations
    })

@login_required
def messageDetail(request, pk):
    """
    Display the details of a conversation and allow sending messages.
    """

    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('core:convo-detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'core/message-detail.html', {
        'conversation': conversation,
        'form': form
    })

def deleteComment(request, pk):
    """
    Delete a user comment and redirect to their profile.
    """

    comment = get_object_or_404(Comments, pk=pk)
    comment.delete()
    return redirect('core:profile', comment.seller.id)
    
    
def about(request):
    """
    Render the About page.
    """

    return render(request, 'core/about.html')
