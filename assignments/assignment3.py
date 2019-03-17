# Q1: Create a list of "person" dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.

people = [{'name': 'Jorge', 'age': '26', 'hobbies': ['Hobby1, Hobby2, Hobby3']},{'name': 'Hugo', 'age': '28', 'hobbies': ['Hobby4, Hobby5, Hobby6']},{'name': 'Luke', 'age': '30', 'hobbies': ['Hobby1, Hobby5, Hobby7']}]

# Q2: Use a list comprehension to convert this list of person into a list of names (of the persons).

names = [el['name'] for el in people]
print('Names in people: ', names)

# Q3: Use a list comprehension to check whether all persons are older than 20

older_than_20 = any([int(el['age']) > 20 for el in people])
print('All persons are older than 20? ', older_than_20)

# Q4: Copy the person list such that you can safely edit the name of the first person (without changing the original list).

# Copying a simple list so we can edit the element without changing the 'names' list.
copied_names = names[:]
copied_names[0] = 'NotJorge'
print('copied_names: ', copied_names)
# Confirm names variable is unchanged
print('names: ', names)

# Q5: Unpack the persons of the original list into different variables and output these variables.

j, h, l = people
print('Person 1: ', j)
print('Person 2: ', h)
print('Person 3: ', l)