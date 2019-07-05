import nltk
import numpy as np
import datetime as dt

birthday = {
    "day": 0,
    "month": 0,
    "year": 0
}

ambiguity = {
    "day": [],
    "month": [],
    "year": []
}


num_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
    "hundred": 100,
    "thousand": 1000
}

day_map = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
    "eleventh": 11,
    "twelfth": 12,
    "thirteenth": 13,
    "fourteenth": 14,
    "fifteenth": 15,
    "sixteenth": 16,
    "seventeenth": 17,
    "eighteenth": 18,
    "nineteenth": 19,
    "twentieth": 20,
    "thirtieth": 30
}

month_map = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12
}

weekday_map = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
    "mon": 0,
    "tu": 1,
    "tue": 1,
    "tues": 1,
    "wed": 2,
    "th": 3,
    "thu": 3,
    "thur": 3,
    "thurs": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6
}

indicator = [
    "last",
    "this",
    "next"
]

recent_day = [
    "yesterday",
    "today",
    "tomorrow"
]

month_length = [
    31,
    28,
    31,
    30,
    31,
    30,
    31,
    31,
    30,
    31,
    30,
    31
]

suffix_map = {
    1: "st",
    2: "nd",
    3: "rd",
    -1: "th"
}

question_list = [
    "When were you born?\n",
    "When is your birthday?\n",
    "What's your date of birth?\n",
    "Which year, month and date were you born?\n"
]

response_to_negative_list = [
    "That's OK, I respect your privacy"
]


def number_processor(number):
    """
    This function processes word in user's answer labeled as "number"
    :param number: Word labeled "number"
    :return: Updates birthday accordingly
    """
    # If this is a day, return
    if number[-2:] in suffix_map.values():
        birthday["day"] = int(number[:-2])
        return

    # Check for delimiters and separates the numbers in a list
    data = []
    temp = ""
    for c in number:
        if not c.isdigit():
            data.append(int(temp))
            temp = ""
        else:
            temp += c
    if temp != "":
        data.append(int(temp))
    # There is no delimiter
    if len(data) == 1:
        num = data[0]
        number_categorize(num)
    else:
        # Delimiter exists, examine each number
        for num in data:
            number_categorize(num)


def number_categorize(number):
    """
    This function determines which category in birthday should the provided number fall under
    :param number: Number to be examined
    :return: Updates birthday accordingly
    """
    if number > 31:
        change_validate("year", number)
    elif number in range(13, 32):
        change_validate("day", number)
    elif number in range(1, 13):  # When the number is less than 12, it can be either a month or a day
        if not in_range("month"):
            birthday["month"] = number + 0.1
        elif not in_range("day"):
            birthday["day"] = number + 0.1

        if in_range("month"):
            if number != birthday["month"] and number + 0.1 != birthday["month"]:
                ambiguity["month"].append(number)
        elif in_range("day"):
            if number != birthday["day"] and number + 0.1 != birthday["day"]:
                ambiguity["day"].append(number)


def word_categorize(word):
    """
    This function labels each word in user's answer
    :param word: Word from user's answer
    :return: Label of the word
    """
    # Check for digit in word first, if digit present, return label "number"
    for c in word:
        if c.isdigit():
            return "number"
    # If "-" is in the word, then it is most likely number in word expression, representing day or part of year
    if "-" in word:
        component = word.split("-")
        if len(component) == 2:
            if component[1] in day_map:
                return "day"
            elif component[0] in num_map and component[1] in num_map:
                return "year component"
    if word in num_map:
        return "year component"
    elif word in month_map:
        return "month"
    elif word in day_map:
        return "day"
    elif word in weekday_map:
        return "weekday"
    elif word in indicator:
        return "indicator"
    elif word in recent_day:
        return "recent"
    else:
        return "word"


def day_processor(word):
    """
    This function maps a word labelled as "day" to a number
    :param word: Word representing a day
    :return: Updates birthday accordingly
    """
    if "-" in word:
        ten, one = word.split("-")
        day = num_map[ten] + day_map[one]
    else:
        day = day_map[word]

    change_validate("day",day)


