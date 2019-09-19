import pytesseract
from PIL import Image
from sklearn.base import BaseEstimator, TransformerMixin # ??????
import spacy
from spacy_langdetect import LanguageDetector
from googletrans import Translator


# OK
class OcrImg(BaseEstimator, TransformerMixin):
    def fit(self, X, y):
        return self

    def transform(self, X):
        return pytesseract.image_to_string(Image.open(X))


# TO DO:
class FormatText(BaseEstimator, TransformerMixin):
    def fit(self, X, y):
        return self

    def transform(self, X):
        return X


# TO CHECK: should be ok, but syntax and formatting errors is possible + see how to X will be formatted ??
class LanguageProcessing(BaseEstimator, TransformerMixin):
    def fit(self, X, y):
        return self

    def transform(self, X):
        # Load spacy
        nlp = spacy.load("en_core_web_sm")
        # Add language detection to spacy
        nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
        # Analyse text to get the language
        texte_processed = nlp(X)
        texte_language = texte_processed._.language
        if texte_language['language'] != 'en':
            translator = Translator(service_urls=['translate.google.com',])
            translations = translator.translate(X, dest='en')
            translated_text = {}
            for translation in translations:
                translated_text[translation] = translation.text
            final_text = translated_text
        else:
            final_text = X
        return final_text


# TO DO:
class ClassifyArticles(BaseEstimator, TransformerMixin):
    def fit(self, X, y):
        return self

    def transform(self, X):
        return X


# TO DO:
class AddToDb(BaseEstimator, TransformerMixin):
    def fit(self, X, y):
        return self

    def transform(self, X):
        return X