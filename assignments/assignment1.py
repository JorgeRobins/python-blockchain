# Q1: Create two variables - one with your name and one with your age. Score bonus points by using the input function.

def get_user_name():
    """ Receive the user name as input """
    user_name = input('Your name: ')
    return user_name


def get_user_age():
    """ Receive the user age as input
        Wrapped in int() so that calculations can be performed with the input
    """
    user_age = int(input('Your age: '))
    return user_age


# Set name variable to the input function
name = get_user_name()

# Set age variable to the input function
age = get_user_age()

# Q2: Create a function which prints your data as one string - concatenation

# Print name by itself
print(name)

# Print age by itself
print(age)

def concat_user_details():
    """ Concatenate the name and age, presented in a sentence
        str() added around age so that the concatenation works after changing get_user_age() to use int() for the decades_lived function
    """
    user_details = 'My name is ' + name + ' and I am ' + str(age) + ' years old'
    return user_details


# Set user details variable to the concatenation function
user_details = concat_user_details()
# Print concatenated output
print(user_details)

# Q3: Create a function which prints ANY data (two arguments) as one string

def concat_args(Arg1, Arg2):
    """ Print two concatenated strings

    Arguments:
        :param Arg1: The first string to be concatenated
        :param Arg2: The second string to be concatenated
    
    """
    args = 'This is my first argument: ' + Arg1 + ' and this is my second argument: ' + Arg2
    return args


args_test = concat_args('ONE', 'TWO')
print(args_test)

# Q4: Create a function which calculates and returns the number of decades you already lived (e.g. 23 = 2 decades)

def decades_lived(age):
    """ Calculates the number of decades lived based on the age provided
    
    Arguments:
        :param age: The age for which the decades should be calculated.
    """
    decade_floor = age // 10
    return decade_floor


decade_age = 'I have lived ' + str(decades_lived(age)) + ' decades'
print(decade_age)