
vowels = ['a', 'e', 'i', 'o', 'u']
word = "Milliways"

''' the list that keeps track of vowels found in word '''
found = []

for letter in word:
    if letter in vowels:
        if letter not in found:
            found.append(letter)

''' Print the list of vowels in the word '''
print(found)
