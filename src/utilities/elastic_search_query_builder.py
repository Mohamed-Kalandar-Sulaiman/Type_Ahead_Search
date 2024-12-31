class ElasticsearchQueryBuilder:
    def __init__(self):
        self.query = {"query": {"bool": {"must": []}}}
    
    # Add a term query
    def add_term(self, field, value):
        self.query["query"]["bool"]["must"].append({"term": {field: value}})
        return self
    
    # Add a match query
    def add_match(self, field, value):
        self.query["query"]["bool"]["must"].append({"match": {field: value}})
        return self
    
    # Add a match_phrase query (exact sequence of words)
    def add_match_phrase(self, field, value):
        self.query["query"]["bool"]["must"].append({"match_phrase": {field: value}})
        return self
    
    # Add a range query
    def add_range(self, field, gte=None, lte=None, gt=None, lt=None):
        range_query = {}
        if gte:
            range_query["gte"] = gte
        if lte:
            range_query["lte"] = lte
        if gt:
            range_query["gt"] = gt
        if lt:
            range_query["lt"] = lt
        self.query["query"]["bool"]["must"].append({"range": {field: range_query}})
        return self
    
    # Add a boolean query (must, should, must_not, filter)
    def add_bool(self, must=None, should=None, must_not=None, filter=None):
        bool_query = {"bool": {}}
        
        if must:
            bool_query["bool"]["must"] = must
        if should:
            bool_query["bool"]["should"] = should
        if must_not:
            bool_query["bool"]["must_not"] = must_not
        if filter:
            bool_query["bool"]["filter"] = filter
        
        self.query["query"]["bool"]["must"].append(bool_query)
        return self
    
    # Add a fuzzy query
    def add_fuzzy(self, field, value, fuzziness=1):
        self.query["query"]["bool"]["must"].append({
            "fuzzy": {
                field: {
                    "value": value,
                    "fuzziness": fuzziness
                }
            }
        })
        return self
    
    # Add a wildcard query
    def add_wildcard(self, field, value):
        self.query["query"]["bool"]["must"].append({
            "wildcard": {
                field: value
            }
        })
        return self
    
    # Add a prefix query
    def add_prefix(self, field, value):
        self.query["query"]["bool"]["must"].append({
            "prefix": {
                field: value
            }
        })
        return self
    
    # Add exists query
    def add_exists(self, field):
        self.query["query"]["bool"]["must"].append({
            "exists": {
                "field": field
            }
        })
        return self
    
    # Add ids query
    def add_ids(self, ids):
        self.query["query"]["bool"]["must"].append({
            "ids": {
                "values": ids
            }
        })
        return self
    
    # Add geo_distance query
    def add_geo_distance(self, field, lat, lon, distance):
        self.query["query"]["bool"]["must"].append({
            "geo_distance": {
                "distance": distance,
                "location": {"lat": lat, "lon": lon}
            }
        })
        return self
    
    # Add aggregation (terms aggregation example)
    def add_aggregation(self, name, field, agg_type="terms", size=10):
        if "aggs" not in self.query:
            self.query["aggs"] = {}
        self.query["aggs"][name] = {agg_type: {"field": field, "size": size}}
        return self
    
    # Add more like this query
    def add_more_like_this(self, field, value, min_term_freq=2):
        self.query["query"]["bool"]["must"].append({
            "more_like_this": {
                "fields": [field],
                "like": value,
                "min_term_freq": min_term_freq
            }
        })
        return self
    
    # Add highlighting
    def add_highlighting(self, field):
        if "highlight" not in self.query:
            self.query["highlight"] = {}
        self.query["highlight"]["fields"] = {field: {}}
        return self
    
    # Add pagination
    def add_pagination(self, from_, size):
        self.query["from"] = from_
        self.query["size"] = size
        return self
    
    # Add script score (custom scoring)
    def add_script_score(self, script):
        self.query["query"] = {
            "script_score": {
                "query": self.query["query"],
                "script": {"source": script}
            }
        }
        return self
    
    # Add term vector query
    def add_term_vector(self, doc_id):
        self.query["query"]["term_vector"] = {
            "ids": {"values": [doc_id]}
        }
        return self


    def add_source(self, fields:list):
        self.query["_source"] = fields
        return self
    
    def add_size(self, size:int):
        self.query["size"] = size
        return self
    
    def add_sort(self, field:str, order:str):
        self.query["sort"] = [] if "sort" not in self.query else self.query["sort"]
        self.query["sort"].append(
                                    {field:{
                                        "order":order
                                    }}
                                )
        return self

    
    # Build the final query
    def build(self)->dict:
        return self.query

