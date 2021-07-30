from random import random
from typing import Any, List


def even_random_distribution(return_values: List[Any], ratio_of_probabilities: List[float], times: int = 1) -> Any:
    """
    Returns a list of random values, each from the given return_values, based on the probabilities from
    ratio_of_probabilities

    :param return_values: a list of values corresponding to the ratio_of_probabilities list based on how likely each
        outcome is
    :param ratio_of_probabilities: give a list of numbers representing the probabilities of returning certain things
    :param times: number of times to repeat this operation
    :return: a list of random values, each from the given return_values, based on the probabilities from
        ratio_of_probabilities
    """
    returns = []
    for j in range(times):
        r = 1 / sum(ratio_of_probabilities)
        probs = [num * r for num in ratio_of_probabilities]
        rand = random()
        last = True
        for i in range(1, len(probs)):
            probs[i] += probs[i-1]
            if rand < probs[i-1]:
                returns.append(return_values[i-1])
                last = False
                break
        if last:
            returns.append(return_values[-1])
    return returns[:-1]
