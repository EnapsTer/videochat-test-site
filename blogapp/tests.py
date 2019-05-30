# """test.py"""
# from django.test import TestCase
# from django.test import SimpleTestCase
# from blogapp.forms import *
# from .models import *
# from django.urls import reverse
# 
# 
# class LogInTest(TestCase):
#     """login test 1"""
#     def setUp(self):
#         """test"""
#         self.credentials = {
#             'username': 'testuser',
#             'password': 'secret'}
#         User.objects.create_user(**self.credentials)
# 
#     def test_login(self):
#         """test 2"""
#         # send login data
#         response = self.client.post('/login/', self.credentials, follow=True)
#         # should be logged in now
#         self.assertTrue(response.context['user'].is_active)
# 
# 
# class FormsTest(TestCase):
#     """forms test"""
#     def PostCreateFormTest(self):
#         """test 3"""
#         form = forms.PostCreateForm(title='qwerty',
#                                     private=True,
#                                     body='')
#         self.assertTrue(form.is_valid())
# 
#     def PostEditFormTest(self):
#         """test 4"""
#         form = forms.PostCreateForm(title='qwerty',
#                                     private=True,
#                                     body='')
#         self.assertTrue(form.is_valid())
# 
#     def UserLoginFormTest(self):
#         """test 5"""
#         form = forms.PostCreateForm(username='test',
#                                     password='test')
#         self.assertTrue(form.is_valid())
# 
#     def UserRegistrationFormTest(self):
#         """test 6"""
#         form = forms.PostCreateForm(username='test',
#                                     password='test',
#                                     first_name='test',
#                                     last_name='test',
#                                     confirm_password='test',
#                                     email='test@test.com')
#         self.assertTrue(form.is_valid())
# 
#     def UserEditFormTest(self):
#         """test 7"""
#         form = forms.PostCreateForm(username='test',
#                                     password='test',
#                                     first_name='test',
#                                     last_name='test',
#                                     email='test@test.com')
#         self.assertTrue(form.is_valid())
# 
#     def CommentFormTest(self):
#         """test 8"""
#         form = forms.PostCreateForm(content='testtsetsetset')
#         self.assertTrue(form.is_valid())
# 
#     def UserFormTest(self):
#         """test 9"""
#         form = forms.UserForm(username='user',
#                               first_name='ivan',
#                               last_name='ivanov',
#                               email='email@mail.ru')
#         self.assertTrue(form.is_valid())
# 
#     def ProfileFormTest(self):
#         """test 10"""
#         form = ProfileForm(country='Russia',
#                            contacts='89993332244',
#                            image='media/avatar.jpg')
#         self.assertTrue(form.is_valid())
# 
# 
# class TestSignup(TestCase):
#     """register test"""
#     def setUp(self):
#         """test 11"""
#         pass
# 
#     def test_signup_fire(self):
#         """test 12"""
#         self.driver.get("https://talkhub.herokuapp.com/")
#         self.driver.find_element_by_id('id_title').send_keys("test title")
#         self.driver.find_element_by_id('id_body').send_keys("test body")
#         self.driver.find_element_by_id('submit').click()
#         self.assertIn("https://talkhub.herokuapp.com/", self.driver.current_url)
# 
#     def tearDown(self):
#         """test 13"""
#         self.driver.quit
# 
# 
# class HomePageTests(SimpleTestCase):
#     """main page test"""
#     def test_home_page_status_code(self):
#         """test 14"""
#         response = self.client.get('/')
#         self.assertEquals(response.status_code, 200)
# 
#     def test_view_url_by_name(self):
#         """test 15"""
#         response = self.client.get(reverse('home'))
#         self.assertEquals(response.status_code, 200)
# 
#     def test_view_uses_correct_template(self):
#         """test 16"""
#         response = self.client.get(reverse('home'))
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'base.html')
# 
#     def test_home_page_contains_correct_html(self):
#         """test 17"""
#         response = self.client.get('/')
#         self.assertContains(response, '<h1>Homepage</h1>')
# 
#     def test_home_page_does_not_contain_incorrect_html(self):
#         """test 18"""
#         response = self.client.get('/')
#         self.assertNotContains(
#             response, 'Hi there! I should not be on the page.')
# 
# 
# class ChatPageTests(SimpleTestCase):
#     """chat page test"""
# 
#     def delete_post_test(self):
#         """test 19"""
#         self.driver.get("https://talkhub.herokuapp.com/")
#         self.driver.find_element_by_id('delete').click()
#         self.assertIn("https://talkhub.herokuapp.com/", self.driver.current_url)
# 
#     def edit_post_test(self):
#         """test 20"""
#         self.driver.get("https://talkhub.herokuapp.com/")
#         self.driver.find_element_by_id('edit-post').click()
#         self.assertIn("https://talkhub.herokuapp.com/", self.driver.current_url)
# 
#     def like_post_test(self):
#         """test 21"""
#         self.driver.get("https://talkhub.herokuapp.com/")
#         self.driver.find_element_by_id('like').click()
#         self.assertIn("https://talkhub.herokuapp.com/", self.driver.current_url)
# 
#     def delete_comment_test(self):
#         """test 22"""
#         self.driver.get("https://talkhub.herokuapp.com/")
#         self.driver.find_element_by_id('delete-comment').click()
#         self.assertIn("https://talkhub.herokuapp.com/", self.driver.current_url)
# 
#     def send_comment_test(self):
#         """test 23"""
#         self.driver.get("https://talkhub.herokuapp.com/")
#         self.driver.find_element_by_id('send-comment').click()
#         self.assertIn("https://talkhub.herokuapp.com/", self.driver.current_url)
# 
# 
# class ProfilePageTests(SimpleTestCase):
#     """profile page tests"""
# 
#     def edit_profile_test(self):
#         """test 24"""
#         self.driver.get("https://talkhub.herokuapp.com/profile")
#         self.driver.find_element_by_id('edit-profile').click()
#         self.assertIn("https://talkhub.herokuapp.com/", self.driver.current_url)
# 
#     def delete_profile_test(self):
#         """test 25"""
#         self.driver.get("https://talkhub.herokuapp.com/profile")
#         self.driver.find_element_by_id('delete-user').click()
#         self.assertIn("https://talkhub.herokuapp.com/", self.driver.current_url)
# 
# 
# class PostEditPageTests(SimpleTestCase):
#     """post edit tests"""
# 
#     def PostEditFormTest(self):
#         """test 26"""
#         form = forms.PostCreateForm(title='Java gradle test',
#                                     private=False,
#                                     body='<div>Hello! I have a problem with java code!</div>')
# 
#         self.assertTrue(form.is_valid())
# 
# 
# class ResetPasswordTests(SimpleTestCase):
#     """reset password test"""
# 
#     def ResetPasswordFormTest(self):
#         """test 27"""
#         form = forms.PasswordResetForm(email='user@gmail.com')
#         self.assertTrue(form.is_valid())
# 
#     def NewPasswordFormTest(self):
#         """test 28"""
#         form = forms.NewPasswordResetForm(password='qwerty321qwerty',
#                                           password_again='qwerty321qwerty')
#         self.assertTrue(form.is_valid())
# 
#     def PasswordDonePageTest(self):
#         """test 29"""
#         self.driver.get("https://talkhub.herokuapp.com/reset-password-done")
#         self.driver.find_element_by_id('log-in').click()
#         self.assertIn("https://talkhub.herokuapp.com/", self.driver.current_url)
# 
#     def CheckLoginTest(self):
#         """test 30"""
#         form = forms.UserLoginForm(username='user',
#                                    password='qwerty321qwerty')
#         self.assertTrue(form.is_valid())
#         response = self.client.post('/login/', self.credentials, follow=True)
#         # should be logged in now
#         self.assertTrue(response.context['user'].is_active)
# 