import re
import string

file_name = 'review.csv'

total_number_of_review = number_of_negative_review = number_of_positive_review = 0
reviews = []
with open(file_name, 'r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        matchObj = re.match('^\s*(\d+)\s*\,\s*\"(.*)\"$', line)
        if matchObj:
            digit = matchObj[1]
            review_str = matchObj[2]
            opinion = ''
            if digit == '0':
                opinion = 0
                number_of_negative_review += 1
            else:
                opinion = 1
                number_of_positive_review += 1
            total_number_of_review += 1
            review_str = review_str.replace('Full review in Spanish', '')
            review_str = review_str.replace('Full Review in Spanish', '')
            review_str = review_str.replace('Full Content Review for Parents also available', '')
            if review_str.find('Full Content Review') >= 0:
                review_str = review_str[0:review_str.find('Full Content Review')]
            review_str = review_str.translate(str.maketrans('', '', string.punctuation))
            reviews.append((opinion, review_str))
            if (total_number_of_review % 50 == 0):
                print("processing review number", total_number_of_review)

print("total number of review:", total_number_of_review)
print("total number of postive review:", number_of_positive_review)
print("total number of negative review:", number_of_negative_review)
pre_processed_file_name = 'processed_review.csv'
with open(pre_processed_file_name, 'w', encoding='utf-8') as wfh:
    for review_opinion in reviews:
        wfh.write(str(review_opinion[0]) + ',' + review_opinion[1].strip() + '\n')
