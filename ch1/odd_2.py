from datetime import datetime
from time import sleep
import random

odds = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19,
        21, 23, 25, 27, 29, 31, 33, 35, 37, 39,
        41, 43, 45, 47, 49, 51, 53, 55, 57, 59]

for iterate in range(5):
    ''' Get current time '''
    right_this_minute = datetime.today().minute

    if right_this_minute in odds:
        print("This minute seems a little odd")
    else:
        print("Not an odd minute")

    '''sleep for some random time before taking next time value '''
    random_seconds=random.randint(1, 10)
    sleep(random_seconds)