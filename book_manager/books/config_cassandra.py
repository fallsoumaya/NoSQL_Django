import astrapy

# Configuration des variables
ASTRA_DB_ID = "c93c29a7-087a-4671-b065-b349bc57572f"
ASTRA_DB_REGION = "us-east-2"
ASTRA_DB_KEYSPACE = "book_manager_keyspace"
ASTRA_DB_APPLICATION_TOKEN = "AstraCS:whAkocyzXtGbyGtZradZoMdn:b64d1fc14d38d81a9dc51e946924c2475c927399076a08adfc7cd20449d65222"

def config_cassandra():
    client = astrapy.create_client(
        astra_database_id=ASTRA_DB_ID,
        astra_database_region=ASTRA_DB_REGION,
        astra_application_token=ASTRA_DB_APPLICATION_TOKEN
    )
    
    # Se connecter à un espace de noms (keyspace)
    db = client.namespace(ASTRA_DB_KEYSPACE)
    
    print(f"Connected to Astra DB with namespace: {ASTRA_DB_KEYSPACE}")
    return db