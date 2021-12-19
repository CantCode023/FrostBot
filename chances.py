import random

def Chances(list):
    def sumofchance():
        sum = 0
        for i in list:
            sum += list[i]
        return sum

    def getrandom():
        randomnumber = random.randint(1, sumofchance()+1)

        for i in list:
            if randomnumber < list[i]:
                return i
            else:
                randomnumber -= list[i]

    item = getrandom()
    return item