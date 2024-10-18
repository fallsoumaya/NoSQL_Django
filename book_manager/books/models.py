from djongo import models
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    favorites = models.ManyToManyField(Book, related_name='favorited_by')

    def __str__(self):
        return self.username

class UserInteraction(Model):
    user_id = columns.UUID(primary_key=True)
    book_id = columns.UUID(primary_key=True)
    interaction_type = columns.Text()    # e.g., "favorite", "view"
    event_timestamp = columns.DateTime()

class BookNode:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def save(self, driver):
        with driver.session() as session:
            session.write_transaction(self._create_book_node)

    def _create_book_node(self, tx):
        tx.run("CREATE (b:Book {title: $title, author: $author})", 
               title=self.title, author=self.author)
