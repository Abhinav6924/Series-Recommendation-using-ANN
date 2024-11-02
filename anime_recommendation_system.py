# -*- coding: utf-8 -*-
"""anime_recommendation_system.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YhPvHbF6-wn0NOhLiHF-mLMEpfJkownQ
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Flatten, Dot, Dense
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split

ratings = pd.read_csv('rating.csv')
ratings.replace({-1: np.nan}, inplace = True)
ratings.dropna(inplace = True)

anime=pd.read_csv('anime.csv')
anime['anime_id']=anime['anime_id'].unique()
x=anime.iloc[:,:2].values
dict_anime={i:j for i,j in x}

user_ids = ratings["user_id"].unique().tolist()
user2user_encoded = {x: i for i, x in enumerate(user_ids)}
userencoded2user = {i: x for i, x in enumerate(user_ids)}
anime_ids = ratings["anime_id"].unique().tolist()
anime2anime_encoded = {x: i for i, x in enumerate(anime_ids)}
anime_encoded2anime = {i: x for i, x in enumerate(anime_ids)}
ratings["user"] = ratings["user_id"].map(user2user_encoded)
ratings["anime"] = ratings["anime_id"].map(anime2anime_encoded)

num_users = len(user2user_encoded)
num_animes = len(anime_encoded2anime)
ratings["rating"] = ratings["rating"].values.astype(np.float32)
X = ratings[["user", "anime"]].values
y = ratings["rating"].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

embedding_size = 50
user_input = Input(shape=(1,), name="user_input")
user_embedding = Embedding(num_users, embedding_size, name="user_embedding")(user_input)#converts it to a vector
user_vec = Flatten(name="flatten_users")(user_embedding)#flattens the vector for the model
anime_input = Input(shape=(1,), name="anime_input")
anime_embedding = Embedding(num_animes, embedding_size, name="anime_embedding")(anime_input)
anime_vec = Flatten(name="flatten_animes")(anime_embedding)
dot_product = Dot(name="dot_product", axes=1)([user_vec, anime_vec])#output node
model = Model(inputs=[user_input, anime_input], outputs=dot_product)
#The model consists of two main parts: the user embedding and the anime embedding. Each part is an embedding layer followed by a flatten layer.
# The outputs of the two parts are then merged using a dot product operation, forming a prediction for a user's rating on an anime.

model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit([X_train[:, 0], X_train[:, 1]], y_train, batch_size=64, epochs=5, verbose=1, validation_data=([X_test[:, 0], X_test[:, 1]], y_test))
#The validation data is used to provide a check on the model performance on unseen data.

user_id = user_ids[895]
user_enc = user2user_encoded[user_id]
user_anime_ids = ratings[ratings["user_id"]==user_id]["anime_id"].values
user_anime_ids = [anime2anime_encoded[x] for x in user_anime_ids]
all_anime_ids = np.array(list(set(range(num_animes)) - set(user_anime_ids)))
user_encs = np.array([user_enc] * len(all_anime_ids))
ratings_pred = model.predict([user_encs, all_anime_ids])#gives out the predicted ratings
top_10_indices = ratings_pred.flatten().argsort()[-10:][::-1]#gives out the indices of the sorted order of predicted values
recommended_anime_ids = [anime_encoded2anime[x] for x in top_10_indices]

print("Recommended animes are: ")
for i in recommended_anime_ids:
  print(dict_anime[i],end="\n")

from sklearn.metrics import confusion_matrix,mean_squared_error
y_pred = model.predict([X_test[:, 0], X_test[:, 1]])
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print("Mean Squared Error:", mse)
print("Root Mean Squared Error:", rmse)