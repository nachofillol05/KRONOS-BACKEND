from Kronosapp.models import DocumentType

def seed_DocumentType():
    # Defines of document types to create
    document_types = [
        {"name": "DNI", "description": "Documento Nacional de Identidad"},
        {"name": "Pasaporte", "description": "Numero de pasaporte internacional"},
        {"name": "CUIT", "description": "CUIT"},
    ]
    
    # Bulk creation of document types
    DocumentType.objects.bulk_create(
        [DocumentType(name=doc["name"], description=doc["description"]) for doc in document_types]
    )
