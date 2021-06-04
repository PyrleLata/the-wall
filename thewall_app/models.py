from django.db import models
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
  def registration_val(self, post_data):
    errors = {}
    if len(post_data['first_name']) < 2:
      errors['first_name'] = 'First name should be at least 2 characters'
    if len(post_data['last_name']) < 2:
      errors['last_name'] = 'Last name should be at least 2 characters'
    if not EMAIL_REGEX.match(post_data['email']):
      errors['email'] = 'Email is not valid'
    if len(post_data['password']) < 8:
      errors['password'] = "Password must be 8 characters long"
    if post_data['password'] != post_data['confirm_password']:
      errors['password'] = 'Your password do not match'
    print('gets inside registration val function')
    emailCheck = self.filter(email=post_data['email'])
    if emailCheck:
      errors['email'] = "That email is already in use"
    return errors
  def authenticate(self, email, password):
    users = self.filter(email=email)
    if not users:
      return False
    user = users[0]
    return bcrypt.checkpw(password.encode(), user.password.encode())

class User(models.Model):
  first_name = models.CharField(max_length=45)
  last_name = models.CharField(max_length=45)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)

  objects = UserManager()

  def __str__(self):
    return f"{self.first_name} {self.last_name} {self.email}"

class PostManager(models.Manager):
  def validate_post(self, post_text):
    errors = {}
    if len(post_text) < 2:
      errors['length'] = 'Posts must be at least 2 characters'
    if len(post_text) > 280:
      errors['length'] = f"Posts can be a max of 281 characters. This post is {len(post_text)}"
    return errors

class Post(models.Model):
  text = models.CharField(max_length=280)
  user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)
  likes = models.ManyToManyField(User, related_name="likes")

  objects = PostManager()

class Comment(models.Model):
  text = models.CharField(max_length=280)
  user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
  post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)