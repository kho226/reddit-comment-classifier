from flask import current_app



def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, doc_type=index, id=model.id,
                                    body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)


def query_index(index, query, docType):
    if not current_app.elasticsearch:
        return [], 0
    if current_app.redis_store.exists(query):
        print ("Using cached query")
        return current_app.redis_store.get(query) 
    search = current_app.elasticsearch.search(
        index=index, doc_type=docType,
        body=query)
    current_app.redis_store.set(query, search, 300) #cache queries for 300 seconds
    return search
