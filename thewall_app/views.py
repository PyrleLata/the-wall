from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Max
from .models import *
from django.contrib import messages
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
  return render(request, 'index.html')

def register(request):
  if request.method == "POST":
    errors = User.objects.registration_val(request.POST)
    if len(errors) > 0:
      for key, val in errors.items():
        messages.error(request, val)
      return redirect("/")
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash_pw)
  return redirect('/wall')

def login(request):
  if request.method == "POST":
    email = request.POST['email']
    password = request.POST['password']
    if not User.objects.authenticate(email, password):
      messages.error(request, 'Email and Password do not match')
      return redirect("/")
    user = User.objects.get(email=email)
    request.session['user_id'] = user.id
    return redirect("/wall")
  return redirect('/')

def logout(request):
  del request.session['user_id']
  return redirect('/')

def add_post(request):
  post_text = request.POST['post_text']
  errors = Post.objects.validate_post(post_text)
  if len(errors) > 0:
    for key, val in errors.items():
      messages.error(request, val)
    return redirect('/wall')
  user = User.objects.get(id=request.session['user_id'])
  Post.objects.create(text=post_text, user=user)
  return redirect('/wall')

def wall(request):
  if 'user_id' not in request.session:
    print('GETS HERE: USER NOT LOGGED IN')
    return HttpResponse("<h1>You must be logged in to get to your wall</h1>")
  user = User.objects.get(id=request.session['user_id'])
  all_posts = Post.objects.all().order_by("-created_at")
  context = {
    "user": user,
    "all_posts": all_posts
  }
  return render(request, 'wall.html', context)

def edit_post(request, post_id):
  post_to_edit = Post.objects.get(id=post_id)
  context = {
    "post": post_to_edit
  }
  return render(request, 'edit-post.html', context)

def modify_post(request):
  if request.method == "POST":
    post_id = request.POST['post_id']
    new_text = request.POST['post_text']
    errors = Post.objects.validate_post(new_text)
    if len(errors) > 0:
      for key, val in errors.items():
        messages.error(request, val)
      return redirect('/post')
    post_to_edit = Post.objects.get(id=post_id) 
    post_to_edit.text = new_text
    post_to_edit.save()
    return redirect('/wall')

def add_comment(request):
  comment_text = request.POST['comment_text']
  post_id = request.POST['post_id']
  user = User.objects.get(id=request.session['user_id'])
  post = Post.objects.get(id=post_id)
  Comment.objects.create(text=comment_text, user=user, post=post)
  return redirect('/wall')

def add_like(request, post_id):
  # query tweet to add likes to
  post = Post.objects.get(id=post_id)
  # query the user
  user = User.objects.get(id=request.session['user_id'])
  # add likes
  post.likes.add(user)
  return redirect('/wall')

def delete_post(request, post_id):
  post_to_delete = Post.objects.get(id=post_id) 
  post_to_delete.delete()
  return redirect('/wall')

# def delete_comment(request, post_id):
#   comment_to_delete = Comment.objects.get(id=post_id) 
#   comment_to_delete.delete()
#   return redirect('/wall')
