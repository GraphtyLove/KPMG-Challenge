from tika import parser
import spacy
from spacy_langdetect import LanguageDetector

# Extract text from a document
raw = parser.from_file('test.pdf')

# Load SpaCy to detect the language
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

# Detect the language
doc = nlp(raw['content'])
print(doc._.language)