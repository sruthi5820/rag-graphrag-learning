
# 2.1 What Is an API?

## 1. Introduction

API stands for Application Programming Interface.

An API allows two software applications to communicate with each other and exchange data or functionality.

Instead of building every feature from scratch, an application can use an API to access services provided by another application.

For example, a Python RAG application can send a user's question to an LLM API and receive a generated answer.

APIs are commonly used in web applications, mobile applications, databases, cloud services, artificial intelligence, and machine learning systems.

## 2. Real-World Example

Consider a restaurant.

- Customer: Requests food.
- Waiter: Takes the order to the kitchen.
- Kitchen: Prepares the food.
- Waiter: Returns the food to the customer.

An API works similarly.

- Client: Sends a request.
- API: Receives and routes the request.
- Server: Processes the request.
- API: Returns the response to the client.

The API provides a defined way for the client to interact with the server without needing to know all the internal implementation details.

Note: A real API is software, not a physical person. The waiter is simply an analogy to understand its role.

## 3. Why Do We Need APIs?

APIs are useful for the following reasons:

1. Communication: Allow different applications to exchange information.
2. Reusability: Use existing services instead of implementing everything from scratch.
3. Integration: Connect Python applications with databases, websites, and AI models.
4. Automation: Perform operations programmatically.
5. Security: Control which operations and data a client can access.
6. Scalability: Separate applications into services that can be developed and maintained independently.
7. Standardization: Define consistent request and response formats.

## 4. Important API Terminology

### 4.1 Client

A client is an application or program that sends a request to an API.

Examples:
- Python script
- Web browser
- Mobile application
- Frontend chatbot

In a RAG application, the Python backend can act as a client when calling an LLM API.

### 4.2 Server

A server receives requests, processes them, and returns responses.

For example, an LLM service may receive a prompt, run the language model, and return the generated text.

### 4.3 Request

A request is a message sent by a client to an API.

A request may contain:
- URL
- HTTP method
- Headers
- Query parameters
- Request body

Example:

POST /api/chat

Request body:

{
    "question": "What is RAG?"
}

The client is asking the API to process the question.

### 4.4 Response

A response is the information returned by the API after processing a request.

A response may contain:
- Status code
- Response headers
- Response body

Example response:

{
    "answer": "RAG stands for Retrieval-Augmented Generation."
}

The response body contains the generated answer.

### 4.5 Endpoint

An endpoint is a specific API URL used to access a particular resource or operation.

Example:

https://api.example.com/users

Here:
- https://api.example.com is the base URL.
- /users is the endpoint path.

An API may provide multiple endpoints.

Examples:
- GET /users
- GET /users/10
- POST /users
- DELETE /users/10

Each endpoint supports a particular operation, depending on the API design.

Note: The URLs above are illustrative examples, not real services.

### 4.6 HTTP Method

An HTTP method indicates the type of operation a client wants to perform.

Common methods include:

GET:
Retrieve information from a server.

POST:
Submit data to a server, commonly to create a resource or execute an operation.

PUT:
Replace a resource, usually providing its complete new representation.

PATCH:
Update part of an existing resource.

DELETE:
Delete a resource.

Example:

GET /products

This requests product information.

POST /products

This may create a new product using the submitted request body.

Important: The exact behavior depends on how the API is designed.

### 4.7 Status Code

An HTTP status code indicates the result of an HTTP request.

Common status codes:

200 OK:
The request succeeded.

201 Created:
A resource was successfully created.

204 No Content:
The request succeeded and has no response body.

400 Bad Request:
The request contains invalid data or cannot be processed.

401 Unauthorized:
Authentication is missing or invalid.

403 Forbidden:
The client is not permitted to perform the operation.

404 Not Found:
The requested resource or endpoint was not found.

422 Unprocessable Content:
The request content failed validation or could not be processed according to the API's rules.

429 Too Many Requests:
The client exceeded a rate limit.

500 Internal Server Error:
The server encountered an unexpected error.

502 Bad Gateway:
A gateway or proxy received an invalid response from an upstream server.

503 Service Unavailable:
The service is temporarily unable to handle the request.

Status codes are useful when debugging API integrations.

### 4.8 Headers

Headers provide additional information about a request or response.

Examples:

Content-Type: application/json

Indicates that the message body contains JSON data.

Accept: application/json

Indicates that the client prefers a JSON response.

Authorization: Bearer <access_token>

Provides a bearer access token for authentication.

Headers may be used for authentication, content negotiation, caching, and other purposes.

Never commit real access tokens, API keys, or passwords to GitHub.

### 4.9 Request Body

The request body contains data sent to the server.

It is commonly used with POST, PUT, and PATCH requests.

Example:

{
    "name": "Sruthi",
    "role": "Developer"
}

