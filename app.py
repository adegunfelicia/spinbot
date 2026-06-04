import os
import random
from flask import Flask, request, jsonify
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Render doesn't keep downloaded data across builds reliably, 
# so we ensure NLTK packages download on startup if missing.
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

def get_wordnet_pos(treebank_tag):
    """Maps treebank POS tags to WordNet POS tags"""
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def paraphrase_text(text):
    words = word_tokenize(text)
    tagged_words = pos_tag(words)
    new_words = []

    for word, tag in tagged_words:
        wn_tag = get_wordnet_pos(tag)
        
        # Only try to replace nouns, verbs, adjectives, and adverbs
        if wn_tag is None or not word.isalnum():
            new_words.append(word)
            continue
            
        synonyms = set()
        for syn in wordnet.synsets(word, pos=wn_tag):
            for lemma in syn.lemmas():
                # Replace underscores with spaces for multi-word synonyms
                syn_word = lemma.name().replace('_', ' ')
                # Avoid just capitalizing the same word or using the exact same word
                if syn_word.lower() != word.lower():
                    synonyms.add(syn_word)
        
        if synonyms:
            # Randomly pick a synonym to keep the rewrites dynamic
            chosen_synonym = random.choice(list(synonyms))
            # Match capitalization of original word roughly
            if word.istitle():
                chosen_synonym = chosen_synonym.title()
            new_words.append(chosen_synonym)
        else:
            new_words.append(word)
            
    # Reconstruct the sentence (basic spacing logic)
    return "".join([" " + w if not w.startswith(("'") or w in ".,!?;:") else w for w in new_words]).strip()

@app.route('/', sorted_keys=False)
def home():
    return "Local Rewriter Bot is Running!"

@app.route('/rewrite', methods=['POST'])
def rewrite():
    data = request.json or {}
    original_text = data.get("text", "")
    
    if not original_text:
        return jsonify({"error": "No text provided"}), 400
        
    rewritten_text = paraphrase_text(original_text)
    
    return jsonify({
        "original": original_text,
        "rewritten": rewritten_text
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
