from django.contrib import admin
from .models import Category, Item, Conversation, ConversationMessage, User, Comments, Rating

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Comments)
admin.site.register(Rating)
admin.site.register(Conversation)
admin.site.register(ConversationMessage)
