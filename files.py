# Modes
# r - Read Access Only
# w - Write Access Only
# r+ - Read & Write Access
# x - Wrie Access Only: Exclusive Creation, Fails if File Exists
# a - Write Access Only: Append to End of File if it Exists
# b - Open in Binary Mode (for Writing Binary Data)

# w overwrites the file every time it's opened. Use a for append.
fw = open('data/demo.txt', mode='w')
fw.write('Hello from Python!')
# Python can close automatically but only after the script has completely executed. You can manually call close() like below
fw.close()

# a appends on the same line by default. Use \n to signal new line.
fa = open('data/demo.txt', mode='a')
fa.write('\nAdd this content!')
fa.write('\nAdd this content!')
fa.write('\nAdd this content!')
fa.close()

fr = open('data/demo.txt', mode='r')
# read prints the file content and it reads the entire file and gives one long string
file_content = fr.read()
print(file_content)
fr.close()

fr = open('data/demo.txt', mode='r')
# readlines gives a list of strings and each string is one line
file_content_lines = fr.readlines()
print(file_content_lines)
fr.close()

for line in file_content_lines:
    # removes the last character \n with :-1
    print(line[:-1])


fr = open('data/demo.txt', mode='r')
# readlines gives a list of strings and each string is one line
file_content_single_line = fr.readline()
# steps through the lines one at a time
print(file_content_single_line)
print(file_content_single_line)
print(file_content_single_line)

# print content for each line in the file
while line:
    print(line)
    line = fr.readline()
fr.close()


# Using the "with" Block Statement
# It will automatically close the file
with open('data/demo.txt', mode='w') as fwith:
    fwith.write('Testing if this closes...')
user_input = input('Testing: ')
print('Done!')
