import numpy as np
from imblearn.pipeline import Pipeline


def get_probabilities(text: str, classes: list, model: Pipeline):
    """ Calculates probabilities of text belonging to each model's class.

    Parameters:
    ----------
    text:
        Text for analysis.
    classes:
        Models' classes.
    model:
        The trained model.

    Returns:
    ----------
        Probabilities of finding a word in a particular class.
    """
    probabilities = np.array(
        np.around(model.predict_proba([text])[0], 3), dtype=float
    ).flatten()
    probabilities = dict(zip(classes, probabilities))
    return probabilities