def weekday_processor(previous_word, word):
    """
    This function finds the birthday date from the weekday given and the week indicator,
    which has been limited to "last" "this", and "next"
    :param previous_word: The previous word indicating which week
    :param word: Word representing weekday
    :return: Updates birthday accordingly
    """
    bday = {
        "day": 0,
        "month": 0,
    }
    # Only process weekday when week indicator exists or weekday is the first word
    if previous_word in indicator or previous_word is None:
        curr_year = dt.datetime.today().year
        curr_month = dt.datetime.today().month
        curr_day = dt.datetime.today().day
        curr_weekday = dt.datetime.today().weekday()
        word_day = weekday_map[word]
        # A year is a leap year not only if it is divisible by 4,
        # it also has to be divisible by 400 if it is a centurial year
        if (curr_year % 4 == 0 and curr_year % 100 != 0) or curr_year % 400 == 0:
            # Leap year so Feb has 29 days
            month_length[1] += 1
        # difference is the number of days between today and the weekday specified
        difference = 0
        if previous_word == "last":
            difference -= 7
        if previous_word == "next":
            difference += 7
        difference += word_day - curr_weekday
        # If the time length between today and weekday specified is greater than the days elapsed this month
        if curr_day + difference < 0:
            # The last month is from previous year
            if curr_month == 1:
                bday["day"] = month_length[12] + curr_day + difference
                bday["month"] = 12
            else:
                bday["day"] = month_length[curr_month - 2] + curr_day + difference
                bday["month"] = curr_month - 1
        # If the time length between today and weekday specified plus today's date is
        # greater than the length of this month
        elif curr_day + difference > month_length[curr_month - 1]:
            # The next month is from next year
            if curr_month == 12:
                bday["day"] = curr_day + difference - month_length[12]
                bday["month"] = 1
            else:
                bday["day"] = curr_day + difference - month_length[curr_month - 1]
                bday["month"] = curr_month + 1
        else:
            bday["day"] = curr_day + difference
            bday["month"] = curr_month
        month_length[1] -= 1
        change_validate("day", bday["day"])
        change_validate("month", bday["month"])


def year_processor(year):
    """
    This function generates year from the year list gathered from user's answer
    :param year: Year list containing the numbers to contruct this year
    :return: Updates birthday year accordingly
    """
    # There should be at least 2 components and at most 3 components
    if len(year) not in range(2, 4):
        return
    # Year is expressed in word form
    num = []
    special_year = False
    for n in year:
        num.append(int(n))
        if n == 1000 or n == 100:
            special_year = True
    # "thousand" or "hundred" is present in the user's answer ==> n * 1000 or 100 + 10s + 1s
    if special_year:
        temp_year = num[0] * num[1]
        for i in range(2, len(num)):
            temp_year += num[i]
    # Regular word expression
    else:
        temp_year = num[0] * 100
        for i in range(1, len(num)):
            temp_year += num[i]
    change_validate("year", temp_year)


def recent_day_processor(word):
    bday = {
        "day": 0,
        "month": 0,
    }
    curr_month = dt.datetime.today().month
    curr_day = dt.datetime.today().day
    curr_year = dt.datetime.today().year
    if (curr_year % 4 == 0 and curr_year % 100 != 0) or curr_year % 400 == 0:
        # Leap year so Feb has 29 days
        month_length[1] += 1
    if word == "yesterday":
        if curr_day == 1:
            if curr_month == 1:
                bday["month"] = 12
            else:
                bday["month"] = curr_month - 1
            bday["day"] = month_length[bday["month"] - 1]
        else:
            bday["day"] = curr_day - 1
            bday["month"] = curr_month
    elif word == "today":
        bday["day"] = curr_day
        bday["month"] = curr_month
    elif word == "tomorrow":
        if curr_day == month_length[curr_month - 1]:
            if curr_month == 12:
                bday["month"] = 1
            else:
                bday["month"] = curr_month + 1
            bday["day"] = 1
        else:
            bday["day"] = curr_day + 1
            bday["month"] = curr_month
    month_length[1] -= 1
    change_validate("day", bday["day"])
    change_validate("month", bday["month"])


def special_month_processor(indicator):
    curr_month = dt.datetime.today().month
    if indicator == "last":
        if curr_month == 1:
            temp_month = 12
        else:
            temp_month = curr_month - 1
    elif indicator == "this":
        temp_month = curr_month
    elif indicator == "next":
        if curr_month == 12:
            temp_month = 1
        else:
            temp_month = curr_month + 1
    change_validate("month", temp_month)


