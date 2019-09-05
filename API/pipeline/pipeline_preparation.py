from sklearn.pipeline import Pipeline
from .preprocessor import OcrImg, FormatText, LanguageProcessing, ClassifyArticles, AddToDb


pipeline_file_from_img = Pipeline([
    ('Make OCR to img file to get the text', OcrImg()),
    ('Format text', FormatText()),
    ('Identify language + translate to EN if needed', LanguageProcessing()),
    ('Classify articles', ClassifyArticles()),
    ('Add all datas to DB', AddToDb())
])

pipeline_file_from_PDF = Pipeline([
    ('Format text', FormatText()),
    ('Identify language + translate to EN if needed', LanguageProcessing()),
    ('Classify articles', ClassifyArticles()),
    ('Add all datas to DB', AddToDb())
])