The server can use this information to perform the requested operation.

### 4.10 Query Parameters

Query parameters pass additional information through the URL.

Example:

GET /products?category=books&limit=10

Here:
- category=books filters the products by category.
- limit=10 requests at most ten products, if supported.

Query parameters are useful for filtering, pagination, and sorting.

### 4.11 JSON

JSON stands for JavaScript Object Notation.

It is a lightweight format used to exchange structured data between applications.

JSON supports:
- Objects
- Arrays
- Strings
- Numbers
- Booleans
- Null values

Example:

{
    "question": "What is an API?",
    "category": "programming",
    "active": true,
    "tags": ["Python", "RAG", "LLM"],
    "rating": null
}

JSON objects contain key-value pairs.

JSON arrays contain ordered collections of values.

JSON is language-independent and is widely used by Python APIs.

Important: JSON requires double quotes around strings and property names. It does not support comments or trailing commas.

## 5. How an API Works Step by Step

Consider a Python application requesting an answer from an LLM service.

Step 1:
The user enters a question.

Step 2:
The Python application prepares an HTTP request.

Step 3:
The application sends the request to the API endpoint.

Step 4:
The API validates the request and performs authentication if required.

Step 5:
The server processes the request.

Step 6:
The server returns an HTTP response containing a status code and data.

Step 7:
The Python application reads the response and displays the answer.

Example flow:

User Question
      |
      v
Python Application
      |
      v
HTTP Request
      |
      v
API Endpoint
      |
      v
Server Processing
      |
      v
HTTP Response
      |
      v
Python Application
      |
      v
Display Answer

## 6. Types of APIs

### 6.1 REST API

REST APIs commonly use HTTP methods and URLs to access resources.

They often exchange JSON data.

Example:
GET /articles

A client requests a collection of articles.

### 6.2 SOAP API

SOAP is a protocol for exchanging structured messages between applications.

SOAP commonly uses XML and defines specific messaging rules.

It is used in some enterprise and legacy integrations.

### 6.3 GraphQL API

GraphQL allows clients to request specific fields of data through a query.

It can help avoid retrieving unnecessary fields when the API supports the requested query.

### 6.4 WebSocket API

WebSockets provide a persistent, two-way communication channel between a client and a server.

They are useful for real-time applications such as:
- Live chat
- Real-time notifications
- Streaming updates
- Collaborative applications

### 6.5 AI and LLM APIs

AI APIs expose model capabilities through programmatic interfaces.

They may support:
- Text generation
- Embeddings
- Image processing
- Speech processing
- Structured output

For example, a Python application can send a prompt to an LLM API and receive generated text.

## 7. API vs. Web Application

A web application usually provides an interface for users to interact with a service.

An API provides a defined interface for software to interact with a service.

Example:

A chatbot web page allows a user to type a question.

The frontend sends the question to a backend API.

The backend retrieves relevant information and calls an LLM.

The backend returns the answer to the frontend.

The frontend displays the response.

An API can be used by many clients, provided they have the required access and follow the API contract.

## 8. API Example Using Python

Python provides libraries such as requests and httpx for making HTTP requests.

Install requests:

pip install requests

Example code:

import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = requests.get(url, timeout=10)

    print("Status code:", response.status_code)

    response.raise_for_status()

    data = response.json()

    print("Title:", data["title"])
    print("Body:", data["body"])

except requests.exceptions.Timeout:
    print("The request timed out.")

except requests.exceptions.HTTPError as error:
    print("HTTP error:", error)

except requests.exceptions.RequestException as error:
    print("Request failed:", error)

Explanation:

1. Import the requests library.
2. Define the API endpoint.
3. Send a GET request.
4. Set a timeout to avoid waiting indefinitely.
5. Print the HTTP status code.
6. Call raise_for_status() to detect unsuccessful HTTP responses.
7. Convert the JSON response into Python objects.
8. Access the title and body fields.
9. Handle common request errors.

The example uses JSONPlaceholder, a public test API. It does not require an API key.

## 9. API Example Using POST

The following example sends JSON data to a public test API.

import requests

url = "https://jsonplaceholder.typicode.com/posts"

payload = {
    "title": "Learning APIs",
    "body": "I am learning API fundamentals with Python.",
    "userId": 1
}

try:
    response = requests.post(
        url,
        json=payload,
        timeout=10
    )

    print("Status code:", response.status_code)

    response.raise_for_status()

    print("Response:", response.json())

except requests.exceptions.RequestException as error:
    print("Request failed:", error)

Explanation:

- url identifies the endpoint.
- payload contains the data to send.
- json=payload serializes the dictionary into JSON and sets the appropriate content type.
- requests.post() sends the POST request.
- response.json() parses the response body into Python data.

