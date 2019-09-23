import re

comb_rule_capture_groups = list()


def compile_combination_rule_capture_group(Gc):
    global comb_rule_capture_groups
    comb_rule_capture_groups = list()
    for (rule_type, rule) in Gc:
        if rule_type == 'negation':
            regex_matching = ''
            for rule_index in range(1, len(rule)):
                rule_component = rule[rule_index]
                if rule_component == ':1' or rule_component == ':0':
                    regex_matching = regex_matching + '(.*)'
                else:
                    regex_matching = regex_matching + '\s*' + re.escape(rule_component)
            regex_matching = regex_matching + '\s*'
            comb_rule_capture_groups.append(re.compile(regex_matching))


def is_wij_covered_in_negation_rule(Gc, sentence, wij):
    global comb_rule_capture_groups
    for pattern in comb_rule_capture_groups:
        # print("regex rule:"+str(regex_matching))
        # the sentence format match with current existing negation rule
        matchObj = pattern.search(sentence)
        if matchObj:
            for index in range(0, pattern.groups):
                if matchObj.group(index).find(wij):
                    # print("true")
                    return True
    return False


# Dictionary Rule Learning
# input:
# dataset         array of (label,sentence) pairs
# Gc              list of combination rules 
# freq_threshold  frequency threshold
# output:
# Gd              list of dictionary rules, in the format 'sentence:label'
# rules_prob      dictionary of rules' probability
def dictionary_rule_learning(dataset, Gc, freq_threshold=4):
    gd_temp = dict()
    compile_combination_rule_capture_group(Gc)
    counter = 0
    for (label, sentence) in dataset:
        counter += 1
        if (counter % 100 == 0):
            print("processing dict rule:", counter)
        # first tokenize the sentence by white space
        sentence_array = sentence.split()
        # for 0<=i<=j<=len(sentence), when i=j just the interested in the single word
        for i in range(0, len(sentence_array)):
            for j in range(i, len(sentence_array)):
                w_i_j = ' '.join(sentence_array[i:j + 1])
                # if no negation rule cover Wi,j
                if is_wij_covered_in_negation_rule(Gc, sentence, w_i_j) == False:
                    rule = w_i_j + ':' + label
                    if (rule not in gd_temp):
                        gd_temp[rule] = 1
                    else:
                        gd_temp[rule] += 1
    gd = []
    prob_rules = dict()
    for rule in gd_temp.keys():
        positive_rule = rule[0:len(rule) - 2] + ':1'
        negative_rule = rule[0:len(rule) - 2] + ':0'
        # if the expression exist in both type of the expression, and both greater than the threshold
        if (positive_rule in gd_temp and negative_rule in gd_temp and (
                gd_temp[positive_rule] >= freq_threshold and gd_temp[negative_rule] >= freq_threshold)):
            probability_of_positive = (gd_temp[positive_rule] + 1) * 1.0 / (
                        (gd_temp[positive_rule] + gd_temp[negative_rule] + 2) * 1.0)
            probability_of_negative = 1 - probability_of_positive
            if (probability_of_negative > probability_of_positive):
                if rule[0:len(rule) - 2] + ':0' not in gd:
                    gd.append(rule[0:len(rule) - 2] + ':0')
                    prob_rules[rule[0:len(rule) - 2] + ':0'] = probability_of_negative
            else:
                if rule[0:len(rule) - 2] + ':1' not in gd:
                    gd.append(rule[0:len(rule) - 2] + ':1')
                    prob_rules[rule[0:len(rule) - 2] + ':1'] = probability_of_positive
    return gd, prob_rules


