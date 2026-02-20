DOCUMENTS = {
    "public_doc": "The weather today is sunny.",
    "private_doc": "User SSN: 123-45-6789",
}

def retrieve_docs(query: str, user_role: str):
    """
    Simulates retrieval-augmented generation with access control.
    """
    # Only allow non-sensitive docs for normal users
    if user_role == "user":
        return [DOCUMENTS["public_doc"]]
    elif user_role == "admin":
        return list(DOCUMENTS.values())