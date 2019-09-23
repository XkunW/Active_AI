import datetime as dt
import random

import nltk


class BirthdayParser:
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
        "When were you born? ",
        "When is your birthday? ",
        "What's your date of birth? ",
        "Which year, month and date were you born? "
    ]

    response_to_negative_list = [
        "That's OK, I respect your privacy.",
        "That's fine, I understand that you don't want to share this information."
    ]

    # internal state of the parser, specific to each parsing session
    class State:
        def __init__(self):
            self.follow_up = False
            self.conversation_started = False
            self.parse_unsuccessful = False
            self.ask_month_and_day = False
            self.parse_complete = False
            self.parse_ambiguous = False
            self.missing_month = False
            self.day_month_swappable = False
            self.missing_year = False
            self.responses = []

        def needs_follow_up(self):
            return not (self.parse_complete or self.parse_unsuccessful)

    def __init__(self):

        self.answer = ""

        self.birthday = {
            "day": 0,
            "month": 0,
            "year": 0
        }

        self.state = BirthdayParser.State()

    def get_birthday(self):
        if self.state.parse_complete:
            if not self.is_int(self.birthday["month"]):
                self.birthday["month"] = int(self.birthday["month"] - 0.1)
            if not self.is_int(self.birthday["day"]):
                self.birthday["day"] = int(self.birthday["day"] - 0.1)
        return self.birthday

    def __iter__(self):

        while not self.state.parse_complete:

            if not self.state.conversation_started:
                index = random.randint(0, len(BirthdayParser.question_list) - 1)
                yield BirthdayParser.question_list[index]

            elif self.state.parse_unsuccessful:
                yield BirthdayParser.response_to_negative_list[
                    random.randint(0, len(BirthdayParser.response_to_negative_list) - 1)]
                break

            elif self.state.ask_month_and_day or self.state.parse_ambiguous:
                yield "Sorry, I didn't get your date of birth, would you mind telling me that?"

            elif self.state.missing_month:
                yield "Sorry, I didn't get the month of your birth, would you mind telling me that?"

            elif self.state.day_month_swappable:
                yield self.ask_clarification()

            elif self.state.missing_year:
                yield "Would you mind telling me which year were you born?"
            else:
                raise NotImplementedError
            self.state.conversation_started = False

    def add_response(self, response):
        self.state.responses.append(self.answer)
        self.answer = response.strip().lower()

    def engage_conversation(self):
        self.find_birthday()

    def dump_result(self):
        bt = self.get_birthday()
        print("Dumping birthday information:\n")
        print("\tyear :", bt["year"])
        print("\tmonth:", bt["month"])
        print("\tday  :", bt["day"])
        print()

    def reply(self, ans):
        self.answer = ans
        return self.find_birthday()

    def find_birthday(self, test=False):
        assert (len(self.answer))

        if not self.state.conversation_started:
            # gather information
            self.answer_processor()
            # Could not detect any keyword
            if self.birthday["day"] == 0 and \
                    self.birthday["month"] == 0 and \
                    self.birthday["year"] == 0:
                if test:
                    self.birthday["day"] = "N/A"
                    self.birthday["month"] = "N/A"
                    self.birthday["year"] = "N/A"
                else:
                    self.state.parse_unsuccessful = True

            elif not self.in_range("month") and not self.in_range("day"):
                # Missing month and day
                if test:
                    self.birthday["month"] = "follow up"
                    self.birthday["day"] = "follow up"

                self.birthday["month"] = 0
                self.birthday["day"] = 0
                self.state.ask_month_and_day = True

            elif (self.in_range("month") and not self.in_range("day")) or (
                    (self.birthday["month"] == 2 or self.birthday["month"] == 2.1) and self.birthday["day"] > 29):
                self.state.parse_ambiguous = True

            elif not self.in_range("month") and self.in_range("day"):
                self.state.missing_month = True

            # both are in range
            elif not self.is_int(self.birthday["month"]) and not self.is_int(self.birthday["day"]):
                num1 = int(self.birthday["month"])
                num2 = int(self.birthday["day"])
                if num1 == num2:
                    # The numbers are the same, no need to ask again
                    self.birthday["month"] = num1
                    self.birthday["day"] = self.birthday["month"]
                    self.state.parse_complete = True
                else:
                    self.state.day_month_swappable = True

            elif not self.in_range("year"):
                self.state.missing_year = True

            else:
                self.state.parse_complete = True

            self.state.conversation_started = True

        elif self.state.ask_month_and_day:

            response = self.answer_processor()
            if response == "Negative":
                self.state.parse_unsuccessful = True
            else:
                self.state.parse_complete = True

        elif self.state.parse_ambiguous:

            if test:
                self.birthday["day"] = "follow up"
            self.birthday["day"] = 0

            response = self.answer_processor()
            if response == "Negative":
                self.state.parse_unsuccessful = True
            else:
                self.state.parse_complete = True

        elif self.state.missing_month:
            self.birthday["month"] = 0
            response = self.answer_processor()
            if response == "Negative":
                self.state.parse_unsuccessful = True
            else:
                self.state.parse_complete = True

        elif self.state.day_month_swappable:
            if self.clarify():
                self.state.parse_complete = True
            else:
                self.state.parse_unsuccessful = True

        elif self.state.missing_year:
            response = self.answer_processor()
            if response == "Negative":
                self.state.parse_unsuccessful = True
            else:
                self.state.parse_complete = True

        elif self.state.parse_complete:
            if not self.is_int(self.birthday["month"]):
                self.birthday["month"] = int(self.birthday["month"] - 0.1)
            if not self.is_int(self.birthday["day"]):
                self.birthday["day"] = int(self.birthday["day"] - 0.1)

        else:
            assert (False and "unknown state")

    def number_processor(self, number):
        """
        This function processes word in user's answer labeled as "number"
        :param number: Word labeled "number"
        :return: Updates birthday accordingly
        """
        # If this is a day, return
        if number[-2:] in BirthdayParser.suffix_map.values():
            self.birthday["day"] = int(number[:-2])
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

        for num in data:
            self.number_categorizer(num)

    def number_categorizer(self, number):
        """
        This function determines which category in birthday should the provided number fall under
        :param number: Number to be examined
        :return: Updates birthday accordingly
        """
        if number > 31:
            self.change_validate("year", number)
        elif number > 12:
            self.change_validate("day", number)
        elif number > 0:  # When the number is less than 12, it can be either a month or a day
            if not self.in_range("month"):
                self.birthday["month"] = number + 0.1
            elif not self.in_range("day"):
                self.birthday["day"] = number + 0.1

    def word_categorizer(self, word):
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
                if component[1] in BirthdayParser.day_map:
                    return "day"
                elif component[0] in BirthdayParser.num_map and component[1] in BirthdayParser.num_map:
                    return "year component"
        if word in BirthdayParser.num_map:
            return "year component"
        elif word in BirthdayParser.month_map:
            return "month"
        elif word in BirthdayParser.day_map:
            return "day"
        elif word in BirthdayParser.weekday_map:
            return "weekday"
        elif word in BirthdayParser.indicator:
            return "indicator"
        elif word in BirthdayParser.recent_day:
            return "recent"
        else:
            return "word"

    def day_processor(self, word):
        """
        This function maps a word labelled as "day" to a number
        :param word: Word representing a day
        :return: Updates birthday accordingly
        """
        if "-" in word:
            ten, one = word.split("-")
            day = BirthdayParser.num_map[ten] + BirthdayParser.day_map[one]
        else:
            day = BirthdayParser.day_map[word]

        self.change_validate("day", day)

    def weekday_processor(self, previous_word, word):
        """
        This function finds the birthday date from the weekday given and the week BirthdayParser.indicator,
        which has been limited to "last" "this", and "next"
        :param previous_word: The previous word indicating which week
        :param word: Word representing weekday
        :return: Updates birthday accordingly
        """
        bday = {
            "day": 0,
            "month": 0,
        }
        # Only process weekday when week BirthdayParser.indicator exists or weekday is the first word
        if previous_word in BirthdayParser.indicator or previous_word is None:
            curr_year = dt.datetime.today().year
            curr_month = dt.datetime.today().month
            curr_day = dt.datetime.today().day
            curr_weekday = dt.datetime.today().weekday()
            word_day = BirthdayParser.weekday_map[word]
            # A year is a leap year not only if it is divisible by 4,
            # it also has to be divisible by 400 if it is a centurial year
            if (curr_year % 4 == 0 and curr_year % 100 != 0) or curr_year % 400 == 0:
                # Leap year so Feb has 29 days
                BirthdayParser.month_length[1] += 1
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
                    bday["day"] = BirthdayParser.month_length[12] + curr_day + difference
                    bday["month"] = 12
                    curr_year -= 1
                else:
                    bday["day"] = BirthdayParser.month_length[curr_month - 2] + curr_day + difference
                    bday["month"] = curr_month - 1
            # If the time length between today and weekday specified plus today's date is
            # greater than the length of this month
            elif curr_day + difference > BirthdayParser.month_length[curr_month - 1]:
                # The next month is from next year
                if curr_month == 12:
                    bday["day"] = curr_day + difference - BirthdayParser.month_length[12]
                    bday["month"] = 1
                    curr_year += 1
                else:
                    bday["day"] = curr_day + difference - BirthdayParser.month_length[curr_month - 1]
                    bday["month"] = curr_month + 1
            else:
                bday["day"] = curr_day + difference
                bday["month"] = curr_month
            BirthdayParser.month_length[1] -= 1
            self.change_validate("day", bday["day"])
            self.change_validate("month", bday["month"])
            self.change_validate("year", curr_year)

    def year_processor(self, year):
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
        self.change_validate("year", temp_year)

    def recent_day_processor(self, word):
        bday = {
            "day": 0,
            "month": 0,
        }
        curr_month = dt.datetime.today().month
        curr_day = dt.datetime.today().day
        curr_year = dt.datetime.today().year
        if (curr_year % 4 == 0 and curr_year % 100 != 0) or curr_year % 400 == 0:
            # Leap year so Feb has 29 days
            BirthdayParser.month_length[1] += 1
        if word == "yesterday":
            if curr_day == 1:
                if curr_month == 1:
                    bday["month"] = 12
                    curr_year -= 1
                else:
                    bday["month"] = curr_month - 1
                bday["day"] = BirthdayParser.month_length[bday["month"] - 1]
            else:
                bday["day"] = curr_day - 1
                bday["month"] = curr_month
        elif word == "today":
            bday["day"] = curr_day
            bday["month"] = curr_month
        elif word == "tomorrow":
            if curr_day == BirthdayParser.month_length[curr_month - 1]:
                if curr_month == 12:
                    bday["month"] = 1
                    curr_year += 1
                else:
                    bday["month"] = curr_month + 1
                bday["day"] = 1
            else:
                bday["day"] = curr_day + 1
                bday["month"] = curr_month
        BirthdayParser.month_length[1] -= 1
        self.change_validate("day", bday["day"])
        self.change_validate("month", bday["month"])
        self.change_validate("year", curr_year)

    def special_month_processor(self, word):
        curr_month = dt.datetime.today().month
        if word == "last":
            if curr_month == 1:
                temp_month = 12

            else:
                temp_month = curr_month - 1
        elif word == "this":
            temp_month = curr_month
        elif word == "next":
            if curr_month == 12:
                temp_month = 1
            else:
                temp_month = curr_month + 1
        self.change_validate("month", temp_month)

    def special_day_processor(self, special_day):
        if len(special_day) == 2:
            if special_day[0] == "last" and self.in_range("month"):
                if not self.is_int(self.birthday["month"]):
                    month = self.birthday["month"] - 0.1
                else:
                    month = self.birthday["month"]
                curr_year = dt.datetime.today().year
                if (curr_year % 4 == 0 and curr_year % 100 != 0) or curr_year % 400 == 0:
                    # Leap year so Feb has 29 days
                    BirthdayParser.month_length[1] += 1
                temp_day = BirthdayParser.month_length[month - 1]
                BirthdayParser.month_length[1] -= 1
                self.change_validate("day", temp_day)

    def change_validate(self, category, temp_value):
        if not self.in_range(category):
            self.birthday[category] = temp_value

    def in_range(self, category):
        """
        This function checks whether the provided category in birthday is in its reasonable range
        :param category: "month" "day" or "year"
        :return: Provided category in range or not
        """
        if self.birthday[category] == "follow up" or self.birthday[category] == "N/A":
            return True
        if category == "day":
            if self.birthday[category] == 0 or self.birthday[category] > 31.1:
                return False
        elif category == "month":
            if self.birthday[category] == 0 or self.birthday[category] > 12.1:
                return False
        elif category == "year":
            this_year = dt.datetime.today().year
            if self.birthday[category] not in range(this_year - 120, this_year + 1):
                return False
        return True

    def is_int(self, num):
        """
        Checks whether a number is an integer
        :param num: Number to be checked
        :return: Boolean
        """
        string = str(num)
        if string == "follow up":
            return True
        try:
            int(string)
            return True
        except ValueError:
            return False

    def number_converter(self, number):
        if "-" in number:
            ten, one = number.split("-")
            return BirthdayParser.num_map[ten] + BirthdayParser.num_map[one]
        else:
            return BirthdayParser.num_map[number]

    def ask_clarification(self, test=False):
        num_1 = int(self.birthday["month"] - 0.1)
        num_2 = int(self.birthday["day"] - 0.1)
        # The numbers are different, need to confirm format user used
        if num_1 != num_2:
            if test:
                self.birthday["month"] = "follow up"
                self.birthday["day"] = "follow up"
                return
            month_1 = list(BirthdayParser.month_map.keys())[
                list(BirthdayParser.month_map.values()).index(num_1)].capitalize()
            month_2 = list(BirthdayParser.month_map.keys())[
                list(BirthdayParser.month_map.values()).index(num_2)].capitalize()
            if num_1 < 4:
                day_1 = str(num_1) + BirthdayParser.suffix_map[num_1]
            else:
                day_1 = str(num_1) + "th"
            if num_2 < 4:
                day_2 = str(num_2) + BirthdayParser.suffix_map[num_2]
            else:
                day_2 = str(num_2) + "th"

            return "Would you mind to clarify whether your birthday is {} {} or {} {}?\n".format(
                month_1, day_2, month_2, day_1)

    def clarify(self, test=False):
        num_1 = int(self.birthday["month"] - 0.1)
        num_2 = int(self.birthday["day"] - 0.1)
        # The numbers are different, need to confirm format user used
        assert (num_2 != num_1)
        month_1 = list(BirthdayParser.month_map.keys())[
            list(BirthdayParser.month_map.values()).index(num_1)].capitalize()
        month_2 = list(BirthdayParser.month_map.keys())[
            list(BirthdayParser.month_map.values()).index(num_2)].capitalize()
        month_1_abbrev = month_1[0:3]
        month_2_abbrev = month_2[0:3]

        answer = nltk.word_tokenize(self.answer)
        # We can only get clarification if user expressed date in words

        if (month_1.lower() in answer) or \
                (month_1_abbrev.lower() in answer) or \
                ("first" in answer) or \
                ("previous" in answer) or \
                ("former" in answer) or \
                ("prior" in answer) or \
                ("preceding" in answer):
            self.birthday["month"] = num_1
            self.birthday["day"] = num_2
            return True

        elif month_2.lower() in answer or \
                (month_2_abbrev.lower() in answer) or \
                ("second" in answer) or \
                ("last" in answer) or \
                ("following" in answer) or \
                ("latter" in answer) or \
                ("later" in answer) or \
                ("subsequent" in answer) or \
                ("succeeding" in answer):
            self.birthday["month"] = num_2
            self.birthday["day"] = num_1
            return True

    def answer_processor(self):
        """
        This function processes user's answer and updates birthday
        :return: Updates user's birthday
        """
        # Transform user's answer string into a list of words
        answer_list = nltk.word_tokenize(self.answer)
        if "no" in answer_list:
            return "Negative"
        year = []
        special_day = []
        i = 0
        # skip is true if next word is being processed with the current one
        skip = False
        for word in answer_list:
            if skip:
                i += 1
                skip = False
                continue
            category = self.word_categorizer(word)
            if category == "month":
                temp_month = BirthdayParser.month_map[word]
                self.change_validate("month", temp_month)
            elif category == "day":
                self.day_processor(word)
            elif category == "indicator":
                next_word = None
                # Check for next word to see if this is a special day or weekday
                if i + 1 <= len(answer_list) - 1:
                    next_word = answer_list[i + 1]
                if next_word in BirthdayParser.weekday_map:
                    skip = True
                    self.weekday_processor(word, next_word)
                if next_word == "day":
                    skip = True
                    special_day.append(word)
                    special_day.append(next_word)
                if next_word == "month":
                    skip = True
                    self.special_month_processor(word)
            elif category == "recent":
                self.recent_day_processor(word)
            elif category == "weekday":
                # This means no BirthdayParser.indicator, thus current week
                previous_word = None
                self.weekday_processor(previous_word, word)
            elif category == "year component":
                number = self.number_converter(word)
                previous_word = None
                next_word = None
                next_category = None
                # Check neighbor words and determine if this word is correctly categorized
                if i - 1 >= 0:
                    previous_word = answer_list[i - 1]
                if i - 2 >= 0 and (previous_word == "and" or previous_word == "o"):
                    previous_word = answer_list[i - 2]
                previous_category = self.word_categorizer(previous_word)
                if i + 1 <= len(answer_list) - 1:
                    next_word = answer_list[i + 1]
                    next_category = self.word_categorizer(next_word)
                # Mis-categorized scenario: lone number in word form
                if number < 32 and previous_category != "year component" and next_category != "year component":
                    # E.g. twenty third
                    if next_category == "day" and number % 10 == 0:
                        skip = True
                        word = word + "-" + next_word
                        self.day_processor(word)
                    # E.g. twenty-three
                    else:
                        self.number_processor(str(number))
                # Possible mis-categorized scenario: next word is also number in word form but not the previous one
                elif number < 32 and previous_category != "year component" and next_category == "year component":
                    next_number = self.number_converter(next_word)
                    # E.g. twenty three
                    if next_number < 10 and number % 10 == 0:
                        skip = True
                        self.number_processor(str(number + next_number))
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
                # Or previous word is a number in BirthdayParser.num_map
                if next_word == "thousand" or next_word == "hundred" or \
                        previous_word == "thousand" or previous_word == "hundred":
                    year.append(word)
                else:
                    self.number_processor(word)
            i += 1
        self.year_processor(year)
        self.special_day_processor(special_day)
        return "OK"


if __name__ == "__main__":
    bt = BirthdayParser()
    bt.ask()
    bt.find_birthday()
    print(bt.birthday)
