PUT /articles
{
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"  // Assuming id is a unique identifier (like ULID or UUID)
      },
      "title": {
        "type": "text"  // For full-text search on the article title
      },
      "tags": {
        "type": "keyword"  // Exact matching of tags (List of Strings)
      },
      "created_on": {
        "type": "date",  // Storing creation timestamp
        "format": "yyyy-MM-dd'T'HH:mm:ss'Z'"  // Date format as UTC
      },
      "author_id": {
        "type": "keyword"  // Exact match on author ID
      },
      "publication_id": {
        "type": "keyword"  // Exact match on publication ID
      },
       "suggest_title": {
            "type": "completion"
            }
    }
  }
}



PUT /authors
{
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"  // Unique identifier for Person (could be ULID, UUID)
      },
      "name": {
        "type": "text"  // Full-text search on the person's name
      },
      "writes_about": {
        "type": "keyword"  // List of topics the person writes about (exact match)
      }
    }
  }
}




PUT /publications
{
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"  // Unique identifier for the publication (could be ULID, UUID)
      },
      "name": {
        "type": "text"  // Full-text search on the publication name
      },
      "tags": {
        "type": "keyword"  // Exact matching of publication tags (List of Strings)
      },
      "description": {
        "type": "text",  // Optional description field for the publication
        "norms": false   // Disable norms for better performance if description is large
      }
    }
  }
}


PUT /search_history
{
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"
      },
      "prefix": {
        "type": "text"
      },
      "user_id": {
        "type": "keyword"
      },
      "date": {
        "type": "date",
        "format": "yyyy-MM-dd'T'HH:mm:ss'Z'"
      }
    }
  }
}
