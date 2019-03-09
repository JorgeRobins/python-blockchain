# Q1: Create a list of names and use a for loop to output the length of each name (len())

nameList = ["Cassandra", "Rebecca", "Jorge", "Natalia"]

for name in nameList:
    print("Name: " + name + " - Length: " + str(len(name)))
print("-" * 20)

# Q2: Add an if check inside the loop to only output names longer than 5 characters.

for name in nameList:
    if len(name) > 5:
        print("Name: " + name + " - Length: " + str(len(name)))
print("-" * 20)

# Q3: Add another if check to see whether a name includes an "n" or "N". Output should be longer than 5 and contains "n" or "N"

for name in nameList:
    if len(name) > 5:
        if ('n' in name) or ('N' in name):
            print("Name: " + name + " - Length: " + str(len(name)))
print("-" * 20)

# Q4: Use a while loop to empty the list of names (via pop()). Ensure the loop exits when it is empty.

while len(nameList) > 0:
    nameList.pop()
    print(nameList)