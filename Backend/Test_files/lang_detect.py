import spacy
from spacy_langdetect import LanguageDetector

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

text = "du texte ici, cette fonctionnalité est totalement ok."
doc = nlp(text)

lg = doc._.language
print(lg['language'])