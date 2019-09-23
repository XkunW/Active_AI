import nltk
import re

class dateOfBirth:
  number_alias={
  'o':'0',
  'zero':'0',
  'a':'1',
  'one':'1',
  'two':'2',
  'three':'3',
  'four':'4',
  'five':'5',
  'six':'6',
  'seven':'7',
  'eight':'8',
  'nine':'9',
  'ten':'10',
  'eleven':'11',
  'twelve':'12',
  'thirteen':'13',
  'fourteen':'14',
  'fifteen':'15',
  'sixteen':'16',
  'seventeen':'17',
  'eighteen':'18',
  'nineteen':'19',
  'twenty':'20',
  'thirty':'30',
  'forty':'40',
  'fifty':'50',
  'sixty':'60',
  'seventy':'70',
  'eighty':'80',
  'ninety':'90',
  'hundred':'00',
  'thousand':'000'}
  month_alias = {
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
  month_abbreviation_alias={
    "jan":1,
    "feb":2,
    "mar":3,
    "apr":4,
    "may":5,
    "jun":6,
    "jul":7,
    "aug":8,
    "sept":9,
    "oct":10,
    "nov":11,
    "dec":12
  }
  date_alias={
    "first":1,
    "second":2,
    "third":3,
    "fourth":4,
    "fifth":5,
    "sixth":6,
    "seventh":7,
    "eighth":8,
    "ninth":9,
    "tenth":10,
    'eleventh':11,
    'twelveth':12,
    'thirteenth':13,
    'fourteenth':14,
    'fifteenth':15,
    'sixteenth':16,
    'seventeenth':17,
    'eighteenth':18,
    'nineteenth':19,
    'twentyth':20,
    'thirtyth':30
  }
  #constructor 
  def __init__(self):
    self.year=0
    self.month=0
    self.date=0

  def is_year_found(self):
    if(self.year!=0):
      return True
    return False

  def is_month_found(self):
    if(self.month!=0):
      return True
    return False

  def is_date_found(self):
    if(self.date!=0):
      return True
    return False

  def get_date(self):
    return self.date

  def get_month(self):
    return self.month

  def get_year(self):
    return self.year

  #internal helper function to parseYear
  #input an array of digits
  #output possbile digits the array trys to represent
  def year_array_to_digits(self, year_array):
    #the longest word in 1900-2019 should be 3 words i.e. nineteen eighty one
    if(len(year_array)>=4):
      year_array=year_array[len(year_array)-3:]
    #concate the number representation together	
    if(len(year_array)<=3):
      current_numbers=year_array[0]
      #rules for concate numbers if the next one is greater that or equal to current one (in order of magnitude) then we concate, otherwise we add
      for i in range(1,len(year_array)):
        if(len(year_array[i-1])<=len(year_array[i])):
          current_numbers=current_numbers+ year_array[i]
        else:
          current_numbers=int(current_numbers)
          current_numbers+=int(year_array[i])
          current_numbers=str(current_numbers)
    return int(current_numbers)

  #only grep for the year information from input_string
  def parse_year(self, input_string):
    all_possible_digits=[]
    input_string=input_string.lower()
    return_year=False
    tokens = nltk.word_tokenize(input_string)
    current_continuous_digits=[]
    all_digits=[]
    #look for NNP, NN, CD, JJ
    for token in tokens:
      #skip the word 'and','-' if we are in the middle of digits representation
      skip_words=['and','-']
      if(token in skip_words):
        continue
      possible_year=-1
      #if current words are word representation of letter
      #convert word to digits
      if(token in self.number_alias):
        possible_year=self.number_alias[token]

      #if current tag is made of digits
      match_obj= re.match('(\d+)',token)
      if(match_obj):
        possible_year=match_obj.group(1)
        #direct hit 
        if(int(possible_year) >=1900 and int(possible_year) <=2200):
          return_year= int(possible_year)
          break

      #we got the digit
      if(possible_year != -1):
        current_continuous_digits.append(possible_year)
      #we don't have a digit anymore reset the currentContinusDigits
      else:
        if(len(current_continuous_digits)!=0):
          all_digits.append(current_continuous_digits)
        current_continuous_digits=[]
    #handle the case where last word is a digit
    if( len(current_continuous_digits)!=0 ):
      all_digits.append(current_continuous_digits)

    #figure out the year
    for possible_year in all_digits:
      year_in_digits=self.year_array_to_digits(possible_year)
      if year_in_digits >=1900 and year_in_digits <=2200:
        return_year= year_in_digits
    if(return_year):
      self.year=return_year
    return return_year

  #only grep for the month information from input_string
  def parse_month(self, input_string):
    month = ["january","february","march","april","may","june","july","august","september","october","november","december"]
    month_abbreviation = ["jan","feb","mar","apr","may","jun","jul","aug","sept","oct","nov","dec"]
    return_month=False

    input_string=input_string.lower()
    tokens = nltk.word_tokenize(input_string)

    #isCurrentWordADigit=False
    all_digits=[]
    for token in tokens:
      #easy case
      if (token in month):
        return_month= self.month_alias[token]
        break
      elif (token in month_abbreviation):
        return_month= self.month_abbreviation_alias[token]
        break

      #hard case month is in digit format
      match_obj = re.match('(\d+)',token)
      if(match_obj):
          possible_months=match_obj.group(1)
          all_digits.append(int(possible_months))

    #we assume the first digits that is <=12 is the month
    for month in all_digits:
      if month<=12:
       return_month= month
       break
    if(return_month):
      self.month= return_month
    return return_month

  def parse_date(self, input_string):
    return_date=False
    input_string=input_string.lower()
    #handle the easy case (\d+)\s*th
    match_obj= re.search("\W+(\d+)\s*th\W+",input_string)
    if(match_obj):
      return_date= int(match_obj.group(1))
      self.date= return_date
      return return_date

    tokens = nltk.word_tokenize(input_string)
    #isCurrentWordADigit=False
    possbileDates=[]
    previousDigit=''
    currentContinusDigits=[]
    for token in tokens:
      #skip the word 'and','-' if we are in the middle of digits representation
      skipWords=['-']

      match_obj= re.match('(\d+)',token)
      if(token in skipWords):
        continue
      #a word with th ending
      if(token in self.date_alias):
        currentDigit= self.date_alias[token]
        #this is a date greater than tenth, so previous word can't represent a number
        if(currentDigit>=10):
          return_date= currentDigit
          break
        else:
          #look at previous word at add with current one
          return_date= int(previousDigit) + currentDigit
          break
      elif(token in self.number_alias):
        currentDigit= self.number_alias[token]
        previousDigit=currentDigit
        #currentContinusDigits.append(currentDigit)
      elif(match_obj):	#handle all number case
        #don't append the year
        if(int(match_obj.group(1))<=31):
          possbileDates.append(int(match_obj.group(1)))
      #else 
      #	not a number

    #assume the second group that is <=31 is the date
    if(len(possbileDates)>=2):
        return_date= possbileDates[1]
    else:
        return_date= possbileDates[0]

    if(return_date):
        self.date= return_date
    return return_date



if __name__ == '__main__':

  #assumption: the sentiense must contain the month date year info. Does not handle 'my birthday is next Friday' case
  '''
  sentence ='My birthday is jan 12th, 2001 '#"My birthday is jan 12th, two thousand and one"
  myDOB1=dateOfBirth()
  myDOB1.parse_date(sentence)
  myDOB1.parse_year(sentence)
  myDOB1.parse_month(sentence)

  print("Your birthday is (YYYY/MM/DD):"+str(myDOB1.get_year())+"/"+str(myDOB1.get_month())+"/"+str(myDOB1.get_date()))
  '''
  #tokens= nltk.word_tokenize(sentence)
  #print(tokens)
  #nltk.download('averaged_perceptron_tagger') first time only
  #tagged = nltk.pos_tag(tokens)

  #print(tagged)
  
  myDOB=dateOfBirth()
  sentence = input("when is your birthday\n>>>")
  myDOB.parse_year(sentence)
  myDOB.parse_month(sentence)
  myDOB.parse_date(sentence)
  while(myDOB.is_date_found()==False or myDOB.is_month_found()==False or myDOB.is_year_found()==False):
    if(myDOB.is_year_found()==False):
      sentence = input("sorry which year is it? I didn't catch that\n>>>")
      year=myDOB.parse_year(sentence)
    if(myDOB.is_month_found()==False):
      sentence = input("sorry which month is it? I didn't catch that\n>>>")
      year=myDOB.parse_month(sentence)
    if(myDOB.is_date_found()==False):
      sentence = input("what's the date again? I didn't catch that\n>>>")
      year=myDOB.parse_date(sentence)

  print("Your birthday is (YYYY/MM/DD):"+str(myDOB.get_year())+'-'+str(myDOB.get_month())+'-'+str(myDOB.get_date()))

