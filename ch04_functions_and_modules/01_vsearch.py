

def search4vowels():
    ''' Display any vowels found in an asked-for word. '''
    vowels = {'a', 'e', 'i', 'o', 'u'}
    word = input("Enter word to find vowels in it : ")

    ''' the list that keeps track of vowels found in word '''
    found = vowels.intersection(set(word))

    ''' Print the list of vowels in the word '''
    print(found)

