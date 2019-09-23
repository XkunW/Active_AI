import random
import re
#import nltk

QUESTIONS = [
  "What's your date of birth?",
  "When is your birthday?",
  "When were you born?",
  "Which year, month and date were you born?"
]

MONTHS = {
  "january" : 1,
  "february" : 2,
  "march": 3,
  "april" : 4,
  "may" : 5,
  "june" : 6,
  "july" : 7,
  "august" : 8,
  "september" : 9,
  "october" : 10,
  "november" : 11,
  "december" : 12
}

month = "(january|february|march|april|may|june|july|august|september|october|november|december)"
month_abb = "(jan|feb|mar|apr|may|jun|jul|aug|sept|oct|nov|dec)"
month_all = "(" + month + "|" + month_abb + ")"

numbers = \
  "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten|\
eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|\
eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|\
ninety|hundred|thousand)"

# we only find years that are 200 years back
date_sep = "(\s*[-|/|,| ]\s*)"

no_leading_num = "(?<!\d)"
sane_year = "(?=[1-2][9|0][0-9][0-9])\d{4}(?!\d)"
sane_month = "([0-1]*[0-9])"
sane_day = "([0-3]*[0-9])"

month_or_day = "("+ sane_month + "|" + sane_day +")"

day_month = "(" + sane_day + "[(st)|(nd)|(th)]*" + date_sep + "(" + month +"|" + month_abb + "))"
month_day = "((" + month + "|" + month_abb + ")" + date_sep + sane_day + "[(st)|(nd)|(th)]*" + ")"

# if we see these format, we are almost sure, just need to make sanity checks
# to see if the numbers makes sense, and maybe shuffle it around to make it make sense
common_date_format = [
                      "(" + no_leading_num + sane_year + date_sep + month_or_day + date_sep + month_or_day + ")",
                      # yyyy-mm-dd, yyyy,mm,dd, yyyy/mm/dd
                      "(" + no_leading_num + month_or_day + date_sep + month_or_day + date_sep + sane_year + ")",
                      # dd-mm-yyyy, dd,mm,yyyy, dd/mm/yyyy
                      "(" + no_leading_num + sane_year + date_sep + day_month  + ")",
                      # 2019, 13, sept etc
                      "(" + no_leading_num + day_month + date_sep + sane_year + ")",
                      "(" + no_leading_num + sane_year + date_sep + month_day  + ")",
                      "(" + no_leading_num + month_day + date_sep + sane_year + ")",
                      ]

re_month = re.compile(month_all)
re_year = re.compile(sane_year)
re_number = re.compile(numbers)

re_common_date_groups = [re.compile(i) for i in common_date_format]


def parse_birthday(s):
  assert(isinstance(s,str))

  user_input = s.lower()
  #print (nltk.pos_tag(nltk.word_tokenize(user_input)))
  print("*"*20, "TESTING", "*"*20)
  res = [ (id, i.search(s)) for id, i in enumerate(re_common_date_groups) if i.search(s) is not None]
  if (len(res)):
    print("have a match for group", res[0][0],"info", res[0][1])
  else:
    print("prob not a valid birthday")
  return s


def main():
  try:
    print("Entering birthday parse, Ctl-C to exit")
    while True:
      prompt_s = QUESTIONS[random.randint(0, len(QUESTIONS)-1)]
      s = input(prompt_s + "\n>>>")
      bithdate = parse_birthday(s)
      print("Ahh, I see")
  except KeyboardInterrupt:
    print("Bye")


if __name__ == "__main__":
  main()
