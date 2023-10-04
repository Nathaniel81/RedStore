"""
Module: core.models

This module defines custom models used in the RedStore.
"""


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class EthiopianPhoneNumberField(models.CharField):
    """
    Custom field for Ethiopian phone numbers.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 13
        kwargs['validators'] = [
            RegexValidator(
                regex=r'^\+251[79]\d{8}$',
                message="Phone number must start with '+251', followed by either '9' or '7', and then 8 additional digits."
            ),
        ]
        super().__init__(*args, **kwargs)

class User(AbstractUser):
    """
    Custom User model with additional fields.
    """

    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    
    # Social media links
    instagram = models.CharField(max_length=50, blank=True)
    facebook = models.CharField(max_length=50, blank=True)
    whatsup = models.CharField(max_length=50, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    
    total_ratings = models.PositiveIntegerField(default=0)
    total_rating_points = models.PositiveIntegerField(default=0)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def calculate_average_rating(self):
        """
        Calculate the average rating for the user.
        """

        if self.total_ratings > 0:
            return self.total_rating_points / self.total_ratings
        else:
            return 0

    def update_total_ratings(self):
        """
        Update total ratings and rating points for the user.
        """

        ratings = Rating.objects.filter(user=self)
        self.total_ratings = ratings.count()
        self.total_rating_points = sum(rating.rating for rating in ratings)
        self.save()

class Comments(models.Model):
    """
    Comments model for user interactions.
    """

    seller = models.ForeignKey(User, related_name='seller', on_delete=models.CASCADE) 
    created_by = models.ForeignKey(User, related_name='buyers', on_delete=models.CASCADE)
    body = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Comments'

class Rating(models.Model):
    """
    Rating model for user ratings.
    """

    user = models.ForeignKey(User, related_name='received_ratings', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='rated_by', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    """
    Category model for item categorization.
    """

    name = models.CharField(max_length=255)
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

class Item(models.Model):
    """
    Item model for listing products.
    """

    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    featured = models.BooleanField(default=False)
    exclusive = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='item_images', blank=True, null=True)
    image2 = models.ImageField(upload_to='item_images', blank=True, null=True)
    image3 = models.ImageField(upload_to='item_images', blank=True, null=True)
    image4 = models.ImageField(upload_to='item_images', blank=True, null=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL1(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url

    @property
    def imageURL2(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url

    @property
    def imageURL3(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url

    @property
    def imageURL4(self):
        try:
            url = self.image4.url
        except:
            url = ''
        return url

class Conversation(models.Model):
    """
    Conversation model for user interactions.
    """

    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-modified_at',)
        
class ConversationMessage(models.Model):
    """
    ConversationMessage model for messages in conversations.
    """

    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at =  models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)

class Testimonial(models.Model):
    """
    Testimonial model for user testimonials.
    """

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
