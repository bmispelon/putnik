Putnik
======

A small library for rich input that adds validation and casting to builtins.input.

Content
-------

### putnik.input

A drop-in replacement for builtins.input with a few extra parameters:

* validation

    The function that will validate/process the input. Invalid input is signaled by raising ValueError.

* error

    In case of invalid input, that function is called with the raw value given by the user. The default behaviour is to print a simple error message.

* input

    The input function to use. By default, it uses builtins.input but getpass.getpass is another good candidate.


### putnik.limited_input

An extension to putnik.input that will throw an error after a certain amount of
invalid inputs.


Examples
--------

### Integers

    >>> answer = putnik.input("Type a number: ", validation=int)
    Type a number: asdf
    asdf is not a valid input.
    Type a number: 42
    >>> answer
    42


### Booleans

We can create an input function that will return booleans, accepting several values
for True/False.

    def input_bool(prompt, **kwargs):
        """Prompt for yes or no. Return a boolean."""
        yes = {'y', 'yes', '1', 'true', 't'}
        no = {'n', 'no', '0', 'false', 'f'}
        
        def validation(val):
            if val.lower() not in yes | no:
                raise ValueError
            return val.lower() in yes
        
        kwargs['validation'] = validation
        
        return input(prompt, **kwargs)