The test API may return a simulated created resource. It does not necessarily persist the submitted data.

## 10. API in a RAG Application

APIs are important in Retrieval-Augmented Generation systems.

A typical RAG pipeline is:

User Question
      |
      v
RAG Backend API
      |
      v
Convert Question into Embedding
      |
      v
Vector Database Search
      |
      v
Retrieve Relevant Chunks
      |
      v
Build Prompt with Context
      |
      v
Call LLM API
      |
      v
Generate Answer
      |
      v
Return Answer through Backend API
      |
      v
Display Answer to User

Example:

A user asks:

"What is Retrieval-Augmented Generation?"

The backend receives the question through an API endpoint.

The retrieval component searches the vector database for relevant document chunks.

The backend includes the retrieved information in the prompt.

The LLM generates an answer using the supplied context.

The backend returns the answer and, when implemented, its supporting citations.

APIs can connect the frontend, backend, embedding service, vector database service, and LLM service.

Note: A vector database accessed through a local Python library may not require a separate HTTP API call. The architecture depends on the implementation.

## 11. API Security Basics

When working with APIs, follow these practices:

1. Use HTTPS for communication over untrusted networks.
2. Keep API keys and access tokens secret.
3. Store secrets in environment variables or a secrets manager.
4. Validate incoming request data.
5. Use authentication and authorization where required.
6. Set request timeouts.
7. Handle errors without exposing sensitive information.
8. Follow rate limits and usage policies.
9. Avoid logging passwords, access tokens, and confidential data.
10. Never commit .env files containing secrets to GitHub.

Example of loading an API key from an environment variable:

import os

api_key = os.getenv("LLM_API_KEY")

if not api_key:
    raise RuntimeError("LLM_API_KEY is not configured")

The actual API client should use this key according to the service's authentication requirements.

## 12. Common API Errors and Troubleshooting

### Connection Error

Possible causes:
- Server is unavailable.
- Network connectivity is interrupted.
- DNS resolution fails.

What to do:
- Check the server address.
- Check network connectivity.
- Verify that the server is running.

### Timeout Error

Possible causes:
- The server responds slowly.
- The request takes too long to process.
- Network latency is high.

What to do:
- Configure an appropriate timeout.
- Check server performance.
- Retry only when appropriate.

### 401 Unauthorized

Possible causes:
- Missing access token.
- Invalid or expired credentials.

What to do:
- Verify the authentication configuration.
- Obtain a valid token if required.

### 403 Forbidden

Possible causes:
- The authenticated client lacks permission.

What to do:
- Check the account's permissions and access policy.

### 404 Not Found

Possible causes:
- Incorrect endpoint URL.
- Requested resource does not exist.

What to do:
- Verify the URL and resource identifier.

### 422 Unprocessable Content

Possible causes:
- Required fields are missing.
- Data types are incorrect.
- Request validation failed.

What to do:
- Read the response body.
- Compare the request with the API schema.
- Correct the submitted data.

### 429 Too Many Requests

Possible causes:
- Rate limits have been exceeded.

What to do:
- Respect Retry-After when provided.
- Apply appropriate backoff and retry limits.

### 500 Internal Server Error

Possible causes:
- Unexpected server-side failure.

What to do:
- Check server logs if you control the service.
- Retry cautiously if the operation is safe to repeat.

## 13. Practical Exercises

Exercise 1: Send a GET request.
- Call the JSONPlaceholder test API.
- Print the status code.
- Display the response title.

Exercise 2: Read JSON data.
- Retrieve a post from the API.
- Convert the response to a Python dictionary.
- Print individual fields.

Exercise 3: Send a POST request.
- Create a dictionary containing title, body, and userId.
- Submit it to the test API.
- Inspect the response.

Exercise 4: Handle errors.
- Use a timeout.
- Handle connection errors.
- Handle HTTP errors.

Exercise 5: Test a missing endpoint.
- Request a nonexistent resource.
- Inspect the 404 response.
- Use raise_for_status() to handle unsuccessful responses.

Exercise 6: Connect APIs to RAG.
- Create a simple Python backend endpoint.
- Accept a question as JSON.
- Return a JSON response.
- Later, connect the endpoint to retrieval and an LLM.

## 14. Key Takeaways

- API stands for Application Programming Interface.
- An API enables software applications to communicate.
- A client sends requests and receives responses.
- An endpoint identifies where an API operation is accessed.
- HTTP methods describe the requested operation.
- Status codes indicate the outcome of an HTTP request.
- Headers carry metadata and may provide authentication details.
- JSON is a common format for exchanging structured data.
- Python libraries such as requests and httpx make HTTP calls easier.
- APIs connect the different components of a RAG application.
- Error handling, security, and timeouts are important in production systems.


