import os
from flask import Flask, request, jsonify
# If using OpenAI, uncomment the lines below:
# from openai import OpenAI
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route('/', sorted_keys=False)
def home():
    return "Bot is running!"

@app.route('/rewrite', methods=['POST'])
def rewrite_text():
    data = request.json
    original_text = data.get("text", "")
    
    if not original_text:
        return jsonify({"error": "No text provided"}), 400
    
    # --- PLACE YOUR REWRITING LOGIC HERE ---
    # Example placeholder logic:
    rewritten_text = f"Place-holder rewritten version of: {original_text}"
    
    # If using OpenAI, it would look like this:
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": f"Paraphrase this: {original_text}"}]
    # )
    # rewritten_text = response.choices[0].message.content
    # ----------------------------------------

    return jsonify({
        "original": original_text,
        "rewritten": rewritten_text
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
