# Extend a list
simple_list = [1,2,3,4]
simple_list.extend([5,6,7])
print(simple_list)
# Delete item from list
del(simple_list[0])
print(simple_list)


d = {'name': 'Jorge'}
# Get a list of dict items as a tuple
print(d.items())
# Get keys and values ina  for loop
for k, v in d.items():
    print(k,v)
# Delete name from dictionary, creating an empty dictionary
del(d['name'])
print(d)


t = (1,2,3)
# Check index of 1 in the tuple
print(t.index(1))
# Cannot delete from tuple since it is immutable
# del(t[0])


s = {'Max', 'Anna', 'Max'}
# Show that set contains distinct elements only (no repeats)
print(s)
# Cannot delete from set, have to use discard