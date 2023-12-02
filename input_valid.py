from typing import Callable, TypeVar

_T = TypeVar('_T', covariant=True)


def input_till_correct(prompt: str, repeat_prompt: str, input_processor: Callable[[str], _T]) -> _T:
    """
    Prompt the user until they get the input valid
    :param prompt: initial prompt printed on the first input
    :param repeat_prompt: subsequent prompt on reentering input
    :param input_processor: a function that take a string and "process" it then returns something.
                            Throw `ValueError` to indicate that the input is invalid and hence
                            the user should be prompted again
    :return: the processed input
    """

    inp = input(prompt)

    while True:
        try:
            return input_processor(inp)
        except ValueError as e:
            inp = input(f"{e}. {repeat_prompt}")
