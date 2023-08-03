from elasticsearch import Elasticsearch
import csv

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200'], http_auth=('elastic', '4txXMiNr-m5uwU3Omr0e'))

# Index name and mapping
index_name = 'your_index_name3'
mapping = {
    'properties': {
        'field1': {'type': 'text'},
        'field2': {'type': 'text'},
        # Add more field mappings here
    }
}

# Create the index
es.indices.create(index=index_name, body={'mappings': mapping})

# Read CSV file and index data
with open('FileCommits.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Create document to be indexed
        document = {
            'field1': row['author_name'],
            'field2': row['author_email'],
            # Add more fields here according to your CSV columns
        }

    # Index the document
    es.index(index=index_name, body=document)

# Refresh the index to make documents searchable
es.indices.refresh(index=index_name)
