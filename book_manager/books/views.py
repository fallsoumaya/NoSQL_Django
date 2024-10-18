from django.shortcuts import render, redirect
from .models import Book
from .cassandra_utils import *
from .neo4j_utils import *
from django.http import JsonResponse
from .redis_client import increment_book_score, get_top_books


# ---------------------------------------MONGODB---------------------------------------

def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        published_year = request.POST.get("published_year")
        book = Book(title=title, author=author, published_year=published_year)
        book.save()
        return redirect('book_list')
    return render(request, 'create_book.html')

def get_books(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def update_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.published_year = request.POST.get("published_year")
        book.save()
        return redirect('book_list')
    return render(request, 'update_book.html', {'book': book})

def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'confirm_delete.html', {'book': book})

# ---------------------------------------CASSANDRA---------------------------------------

def mark_book_as_read(request, book_id):
    if request.user.is_authenticated:
        user_id = request.user.id
        create_interaction(user_id, book_id, 'read')
        return redirect('book_list')
    else:
        return redirect('login')

def user_interactions_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        interactions = get_user_interactions(user_id, 'read')
        return render(request, 'user_interactions.html', {'interactions': interactions})
    else:
        return redirect('login')

def remove_book_from_read_list(request, book_id):
    if request.user.is_authenticated:
        user_id = request.user.id
        delete_interaction(user_id, book_id, 'read')
        return redirect('book_list')
    else:
        return redirect('login')

# ---------------------------------------NEO4J---------------------------------------
def add_friend(request, friend_id):
    if request.user.is_authenticated:
        user_id = request.user.id
        add_friendship(user_id, friend_id)
        return redirect('friends_list')
    else:
        return redirect('login')

def friends_list(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        friends = get_friends(user_id)
        return render(request, 'friends_list.html', {'friends': friends})
    else:
        return redirect('login')

"""def recommendations_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        recommended_books = recommend_books_for_user(user_id)
        return render(request, 'recommendations.html', {'books': recommended_books})
    else:
        return redirect('login')

def friends_list_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        friends = get_friends(user_id)
        return render(request, 'friends_list.html', {'friends': friends})
    else:
        return redirect('login')
"""


# ---------------------------------------REDIS---------------------------------------
def book_view(request, book_id):
    # Mettre à jour le score du livre
    increment_book_score(book_id)
    
    # Logique pour afficher le livre (par exemple, retourner des informations sur le livre)
    # ...

    return JsonResponse({'message': 'Book viewed', 'book_id': book_id})

def popular_books_view(request):
    top_books = get_top_books()
    
    return JsonResponse({'top_books': top_books})
