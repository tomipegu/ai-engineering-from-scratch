from flask import Flask
from qdrant_client import QdrantClient

app = Flask(__name__)

qdrant = QdrantClient(
    host="qdrant",
    port=6333,
)


@app.get("/")
def home():
    return {"message": "Flask API is running"}


@app.get("/collections")
def collections():
    result = qdrant.get_collections()

    return {"collections": [collection.name for collection in result.collections]}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
    )