def special_day_processor(special_day):
    if len(special_day) == 2:
        if special_day[0] == "last" and in_range("month"):
            if not is_int(birthday["month"]):
                month = birthday["month"] - 0.1
            else:
                month = birthday["month"]
            curr_year = dt.datetime.today().year
            if (curr_year % 4 == 0 and curr_year % 100 != 0) or curr_year % 400 == 0:
                # Leap year so Feb has 29 days
                month_length[1] += 1
            temp_day = month_length[month - 1]
            month_length[1] -= 1
            change_validate("day", temp_day)


def change_validate(category, temp_value):
    if not in_range(category):
        birthday[category] = temp_value
    else:
        if temp_value != birthday[category]:
            ambiguity[category].append(temp_value)


def in_range(category):
    """
    This function checks whether the provided category in birthday is in its reasonable range
    :param category: "month" "day" or "year"
    :return: Provided category in range or not
    """
    if category == "day":
        if birthday[category] == 0 or birthday[category] > 31:
            return False
    if category == "month":
        if birthday[category] == 0 or birthday[category] > 12:
            return False
    if category == "year":
        this_year = dt.datetime.today().year
        if birthday[category] not in range(this_year - 120, this_year + 1):
            return False
    return True


def is_int(num):
    """
    Checks whether a number is an integer
    :param num: Number to be checked
    :return: Boolean
    """
    string = str(num)
    try:
        int(string)
        return True
    except ValueError:
        return False


def number_converter(number):
    if "-" in number:
        ten, one = number.split("-")
        return num_map[ten] + num_map[one]
    else:
        return num_map[number]


def answer_processor(answer):
    """
    This function processes user's answer and updates birthday
    :param answer: User's answer string
    :return: Updates user's birthday
    """
    # Transform user's answer string into a list of words
    answer_list = nltk.word_tokenize(answer)
    if "no" in answer_list:
        return "Negative"
    year = []
    special_day = []
    special_month = []
    i = 0
    # skip is true if next word is being processed with the current one
    skip = False
    for word in answer_list:
        if skip:
            i += 1
            skip = False
            continue
        category = word_categorize(word)
        if category == "month":
            temp_month = month_map[word]
            if not in_range("month"):
                birthday["month"] = temp_month
            else:
                if temp_month != birthday["month"]:
                    ambiguity["month"].append(temp_month)
        elif category == "day":
            day_processor(word)
        elif category == "indicator":
            next_word = None
            # Check for next word to see if this is a special day or weekday
            if i + 1 <= len(answer_list) - 1:
                next_word = answer_list[i + 1]
            if next_word in weekday_map:
                skip = True
                weekday_processor(word, next_word)
            if next_word == "day":
                skip = True
                special_day.append(word)
                special_day.append(next_word)
            if next_word == "month":
                skip = True
                special_month_processor(word)
        elif category == "recent":
            recent_day_processor(word)
        elif category == "weekday":
            # This means no indicator, thus current week
            previous_word = None
            weekday_processor(previous_word, word)
        elif category == "year component":
            number = number_converter(word)
            previous_word = None
            next_word = None
            previous_category = None
            next_category = None
            # Check neighbor words and determine if this word is correctly categorized
            if i - 1 >= 0:
                previous_word = answer_list[i - 1]
            if i - 2 >= 0 and (previous_word == "and" or previous_word == "o"):
                previous_word = answer_list[i - 2]
            previous_category = word_categorize(previous_word)
            if i + 1 <= len(answer_list) - 1:
                next_word = answer_list[i + 1]
                next_category = word_categorize(next_word)
            # Mis-categorized scenario: lone number in word form
            if number < 32 and previous_category != "year component" and next_category != "year component":
                # E.g. twenty third
                if next_category == "day" and number % 10 == 0:
                    skip = True
                    word = word + "-" + next_word
                    day_processor(word)
                # E.g. twenty-three
                else:
                    number_processor(str(number))
            # Possible mis-categorized scenario: next word is also number in word form but not the previous one
            elif number < 32 and previous_category != "year component" and next_category == "year component":
                next_number = number_converter(next_word)
                # E.g. twenty three
                if next_number < 10 and number % 10 == 0:
                    skip = True
                    number_processor(str(number + next_number))
                else:
                    year.append(number)
            else:
                year.append(number)
        elif category == "number":
            next_word = None
            previous_word = None
            if i + 1 <= len(answer_list) - 1:
                next_word = answer_list[i + 1]
            if i - 1 >= 0:
                previous_word = answer_list[i - 1]
            # If previous word is "and" or "o", then we check one word before that to determine
            # whether this number is part of year
            if i - 2 >= 0 and (previous_word == "and" or previous_word == "o"):
                previous_word = answer_list[i - 2]
            # Only when there is a "thousand" or "hundred" present around the number that this is part of year
            # Or previous word is a number in num_map
            if next_word == "thousand" or next_word == "hundred" or \
                    previous_word == "thousand" or previous_word == "hundred":
                year.append(word)
            else:
                number_processor(word)
        i += 1
    year_processor(year)
    special_day_processor(special_day)
    # print(birthday)
    return "OK"


