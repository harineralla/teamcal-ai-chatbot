import json
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

with open('data.json') as file:
    data = json.load(file)

training_sentences = []
training_labels = []
labels = []
responses = {}

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

for intent in data['intents']:
    for pattern in intent['patterns']:
        tokens = nltk.word_tokenize(pattern)
        tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word.lower() not in stop_words]
        clean_pattern = ' '.join(tokens)
        training_sentences.append(clean_pattern)
        training_labels.append(intent['tag'])
    responses[intent['tag']] = intent['responses']
    if intent['tag'] not in labels:
        labels.append(intent['tag'])


tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(training_sentences)
train_sequences = tokenizer.texts_to_sequences(training_sentences)
train_padded = pad_sequences(train_sequences, maxlen=20, padding='post', truncating='post')


label_encoder = LabelEncoder()
training_labels = label_encoder.fit_transform(training_labels)
train_labels = to_categorical(training_labels)

from tensorflow.keras.layers import Dropout, Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.regularizers import l2
from tensorflow.keras.models import Sequential

model = Sequential([
    Embedding(2000, 16, input_length=20),
    GlobalAveragePooling1D(),
    Dense(16, activation='relu', kernel_regularizer=l2(0.01)),
    Dropout(0.5),
    Dense(len(labels), activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Implement early stopping and model checkpointing
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
model_checkpoint = ModelCheckpoint('best_model.keras', monitor='val_loss', save_best_only=True)

# Assume train_padded, train_labels are your training data and labels
# validation_padded, validation_labels are your validation data and labels
history = model.fit(
    train_padded,
    train_labels,
    epochs=50,
    # validation_data=(validation_padded, validation_labels),
    callbacks=[early_stopping, model_checkpoint],
    verbose=1
)


# Save the trained model
model.save("chat_model.keras")

# Save the tokenizer
import pickle
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Save the label encoder
with open('label_encoder.pickle', 'wb') as ecn_file:
    pickle.dump(label_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)