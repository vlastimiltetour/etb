import xml.etree.ElementTree as ET
from datetime import datetime

from pathlib import Path
import os

import pandas as pd
import requests
# Library for performing K-means clustering
from sklearn.cluster import KMeans
# %pip install pandas
# Library for text feature extraction
from sklearn.feature_extraction.text import TfidfVectorizer

from .stop_words import cz_stop_words

import pickle 

import logging
logger = logging.getLogger(__name__)

# Library for evaluating the similarity between true and predicted clusters
# Library for finding nearest neighbors based on input data

# https://www.kaggle.com/code/shawamar/product-recommendation-system-for-e-commerce


class RecommenderSystem:
    def __init__(self, cz_stop_words, model_path='./trained_model_data/model.pkl', vectorizer_path='./trained_model_data/vectorizer.pkl', df_path='./trained_model_data/df.pkl'):
        self.cz_stop_words = cz_stop_words
        self.df = None
        self.vectorizer = None
        self.model = None
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.df_path = df_path

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()

        # Load the model and vectorizer if they exist

        if os.path.exists(self.model_path):
            self.load_model()
            print("model loaded in init")
        else:
            print("Model not found. Please train the model first.")

    def save_model(self):
        try:
            with open(self.model_path, 'wb') as model_file:
                pickle.dump(self.model, model_file)
            with open(self.vectorizer_path, 'wb') as vectorizer_file:
                pickle.dump(self.vectorizer, vectorizer_file)
            with open(self.df_path, 'wb') as data_file:
                pickle.dump(self.df, data_file)
            self.logger.info(f"Model and vectorizer saved to {self.model_path} and {self.vectorizer_path}, and {self.df_path}.")
        except Exception as e:
            self.logger.error(f"Error saving model or vectorizer: {e}")

    def load_model(self):
        if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
            try:
                with open(self.model_path, 'rb') as model_file:
                    self.model = pickle.load(model_file)
                with open(self.vectorizer_path, 'rb') as vectorizer_file:
                    self.vectorizer = pickle.load(vectorizer_file)
                with open(self.df_path, 'rb') as data_file:
                    self.df = pickle.load(data_file)
                self.logger.info(f"Model and vectorizer loaded from {self.model_path} and {self.vectorizer_path}.")
            except Exception as e:
                self.logger.error(f"Error loading model or vectorizer: {e}")



      

    def retrieve_product_feed(self):
        # current_time = datetime.now()
        # if self.last_retrieved_time and (current_time - self.last_trained_time) < timedelta(seconds=1):
        #    return self.df
        url = (
            "https://www.efirthebrand.cz/product_feed"  # Replace with your XML feed URL
        )
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            feed_data = response.content
        else:
            print("Failed to retrieve XML data")
        if feed_data:
            root = ET.fromstring(feed_data)

            data = []

            for item in root.findall(".//SHOPITEM"):
                item_id = item.find("ITEM_ID").text
                product_name = item.find("PRODUCTNAME").text
                product = item.find("PRODUCT").text
                category_text = item.find("CATEGORYTEXT").text
                description = item.find("DESCRIPTION").text
                img_url = item.find("IMGURL").text
                price_vat = item.find("PRICE_VAT").text

                data.append(
                    {
                        "ID": item_id,
                        "PRODUCTNAME": product_name,
                        "PRODUCT": product,
                        "CATEGORYTEXT": category_text,
                        "DESCRIPTION": description,
                        "IMGURL": img_url,
                        "PRICE_VAT": price_vat,
                    }
                )

            self.df = pd.DataFrame(data)

            #print(self.df)

            self.last_retrieved_time = datetime.now()
            print("retrieveing product feed", self.last_retrieved_time)
            return self.df

    def train_model(self):
        # current_time = datetime.now()
        # if self.last_retrieved_time and (current_time - self.last_trained_time) < timedelta(hours=24):
        #    return self.model, self.vectorizer

        if self.df is None:
            print(
                "DataFrame is not available. Please call retrieve_product_feed first."
            )
            return

        self.df = self.df.copy()
        # dataframe characteristics

        print("Shape of ratings dataset is: ", self.df.shape, "\n")
        print("Max values in dataset are \n", self.df["PRICE_VAT"].max(), "\n")
        print("Min values in dataset are \n", self.df["PRICE_VAT"].min(), "\n")

        self.df["DESCRIPTION"].shape
        self.df["DESCRIPTION"].head()

        # fill empty values
        self.df.fillna({"DESCRIPTION": ""}, inplace=True)

        # create a vectorizer matrix
        self.vectorizer = TfidfVectorizer(stop_words=cz_stop_words)
        #
        matrix = self.vectorizer.fit_transform(self.df["DESCRIPTION"])
        matrix
        visualized_m = matrix
        kmeans = KMeans(n_clusters=20, init="k-means++")
        kmeans.fit_predict(visualized_m)

        true_k = 18

        self.model = KMeans(n_clusters=true_k, init="k-means++", max_iter=100, n_init=1)
        self.model.fit(matrix)

        print("Top terms per cluster:")
        self.model.cluster_centers_.argsort()[:, ::-1]
        self.vectorizer.get_feature_names_out()

        self.df["cluster_labels"] = kmeans.labels_
        self.df.sort_values(by="cluster_labels", ascending=True)
        self.df["cluster_labels"].value_counts()

        print("traning the model", self.last_retrieved_time)

        self.save_model()
        
        return self.df, self.vectorizer, self.model
    

        
    def recommend_products(self, product_id):
        # Get the product description using the product ID
        #if self.vectorizer is None or self.model is None:
        self.load_model()

        if self.df is None or self.vectorizer is None or self.model is None:
            print("The model is not trained yet. Please call train_model first.")

            return
        try:
            self.df[self.df["ID"] == product_id]["PRODUCTNAME"].values[0]
        except IndexError:
            self.df = None
            return None

        product_desc = self.df[self.df["ID"] == product_id]["DESCRIPTION"].values[0]

        # Transform the product description to a vector representation
        Y = self.vectorizer.transform([product_desc])

        # Predict the cluster for the product
        prediction = self.model.predict(Y)
        first_prediction = prediction[0]

        # Find products in the same cluster
        recommended_products_df = self.df[self.df["cluster_labels"] == first_prediction]

        # Optionally remove the input product from the recommendations, if it's in the list
        if product_id in recommended_products_df["ID"].values:
            recommended_products_df = recommended_products_df[
                recommended_products_df["ID"] != product_id
            ]

        # Get the top 5 recommended products
        """recommended_products = recommended_products_df[["ID", "PRODUCTNAME", "DESCRIPTION"]]

        return product_name, recommended_products
    """
        recommended_products = recommended_products_df["ID"]
        recommended_products = recommended_products.values.tolist()

        print(recommended_products)
        return recommended_products

