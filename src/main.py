#!/usr/bin/env python3
import os
import sys

lib_dir = os.path.join(os.path.dirname(__file__), "lib")
sys.path.append(os.path.join(lib_dir, "birthday_parser"))
sys.path.append(os.path.join(lib_dir, "city_parser"))

from active_ai import BirthdayParser
from active_ai import CityParser


class App:
    def __init__(self):
        welcome_string = "*-" * 40 + "\n" + \
                         "ECE492 Active AI 0.0.1\n" + \
                         "*-" * 40
        print(welcome_string)

    def run(self):
        while True:
            self.BirthdaySession = BirthdayParser()
            self.CitySession = CityParser()
            print("*" * 10, "Testing birthday and city parser", "*" * 10)
            try:
                for question in self.BirthdaySession:
                    # can have your own ouput mechanism here
                    print(question)
                    # can have your own input mechanism here
                    ans = input("\n>>")

                    self.BirthdaySession.add_response(ans)
                    self.BirthdaySession.engage_conversation()
                self.BirthdaySession.dump_result()

                for question in self.CitySession:
                    # can have your own ouput mechanism here
                    print(question)
                    # can have your own input mechanism here
                    ans = input("\n>>")

                    self.CitySession.add_response(ans)
                    self.CitySession.engage_conversation()
                self.CitySession.dump_result()
            except Exception as err:
                print("Something went wrong during the session, \n\tError: ", err)


if __name__ == "__main__":
    demo = App()
    demo.run()
