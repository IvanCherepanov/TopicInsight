import pickle
import sklearn
from domain.core.utils import get_path_from_root
from settings import Settings


settings = Settings()

vect_word = pickle.load(open(get_path_from_root('domain/notebook/tf_idf_word_vectorizer'), 'rb'))
logreg = pickle.load(open(get_path_from_root('domain/notebook/logreg_classifier'), 'rb'))


def get_cors_address():
    return [data for data in settings.cors_data.split(',')]
