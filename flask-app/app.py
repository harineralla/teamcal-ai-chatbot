from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import re
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

app = Flask(__name__)
CORS(app)


with open('./data.json', 'r', encoding='utf-8') as file:
    intents_data = json.load(file)
intents = intents_data['intents']

# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
# chatbot = pipeline("text-generation", tokenizer=tokenizer, model=model)

def recognize_intent(user_message):
    user_message = user_message.lower()
    print(f"User Message: {user_message}")
    
    for intent in intents_data['intents']:
        for pattern in intent['patterns']:
            regex_pattern = pattern.lower().replace("{time}", r"\d{1,2}(:\d{2})?\s?(am|pm)?").replace("{day}", r"\b(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b").replace("{participant}", r"[a-zA-Z]+")
            if re.search(regex_pattern, user_message):
                return intent
    return None

def replace_placeholders(response, **kwargs):
    for key, value in kwargs.items():
        response = response.replace(f"{{{key}}}", value)
    return response

@app.route('/')
def home():
    return jsonify({'response': "Hi! What can I help you with today?"})

@app.route('/get_response', methods=['POST'])
def get_response_route():
    try:
        user_message = request.json['message']
        
        intent = recognize_intent(user_message)
        print(f"Recognized Intent: {intent}")
        
        if intent:
            if intent['tag'] == 'schedule_meeting_details':
                time_match = re.search(r'\d{1,2}(:\d{2})?\s?(am|pm)?', user_message)
                day_match = re.search(r'\b(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', user_message)
                time = time_match.group() if time_match else ""
                day = day_match.group() if day_match else ""
                response = replace_placeholders(random.choice(intent['responses']), time=time, day=day)
            elif intent['tag'] == 'add_participant':
                participant_match = re.search(r"[a-zA-Z]+", user_message)
                participant = participant_match.group() if participant_match else "the participant"
                response = replace_placeholders(random.choice(intent['responses']), participant=participant)
            else:
                response = random.choice(intent['responses'])
        else:
            response = "I'm not sure how to respond to that."
        
        return jsonify({'response': response})
    except KeyError as e:
        return jsonify({'error': f"KeyError: {str(e)}. 'message' key not found in request JSON."}), 400
    except Exception as e:
        return jsonify({'error': f"Exception: {str(e)}"}), 500

@app.route('/schedule_meeting', methods=['POST'])
def schedule_meeting():
    try:
        data = request.json
        meeting_title = data.get('title')
        meeting_date = data.get('date')
        meeting_time = data.get('time')
        return jsonify({
            "message": f"Meeting titled '{meeting_title}' scheduled successfully for {meeting_date} at {meeting_time}.",
            "title": meeting_title,
            "date": meeting_date,
            "time": meeting_time
        })
    except KeyError as e:
        return jsonify({'error': f"KeyError: {str(e)}. Missing key in request JSON."}), 400
    except Exception as e:
        return jsonify({'error': f"Exception: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)