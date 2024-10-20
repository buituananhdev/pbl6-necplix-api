import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    text = re.sub(r'\W', ' ', text).lower().strip()
    words = [word for word in text.split() if word not in set(stopwords.words('english'))]
    legitimatize = WordNetLemmatizer()
    return ' '.join([legitimatize.lemmatize(word) for word in words])
