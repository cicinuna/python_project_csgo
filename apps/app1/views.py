from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import re
import bcrypt
import datetime
import time

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

# Create your views here.

def index(request):
    first_category = Category.objects.first()
    second_category = Category.objects.get(id = 2)
    third_category = Category.objects.get(id = 3)
    first_services = Service.objects.filter(category_id = first_category)
    second_services = Service.objects.filter(category_id = second_category)
    third_services = Service.objects.filter(category_id = third_category)
    content = {
        'first_category': first_category,
        'second_category': second_category,
        'third_category': third_category,
        'first_service_list': first_services,
        'second_service_list': second_services,
        'third_service_list': third_services
    }
    return render(request, 'app1/index.html', content)

def add_to_cart(request):
    if request.session['user']['id'] == 1:
        messages.error(request, 'Admin cannot purchase like a noob!')
        return redirect(index)
    else:
        if 'cart' not in request.session:
            print "am here?"
            request.session['cart'] = []
            request.session['total_price'] = 0
            item = Service.objects.get(id = int(request.POST['service_id']))
            cart_item = {
                'name': item.service,
                'price': item.price,
                'id': item.id
            }
            request.session['total_price'] += int(item.price)
            request.session['cart'].append(cart_item)
            return redirect(index)
        else:
            print "OR HERE"
            item = Service.objects.get(id = int(request.POST['service_id']))
            cart_item = {
                'name': item.service,
                'price': item.price, 
                'id': item.id
            }
            request.session['total_price'] += int(item.price)
            request.session['cart'].append(cart_item)
            request.session.modified = True
            return redirect(index)

def process_login(request):
    user = User.objects.filter(username = request.POST['username'])
    if not user:
        messages.error(request, 'Invalid Login Information!')
        return redirect(index)
    else:
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            # messages.success(request, 'Successfully Logged In!')
            # request.session['user'] = user
            session_user = {
                'first_name': user[0].first_name,
                'last_name': user[0].last_name,
                'username': user[0].username,
                'id': user[0].id
            }
            request.session['user'] = session_user
            print request.session['user']
            print "success login"
            if request.session['user']['id'] == 1:
                return redirect(admin_dashboard)
            else:
                return redirect(index)
        else:
            messages.error(request, 'Invalid Login Information!')
            return redirect(index)

def process_registration(request):
    error = False
    if len(request.POST['first_name']) < 2 or len(request.POST['first_name']) < 2 or len(request.POST['username']) < 2:
        messages.error(request, 'First and Last names and username must be longer than 2 characters!')
        error = True
    if not request.POST['first_name'].isalpha() or not request.POST['last_name'].isalpha():
        messages.error(request, 'First and last must be alphabets!')
        error = True
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request, 'Please enter a valid e-mail address!')
        error = True
    emails = User.objects.filter(email = request.POST['email'])
    if emails:
        messages.error(request, 'This email is already taken!')
        error = True
    if not PASSWORD_REGEX.match(request.POST['password']):
        messages.error(request, 'Password must be 8 or more characters, contain at least 1 upper case and 1 number!')
        error = True
    if request.POST['password'] != request.POST['confirm_password']:
        messages.error(request, 'Passwords must match!')
        error = True
    usernames = User.objects.filter(username = request.POST['username'])
    if usernames:
        messages.error(request, 'This username is already taken!')
        error = True
    if error:
        return redirect(index)
    else: 
        # print bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'],email = request.POST['email'], username = request.POST['username'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        # request.session['user'] = User.objects.last()
        session_user = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'username': request.POST['username'],
            'id': User.objects.last().id
        }
        request.session['user'] = session_user
        return redirect(index)

def logout(request):
    if 'user' in request.session:
        request.session.pop('user')
        messages.success(request, 'Successfully Logged Out!')
    if 'cart' in request.session:
        request.session.pop('cart')
    if 'total_price' in request.session:
        request.session.pop('total_price')
    
    return redirect(index)

def admin_dashboard(request):
    if 'user' not in request.session or request.session['user']['id'] != 1:
        messages.error(request, 'You must be logged in as Administrator to view this page!')
        return redirect(index)
    else:
        category_list = Category.objects.all()
        service_list = Service.objects.all()
        content = {
            'categories': category_list,
            'services': service_list
        }
        return render(request, 'app1/admin_dashboard.html', content)

def shopping_cart(request):
    return HttpResponse("HERE")

def add_service(request):
    Service.objects.create(service = request.POST['service'], description = request.POST['description'], price = request.POST['price'], category_id = Category.objects.get(id = request.POST['category_id']))
    messages.success(request, "Successfully added service!")
    return redirect(admin_dashboard)

def remove_existing(request):
    to_del = Service.objects.get(id = request.POST['remove'])
    to_del.delete()
    success_message = "Successfully deleted {} service!".format(to_del.service)
    messages.success(request, success_message)
    return redirect(admin_dashboard)

def remove_item_from_cart(request):
    for index, things in enumerate(request.session['cart']):
        if int(things['id']) == int(request.POST['delete_id']):
            request.session['cart'].pop(index)
            request.session['total_price'] -= int(things['price'])
            request.session.modified = True
            messages.success(request, "Successfully modified your cart!")
    return redirect('/')

def make_purchase(request):
    # to have:
    # stripe implementation
    # this section is for stripe things

    # this section is for doing stuff to orders in DB
    Order.objects.create(total = request.session['total_price'], user_id = User.objects.get(id = request.session['user']['id']))
    recent_order = Order.objects.last()
    for things in request.session['cart']:
        service_to_add = Service.objects.get(id = int(things['id']))
        recent_order.services.add(service_to_add)

    