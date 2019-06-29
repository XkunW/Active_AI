import nltk
import numpy as np

"""
Last/This/Next Thursday
"""


birthday = {
    "day": 0,
    "month": 0,
    "year": 0
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

suffix_map = {
    1: "st",
    2: "nd",
    3: "rd",
    -1: "th"
}

question_list = [
    "When were you born?\n",
    "When is your birthday?\n"
]


def jj_processor(date):
    bday = {
        "day": 0,
        "month": 0,
        "year": 0
    }
    year_composition = []
    for d in date:
        if d in day_map:
            bday["day"] = day_map[d]
            continue
        elif d in month_map:
            bday["month"] = month_map[d]
        elif "-" in d:
            if d[-2:] == "th":
                ten, one = d.split("-")
                bday["day"] = num_map[ten] + day_map[one]
                continue
            else:
                data = d.split("-")
                if data[0].isdigit():
                    for num in data:
                        num = int(num)
                        if num > 31:
                            bday["year"] = num
                        elif num in range(13, 32):
                            print("Day: {}".format(num))
                            bday["day"] = num
                        else:
                            print("Month (or Day): {}".format(num))
                            bday["month"] = num
                            if bday["day"] == 0:
                                bday["day"] = num
                else:
                    ten, one = d.split("-")
                    year_composition.append(num_map[ten] + num_map[one])
                    continue
        elif d in num_map:
            year_composition.append(num_map[d])
            continue
    print(year_composition)
    for i in range(len(year_composition)):
        bday["year"] += year_composition[i] * pow(100, len(year_composition) - 1 - i)
    if bday["month"] in range(1, 13) and bday["day"] in range(1, 13):
        bday["month"] = bday["month"] * 100 + bday["day"]
        bday["day"] = bday["month"]
    return bday


def nn_processor(word):
    bday = {
        "day": 0,
        "month": 0,
        "year": 0
    }
    # If word is a month
    if word in month_map:
        bday["month"] = month_map[word]
    # Otherwise it's a day
    elif "-" in word:
        print("Day: {}".format(word))
        ten, one = word.split("-")
        bday["day"] = num_map[ten] + day_map[one]
    return bday


def number_processor(number):
    bday = {
        "day": 0,
        "month": 0,
        "year": 0
    }
    # If this is a day, return
    if number[-2:] in suffix_map.values():
        bday["day"] = int(number[:-2])
        return bday

    data = []
    temp = ""
    for c in number:
        if not c.isdigit():
            # print("Not digit: {}".format(c))
            data.append(int(temp))
            temp = ""
        else:
            # print("Digit: {}".format(c))
            temp += c
    if temp != "":
        data.append(int(temp))
    # print("Numbers: {}".format(data))
    if len(data) == 1:
        # print("One number")
        num = data[0]
        if num > 31:
            # print("Year")
            bday["year"] = num
        elif num in range(13, 32):
            bday["day"] = num
        else:
            if bday["month"] == 0:
                bday["month"] = num
            elif bday["day"] == 0:
                bday["day"] = num
    else:
        # print("Multiple numbers: {}".format(data))
        for num in data:
            if num > 31:
                bday["year"] = num
            elif num in range(13, 32):
                # print("Day: {}".format(num))
                bday["day"] = num
            else:
                # print("Month (or Day): {}".format(num))
                if bday["month"] == 0:
                    bday["month"] = num
                elif bday["day"] == 0:
                    bday["day"] = num
        if bday["month"] in range(1, 13) and bday["day"] in range(1, 13):
            bday["month"] = bday["month"] * 100 + bday["day"]
            bday["day"] = bday["month"]
    # print("bday: {}".format(bday))
    return bday


def word_checker(word):
    if "-" in word:
        component = word.split("-")
        if len(component) == 2:
            if component[1] in day_map:
                return "day"
            elif component[0] in num_map and component[1] in num_map:
                return "year component"
    for c in word:
        if c.isdigit():
            return "number"  # 1997-06/27, 27th
    if word in num_map:
        return "year component"
    elif word in month_map:
        return "month"
    elif word in day_map:
        return "day"
    else:
        return "word"


def day_processor(word):
    if "-" in word:
        ten, one = word.split("-")
        day = num_map[ten] + day_map[one]
    else:
        day = day_map[word]
    return day


def year_processor(year):
    # print("Year list: {}".format(year))
    bday = {
        "day": 0,
        "month": 0,
        "year": 0
    }
    # there should be at least 2 components and at most 3 components
    if len(year) not in range(2, 4):
        # print("No year specified as word")
        return bday
    # print("Year specified as word")
    num = []
    thousand = False
    for n in year:
        if n.isdigit():
            num.append(int(n))
        else:
            num.append(num_map[n])
        if n == "thousand":
            thousand = True
    if thousand:
        bday["year"] = num[0] * num[1]
        if len(num) == 3:
            bday["year"] += num[2]
    else:
        bday["year"] = num[0] * 100 + num[1]
    return bday


def record_data(bday):
    for d in bday:
        if not in_range(d) and bday[d] != 0:
            birthday[d] = bday[d]


def in_range(type):
    if type == "day":
        if birthday[type] == 0 or birthday[type] > 31:
            return False
    if type == "month":
        if birthday[type] == 0 or birthday[type] > 12:
            return False
    if type == "year":
        if birthday[type] == 0:
            return False
    return True


def answer_processor(answer):
    answer = nltk.word_tokenize(answer)
    # print(answer)
    year = []
    for word in answer:
        category = word_checker(word)
        if category == "month":
            birthday["month"] = month_map[word]
        elif category == "day":
            birthday["day"] = day_processor(word)
        elif category == "year component":
            year.append(word)
        elif category == "number":
            next_word = None
            previous_word = None
            if answer.index(word) + 1 <= len(answer) - 1:
                next_word = answer[answer.index(word) + 1]
                # print("Next word: {}".format(next_word))
            if answer.index(word) - 1 >= 0:
                previous_word = answer[answer.index(word) - 1]
                # print("Previous word: {}".format(previous_word))
            if answer.index(word) - 2 >= 0 and previous_word == "and":
                previous_word = answer[answer.index(word) - 2]
                # print("Previous word: {}".format(previous_word))
            if next_word == "thousand" or next_word == "hundred" or \
                    previous_word == "thousand" or previous_word == "hundred":
                # print("Here")
                year.append(word)
            else:
                bday_data = number_processor(word)
                record_data(bday_data)
    bday_data = year_processor(year)
    record_data(bday_data)


if __name__ == "__main__":
    index = np.random.randint(0, len(question_list))
    answer = input(question_list[index]).lower()
    answer_processor(answer)
    while birthday["month"] == 0 or birthday["day"] == 0:
        answer = input("I'm sorry I didn't quite get your birthday, would you mind repeating your answer?\n").lower()
        answer_processor(answer)
    # print("Got date")
    while birthday["month"] > 12:
        num_1 = int(birthday["month"] % 100)
        num_2 = int((birthday["month"] - num_1) / 100)
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
            # print(answer)
            if month_1 in answer:
                birthday["month"] = num_1
                birthday["day"] = num_2
            else:
                birthday["month"] = num_2
                birthday["day"] = num_1
        else:
            birthday["month"] = num_1
            birthday["day"] = birthday["month"]
    # print("Confirmed date")
    while birthday["year"] == 0:
        answer = input("Would you mind telling me which year were you born?\n").lower()
        answer_processor(answer)
    print("Thank you for your information!")
    print(birthday)
