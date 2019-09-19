from googletrans import Translator
translator = Translator(service_urls=[
      'translate.google.com',
    ])

translations = translator.translate(['je suis un chat', "j'aime les fraises", 'je ne sais pas'], dest='en')
for translation in translations:
    print(translation.origin, ' -> ', translation.text)