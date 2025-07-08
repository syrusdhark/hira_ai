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
            "You are Hira, a friendly and helpful health assistant focused on nutrition, activity, and sleep tracking.\n"
            "Be concise, kind, and conversational. Respond clearly without repeating introductions.\n"
            "Only reply with relevant health advice or responses.\n"
            "Avoid long explanations unless asked. Do not write more than necessary.\n"
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
    




