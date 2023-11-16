import numpy as np

from domain.models.list_theme import domain_tags, categories
from domain.models.main import OuterData, AnswerClassification
from inject import vect_word, logreg


def get_topic(raw_text):
    X_val_tfidf = vect_word.transform([raw_text])
    return np.argmax(logreg.predict_proba(X_val_tfidf), axis=1)[0]


def define_theme_category(item: OuterData):
    answer = AnswerClassification(
        category=domain_tags[categories[get_topic(item.text)]],
        theme=categories[get_topic(item.text)]
    )
    return answer
