
#import re for IP address validation
import re

def getValidNumber(min, max):
    isInvalid = True

    while isInvalid:
        try:
            value = input()
            if value == "":
                return value
            else:
                value = int(value)
            if (min <= value <= max) or (value == ""):
                isInvalid = False
            else:
                print("Number out of range, please try again")
        except ValueError:
            print("That was not a number, please try again")

    return value


# taken off https://www.tutorialspoint.com/validate-ip-address-in-python

def validIPAddress():

    isInvalid = True

    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

    address = input("Please enter a valid IP address")
    while isInvalid:
        if re.search(regex, address):
            print("Thank you")
            isInvalid = False
            return address
        else:
            print("Invalid IP address")
            address = input("Please enter a valid IP address")
