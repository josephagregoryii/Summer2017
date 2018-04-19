import csv
import string

#Open the csv file and convert it to a list of dictionaries
def openfileStopWords(filename):
    contents = []
    with open(filename, encoding = 'ascii', errors = 'ignore') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for i in row:
                if i == '':
                    continue
                contents.append(i)
        csvfile.close()
    return contents

def openfile(filename):
    """
    important indexes for tables:
        "id" = 0
        "postURL" = 1
        "message" = 2
        "cta" = 4
        "intents" = 3
    """
    final = []
    contents = []
    with open(filename, encoding = 'ascii', errors = 'ignore') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            stripped = row
            contents.append(stripped)
        csvfile.close()
    tables = contents[0]
    for i in contents[1:]:
        temp_dict = {"id": None, "postURL": None, "message": None, "cta": None, "intent": None }
        temp = i
        temp_dict["id"] = temp[0]
        temp_dict["postURL"] = temp[1]
        temp_dict["message"] = temp[2]
        temp_dict["cta"] = temp[4]
        temp_dict["intent"] = temp[3]
        final.append(temp_dict)
    print(final)
    return final

#stopWords = ["to", "a", "the", "is"]

#Filter the list of the posts depending on the user-inputed intent number
def selectIntent(list_of_dictionary, intent):
    list = []
    for dict in list_of_dictionary:
        if dict['intent'] == intent:
            list.append(dict)
    print(list)
    return list

#Take one message and strip, then make a list of dictionaries of words and its counts within that message
def toWordDict(rawMessage, stopWords):
    word_dict = []
    added = False
    message = str.lower(rawMessage)
    translator = str.maketrans('', '', string.punctuation)
    message = message.translate(translator)
    for word in message.split():
        for i in word_dict:
            if i['word'] == word:
                if word in stopWords:
                    added = True
                else:
                    i['score'] = i['score'] + 1
                    added = True
        if added == False and (word in stopWords) == False:
            word_dict.append({'word': word, 'score': 1})
        else:
            added = False
    return word_dict

#Take a wholeList of words with scores and combine it with one word dictionary extracted from one message
def combine(wholeList, wordDict):
    for i in wordDict:
        dict = list(filter(lambda x: x['word'] == i['word'], wholeList))
        if dict == []:
            wholeList.append({'word': i['word'], 'score': i['score']})
        else:
            foundDict = dict[0]
            foundDict['score'] = foundDict['score'] + i['score']
    return wholeList

test_dict = [{'message': "hi my name! is ellen?", 'intent': "1"},
 {'message': "what is your Name!", 'intent': "1"},
 {'message': "this has a different intent", 'intent': "2"}]

def main():
    intent = input('Which intent bucket? ')
    list_of_dictionary = openfile('data_intent_bucketing.csv')
    stopWords = openfileStopWords('stopWords.csv')
    list_of_selected = selectIntent(list_of_dictionary, intent)
    list_of_messages = []
    list_of_words = [] #List of dictionary [{'word': "Donate", 'score': "13"}, ...]

    #extract a list of messages from a list of posts
    for i in list_of_selected:
        list_of_messages.append(i['message'])

    #extract a list of words/score from a list of messages
    for j in list_of_messages:
        wordDict = toWordDict(j, stopWords)
        list_of_words = combine(list_of_words, wordDict)

    rankedList = sorted(list_of_words, key = (lambda p: -p['score']))

    #export it as a .csv file
    print(rankedList)
    keys = rankedList[0].keys()

    with open('word_counts.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(rankedList)

if __name__ == '__main__':
    main()




























