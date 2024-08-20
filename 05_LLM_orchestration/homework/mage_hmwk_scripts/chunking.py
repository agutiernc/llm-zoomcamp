if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

import hashlib

def generate_document_id(doc):
    combined = f"{doc['course']}-{doc['question']}-{doc['text'][:10]}"
    hash_object = hashlib.md5(combined.encode())
    hash_hex = hash_object.hexdigest()
    document_id = hash_hex[:8]
    
    return document_id

def process_course_documents(course_data):
    documents = []

    for doc in course_data['documents']:
        doc['course'] = course_data['course']
        doc['document_id'] = generate_document_id(doc)
        documents.append(doc)
    
    return documents

@transformer
def transform(data, *args, **kwargs):
    """
    Process documents and generate unique document IDs.
    Args:
        data: The output from the upstream parent block
    Returns:
        List of processed documents
    """
    processed_documents = []

    # Check if data is a list of dictionaries or a single dictionary
    if isinstance(data, list):
        for course_dict in data:
            processed_documents.extend(process_course_documents(course_dict))
    else:
        processed_documents.extend(process_course_documents(data))

    print(f"Total processed documents: {len(processed_documents)}")

    return processed_documents