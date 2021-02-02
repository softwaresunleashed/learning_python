

phrase = "Don't panic!"

''' create a list out of string - phrase '''
plist = list(phrase)

''' initialize phrase and plist '''
print("phrase (before modficaiton) = ", phrase)
print("plist (before modification) = ", plist)

''' transform phrase to new phrase '''

''' extract "on" from list '''
new_phrase = ''.join(plist[1:3])

''' extract "tap" from list... join() takes list as parameter '''
new_phrase = new_phrase + ''.join([plist[5], plist[4]]) + ''.join(plist[7:5:-1])

''' print plist and new phrase '''
print("plist (after modification) = ", plist)
print("phrase (after modification) = ", new_phrase)