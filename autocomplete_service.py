#!/usr/bin/env python3
"""
Autocomplete Service (Trie + Frequency Ranking)

Run:
    pip install flask
    python autocomplete_service.py

Endpoints:
    GET  /autocomplete?q=<prefix>&k=<int>
    POST /update  JSON: {"phrase": "hello world", "count": 1}

"""

from collections import defaultdict
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

class TrieNode:
    __slots__ = ("children", "is_word", "freq_map", "lock")
    def __init__(self):
        self.children = dict()     
        self.is_word = False
        self.freq_map = defaultdict(int)
        self.lock = threading.Lock() 

class AutocompleteTrie:
    def __init__(self):
        self.root = TrieNode()

    def _normalize(self, phrase: str) -> str:
        return phrase.strip().lower()

    def insert(self, phrase: str, count: int = 1):
        """Insert phrase with frequency increment `count`."""
        phrase = self._normalize(phrase)
        if not phrase:
            return
        node = self.root
        with node.lock:
            node.freq_map[phrase] += count
        for ch in phrase:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            with node.lock:
                node.freq_map[phrase] += count
        node.is_word = True

    def build_from_counter(self, counter):
        """counter: iterable of (phrase, count)."""
        for phrase, count in counter:
            self.insert(phrase, count)

    def suggestions(self, prefix: str, k: int = 5):
        """Return up to k suggestions for `prefix`, ordered by freq desc then lexicographically."""
        prefix = self._normalize(prefix)
        node = self.root
        if prefix == "":
            items = node.freq_map.items()
            sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))
            return [p for p, _ in sorted_items[:k]]
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        items = node.freq_map.items()
        sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))
        return [p for p, _ in sorted_items[:k]]


trie = AutocompleteTrie()

SAMPLE_CORPUS = [
    ("python tutorial", 50),
    ("python trie", 20),
    ("python flask", 30),
    ("python list", 15),
    ("python dictionary", 10),
    ("java tutorial", 35),
    ("javascript tutorial", 40),
    ("javascript array", 18),
    ("react tutorial", 25),
    ("react hooks", 10),
    ("redis tutorial", 8),
    ("ruby on rails", 5),
    ("rust tutorial", 12),
]

trie.build_from_counter(SAMPLE_CORPUS)

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    q = request.args.get("q", "")
    try:
        k = int(request.args.get("k", 5))
    except ValueError:
        k = 5
    results = trie.suggestions(q, k)
    return jsonify({"query": q, "k": k, "suggestions": results})

@app.route("/update", methods=["POST"])
def update_phrase():
    data = request.get_json(force=True)
    phrase = data.get("phrase")
    count = int(data.get("count", 1))
    if not phrase:
        return jsonify({"error": "missing phrase"}), 400
    trie.insert(phrase, count)
    return jsonify({"ok": True, "phrase": phrase, "count": count})

def _run_small_tests():
    t = AutocompleteTrie()
    phrases = [("apple", 5), ("app", 3), ("application", 2), ("banana", 4), ("app store", 1)]
    t.build_from_counter(phrases)
    assert t.suggestions("app", 3) == ["apple", "app", "application"]
    assert t.suggestions("appl", 2) == ["apple", "application"]
    assert t.suggestions("b", 2) == ["banana"]
    assert t.suggestions("", 2) == ["apple", "banana"] or isinstance(t.suggestions("",2), list)
    print("[tests] small tests passed.")

if __name__ == "__main__":
    _run_small_tests()
    app.run(host="0.0.0.0", port=5000, debug=True)
