import helperFunctions as h

if __name__ == '__main__':
    data_set = []
    # load the rottan tomato review
    with open('processed_rt_reviews.csv')as fh:
        for line in fh:
            label = line[0]
            sentence = line[2:len(line)]
            data_set.append((label, sentence))

    Gc = []
    Gd = []
    counter = 0
    while counter < 5:
        counter += 1
        # do a dictionary rule learning
        Gd, dict_rules_prob = h.dictionary_rule_learning(data_set, Gc, 4)
        '''
        for rule in Gd:
          label=rule[-2:]
          sentence=rule[0:len(rule)-2]
          print("label:",label," rule:",sentence,' probability:',dict_rules_prob[rule])
        '''

        # do a combination rule learning
        Gc = h.combination_rule_learning(data_set, Gd, dict_rules_prob, threshold_p=0.6, threshold_delta=0.05,
                                         threshold_r=2, threshold_c=1)
        # for (type_of_rule,combination_rule) in Gc:
        h.saveRulesToFile(Gc, dict_rules_prob, Gd, 'learn')
        #  print(type_of_rule+str(combination_rule))
        '''
        #do a dictionary rule learning
        Gd,dict_rules_prob=h.dictionary_rule_learning(data_set,Gc,4)
        for rule in Gd:
          label=rule[-2:]
          sentence=rule[0:len(rule)-2]
          print("label:",label," rule:",sentence,' probability:',dict_rules_prob[rule])
        '''
    '''
    for rule in Gd:
      label=rule[-2:]
      sentence=rule[0:len(rule)-2]
      print("label:",label," rule:",sentence,' probability:',dict_rules_prob[rule])
    for (type_of_rule,combination_rule) in Gc:
      print(type_of_rule+str(combination_rule))
    '''
    print('End of Program')
