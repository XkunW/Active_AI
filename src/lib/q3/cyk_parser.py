import re
import string
import copy

dictionary_rule = dict()
probability_of_dictionary_rule = dict()
combination_rule = dict()
rules = list()
types_of_rule = list()


def load_rules(combination_rule_location, dictionary_rule_location):
    # load the dictionary_rule with its probability
    # file_pattern=re.compile('^label:([N|P]), rule:(.*), probability:(.*)$')
    # global dictionary_rule
    # global probability_of_dictionary_rule
    # with open(dictionary_rule_location,'r',encoding = 'utf-8') as fh:
    #  for line in fh:
    #    matchObj=file_pattern.match(line)
    #    if matchObj:
    # sentence = label
    #      dictionary_rule[matchObj.group(2)]=matchObj.group(1)
    #      probability_of_dictionary_rule[matchObj.group(2)]=matchObj.group(3)
    # load the combination_rule
    # file_pattern=re.compile('^(\S+)\s*,\s*([N|P])\s*->\s*(.*)$')
    # with open(combination_rule_location,'r',encoding = 'utf-8') as fh:
    #  for line in fh:
    #    matchObj=file_pattern.match(line)
    #    if matchObj:
    # rule sentence = (type, label)
    #      combination_rule[str(matchObj.group(3))]=(matchObj.group(1),matchObj.group(2))
    # hand writing combination rule
    global rules
    global types_of_rule
    types_of_rule = ['N', 'P']
    rules = [('N', 'not'),
             ('N', 'doing'),
             ('P', 'well'),
             ('N', 'but'),
             ('N', 'getting'),
             ('P', 'better'),
             ('P', 'now'),
             ('P', 'not', 'N'),
             ('N', 'P', 'but'),
             ('P', 'Im', 'N', 'doing', 'P', 'but')
             ]


def is_array_elements_match(beginning_index, array, sub_array):
    is_array_found = True
    subarray_index = 0
    for index in range(beginning_index, len(sub_array) + beginning_index):
        if array[index] != sub_array[subarray_index]:
            return False
        subarray_index += 1
    return True


def is_array_label_match(beginning_index, row_in_parsing_array, merge_order):
    merge_order_counter = 0
    for index in range(beginning_index, len(merge_order)):
        is_desired_label_found = False
        for tuple_sub_tree in row_in_parsing_array[index]:
            if tuple_sub_tree[0] == merge_order[merge_order_counter]:
                is_desired_label_found = True
                break
        merge_order_counter += 1
        if is_desired_label_found == False:
            return False
    return True


