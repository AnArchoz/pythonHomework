# counters
total = correct = male = female = 0
invalidLength = invalidDigit = invalidDate = invalidChecksum = 0
PESEL_LENGTH = 11
PESEL_WEIGHTS = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)


def checkSumCorrect(pesel):
    sourceCheckSum = int(pesel[10])
    sum = 0

    for i in range(len(PESEL_WEIGHTS)):
        sum += (PESEL_WEIGHTS[i] * int(pesel[i]))

    computedCheckSum = (10 - (sum % 10)) % 10

    return sourceCheckSum == computedCheckSum


def dateIsValid(pesel):
    yyyy = int(pesel[0] + pesel[1])
    mm = int(pesel[2] + pesel[3]) % 20
    dd = int(pesel[4] + pesel[5])
    leapYear = False
    centuryCheck = int(pesel[2] + pesel[3])
    daysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if mm <= 0 or mm > 12:
        return False

    if dd <= 0 or dd > 31:
        return False

    if dd > daysInMonths[mm - 1]:
        return False

    # To find exact year
    if mm == centuryCheck:
        yyyy += 1900
    elif mm == centuryCheck - 80:
        yyyy += 1800
    elif mm == centuryCheck - 20:
        yyyy += 2000
    elif mm == centuryCheck - 40:
        yyyy += 2100
    elif mm == centuryCheck - 60:
        yyyy += 2200

    if 1800 > yyyy > 2300:
        return False

    # Check for leap year
    if (yyyy % 4) == 0:
        if (yyyy % 100) == 0:
            if (yyyy % 400) == 0:
                leapYear = True

    if mm == 2:
        if dd > 28 and leapYear is False:
            return False

    return True


def isFemale(pesel):
    return int(pesel[9]) % 2 == 0


file = open("1e3.dat", 'r')

for PESEL in file:
    PESEL = PESEL.strip()
    total += 1

    # verify length
    if len(PESEL) != 11:
        invalidLength += 1
        continue

    if PESEL.isdigit() is not True:
        invalidDigit += 1
        continue

    if dateIsValid(PESEL) is not True:
        invalidDate += 1
        continue

    if checkSumCorrect(PESEL) is not True:
        invalidChecksum += 1
        continue

    if isFemale(PESEL):
        female += 1
        correct += 1
    else:
        male += 1
        correct += 1

file.close()
print("Correct: Female, Male ")
print(correct, female, male, "\n")
print("Invalid: Lengths, Digits, Dates, Checksum ")
print(invalidLength, invalidDigit, invalidDate, invalidChecksum, "\n")
print("Total : ")
print(invalidLength + invalidDigit + invalidDate + invalidChecksum + correct, "\n")
