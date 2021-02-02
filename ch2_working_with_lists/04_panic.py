

phrase = "Don't panic!"

''' create a list out of string - phrase '''
plist = list(phrase)

''' initialize phrase and plist '''
print("phrase (before modficaiton) = ", phrase)
print("plist (before modification) = ", plist)

''' transform phrase to new phrase '''
letters_to_keep = ['o', 'n', 't', 'a', 'p', ' ']

''' remove last few letters "nic!" '''
for i in range(4):
    plist.pop()

for letter in plist:
    if letter not in letters_to_keep:
        plist.remove(letter)

''' swap p & a '''
plist.extend([plist.pop(), plist.pop()])

''' pop space and insert it after "on" '''
plist.insert(2, plist.pop(3))

''' create a string back from a list '''
new_phrase = ''.join(plist)

''' print plist and new phrase '''
print("plist (after modification) = ", plist)
print("phrase (after modification) = ", new_phrase)