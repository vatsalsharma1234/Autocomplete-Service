# Autocomplete Service (Trie + Frequency Ranking)

A lightweight **Autocomplete API** that returns top-k phrase suggestions for a given prefix using a **Trie data structure** with frequency-based ranking.

This project demonstrates efficient prefix search, API design, and practical use of data structures in building low-latency backend services.

---

## Features

- Fast **prefix-based search** using a Trie
- **Top-k ranked suggestions** based on phrase frequency
- REST API for querying suggestions
- Endpoint to **update phrase frequencies dynamically**
- Simple and lightweight architecture
- Easy to extend for large-scale systems

---

## Tech Stack

- **Python**
- **Flask** (REST API)
- **Trie Data Structure**
- JSON APIs


---

## How It Works

### Trie Structure

Each node in the Trie contains:

- `children` → next characters
- `is_word` → indicates end of phrase
- `freq_map` → maps phrases to their frequency

### Query Flow

1. User sends prefix to API
2. Service traverses the Trie using prefix characters
3. Node corresponding to prefix is reached
4. Top-k phrases are returned based on frequency ranking

---

## API Endpoints

### Get Suggestions


GET /autocomplete?q=<prefix>&k=<number>


Example:


GET /autocomplete?q=py&k=5


Response:

```json
{
  "query": "py",
  "k": 5,
  "suggestions": [
    "python tutorial",
    "python flask",
    "python trie"
  ]
}
Update Phrase Frequency

POST /update


Request Body:

{
  "phrase": "python scripts",
  "count": 3
}

Response:

{
  "ok": true,
  "phrase": "python scripts",
  "count": 3
}
Installation & Running
1. Clone the repository
git clone https://github.com/yourusername/autocomplete-service.git
cd autocomplete-service
2. Install dependencies
pip install flask
3. Run the server
python autocomplete_service.py

Server will start at:

http://127.0.0.1:5000
Example Requests

Using curl:

curl "http://127.0.0.1:5000/autocomplete?q=py&k=5"

Update phrase frequency:

curl -X POST -H "Content-Type: application/json" \
-d '{"phrase":"python scripts","count":2}' \
http://127.0.0.1:5000/update
Time Complexity
Operation	Complexity
Insert Phrase	O(L)
Search Prefix	O(P + K log N)

Where:

L = length of phrase

P = length of prefix

K = number of suggestions returned

N = number of phrases under prefix
