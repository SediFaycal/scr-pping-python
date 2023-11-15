# Import des packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
from nltk import FreqDist, word_tokenize
from nltk.corpus import stopwords
import nltk


nltk.download('punkt')
nltk.download('stopwords')


url = "http://feeds.bbci.co.uk/news/rss.xml"

# code de la page
reponse = requests.get(url)
soup = BeautifulSoup(reponse.text, "html.parser")

items = soup.findAll('item')

news_items = []

for i in items:
    news_i = {}
    news_i['title'] = i.title.text
    news_i['description'] = i.description.text
    news_i['pubdate'] = i.pubdate.text
    news_items.append(news_i)

# Convertir en DataFrame
df = pd.DataFrame(news_items, columns=['title', 'description', 'pubdate'])

# Analyse des mots fréquents
all_descriptions = df['description'].astype(str)


stop_words = set(stopwords.words('english'))
tokenized_descriptions = [word_tokenize(desc) for desc in all_descriptions]
filtered_tokens = [[word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words] for tokens in tokenized_descriptions]

# Calcul des fréquences
freq_dist = FreqDist([word for sublist in filtered_tokens for word in sublist])

# Ajouter une colonne au DataFrame avec la liste des mots fréquents
df['frequent_words'] = filtered_tokens

# Supprimer la colonne 'description'
df = df.drop(columns=['description'])

# Enregistrement en CSV avec les colonnes supplémentaires
df.to_csv('scrapping_bbc.csv', index=False, encoding='utf-8')

# Afficher les 10 mots les plus fréquents
print("Mots fréquents:")
print(freq_dist.most_common(10))


# Afficher les produits les plus mentionnés
print("\nles produits les plus mentionnés:")

