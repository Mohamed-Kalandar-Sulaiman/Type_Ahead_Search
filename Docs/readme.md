# Functional Requirements
    1. A distributed search service , we can focus on type ahead results alone
    2. func Search(prefix string) -> dict()
        - The search api takes in a prefix string and with some optional args
        - Based on prefix various documents needs to be searched
            - Fuzzy Search on primary index
            - Domain
            - AUth

            