def cyk_parse(input_sentence):
    global rules
    global types_of_rule
    # pre process the sentence so it can match with dictionary and combination rule
    # remove punctuation from string
    input_sentence = input_sentence.translate(str.maketrans('', '', string.punctuation))
    # trim off extra space
    input_sentence_array = input_sentence.split()
    input_sentence = ' '.join(input_sentence.split())
    dimension = len(input_sentence_array)
    bottom_up_parsing_array = [None] * dimension
    # create the 2d triangular array for cyk algorthim
    for index in range(0, dimension):
        bottom_up_parsing_array[index] = [None] * (len(input_sentence_array) - index)

    # loop through all the dictionary rule and see if there are any match
    for rule in rules:
        if len(rule) == 2 and rule[1] not in types_of_rule:
            dict_rule_pattern_array = rule[1].split()
            if len(dict_rule_pattern_array) <= dimension:
                # check starting from which element, the dictionary rule is a full match with input sentence
                for beginning_index in range(0, len(bottom_up_parsing_array[len(dict_rule_pattern_array) - 1])):
                    if is_array_elements_match(beginning_index, input_sentence_array, dict_rule_pattern_array):
                        if bottom_up_parsing_array[len(dict_rule_pattern_array) - 1][
                            beginning_index] == None:  # Label (N or P) , sentence
                            bottom_up_parsing_array[len(dict_rule_pattern_array) - 1][beginning_index] = [
                                (rule[0], rule[1])]
                        else:
                            bottom_up_parsing_array[len(dict_rule_pattern_array) - 1][beginning_index].append(
                                (rule[0], rule[1]))
                        print(len(dict_rule_pattern_array) - 1, beginning_index, rule[0], '->', rule[1])

    for row_index in range(1,
                           dimension):  # sum up the sentence in a bottom up fasion, row_index +1 = length of text span under consideration
        # for text span with length begin at i, end at j+1 = row_index +1
        for beginning_index in range(0, len(bottom_up_parsing_array[row_index])):
            # loop through all combination rule
            for rule in rules:
                if (len(rule) == 2 and rule[1] in types_of_rule):  # replacement rule like NOUN->PP
                    for stored_rule in bottom_up_parsing_array[row_index][beginning_index]:
                        if stored_rule != None:
                            if stored_rule[0] == rule[0]:
                                bottom_up_parsing_array[row_index][beginning_index].append((rule[0], stored_rule[1:]))
                # combination rule like N-> P but
                # Assume there is atmost 2 Non terminal labels in a rule
                if (len(rule) > 2):
                    number_of_labels = 0
                    for element in rule[1:]:
                        if element in types_of_rule:
                            number_of_labels += 1
                    # one label case
                    if number_of_labels == 1:
                        desired_label = ''
                        for element in rule[1:]:
                            if element in types_of_rule:
                                desired_label = element
                        # joining sentence
                        sentence_before_non_terminal = ''
                        sentence_after_non_terminal = ''
                        for element in rule[1:]:
                            if element in types_of_rule:
                                break
                            else:
                                sentence_before_non_terminal = element
                        sentence_before_non_terminal_array_rep = sentence_before_non_terminal.split()
                        is_label_found = False
                        for element in rule[1:]:
                            if is_label_found:
                                sentence_after_non_terminal = element
                            if element in types_of_rule:
                                is_label_found = True

                        sentence_after_non_terminal_array_rep = sentence_after_non_terminal.split()
                        length_for_non_terminal = row_index + 1 - (len(sentence_before_non_terminal_array_rep) + len(
                            sentence_after_non_terminal_array_rep))
                        # the length of non terminal can't be <=0
                        if length_for_non_terminal <= 0:
                            next
                        # go to the appropate place in the 2d array and search for this desired non terminal label
                        check_row = length_for_non_terminal - 1
                        check_col = beginning_index + len(sentence_before_non_terminal_array_rep)
                        # check if the row and col calculated above is in the range
                        if check_row >= 0 and check_row < len(bottom_up_parsing_array):
                            if check_col >= 0 and check_col < len(bottom_up_parsing_array[check_row]):
                                # get the label stored in at this element of 2d array
                                rules_stored = bottom_up_parsing_array[check_row][check_col]
                                if rules_stored != None:
                                    for tuple_sub_tree in rules_stored:
                                        # if Non terminal symbol is a match
                                        if tuple_sub_tree[0] == desired_label:
                                            # check the terminal words exist in the input sentence
                                            is_sentence_before_non_termianl_match = is_array_elements_match(
                                                beginning_index, input_sentence_array,
                                                sentence_before_non_terminal_array_rep)
                                            is_sentence_after_non_terminal_match = is_array_elements_match(
                                                beginning_index + len(
                                                    sentence_before_non_terminal_array_rep) + length_for_non_terminal,
                                                input_sentence_array, sentence_after_non_terminal_array_rep)
                                            # if the terminal words is a match
                                            if is_sentence_before_non_termianl_match and is_sentence_after_non_terminal_match:
                                                # store the appropate label at the corresponding array element
                                                overall_label = rule[0]
                                                store_row = row_index
                                                store_col = beginning_index
                                                print(
                                                'rule', '\'' + overall_label + '->' + str(rule[1:]) + '\'', 'at row',
                                                store_row, 'col', store_col)
                                                if bottom_up_parsing_array[store_row][store_col] == None:
                                                    bottom_up_parsing_array[store_row][store_col] = [(overall_label,
                                                                                                      sentence_before_non_terminal,
                                                                                                      tuple_sub_tree,
                                                                                                      sentence_after_non_terminal)]
                                                else:
                                                    bottom_up_parsing_array[store_row][store_col].append((overall_label,
                                                                                                          sentence_before_non_terminal,
                                                                                                          tuple_sub_tree,
                                                                                                          sentence_after_non_terminal))

                    # two labels case
                    else:
                        desired_labels = []
                        for element in rule[1:]:
                            if element in types_of_rule:
                                desired_labels.append(element)
                        # joining sentence
                        sentence_before_non_terminal = ''
                        senetence_between_non_terminal = ''
                        sentence_after_non_terminal = ''
                        for element in rule[1:]:
                            if element not in types_of_rule:
                                sentence_before_non_terminal = element
                                break
                            if element in types_of_rule:
                                break
                        is_first_element_found = False
                        for element in rule[1:]:
                            if is_first_element_found:
                                sentence_between_non_terminal = element
                                break
                            if element in types_of_rule:
                                is_first_element_found = True
                        number_of_non_terminals = 0
                        for element in rule[1:]:
                            if number_of_non_terminals == 2:
                                sentence_after_non_terminal = element
                                break
                            if element in types_of_rule:
                                number_of_non_terminals += 1
                        sentence_before_non_terminal_array_rep = sentence_before_non_terminal.split()
                        senetence_between_non_terminal_array_rep = sentence_between_non_terminal.split()
                        sentence_after_non_terminal_array_rep = sentence_after_non_terminal.split()
                        space_left_for_non_terminal = row_index + 1 - len(sentence_before_non_terminal_array_rep) - len(
                            senetence_between_non_terminal_array_rep) - len(sentence_after_non_terminal_array_rep)
                        if row_index == 3 and beginning_index == 1:
                            print('space left for non terminal', space_left_for_non_terminal,
                                  len(sentence_before_non_terminal_array_rep),
                                  len(senetence_between_non_terminal_array_rep),
                                  len(sentence_after_non_terminal_array_rep))
                        if space_left_for_non_terminal <= 1:
                            next
                        for first_non_terminal_length in range(1, space_left_for_non_terminal):
                            second_non_terminal_length = space_left_for_non_terminal - first_non_terminal_length
                            first_element_check_row = first_non_terminal_length - 1
                            first_element_check_col = beginning_index + len(sentence_before_non_terminal_array_rep)
                            second_element_check_row = second_non_terminal_length - 1
                            second_element_check_col = beginning_index + len(
                                sentence_before_non_terminal_array_rep) + first_non_terminal_length + len(
                                senetence_between_non_terminal_array_rep)
                            if row_index == 3 and beginning_index == 1:
                                print('first non terminal row:', first_element_check_row, 'first non terminal col:',
                                      first_element_check_col, 'second non terminal row:', second_element_check_row,
                                      'second non terminal col:', second_element_check_col)
                            if first_element_check_row >= 0 and first_element_check_row <= len(bottom_up_parsing_array):
                                if first_element_check_col >= 0 and first_element_check_col <= len(
                                        bottom_up_parsing_array[first_element_check_row]):
                                    if second_element_check_row >= 0 and second_element_check_row <= len(
                                            bottom_up_parsing_array):
                                        if second_element_check_col >= 0 and second_element_check_col <= len(
                                                bottom_up_parsing_array[second_element_check_row]):
                                            if bottom_up_parsing_array[first_element_check_row][
                                                first_element_check_col] != None:
                                                if bottom_up_parsing_array[second_element_check_row][
                                                    second_element_check_col] != None:
                                                    first_subtree = bottom_up_parsing_array[first_element_check_row][
                                                        first_element_check_col]
                                                    second_subtree = bottom_up_parsing_array[second_element_check_row][
                                                        second_element_check_col]
                                                    is_first_label_found = False
                                                    is_second_label_found = False
                                                    for rule_stored in first_subtree:
                                                        if rule_stored[0] == desired_labels[0]:
                                                            is_first_label_found = True
                                                    for rule_stored in second_subtree:
                                                        if rule_stored[0] == desired_labels[1]:
                                                            is_second_label_found = True

                                                    if is_first_label_found and is_second_label_found:
                                                        print('labels found')
                                                        # check the terminal words exist in the input sentence
                                                        is_sentence_before_non_termianl_match = is_array_elements_match(
                                                            beginning_index, input_sentence_array,
                                                            sentence_before_non_terminal_array_rep)
                                                        is_senetence_between_non_terminal_match = is_array_elements_match(
                                                            beginning_index + len(
                                                                sentence_before_non_terminal_array_rep) + first_non_terminal_length,
                                                            input_sentence_array,
                                                            senetence_between_non_terminal_array_rep)
                                                        is_sentence_after_non_terminal_match = is_array_elements_match(
                                                            beginning_index + len(
                                                                sentence_before_non_terminal_array_rep) + first_non_terminal_length + len(
                                                                senetence_between_non_terminal_array_rep) + second_non_terminal_length,
                                                            input_sentence_array, sentence_after_non_terminal_array_rep)
                                                        if is_sentence_before_non_termianl_match and is_senetence_between_non_terminal_match and is_sentence_after_non_terminal_match:
                                                            # store the appropate label at the corresponding array element
                                                            overall_label = rule[0]
                                                            store_row = row_index
                                                            store_col = beginning_index
                                                            print(
                                                            'rule', '\'' + overall_label + '->' + str(rule[1:]) + '\'',
                                                            'at row', store_row, 'col', store_col)
                                                            if bottom_up_parsing_array[store_row][store_col] == None:
                                                                bottom_up_parsing_array[store_row][store_col] = [(
                                                                                                                 overall_label,
                                                                                                                 sentence_before_non_terminal,
                                                                                                                 first_subtree,
                                                                                                                 sentence_between_non_terminal,
                                                                                                                 second_subtree,
                                                                                                                 sentence_after_non_terminal)]
                                                            else:
                                                                bottom_up_parsing_array[store_row][store_col].append((
                                                                                                                     overall_label,
                                                                                                                     sentence_before_non_terminal,
                                                                                                                     first_subtree,
                                                                                                                     sentence_between_non_terminal,
                                                                                                                     second_subtree,
                                                                                                                     sentence_after_non_terminal))

    # print the tree array
    for row_index in range(0, dimension):
        for col_index in range(0, dimension - row_index):
            print(row_index, col_index, bottom_up_parsing_array[row_index][col_index])
    return bottom_up_parsing_array
