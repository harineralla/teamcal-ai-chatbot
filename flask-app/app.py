# from flask import Flask, request, jsonify
# from transformers import BertTokenizer, BertForSequenceClassification
# import torch
# import random
# import json
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Load model and tokenizer
# model = BertForSequenceClassification.from_pretrained('./model')
# tokenizer = BertTokenizer.from_pretrained('./model')

# # Load intents data
# with open('data.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
# classes = [intent['tag'] for intent in data['intents']]

# def predict_intent(text):
#     inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=64)
#     outputs = model(**inputs)
#     probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
#     confidence, predicted_label = torch.max(probs, dim=1)
#     predicted_intent = classes[predicted_label]
#     return predicted_intent, confidence.item()

# @app.route('/')
# def home():
#     return jsonify({'response': "Hello, this is your AI chatbot."})

# @app.route('/get_response', methods=['POST'])
# def get_response():
#     try:
#         user_message = request.json['message']
#         intent_tag, confidence = predict_intent(user_message)
#         if confidence < 0.7:
#             response = "I'm not sure how to respond to that."
#         else:
#             for intent in data['intents']:
#                 if intent['tag'] == intent_tag:
#                     response = random.choice(intent['responses'])
#                     break
#         return jsonify({'response': response})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run()


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import json
# import random
# import re
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# app = Flask(__name__)
# CORS(app)

# # Initialize ChatGPT
# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
# chatbot = pipeline("text-generation", tokenizer=tokenizer, model=model)

# # Load intents data from JSON file
# with open('./data.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
# intents = data['intents']

# def match_pattern(user_message):
#     for intent in intents:
#         for pattern in intent['patterns']:
#             if re.search(pattern, user_message, flags=re.IGNORECASE):
#                 return random.choice(intent['responses'])
#     return chatbot(user_message)[0]['generated_text']

# @app.route('/')
# def home():
#     return jsonify({'response': "Hi! What can I help you with today?"})

# @app.route('/get_response', methods=['POST'])
# def get_response_route():
#     try:
#         user_message = request.json['message']
#         response = match_pattern(user_message)
#         return jsonify({'response': response})
#     except KeyError as e:
#         return jsonify({'error': f"KeyError: {str(e)}. 'message' key not found in request JSON."}), 400
#     except Exception as e:
#         return jsonify({'error': f"Exception: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import re

app = Flask(__name__)
CORS(app)


with open('./data.json', 'r', encoding='utf-8') as file:
    intents_data = json.load(file)

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

if __name__ == '__main__':
    app.run(debug=True)