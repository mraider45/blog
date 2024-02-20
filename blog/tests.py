from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from.models import Post

# Create your tests here.
# view test
class BlogTests(TestCase):
    # using setup method to  sets up a test user and a test post to be used in the subsequent test cases.
    def setup(self):
        self.user = get_user_model.objects.create_user(
            username = 'Testuser',
            email = 'test@gmail.com',
            password = 'secret'
        ) # user
        
        self.post = Post.objects.create(
            title = 'A good title',
            body = 'Nice body content',
            author = self.user,
        ) # post
        
    # This test checks if the string representation of a Post object is equal to its title.
    def test_string_representation(self):
        post = Post(title = 'A sample title')
        self.assertEqual(str(post), post.title)
        
    # This test checks if the title, author, and body of the test post match the expected values.
    def test_post_content(self):
         self.assertEqual(f'{self.post.title}', 'A good title')
         self.assertEqual(f'{self.post.author}', 'testuser')
         self.assertEqual(f'{self.post.body}', 'Nice body content')
         
    # This test checks the behavior of the blog's post list view. 
    # It sends a GET request to the home URL, checks if the response status code is as expected, 
    # verifies that the response contains 'Nice body content', and checks if the correct template is used.
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'home.html')
        
    # This test checks the behavior of the blog's post detail view.
    # It sends GET requests to a specific post URL and a non-existing post URL, checks the response status codes, 
    # verifies that the correct post title is present in the response, and checks if the correct template is used.
    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')
    # verifies    
    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')
        
    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)
        
    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {'title': 'Updated title', 'body': 'Updated text',})
        self.assertEqual(response.status_code, 302)
        
    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {'title': 'New title','body': 'New text','author': self.user,})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')
