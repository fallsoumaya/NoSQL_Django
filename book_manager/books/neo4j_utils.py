from neo4j import GraphDatabase
from django.conf import settings

class Neo4jDatabase:
    def __init__(self):
        self.uri = settings.NEO4J_DATABASES['default']['HOST']
        self.user = settings.NEO4J_DATABASES['default']['USER']
        self.password = settings.NEO4J_DATABASES['default']['PASSWORD']
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return result



# Recommendations

def add_read_relationship(user_id, book_id):
    query = """
    MATCH (u:User {id: $user_id}), (b:Book {id: $book_id})
    MERGE (u)-[:READ]->(b)
    """
    neo4j_client.run_query(query, {"user_id": user_id, "book_id": book_id})

def add_recommendation(user_id, book_id):
    query = """
    MATCH (u:User {id: $user_id}), (b:Book {id: $book_id})
    MERGE (u)-[:RECOMMENDS]->(b)
    """
    neo4j_client.run_query(query, {"user_id": user_id, "book_id": book_id})

def get_recommendations_for_user(user_id):
    query = """
    MATCH (u:User {id: $user_id})-[:RECOMMENDS]->(book)
    RETURN book
    """
    result = neo4j_client.run_query(query, {"user_id": user_id})
    return [record["book"] for record in result]

def get_recommendations_based_on_friends(user_id):
    query = """
    MATCH (u:User {id: $user_id})-[:FRIENDS_WITH]->(friend)-[:RECOMMENDS]->(book)
    RETURN DISTINCT book
    """
    result = neo4j_client.run_query(query, {"user_id": user_id})
    return [record["book"] for record in result]

def delete_recommendation(user_id, book_id):
    query = """
    MATCH (u:User {id: $user_id})-[r:RECOMMENDS]->(b:Book {id: $book_id})
    DELETE r
    """
    neo4j_client.run_query(query, {"user_id": user_id, "book_id": book_id})

# Réseau social des lecteurs

def add_friendship(user_id1, user_id2):
    query = """
    MATCH (u1:User {id: $user_id1}), (u2:User {id: $user_id2})
    MERGE (u1)-[:FRIENDS_WITH]->(u2)
    """
    neo4j_client.run_query(query, {"user_id1": user_id1, "user_id2": user_id2})

def add_follow(user_id1, user_id2):
    query = """
    MATCH (u1:User {id: $user_id1}), (u2:User {id: $user_id2})
    MERGE (u1)-[:FOLLOWS]->(u2)
    """
    neo4j_client.run_query(query, {"user_id1": user_id1, "user_id2": user_id2})

def get_friends(user_id):
    query = """
    MATCH (u:User {id: $user_id})-[:FRIENDS_WITH]->(friend)
    RETURN friend
    """
    result = neo4j_client.run_query(query, {"user_id": user_id})
    return [record["friend"] for record in result]

def get_following(user_id):
    query = """
    MATCH (u:User {id: $user_id})-[:FOLLOWS]->(followed)
    RETURN followed
    """
    result = neo4j_client.run_query(query, {"user_id": user_id})
    return [record["followed"] for record in result]

def get_followers(user_id):
    query = """
    MATCH (u:User {id: $user_id})<-[:FOLLOWS]-(follower)
    RETURN follower
    """
    result = neo4j_client.run_query(query, {"user_id": user_id})
    return [record["follower"] for record in result]

def delete_friendship(user_id1, user_id2):
    query = """
    MATCH (u1:User {id: $user_id1})-[r:FRIENDS_WITH]-(u2:User {id: $user_id2})
    DELETE r
    """
    neo4j_client.run_query(query, {"user_id1": user_id1, "user_id2": user_id2})

def delete_follow(user_id1, user_id2):
    query = """
    MATCH (u1:User {id: $user_id1})-[r:FOLLOWS]-(u2:User {id: $user_id2})
    DELETE r
    """
    neo4j_client.run_query(query, {"user_id1": user_id1, "user_id2": user_id2})