if __name__ == "__main__":
    index = np.random.randint(0, len(question_list))
    answer = input(question_list[index]).lower()
    answer_processor(answer)
    while not in_range("month") and not in_range("day"):
        # Missing month and day
        birthday["month"] = 0
        birthday["day"] = 0
        answer = input("Sorry, I didn't quite get your birthday, would you mind repeating your answer?\n").lower()
        response = answer_processor(answer)
        if response == "Negative":
            print("That's OK, I respect your privacy")
            break
    while (in_range("month") and not in_range("day")) or (birthday["month"] == 2 and birthday["day"] > 29):
        # Missing day only or Feb out of range
        birthday["day"] = 0
        answer = input("Sorry, I didn't quite get the day of your birth, would you mind telling me that?\n").lower()
        response = answer_processor(answer)
        if response == "Negative":
            print("That's OK, I respect your privacy")
            break
    while not in_range("month") and in_range("day"):
        # Missing month only
        birthday["month"] = 0
        answer = input("Sorry, I didn't quite get the month of your birth, would you mind telling me that?\n").lower()
        response = answer_processor(answer)
        if response == "Negative":
            print("That's OK, I respect your privacy")
            break
    while not is_int(birthday["month"]) and not is_int(birthday["day"]):
        # Month and day both less than 12 and expressed as numbers
        num_1 = int(birthday["month"] - 0.1)
        num_2 = int(birthday["day"] - 0.1)
        # The numbers are different, need to confirm format user used
        if num_1 != num_2:
            month_1 = list(month_map.keys())[list(month_map.values()).index(num_1)].capitalize()
            month_2 = list(month_map.keys())[list(month_map.values()).index(num_2)].capitalize()
            if num_1 < 4:
                day_1 = str(num_1) + suffix_map[num_1]
            else:
                day_1 = str(num_1) + "th"
            if num_2 < 4:
                day_2 = str(num_2) + suffix_map[num_2]
            else:
                day_2 = str(num_2) + "th"

            answer = input("Would you mind to clarify whether your birthday is {} {} or {} {}?\n".format(
                month_1, day_2, month_2, day_1)).lower()
            answer = nltk.word_tokenize(answer)
            # We can only get clarification if user expressed date in words
            if month_1.lower() in answer:
                birthday["month"] = num_1
                birthday["day"] = num_2
            elif month_2.lower() in answer:
                birthday["month"] = num_2
                birthday["day"] = num_1
        # The numbers are the same, no need to ask again
        else:
            birthday["month"] = num_1
            birthday["day"] = birthday["month"]
    if not is_int(birthday["month"]):
        birthday["month"] = int(birthday["month"] - 0.1)
    if not is_int(birthday["day"]):
        birthday["day"] = int(birthday["day"] - 0.1)
    while not in_range("year"):
        # Missing year
        answer = input("Would you mind telling me which year were you born?\n").lower()
        response = answer_processor(answer)
        if response == "Negative":
            print("That's OK, I respect your privacy")
            break
    """
    while len(ambiguity["day"]) > 0 or len(ambiguity["month"]) > 0 or len(ambiguity["year"]) > 0:
        if len(ambiguity["day"]) > 0:
            ambiguity["day"] = []
            birthday["day"] = 0
            answer = input("Sorry, would you mind telling me again which day is your birthday?\n")
    """
    print("Thank you for your information!")
    print(birthday)
