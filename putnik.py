"""A small library for rich input.
Adds validation and casting to builtins.input."""

import builtins
from functools import wraps


class TooManyAttempts(Exception): pass


def limiter(limit, error=TooManyAttempts):
    """A decorator that limits the amount of times a function can be called.
    The decorated function can be called `limit` times but will raise an error
    (TooManyAttempts by default) the next time it's called.
    
    """
    def decorating_function(user_function):
        countdown = limit
        
        @wraps(user_function)
        def wrapper(*args, **kwargs):
            nonlocal countdown
            if not countdown: # the final countdown!
                raise error
            countdown -= 1
            return user_function(*args, **kwargs)
        
        return wrapper
    
    return decorating_function


def input(prompt, validation=None, error=None, input=builtins.input):
    """Prompt for a value until it's valid according to the given validation
    function.
    The validation function also acts as a converter function to cast the input
    into the desired data types.
    ValueError exceptions raised inside it are interpreted as invalid inputs.
    
    """
    
    if validation is None:
        validation = lambda v: True
    if error is None:
        error = lambda v: print("{} is not a valid input.".format(v))
    
    while True:
        val = input(prompt)
        try:
            val = validation(val)
        except ValueError:
            error(val)
        else:
            return val


def limited_input(prompt, limit=3, **kwargs):
    """Prompt for a value a limited amount of times (3 by default)."""
    kwargs['input'] = limiter(limit)(kwargs.get('input', builtins.input))
    return input(prompt, **kwargs)
