"""
Project Test Cases Module

This module contains comprehensive test cases for various components of the project, including models, views, and forms. These test cases are designed to ensure the correctness, reliability, and robustness of the project's functionality.

Test Suites:
-------------
- Model Tests: Validate the behavior of project models, including User, Comments, Rating, Category, Item, Conversation, and ConversationMessage.
- View Tests: Examine the behavior of project views, covering endpoints such as products, detail, new, edit, delete, login, logout, signup, rate_and_comment, userProfile, updateUser, new_conversation, inbox, and messageDetail.
- Form Tests: Verify the correctness of project forms, including SignUpForm, UserForm, NewItemForm, EditItemForm, and ConversationMessageForm.

These tests serve as a crucial part of the development process, helping maintain code quality and ensuring that the project functions as intended.

"""


from django.test import TestCase
from django.urls import reverse

from .models import User, Rating, Category, Item, Comments, Conversation, ConversationMessage
from .forms import SignUpForm, UserForm, NewItemForm, EditItemForm, ConversationMessageForm

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.rating1 = Rating.objects.create(user=self.user, rating=5)
        self.rating2 = Rating.objects.create(user=self.user, rating=4)

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_calculate_average_rating(self):
        average_rating = self.user.calculate_average_rating()
        self.assertEqual(average_rating, 4.5)

    def test_update_total_ratings(self):
        self.user.update_total_ratings()
        self.assertEqual(self.user.total_ratings, 2)
        self.assertEqual(self.user.total_rating_points, 9)

class CommentsModelTestCase(TestCase):
    def setUp(self):
        self.seller_user = User.objects.create(username='seller', email='seller@example.com')
        self.buyer_user = User.objects.create(username='buyer', email='buyer@example.com')
        self.comment = Comments.objects.create(seller=self.seller_user, created_by=self.buyer_user, body='Test Comment')

    def test_comments_creation(self):
        self.assertEqual(self.comment.seller, self.seller_user)
        self.assertEqual(self.comment.created_by, self.buyer_user)
        self.assertEqual(self.comment.body, 'Test Comment')

class RatingModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', email='user1@example.com')
        self.user2 = User.objects.create(username='user2', email='user2@example.com')
        self.rating = Rating.objects.create(user=self.user1, created_by=self.user2, rating=4)

    def test_rating_creation(self):
        self.assertEqual(self.rating.user, self.user1)
        self.assertEqual(self.rating.created_by, self.user2)
        self.assertEqual(self.rating.rating, 4)

class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')

class ItemModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        category = Category.objects.create(name='Test Category')
        self.item = Item.objects.create(
            category=category,
            name='Test Item',
            description='This is a test item',
            price=10.99,
            created_by=user,
            image1='item_images/test_image1.jpg',
            image2='item_images/test_image2.jpg',
        )

    def test_item_creation(self):
        self.assertEqual(self.item.name, 'Test Item')
        self.assertEqual(self.item.description, 'This is a test item')
        self.assertEqual(self.item.price, 10.99)
        self.assertEqual(self.item.created_by.username, 'testuser')

    def test_image_urls(self):
        self.assertEqual(self.item.imageURL1, 'item_images/test_image1.jpg')
        self.assertEqual(self.item.imageURL2, 'item_images/test_image2.jpg')

    def test_featured_item(self):
        self.assertFalse(self.item.featured)  # Default value should be False

    def test_exclusive_item(self):
        self.assertFalse(self.item.exclusive)  # Default value should be False

    def test_is_sold_item(self):
        self.assertFalse(self.item.is_sold)  # Default value should be False

class ConversationModelTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1', email='user1@example.com')
        user2 = User.objects.create(username='user2', email='user2@example.com')
        category = Category.objects.create(name='Test Category')
        item = Item.objects.create(
            category=category,
            name='Test Item',
            description='This is a test item',
            price=10.99,
            created_by=user1,
        )
        self.conversation = Conversation.objects.create(item=item)
        self.conversation.members.add(user1, user2)

    def test_conversation_creation(self):
        self.assertEqual(self.conversation.item.name, 'Test Item')
        self.assertEqual(self.conversation.members.count(), 2)

class ConversationMessageModelTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1', email='user1@example.com')
        user2 = User.objects.create(username='user2', email='user2@example.com')
        category = Category.objects.create(name='Test Category')
        item = Item.objects.create(
            category=category,
            name='Test Item',
            description='This is a test item',
            price=10.99,
            created_by=user1,
        )
        conversation = Conversation.objects.create(item=item)
        conversation.members.add(user1, user2)
        self.message = ConversationMessage.objects.create(
            conversation=conversation,
            content='Hello, this is a test message.',
            created_by=user1,
        )

    def test_message_creation(self):
        self.assertEqual(self.message.content, 'Hello, this is a test message.')
        self.assertEqual(self.message.created_by.username, 'user1')

