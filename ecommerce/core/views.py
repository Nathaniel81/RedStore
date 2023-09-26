from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from .models import User, Category, Item, Conversation, ConversationMessage, Comments, Rating
from .forms import NewItemForm, EditItemForm, SignUpForm, ConversationMessageForm, UserForm


def landing(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    context = {
		'items':items,
		'categories':categories
	}
    return render(request, 'core/landing.html', context)


def index(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()
    context = {
		'items':items,
		'categories':categories
	}
    return render(request, 'core/index.html', context)

def contact(request):
    return render(request, 'core/contact.html')

def products(request):
    query = request.GET.get('query', '')
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()
    selected_category_name = 'All Items'
    category_id = request.GET.get('category', 0)
    
    if category_id:
        items = Item.objects.filter(category_id=category_id)
        category = Category.objects.get(pk=category_id)
        selected_category_name = category.name
    if query:
        items = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
    context = {'items':items, 'query':query, 'categories':categories, 'selected_category_name': selected_category_name, 'category_id':category_id}
    
    return render(request, 'core/products.html', context)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    context = {
		'item':item,
		'related_items':related_items
	}
    return render(request, 'core/detail.html', context)

@login_required
def dashboard(request):
    items = Item.objects.filter(created_by=request.user)
    selected_category_name = 'My Items'

    context = {'items': items, 'selected_category_name':selected_category_name}

    return render(request, 'core/dashboard.html', context)

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('detail', pk=item.id)
    else:
        form = NewItemForm()
    
    context = {'form':form}

    return render(request, 'core/item-form.html', context)
      
@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    
    context = {'form': form, 'pk':pk}
    
    return render(request, 'core/item-form.html', context)

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect('/')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')

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
            return redirect('home')
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
    logout(request)
    return redirect('/')

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    context = {'form':form}

    return render(request, 'core/signup.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    comments = Comments.objects.filter(seller=user)
    context = {'user':user, 'comments':comments}
    
    return render(request, 'core/profile.html', context)

@login_required
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    return render(request, 'core/update-user.html', {'form': form})

@login_required
def rate_and_comment(request, pk):
    user = get_object_or_404(User, id=pk)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment_text = request.POST.get('body')
        
        if request.user == user:
            return redirect('profile', pk=pk)
        
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
  
    return redirect('profile', pk=user.id)


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    if item.created_by == request.user:
        return redirect('dashboard')
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('convo-detail', pk=conversations.first().id)
    
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

            return redirect('detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'core/new-convo.html', {
        'form': form
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'core/inbox.html', {
        'conversations': conversations
    })

@login_required
def messageDetail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('convo-detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'core/message-detail.html', {
        'conversation': conversation,
        'form': form
    })