# input:
# dataset           array of (label,sentence) pairs
# Gd                list of dictionary rules (sentence:label)
# prob_Gd           dict of dictionary rules' probability
# threshold_p       threshold of dictionary rule's probability to be consider as a combination rule 
# threshold_delta   threshold of strength
# threshold_r       threshold of number of total occurence of the rule in order to be considered as a combination rule
# threshold_c       threshold of combination rule probabiltiy 
# output:
# list of combination rule, and types of combination rule
def combination_rule_learning(dataset, gd, prob_gd, threshold_p, threshold_delta, threshold_r, threshold_c):
    gc_temp = list()
    negation_rule_temp = dict()
    strengthen_rule_temp = dict()
    weaken_rule_temp = dict()
    contrast_rule_temp = dict()
    counter = 0
    print("number of dictionary rules: " + str(len(gd)))
    for rule in gd:
        counter += 1
        if counter % 100 == 0:
            print("processing comb rule: " + str(counter))
        dict_rule_sentence = rule[0:len(rule) - 2]
        dict_rule_label = rule[-2:]
        # first tokenize the sentence by white space
        sentence_array = dict_rule_sentence.split()
        # for 0<=i<=j<=len(sentence), when i=j just the interested in the single word
        for i in range(0, len(sentence_array)):
            for j in range(i, len(sentence_array)):
                # negative expression
                if str(' '.join(sentence_array[i:j + 1]) + ':0') in gd:
                    polarity_label_of_ij = 0
                    if str(' '.join(sentence_array[i:j + 1]) + ':0') in prob_gd:
                        polarity_label_of_ij = prob_gd[str(' '.join(sentence_array[i:j + 1]) + ':0')]
                    if polarity_label_of_ij > threshold_p:
                        #                       overall sentence label, W-0i                  label of W-ij W-j+1,f
                        new_combination_rule = (
                        dict_rule_label, ' '.join(sentence_array[0:i]), ':0', ' '.join(sentence_array[j + 1:]))
                        # print('temp rule : '+str(new_combination_rule))
                        # if it's negation rule
                        if dict_rule_label != ':0':
                            if new_combination_rule in negation_rule_temp:
                                negation_rule_temp[new_combination_rule] += 1
                            else:
                                negation_rule_temp[new_combination_rule] = 1
                            gc_temp.append(new_combination_rule)
                        # if it's a strengthen rule
                        elif prob_gd[rule] > polarity_label_of_ij + threshold_delta:
                            if new_combination_rule in strengthen_rule_temp:
                                strengthen_rule_temp[new_combination_rule] += 1
                            else:
                                strengthen_rule_temp[new_combination_rule] = 1
                            gc_temp.append(new_combination_rule)
                        # if it's a weaken rule
                        elif prob_gd[rule] < polarity_label_of_ij - threshold_delta:
                            if new_combination_rule in weaken_rule_temp:
                                weaken_rule_temp[new_combination_rule] += 1
                            else:
                                weaken_rule_temp[new_combination_rule] = 1
                            gc_temp.append(new_combination_rule)
                # positive expression
                elif str(' '.join(sentence_array[i:j + 1]) + ':1') in gd:
                    polarity_label_of_ij = 0
                    if str(' '.join(sentence_array[i:j + 1]) + ':1') in prob_gd:
                        polarity_label_of_ij = prob_gd[str(' '.join(sentence_array[i:j + 1]) + ':1')]
                    if polarity_label_of_ij > threshold_p:
                        #                       overall sentence label, W-0i                  label of W-ij W-j+1,f
                        new_combination_rule = (
                        dict_rule_label, ' '.join(sentence_array[0:i]), ':1', ' '.join(sentence_array[j + 1:]))
                        # print('temp rule : '+str(new_combination_rule))
                        # if it's negation rule
                        if dict_rule_label != ':1':
                            if new_combination_rule in negation_rule_temp:
                                negation_rule_temp[new_combination_rule] += 1
                            else:
                                negation_rule_temp[new_combination_rule] = 1
                            gc_temp.append(new_combination_rule)
                        # if it's a strengthen rule
                        elif prob_gd[rule] > polarity_label_of_ij + threshold_delta:
                            if new_combination_rule in strengthen_rule_temp:
                                strengthen_rule_temp[new_combination_rule] += 1
                            else:
                                strengthen_rule_temp[new_combination_rule] = 1
                            gc_temp.append(new_combination_rule)
                        # if it's a weaken rule
                        elif prob_gd[rule] < polarity_label_of_ij - threshold_delta:
                            if new_combination_rule in weaken_rule_temp:
                                weaken_rule_temp[new_combination_rule] += 1
                            else:
                                weaken_rule_temp[new_combination_rule] = 1
                            gc_temp.append(new_combination_rule)
        for i0 in range(0, len(sentence_array)):
            for j0 in range(i0, len(sentence_array)):
                for i1 in range(j0 + 1, len(sentence_array)):
                    for j1 in range(i1, len(sentence_array)):
                        # check if W-i0j0, W-i1j1 is in dictionary rule
                        polarity_label_of_i0j0 = ''
                        polarity_label_of_i1j1 = ''
                        if str(' '.join(sentence_array[i0:j0 + 1]) + ':0') in gd:
                            polarity_label_of_i0j0 = ':0'
                        elif str(' '.join(sentence_array[i0:j0 + 1]) + ':1') in gd:
                            polarity_label_of_i0j0 = ':1'
                        if str(' '.join(sentence_array[i1:j1 + 1]) + ':0') in gd:
                            polarity_label_of_i1j1 = ':0'
                        elif str(' '.join(sentence_array[i1:j1 + 1]) + ':1') in gd:
                            polarity_label_of_i1j1 = ':1'
                        if polarity_label_of_i0j0 != '' and polarity_label_of_i1j1 != '':
                            if str(' '.join(sentence_array[i0:j0 + 1]) + polarity_label_of_i0j0) in prob_gd and str(
                                    ' '.join(sentence_array[i1:j1 + 1]) + polarity_label_of_i1j1) in prob_gd:
                                if prob_gd[
                                    str(' '.join(sentence_array[i0:j0 + 1]) + polarity_label_of_i0j0)] > threshold_p and \
                                        prob_gd[str(' '.join(
                                                sentence_array[i1:j1 + 1]) + polarity_label_of_i1j1)] > threshold_p:
                                    # doesn't allow 2 dictionary rules near directly combine with each other i.e. not allow P->NP
                                    if str(' '.join(sentence_array[j0 + 1:i1])) != '':
                                        new_combination_rule = (
                                        dict_rule_label, ' '.join(sentence_array[0:i0]), polarity_label_of_i0j0,
                                        ' '.join(sentence_array[j0 + 1:i1]), polarity_label_of_i1j1,
                                        ' '.join(sentence_array[j1 + 1:]))
                                        if polarity_label_of_i0j0 != polarity_label_of_i1j1:
                                            if new_combination_rule in contrast_rule_temp:
                                                contrast_rule_temp[new_combination_rule] += 1
                                            else:
                                                contrast_rule_temp[new_combination_rule] = 1
                                            gc_temp.append(new_combination_rule)
    # convert to unique
    gc_temp_hash = dict()
    for rule in gc_temp:
        if rule not in gc_temp_hash:
            gc_temp_hash[rule] = 1
    # add the new combination rules
    gc = list()
    for comb_rule in gc_temp_hash.keys():
        print(comb_rule)

        num_of_occurance_in_negation = 0
        num_of_occurance_in_strengthen = 0
        num_of_occurance_in_weaken = 0
        num_of_occurance_in_contrast = 0
        if comb_rule in negation_rule_temp:
            num_of_occurance_in_negation = negation_rule_temp[comb_rule]
        if comb_rule in strengthen_rule_temp:
            num_of_occurance_in_strengthen = strengthen_rule_temp[comb_rule]
        if comb_rule in weaken_rule_temp:
            num_of_occurance_in_weaken = weaken_rule_temp[comb_rule]
        if comb_rule in contrast_rule_temp:
            num_of_occurance_in_contrast = contrast_rule_temp[comb_rule]
        if (
                num_of_occurance_in_negation + num_of_occurance_in_strengthen + num_of_occurance_in_weaken + num_of_occurance_in_contrast) > threshold_r:
            max_num_occurance = max(num_of_occurance_in_negation, num_of_occurance_in_strengthen,
                                    num_of_occurance_in_weaken, num_of_occurance_in_contrast)
            if max_num_occurance == num_of_occurance_in_negation and num_of_occurance_in_negation > threshold_c:
                gc.append(('negation', comb_rule))
            elif max_num_occurance == num_of_occurance_in_strengthen and num_of_occurance_in_strengthen > threshold_c:
                gc.append(('strengthen', comb_rule))
            elif max_num_occurance == num_of_occurance_in_weaken and num_of_occurance_in_weaken > threshold_c:
                gc.append(('weaken', comb_rule))
            elif max_num_occurance == num_of_occurance_in_contrast and num_of_occurance_in_contrast > threshold_c:
                gc.append(('contrast', comb_rule))
    return gc


# input
# Gc              combination rules learned
# probability_Gd  the probability of combination rules
# Gd              dictionary rules learned
# fileName        the file name will be <fileName>_combination_rule.txt, <fileName>_directionary_rule.txt
def saveRulesToFile(Gc, probability_Gd, Gd, fileName):
    # save the combination rule
    with open(fileName + '_combination_rule.txt', 'w', encoding='utf-8') as wfh:
        for (type_of_rule, combination_rule) in Gc:
            combination_rule = ' '.join(str(element) for element in combination_rule)
            combination_rule = combination_rule.replace(':0', 'N')
            combination_rule = combination_rule.replace(':1', 'P')
            combination_rule = combination_rule[0] + '->' + combination_rule[1:]
            wfh.write(str(type_of_rule + ' , ' + combination_rule) + '\n')
    # save the dictionary rule
    with open(fileName + '_dictionary_rule.txt', 'w', encoding='utf-8') as wfh:
        for rule in Gd:
            label = rule[-2:]
            if label == ':0':
                label = 'N'
            if label == ':1':
                label = 'P'
            sentence = rule[0:len(rule) - 2]
            wfh.write("label:" + label + ", rule:" + sentence + ', probability:' + str(probability_Gd[rule]) + '\n')