class TestProductsView(TestCase):
    def setUp(self):
        # Create some test categories and items
        self.category1 = Category.objects.create(name="Category 1")
        self.category2 = Category.objects.create(name="Category 2")

        self.item1 = Item.objects.create(
            category=self.category1,
            name="Item 1",
            description="Description 1",
            price=10.0,
        )

        self.item2 = Item.objects.create(
            category=self.category2,
            name="Item 2",
            description="Description 2",
            price=20.0,
        )

    def test_products_view_with_no_query(self):
        # Test the products view with no query parameter
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/products.html')

    def test_products_view_with_query(self):
        # Test the products view with a query parameter
        response = self.client.get(reverse('products'), {'query': 'Item 1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/products.html')

class TestDetailView(TestCase):
    def setUp(self):
        # Create a test category and item
        self.category = Category.objects.create(name="Category 1")
        self.item = Item.objects.create(
            category=self.category,
            name="Item 1",
            description="Description 1",
            price=10.0,
        )

    def test_detail_view(self):
        # Test the detail view for an item
        response = self.client.get(reverse('detail', args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/detail.html')

class TestNewItemView(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_new_item_view_authenticated(self):
        # Test the new item view for an authenticated user
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/item-form.html')

    def test_new_item_view_not_authenticated(self):
        # Test the new item view for a non-authenticated user
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

class TestEditItemView(TestCase):
    def setUp(self):
        # Create a test user and item
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.category = Category.objects.create(name="Category 1")
        self.item = Item.objects.create(
            category=self.category,
            name="Item 1",
            description="Description 1",
            price=10.0,
            created_by=self.user,
        )

    def test_edit_item_view_authenticated(self):
        # Test the edit item view for an authenticated user
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('edit', args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/item-form.html')

    def test_edit_item_view_not_authenticated(self):
        # Test the edit item view for a non-authenticated user
        response = self.client.get(reverse('edit', args=[self.item.pk]))
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

class TestDeleteItemView(TestCase):
    def setUp(self):
        # Create a test user and item
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.category = Category.objects.create(name="Category 1")
        self.item = Item.objects.create(
            category=self.category,
            name="Item 1",
            description="Description 1",
            price=10.0,
            created_by=self.user,
        )

    def test_delete_item_view_authenticated(self):
        # Test the delete item view for an authenticated user
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('delete', args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/confirmation.html')

    def test_delete_item_view_not_authenticated(self):
        # Test the delete item view for a non-authenticated user
        response = self.client.get(reverse('delete', args=[self.item.pk]))
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

class TestRateAndCommentView(TestCase):
    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

    def test_rate_and_comment_view_authenticated_user(self):
        # Test the rate_and_comment view for an authenticated user
        self.client.login(username="user1", password="password1")
        response = self.client.post(reverse('rate_and_comment', args=[self.user2.id]), {'rating': 5, 'body': 'Great user!'})
        self.assertRedirects(response, reverse('profile', args=[self.user2.id]))  # Should redirect to user2's profile
        self.assertEqual(Rating.objects.count(), 1)  # One rating should be created
        self.assertEqual(Comments.objects.count(), 1)  # One comment should be created

    def test_rate_and_comment_view_invalid_user(self):
        # Test the rate_and_comment view for an invalid user
        self.client.login(username="user1", password="password1")
        response = self.client.post(reverse('rate_and_comment', args=[999]), {'rating': 5, 'body': 'Great user!'})
        self.assertEqual(response.status_code, 404)  # User not found, should return 404

    def test_rate_and_comment_view_self_rating(self):
        # Test the rate_and_comment view when a user tries to rate and comment on their own profile
        self.client.login(username="user1", password="password1")
        response = self.client.post(reverse('rate_and_comment', args=[self.user1.id]), {'rating': 5, 'body': 'Great user!'})
        self.assertRedirects(response, reverse('profile', args=[self.user1.id]))  # Should redirect to user1's profile
        self.assertEqual(Rating.objects.count(), 0)  # No rating should be created
        self.assertEqual(Comments.objects.count(), 0)  # No comment should be created

    def test_rate_and_comment_view_existing_rating_and_comment(self):
        # Test the rate_and_comment view when a user updates an existing rating and comment
        self.client.login(username="user1", password="password1")

        # Create an initial rating and comment by user1 for user2
        Rating.objects.create(user=self.user2, rating=3, created_by=self.user1)
        Comments.objects.create(seller=self.user2, created_by=self.user1, body='Average user!')

        response = self.client.post(reverse('rate_and_comment', args=[self.user2.id]), {'rating': 5, 'body': 'Great user!'})
        self.assertRedirects(response, reverse('profile', args=[self.user2.id]))  # Should redirect to user2's profile

        # Check that the rating and comment were updated
        updated_rating = Rating.objects.get(user=self.user2, created_by=self.user1)
        self.assertEqual(updated_rating.rating, 5)
        updated_comment = Comments.objects.get(seller=self.user2, created_by=self.user1)
        self.assertEqual(updated_comment.body, 'Great user!')

class TestNewConversationView(TestCase):
    def setUp(self):
        # Create a test user and item
        self.user = User.objects.create_user(username="testuser", password="password")
        self.item = Item.objects.create(name="Test Item", description="Description", price=10.0, created_by=self.user)

    def test_new_conversation_view_authenticated_user(self):
        # Test the new_conversation view for an authenticated user
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('new_conversation', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)  # Should return a success status code

    def test_new_conversation_view_unauthenticated_user(self):
        # Test the new_conversation view for an unauthenticated user
        response = self.client.get(reverse('new_conversation', args=[self.item.id]))
        self.assertRedirects(response, f'/login/?next=/new_conversation/{self.item.id}/')  # Should redirect to login page


class TestInboxView(TestCase):
    def setUp(self):
        # Create a test user and conversations
        self.user = User.objects.create_user(username="testuser", password="password")
        self.conversation = Conversation.objects.create()
        self.conversation.members.add(self.user)
    
    def test_inbox_view_authenticated_user(self):
        # Test the inbox view for an authenticated user
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)  # Should return a success status code

    def test_inbox_view_unauthenticated_user(self):
        # Test the inbox view for an unauthenticated user
        response = self.client.get(reverse('inbox'))
        self.assertRedirects(response, '/login/?next=/inbox/')  # Should redirect to login page

class TestMessageDetailView(TestCase):
    def setUp(self):
        # Create a test user and conversation
        self.user = User.objects.create_user(username="testuser", password="password")
        self.conversation = Conversation.objects.create()
        self.conversation.members.add(self.user)
    
    def test_message_detail_view_authenticated_user(self):
        # Test the messageDetail view for an authenticated user
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('message_detail', args=[self.conversation.id]))
        self.assertEqual(response.status_code, 200)  # Should return a success status code

    def test_message_detail_view_unauthenticated_user(self):
        # Test the messageDetail view for an unauthenticated user
        response = self.client.get(reverse('message_detail', args=[self.conversation.id]))
        self.assertRedirects(response, f'/login/?next=/message_detail/{self.conversation.id}/')  # Should redirect to login page

class TestSignUpForm(TestCase):
    def test_signup_form_valid_data(self):
        form = SignUpForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_missing_data(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)


class TestUserForm(TestCase):
    def setUp(self):
        # Create a test user for the UserForm
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_user_form_valid_data(self):
        form = UserForm(instance=self.user, data={
            'name': 'Test Name',
            'email': 'test@example.com',
            'bio': 'Test bio',
        })
        self.assertTrue(form.is_valid())

    def test_user_form_missing_data(self):
        form = UserForm(instance=self.user, data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('bio', form.errors)

class TestSignUpForm(TestCase):
    def test_signup_form_valid_data(self):
        form = SignUpForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_missing_data(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

class TestUserForm(TestCase):
    def setUp(self):
        # Create a test user for the UserForm
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_user_form_valid_data(self):
        form = UserForm(instance=self.user, data={
            'name': 'Test Name',
            'email': 'test@example.com',
            'bio': 'Test bio',
        })
        self.assertTrue(form.is_valid())

    def test_user_form_missing_data(self):
        form = UserForm(instance=self.user, data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('bio', form.errors)

class TestNewItemForm(TestCase):
    def setUp(self):
        # Create a test user and category for the ItemForm
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.category = Category.objects.create(name="Test Category")

    def test_new_item_form_valid_data(self):
        form = NewItemForm(data={
            'category': self.category.pk,
            'name': 'Test Item',
            'description': 'Test description',
            'price': 10.99,
            'image1': 'path/to/image1.jpg',
            'image2': 'path/to/image2.jpg',
            'image3': 'path/to/image3.jpg',
            'image4': 'path/to/image4.jpg',
        })
        self.assertTrue(form.is_valid())

    def test_new_item_form_missing_data(self):
        form = NewItemForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
        self.assertIn('name', form.errors)
        self.assertIn('description', form.errors)
        self.assertIn('price', form.errors)

class TestEditItemForm(TestCase):
    def setUp(self):
        # Create a test user, category, and item for the EditItemForm
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.category = Category.objects.create(name="Test Category")
        self.item = Item.objects.create(
            category=self.category,
            name="Test Item",
            description="Test description",
            price=10.99,
            created_by=self.user,
        )

    def test_edit_item_form_valid_data(self):
        form = EditItemForm(instance=self.item, data={
            'name': 'Updated Item Name',
            'description': 'Updated description',
            'price': 19.99,
        })
        self.assertTrue(form.is_valid())

    def test_edit_item_form_missing_data(self):
        form = EditItemForm(instance=self.item, data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('price', form.errors)

class TestConversationMessageForm(TestCase):
    def setUp(self):
        # Create test users and an item
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.category = Category.objects.create(name="Test Category")
        self.item = Item.objects.create(
            category=self.category,
            name="Test Item",
            description="Test description",
            price=10.99,
            created_by=self.user1,
        )
        self.conversation = Conversation.objects.create(item=self.item)
        self.conversation.members.add(self.user1, self.user2)

    def test_conversation_message_form_valid_data(self):
        form = ConversationMessageForm(data={
            'content': 'This is a test message.',
        })
        form.instance.conversation = self.conversation
        form.instance.created_by = self.user1
        self.assertTrue(form.is_valid())

    def test_conversation_message_form_missing_content(self):
        form = ConversationMessageForm(data={})
        form.instance.conversation = self.conversation
        form.instance.created_by = self.user1
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
