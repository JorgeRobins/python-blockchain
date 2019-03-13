# Unpacking function arguments

# *args unpacks the arguments into a tuple
# **args unpacks the arguments into a dictionary

def unlimited_arguments(*args, **keyword_args):
    print(args)
    for arg in args:
        print(arg)

    print(keyword_args)
    for k, argument in keyword_args.items():
        print(k, argument)

unlimited_arguments(1,2,3,4, name='Max', age=29)


a = [1,2,3]
# *a unpacks the list and puts the elements as arguments into the string placeholders
some_text = 'Some text: {} {} {}'.format(*a)
print(some_text)