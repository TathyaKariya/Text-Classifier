import tensorflow as tf
from tensorflow import keras
import numpy as np 
import matplotlib.pyplot as plt 

data = keras.datasets.imdb

(train_data, train_labels), (test_data, test_labels) = data.load_data(num_words=880000)

# print(train_data[0])

word_index = data.get_word_index()

word_index = {k:(v+3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

reverse_word_idex = dict([(value, key) for (key, value) in word_index.items()])

# print(len(test_data[0]), len(test_data[1]))
# Unequall length of both the arrays
# Hence we use <PAD> or padding tag to make every lenght of array equal

train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding = "post", maxlen= 250)
test_data = keras.preprocessing.sequence.pad_sequences(test_data, value=word_index["<PAD>"], padding = "post", maxlen= 250)


def decode_review(text):
    return " ".join([reverse_word_idex.get(i, "?") for i in text])

# print(decode_review(train_data[0]))

## MODEL
'''
model = keras.Sequential()
model.add(keras.layers.Embedding(880000, 16)) # Sorts all the words in 16 different categories
model.add(keras.layers.GlobalAveragePooling1D()) # Lowers the demnsion of the network
model.add(keras.layers.Dense(16, activation="relu"))
model.add(keras.layers.Dense(1, activation="sigmoid"))

model.summary()
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
# binary_crossentropy comapres the output and predicted 

x_val = train_data[:10000]
x_train = train_data[10000:]

y_val = train_labels[:10000]
y_train = train_labels[10000:]

fitmodel = model.fit(x_train, y_train, epochs = 40, batch_size=512, validation_data=(x_val, y_val), verbose=1)

results =  model.evaluate(test_data, test_labels)

print(results)

model.save("modelTextClassi.h5")  
# Model has been saved with the name of: modelTextClassi.h5 Now no need to retrain it.
'''
def review_encode(s):
    encoded = [1]

    for word in s:
        if word.lower() in word_index:
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)

    return encoded

model = keras.models.load_model("modelTextClassi.h5")

with open("test.txt", encoding = "utf-8") as f:
    for line in f.readlines():
        nline = line.replace(",", "").replace(".", "").replace("(", "").replace(")","").replace(":","").replace("!", "").replace("\"","").strip().split(" ")
        encode =  review_encode(nline)
        encode = keras.preprocessing.sequence.pad_sequences([encode], value=word_index["<PAD>"], padding = "post", maxlen= 250)
        predict = model.predict(encode)
        print(nline)
        print(encode)
        print(predict[0])