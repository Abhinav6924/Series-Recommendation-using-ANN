This script implements the core recommendation functionality using a neural collaborative filtering approach. It processes user and anime data, builds embedding layers for both, and trains a neural network model to predict ratings.

Key Components
Data Loading and Preprocessing:

Loads two datasets:
rating.csv: Contains user ratings for various anime.
anime.csv: Provides additional information about the anime, including anime_id.
Cleans the rating.csv dataset by handling missing values.
Maps user and anime IDs to a unique encoding for embedding.
Model Architecture:

The model is built using Keras with the following layers:
Embedding Layers: Separate embeddings for users and anime.
Dot Layer: Calculates the similarity score between user and anime embeddings.
Dense Layer: A dense layer added for non-linear interactions.
Training and Evaluation:

Splits the data into training and testing sets.
Compiles the model with Mean Squared Error as the loss function.
Trains the model to optimize for predicting user ratings of anime.
Prediction:

The trained model can be used to predict ratings for specific anime based on user preferences.
Requirements
Python
Libraries:
bash
Copy code
pip install numpy pandas tensorflow scikit-learn
Usage
Prepare the Data: Ensure rating.csv and anime.csv are in the same directory as the script.
Run the Script:
bash
Copy code
python anime_recommendation_system.py
Get Recommendations: After training, the model can be used to predict user preferences for anime.
Dataset
rating.csv: User ratings for anime.
anime.csv: Contains anime_id and additional details for each anime.
Future Improvements
Consider adding content-based filtering, a user interface, or additional metrics to improve recommendations.
