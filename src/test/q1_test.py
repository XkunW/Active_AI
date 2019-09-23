import sys
import os
import csv
import colorama
from termcolor import colored

colorama.init()
test_dir = os.path.dirname(__file__)

from active_ai import BirthdayParser

if __name__ == "__main__":
    max_length = 0
    test_cases = []
    test_num = 0
    pass_num = 0
    fail_num = 0
    error_num = 0
    with open(os.path.join(test_dir, "q1_cases.csv"), 'r') as f:
        test_vecs = csv.reader(f)
        for vec in test_vecs:
            test_num += 1
            test_cases.append(vec)
            if len(vec[0]) > max_length:
                max_length = len(vec[0])

    max_length += 6
    for t in test_cases:
        length_diff = max_length - len(t[0]) - 2
        connect_str = " " + "-" * length_diff + " "
        testBP = BirthdayParser()
        testBP.answer = t[0].lower()
        fail = ""
        result = ""
        manual_testing = False
        try:
            testBP.find_birthday(test=True)
            birthday = testBP.get_birthday()
            print(birthday)

            if str(t[1]).lower() != str(birthday["year"]).lower():
                if str(t[1]).lower() == "dynamic" and testBP.in_range("year"):
                    manual_testing = True
                elif not testBP.state.needs_follow_up():
                    fail += "YEAR "
            if str(t[2]).lower() != str(birthday["month"]).lower():
                if str(t[2]).lower() == "dynamic" and testBP.in_range("month"):
                    manual_testing = True
                elif not testBP.state.needs_follow_up():
                    fail += "MONTH "

            if str(t[3]).lower() != str(birthday["day"]).lower():
                if str(t[3]).lower() == "dynamic" and testBP.in_range("day"):
                    manual_testing = True
                elif not testBP.state.needs_follow_up():
                    fail += "DAY "
            if fail != "":
                result = "[" + colored("FAIL", "red") + "] ({})".format(fail.rstrip())
                fail_num += 1
            else:
                result = "[" + colored("PASS", "green") + "]"
                if manual_testing:
                    result += " (Dynamic answer, requires manual testing)"
                pass_num += 1
        except KeyboardInterrupt as error:
            result = "[" + colored("ERROR", "yellow") + "] ({})".format(error)
            error_num += 1
        
        print(t[0] + connect_str + result)

    print("=" * (max_length - 1))
    if pass_num == test_num:
        print("Summary: [" + colored("PASS", "green") + "]")
    else:
        print("Summary: [" + colored("FAIL", "red") + "] ---- {} out of {} passed, {} failed, {} errored".format(pass_num,
                                                                                       test_num,
                                                                                       fail_num,
                                                                                       error_num))
