# Problem Statement
- The goal is to design a search microservice for a blogging platform, similar to Medium,  where people (Authors) posts blog (Articles) about wide variety of topics either individually or by a group of people (Publications)
- Blogging sites core api's are not handled here
- A search miroservice which focusses entirely on search. 

# Functional Requirements
    1. Type Ahead Search bar  
        - Users should receive real-time suggestions and top search results as they type.
        - User's search history data should also avilable.
        - Different variety of searching should be suppported [Fuzzy Search / Prefix / Search on metadata fields]   
    2. Advanced search api's
        - Static search api with wide filter options and paginations should be supported
    3. Data Ingestion
        - A pipeline to ingest new and updated data from the core blogging service to keep the search database in sync.


# Non-Functional Requirements
    1. Performance
        - Low latency - realtime results for type-ahead suggestions (response times under 100 ms).
        - High throughput to handle concurrent searches.
    2. Scalability
        - Scale horizontally to support increasing numbers of users and content.
        - Ensure the system can handle peak loads during high-traffic events.     

# Good to have requirements
    1. Based on a user's search history enhance the future search results with tailored suggestions
    2. Push the search pattern to Analytics team to enhance the overall user experience of the platform.
    3. Expand the project as a fully functional Blogging site. 

# Trivial Requirements for a large scale system
    1. Enforce JWT authorization for each requests
    2. Validate rate-limit for the user


# Core Entities
    1. Articles
        - id
        - title
        - author
        - publication
        - created_date
        - likes
        - dislikes
    
    2. Authors
        - id
        - name
        - writes_about 
        - followers
    
    3. Publications
        - id
        - name
        - authors
        - tags
        - subscribers


# High Level Design
    1. Storage Layer
        - Use elastic search to store the entities.
        - Use Redis for storing the frequently accessed queries. 
        - Elastic search and Redis in cluster mode with required no of nodes
    2. Transport Layer
        - Expose websockets for providing near realtime responses for type ahead search results
        - Expose REST API endpoints for static search , 
        - Support cursor based pagination for static search
    3. Data Ingestion Service
        - Use Pub-Sub system like kafka to decouple the core blogging platform and search service. 
        - Operations like Creation / Udpation / Deletion of entities can be queued and bulk inserted into elastic search in small intervals (say each 5 mins).
        - Updates to aggregated fields like (likes count / followers count / Subscribers count) can be queued and prcocessed with stream processing framworks like Apache Flink and flush it to to elastic search on fixed intervals (sayd each day once )

# Tech Stack Used
1. FastAPI - Python based backend framework that supports asycnio for concurrent coding & supports websockets as well . 
2. Elastic Search
3. Redis
4. Docker
5. Kubernetes
6. Kafka


# API Design
```
ws/api/v1/search?auth=<jwt_auth_token>
Payload
{
    "prefix":"grpc"
}
Response
{
    "data":{
        "history":["golang", "python", "docker"],
        "suggestions": ["grpc with golang", "grpc and microservices" , "Pros of using grpc"]
        "articles": {...},
        "authors": {...},
        "publications": {...},
    }
}

```
```

http/api/v1/search
Query Params
    - pageSize
    - pageKey
    - sortBy
    - sortOrder
Payload
{
    "term:"....",
    "entity":"article",
    "...":"...."
}

```
