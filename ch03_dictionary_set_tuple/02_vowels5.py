
vowels = ['a', 'e', 'i', 'o', 'u']
word = input("Enter word to find vowels in it : ")

''' create an empty dictionary '''
found = {}

''' update frequency of vowels in dictionary '''
for letter in word:
    if letter in vowels:
        ''' initialize key value pair if key not already present '''
        found.setdefault(letter, 0)
        found[letter] += 1

print()

''' print the sorted list of vowels and its frequency '''
for k,v in sorted(found.items()):
    print(k, ' was found ', v, ' times.'  )
