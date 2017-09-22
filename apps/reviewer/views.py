# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
import re
import bcrypt

# Create your views here.
def index(request):
    if 'id' in request.session:
        return render(request,'reviewer/index.html')
    else:
        request.session['id'] = ""
        return render(request,'reviewer/index.html')

##########################################################################
def user_register(request):
    if request.method == 'POST':
        first = request.POST['first']
        last = request.POST['last']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['pass']
        con_pw = request.POST['con_pw']
        count = 0
        name_regex = re.compile(r'^[A-Z][a-z]+$')
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        pw_regex = re.compile(r'^[a-zA-Z0-9.+_-]{8,}$')
        #############################
        if len(first) < 2:
            messages.error(request, 'Name field should have at least 2 characters')
        else:
            if not name_regex.match(first):
                messages.error(request, 'Incorrect name format')
            else:
                count += 1
        ####################
        if len(last) < 2:
            messages.error(request, 'Name field should have at least 2 characters')
        else:
            if not name_regex.match(last):
                messages.error(request, 'Incorrect name format')
            else:
                count += 1
        ####################
        if len(alias) < 2:
            messages.error(request, 'Alias field should have at least 2 characters')
        else:
            if not name_regex.match(alias):
                messages.error(request, 'Incorrect alias format')
            else:
                if User.objects.filter(alias = alias):
                    messages.error(request, 'Alias has been used, Please use other alias.')
                else:
                    count += 1
                    
        ###################
        if len(email) < 1:
            messages.error(request, 'Email field can not be empty!!!')
        else:
            if not email_regex.match(email):
                messages.error(request, 'Incorrect email format')
            else:
                if User.objects.filter(email = email):
                    messages.error(request, 'Email has been registered, Please use other emails.')
                else:
                    count += 1
        ######################
        if len(password) < 1:
            messages.error(request, 'password field can not be empty!!!')
        else:
            if not pw_regex.match(password):
                messages.error(request,"Password should have at least 8 characters!")
            else:
                count += 1

        #########################
        if len(con_pw) < 1:
            messages.error(request, 'confirm password field can not be empty!!!')
        else:
            if con_pw != password:
               messages.error(request,"Password confirmation do not match!!")
            else:
                count += 1
        ###########################
        if count == 6:
            hash_pw = bcrypt.hashpw(password.encode(),bcrypt.gensalt())            
            new_user = User.objects.create(first_name = first, last_name = last, alias=alias, email = email, password = hash_pw )
            request.session['id'] = new_user.id
            return redirect('/books')
        
    
    return redirect('/')

############################################################################
def user_login(request):
    if request.method == 'POST':
        login_email = request.POST['login_email']
        login_pass = request.POST['login_pass']
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        pw_regex = re.compile(r'^[a-zA-Z0-9.+_-]{8,}$')
        email_found = False
        
        if len(login_email) < 1:
            messages.error(request, 'Email field can not be empty!!!')
        else:
            if not email_regex.match(login_email):
                messages.error(request, 'Incorrect email format')
            else:
                if not User.objects.get(email = login_email):
                    messages.error(request, 'Please enter correct email!!')
                else:
                    email_found = True
        
        if len(login_pass) < 1:
            messages.error(request, 'Password field can not be empty!!!')
        else:
            if not pw_regex.match(login_pass):
                messages.error(request,"Password should have at least 8 characters!")
            else:
                if email_found:
                    user = User.objects.get(email = login_email)
                    print user.password
                    if bcrypt.checkpw(login_pass.encode(), user.password.encode()):
                        request.session['id'] = user.id
                        return redirect('/books')
                    else:
                        messages.error(request,"Incorrect password!")
                                 
    return redirect('/')

#########################################################################################
def books(request):
    the_user = User.objects.get(id = request.session['id'])
    reviewes = Review.objects.order_by('-created_at')
    print reviewes
    top_review =[]
    if len(reviewes)>3:
        top_review = reviewes[0:3]
        arr = []
        for each in top_review:
            arr.append(each.book.id)
        books = Book.objects.exclude( id__in = arr)
    else:
        top_review = reviewes
    context = {
        'the_user':the_user,
        'top_review':top_review,
        'books':books,
    }
    return render(request,'reviewer/books.html',context)

##########################################
def add_books(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        return render(request,'reviewer/add.html',{'all_authors':authors})

    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST.get('author')
        new_author = request.POST['new_author']
        book_review = request.POST['review']
        stars = request.POST.get('stars')
        count = 0
        #############################
        if len(title) <1:
            messages.error(request,"Please enter book title!")
        else:
            if Book.objects.filter(title = title):
                messages.error(request,"This Book is already in database!")
            else:
                count += 1
        ###########################
        if author == None:
            if len(new_author) < 1:
                messages.error(request,"Please enter author's name!")
            else:
                if Author.objects.filter(name = new_author):
                    messages.error(request,"This author is already in database!")
                else:
                    count += 1
        else:
            count += 1


        #################################
        if len(book_review) < 15:
            messages.error(request,"Review should have at least 15  characters!")
        else:
            count += 1

        #########################################
        if stars == None:
            messages.error(request,"Please select rating stars!")
        else:
            count += 1
        ###########################################
        if author == None and len(new_author) > 0:
            count += 2
        elif author != None and len(new_author) < 1:
            count += 1
        elif author == None and len(new_author) < 1 :
            messages.error(request,"Please select one author!")
        else:
            messages.error(request,"Please select ONLY one author!")
        #######################################
        if count == 5:            
            new_book = Book.objects.create(title = title, author = Author.objects.get(name = author))
            new_review = Review.objects.create(detail = book_review, rating = stars, book = new_book, \
            user = User.objects.get(id = request.session['id'])) 
            return redirect('/books/{}'.format(new_book.id))
        elif count == 6:
            the_author = Author.objects.create(name = new_author)
            new_book = Book.objects.create(title = title, author = the_author)
            new_review = Review.objects.create(detail = book_review, rating = stars, book = new_book, \
            user = User.objects.get(id = request.session['id'])) 
            return redirect('/books/{}'.format(new_book.id))

        return redirect('/books/add')

#################################################
def show_book(request,book_id):
    if request.method == 'GET':
        this_book  = Book.objects.get(id = book_id)
        all_reviews = Review.objects.filter(book = this_book).order_by('-created_at')
        context ={
            "book_name":this_book.title,
            "the_author":this_book.author.name,
            'book_id':book_id,
            'all_reviews':all_reviews,
        }
        return render(request,"reviewer/the_book.html", context)

    elif request.method == 'POST':
        review = request.POST['review']
        stars = request.POST.get('stars')
        count = 0
        if len(review) < 15:
            messages.error(request,"Please write review with at least 15 characters!")
        else:
            count += 1

        if stars == None:
            messages.error(request,"Please select stars!")
        else:
            count += 1

        if count == 2:
            new_review = Review.objects.create(detail = review, rating = stars, \
            book = Book.objects.get(id = book_id),user = User.objects.get(id = request.session['id']))
        return redirect('/books/{}'.format(book_id))


def show_user(request,user_id):
    if request.method == 'GET':
        the_user = User.objects.get(id = user_id )
        reviews = Review.objects.filter(user = the_user)
        books = Book.objects.filter(reviews = reviews )
        print books
        count = reviews.count()
        context ={
            'count':count,
            'the_user':the_user,
            'reviews':reviews,
        }
        return render(request,"reviewer/users.html", context)
   
def delete(request, review_id):
    the_review = Review.objects.get(id = review_id)
    book_id = the_review.book.id
    the_review.delete()
    return redirect('/books/{}'.format(book_id))