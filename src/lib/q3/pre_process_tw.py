import re
import string

# source of training set
# http://help.sentiment140.com/for-students

re_match_user_name = re.compile("(@[A-Za-z0-9_]{1,15})")
re_match_url = re.compile("(http[s]?[:]?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*:\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)")
re_match_html = re.compile("(&#?[a-z0-9]+;)")


# remove @UserName from review
def removeUserName(review):
    matchObj = re_match_user_name.search(review)
    while matchObj:
        review = review.replace(matchObj.group(1), '')
        matchObj = re_match_user_name.search(review)
    return review


# remove http://URL from review
def removeURL(review):
    matchObj = re_match_url.search(review)
    while matchObj:
        review = review.replace(matchObj.group(1), '')
        matchObj = re_match_url.search(review)
    return review


file_name = 'training.1600000.processed.noemoticon.csv'
reviews = []
total_number_of_review = number_of_negative_review = number_of_positive_review = 0


# remove HTML special char
def removeHtmlChar(review):
    matchObj = re_match_html.search(review)
    while matchObj:
        review = review.replace(matchObj.group(1), '')
        matchObj = re_match_html.search(review)
    return review


with open(file_name, 'r', encoding='utf-8', errors='ignore') as fh:
    for line in fh:
        this_review_begin_index = line.rfind(',"') + len(',"')
        this_review_end_index = line.rfind('"')
        this_review = line[this_review_begin_index:this_review_end_index]
        this_review_polarity = int(line[1])
        total_number_of_review += 1
        # remove the person @ID part at the beginning of review
        this_review = removeUserName(this_review)
        this_review = removeURL(this_review)
        this_review = removeHtmlChar(this_review)
        # remove punctuation from string
        this_review = this_review.translate(str.maketrans('', '', string.punctuation))
        # negative review
        if this_review_polarity == 0:
            reviews.append((0, this_review))
            number_of_negative_review += 1
        # positive review
        elif this_review_polarity == 4:
            reviews.append((1, this_review))
            number_of_positive_review += 1
        # else neutral review
print("total number of review:", total_number_of_review)
print("total number of postive review:", number_of_positive_review)
print("total number of negative review:", number_of_negative_review)
pre_processed_file_name = 'processed_review_tw.csv'
with open(pre_processed_file_name, 'w', encoding='utf-8') as wfh:
    for review_opinion in reviews:
        if review_opinion[1].strip() != '':
            wfh.write(str(review_opinion[0]) + ',' + review_opinion[1].strip() + '\n')
