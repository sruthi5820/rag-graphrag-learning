1.1 What is Python?

Python is a programming language used to build applications, process documents, communicate with APIs and implement AI workflows.

In RAG, Python connects the main components:
- Reads PDF, TXT, HTML and other documents.
- Splits documents into smaller chunks.
- Calls embedding models.
- Stores and searches vectors.
- Sends retrieved context to an LLM.
- Returns answers with supporting citations.


1.2 Important Python concepts
Concept	        Meaning	                        RAG example
Variables	    Store values	                Document text
Lists	        Store multiple values	        List of chunks
Dictionaries	Store key-value pairs	        Chunk and metadata
Functions	    Reusable operations	            split_text()
Classes	        Group data and behavior	        DocumentRetriever
Loops	        Repeat operations	            Process multiple files
Exceptions	    Handle errors	                Skip unreadable files
Modules	        Organize code	                ingestion.py