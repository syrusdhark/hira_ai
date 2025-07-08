from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os


app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/chat",methods=["POST"])

def chat():
     data = request.get_json()
     prompt = data.get("message")
 
     if not prompt:
        return jsonify({"error": "No message provided"}), 400

     try:
        # Use non-streaming to simplify Flutter side
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
    {
        "role": "system",
        "content": (
            ''' You are Hira, a warm, friendly, and intelligent health assistant who helps users with nutrition, activity, and sleep tracking, be concise, conversational, and kind, avoid repeating introductions or obvious information, give only relevant, clear advice, keep answers short unless asked to elaborate, speak like a human expert would — professional yet easy to talk to, when possible use bullet points or clear formatting for readability, do not overexplain, prioritize usefulness over length, if unsure or not asked about a topic, politely redirect to what's relevant.'''
        )
    },
    {
        "role": "user",
        "content": prompt
    }
],

            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        ai_response = completion.choices[0].message.content
        return jsonify({"response": ai_response})
     except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  
    
    # Each `chunk` is a `ChatCompletionChunk` object
    




