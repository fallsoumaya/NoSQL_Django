from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from config_cassandra import config_cassandra

db = config_cassandra()


def create_interaction(user_id, book_id, interaction_type):
    try:
        client = config_cassandra()
        payload = {
            "user_id": user_id,
            "book_id": book_id,
            "interaction_type": interaction_type,
            "timestamp": "toTimestamp(now())"
        }
        client.create_document("interactions", f"{user_id}-{book_id}", payload)
        print(f"Interaction created: {interaction_type} for user {user_id} and book {book_id}.")
    except Exception as e:
        print(f"Failed to create interaction: {e}")


def get_user_interactions(user_id, interaction_type):
    try:
        client = config_cassandra()
        query = f"SELECT * FROM interactions WHERE user_id = '{user_id}' AND interaction_type = '{interaction_type}'"
        result = client.execute(query)
        return result
    except Exception as e:
        print(f"Failed to retrieve interactions: {e}")

def update_interaction():
    """

    Cassandra n’est pas conçu pour des mises à jour spécifiques comme dans les bases de données relationnelles.
    Vous devez souvent supprimer et recréer les enregistrements ou gérer les changements au niveau des documents.
    
    """
def delete_interaction(user_id, book_id, interaction_type):
    try:
        client = config_cassandra()
        query = f"DELETE FROM interactions WHERE user_id = '{user_id}' AND book_id = '{book_id}' AND interaction_type = '{interaction_type}'"
        client.execute(query)
        print(f"Interaction deleted: {interaction_type} for user {user_id} and book {book_id}.")
    except Exception as e:
        print(f"Failed to delete interaction: {e}")

