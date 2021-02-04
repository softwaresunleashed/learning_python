
vowels = ['a', 'e', 'i', 'o', 'u']
word = input("Enter word to find vowels in it : ")

''' create an empty dictionary '''
found = {}

''' fill in the vowels '''
found['a'] = 0
found['e'] = 0
found['i'] = 0
found['o'] = 0
found['u'] = 0

''' update frequency of vowels in dictionary '''
for letter in word:
    if letter in vowels:
        found[letter] += 1

print()

''' print the sorted list of vowels and its frequency '''
for k,v in sorted(found.items()):
    print(k, ' was found ', v, ' times.'  )
