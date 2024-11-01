import math


def main():
    creditcardinfo()
    # if (input("retry? y/n: ") == "y"):
    #     main()


def creditcardinfo():
    cardnum = get_cardnumber("Enter Credit Card Number: ")
    n = cardnum
    oddnum = 0
    evennum = 0
    totalnum = 0
    length = 0
    cardtype = 0

    while n > 1:
        j = math.trunc(n / 10)
        j = math.trunc(n - (j * 10))
        # print ("j: " + str(j))

        if iseven(length + 1):
            evennum += evennumbergeneration(j)
        else:
            # print("oddnum")
            oddnum += j

        if length == 15 and j == 5:
            cardtype = cardtype / 10
            cardtype += j * 10
        elif length == 15 and j == 4:
            cardtype = j
        elif length == 14:
            cardtype += j * 10
        elif length == 13:
            cardtype = j
        elif length == 12:
            cardtype = j
        # print("j = " + str(j))
        cardtype = math.trunc(cardtype)
        length += 1
        # print("length: " + str(length))
        n = n / 10

    totalnum = evennum + oddnum
    # print ("final evennum: " + str(evennum) + " oddnum: " + str(oddnum) + " totalnum: " + str(totalnum))
    # print ("cardtype: " + str(cardtype))
    # print ("length: " + str(length))

    if totalnum - (math.trunc((totalnum / 10)) * 10) != 0:
        cardvalidity = "INVALID"
    #     print ("invalid")
    elif cardtype == 4 and (length == 13 or length == 16):
        cardvalidity = "VISA"
    elif (cardtype == 34 or cardtype == 37) and length == 15:
        cardvalidity = "AMEX"
    elif (cardtype == 51 or cardtype == 52 or cardtype == 53 or cardtype == 54 or cardtype == 55) and length == 16:
        cardvalidity = "MASTERCARD"
    else:
        cardvalidity = "INVALID"

    # print("Number: " + str(cardnum))
    print(cardvalidity)


def get_cardnumber(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass


def iseven(n):
    even = False
    if (n - (math.trunc((n / 2)) * 2)) == 0:
        even = True
    else:
        even = False
    return even


def evennumbergeneration(j):
    j = j * 2
    evennum = 0
    if j < 10:
        evennum += j
    else:
        evennum += math.trunc(j / 10)
        evennum += math.trunc((j - (math.trunc(j / 10) * 10)))
    return evennum


main()
