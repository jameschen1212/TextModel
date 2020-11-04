#James chen
#email: jamesche@bu.edu

import math

class TextModel:

    def __init__(self, model_name):
        """constructs a new TextModel object by accepting a string model_name as a parameter and initializing the following three attributes"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.conjunctions = {}

    def __repr__(self):
        """returns a string that includes the name of the model as well as the sizes of the dictionaries for each feature of the text."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of conjunctions: ' + str(len(self.conjunctions))
        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
       to all of the dictionaries in this text model."""
        for i in s:
            if(i == '.' or '!' or '?'):
                i = '.'
        
        listsentences = s.split()
        count = 0
        

        for w in listsentences:
            if('.' in w or '!' in w or '?' in w):
                count += 1
                if(count not in self.sentence_lengths):
                    self.sentence_lengths[count] = 1
                else:
                    self.sentence_lengths[count] += 1
                count = 0
            else:
                count += 1

        cleaned = clean_text(s)
        listwords = cleaned.split()

        for w in listwords:
            if(w not in self.words):
                self.words[w] = 1
            else:
                self.words[w] += 1

        for w in listwords:
            if(len(w) not in self.word_lengths):
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1

        for w in listwords:
            if(stem(w) not in self.stems):
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1

        conjuncted = conjunctions(s)

        for w in conjuncted:
            if(w not in self.conjunctions):
                self.conjunctions[w] = 1
            else:
                self.conjunctions[w] += 1

        

    def add_file(self, filename):
        """adds all of the text in the file identified by filename to the model. It should not explicitly return a value."""
        file = open(filename, 'r', encoding='utf8', errors='ignore')
        text = file.read()      # read it all in at once!
        file.close()
        self.add_string(text)

    def save_model(self):
        """saves the TextModel object self by writing its various feature dictionaries to files."""
        f = open(self.name + '_' + 'words', 'w')
        f.write(str(self.words))
        f.close()

        
        f1 = open(self.name + '_' + 'word_lengths', 'w')
        f1.write(str(self.word_lengths))
        f1.close()

        f2 = open(self.name + '_' + 'stems', 'w')
        f2.write(str(self.stems))
        f2.close()

        f3 = open(self.name + '_' + 'sentence_lengths', 'w')
        f3.write(str(self.sentence_lengths))
        f3.close()

        f4 = open(self.name + '_' + 'conjunctions', 'w')
        f4.write(str(self.conjunctions))
        f4.close()

    def read_model(self):
        """reads the stored dictionaries for the called TextModel object from their files and assigns them to the attributes of the called TextModel."""
        f = open(self.name + '_' + 'words', 'r')
        d_str = f.read()
        f.close()

        self.words = dict(eval(d_str))

        f1 = open(self.name + '_' + 'word_lengths', 'r')
        d1_str = f1.read()
        f1.close()

        self.word_lengths = dict(eval(d1_str))

        f2 = open(self.name + '_' + 'stems', 'w')
        d2_str = f2.read()
        f2.close()

        self.stems = dict(eval(d2_str))

        f3 = open(self.name + '_' + 'sentence_lengths', 'w')
        d3_str = f3.read()
        f3.close()

        self.sentence_lengths = dict(eval(d3_str))

        f4 = open(self.name + '_' + 'conjunctions', 'w')
        d4_str = f4.read()
        f4.close()

        self.conjunctions = dict(eval(d4_str))

    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores measuring the similarity of self and other – one score for each type of feature"""
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        word_stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_length_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        conjunction_score = compare_dictionaries(other.conjunctions, self.conjunctions)

        return [word_score, word_lengths_score, word_stems_score, sentence_length_score, conjunction_score]

    def classify(self, source1, source2):
        """that compares the called TextModel object (self) to two other “source” TextModel objects (source1 and source2) and determines which of these other TextModels is the more likely source of the called TextModel."""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ' + source1.name + ': ' + str(scores1) + '\n')
        print('scores for ' + source2.name + ': ' + str(scores2))
        count1 = 0
        count2 = 0
        for i in range(len(scores1)):
            if(scores1[i] > scores2[i]):
                if(i == 0):
                    count1 += 5*1
                if(i == 1):
                    count1 += 3*1
                if(i == 2):
                    count1 += 4*1
                if(i == 3):
                    count1 += 2*1
                if(i == 4):
                    count1 += 1
            elif(scores1[i] < scores2[i]):
                if(i == 0):
                    count2 += 5*1
                if(i == 1):
                    count2 += 3*1
                if(i == 2):
                    count2 += 4*1
                if(i == 3):
                    count2 += 2*1
                if(i == 4):
                    count2 += 1

        if(count1 > count2):
            print(self.name + ' is more likely to have come from: ' + source1.name)
        elif(count2 > count1):
            print(self.name + ' is more likely to have come from: ' + source2.name)
        else:
            print(self.name + ' is equally likely to have come from: ' + source1.name + ' or ' + source2.name)
                


        

def sample_file_write(filename):
    """A function that demonstrates how to write a
         Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()                    # Close the file.

def sample_file_read(filename):
    """A function that demonstrates how to read a
        Python dictionary from a file.
    """
    f = open(filename, 'r')    # Open for reading.
    d_str = f.read()           # Read in a string that represents a dict.
    f.close()

    d = dict(eval(d_str))      # Convert the string to a dictionary.

    print("Inside the newly-read dictionary, d, we have:")
    print(d)

def clean_text(txt):
    """takes a string of text txt as a parameter and returns a list containing the words in txt after it has been “cleaned”"""
    s = txt.replace('.', ' ')
    s = s.replace(',', ' ')
    s = s.replace('?', ' ')
    s = s.replace('!', ' ')
    s = s.replace(':', ' ')
    s = s.replace(';', ' ')
    return s.lower()

def stem(s):
    """accepts a string as a parameter. The function should then return the stem of s"""
    if(s[-1:] == 's'):
        if(len(s) < 3):
            s = s
        else:
            s = s[:-1]
            return stem(s)
            

    elif(s[-3:] == 'ing'):
        if(len(s) < 5):
            s = s
        else:
            if(s[-4] == s[-5]):
               s = s[:-4]
            else:
                s = s[:-3]
    elif(s[-2:] == 'er'):
        s = s[:-2]

    elif(s[-2:] == 'ed'):
        if(len(s) < 4):
            s = s
        else:
            s = s[:-2]
    elif(s[-2:] == 'es'):
        if(len(s) < 4):
            s = s
        else:
            s = s[:-2]
    elif(s[-3:] == 'est'):
        if(len(s) < 5):
            s = s
        else:
            s = s[:-3]
    elif(s[-3:] == 'less'):
        if(len(s) < 5):
            s = s
        else:
            s = s[:-3]
    elif(s[-1:] == 'y'):
        if(len(s) < 5):
            s = s 
        else:
            s = s[:-1] + 'i'
    return s

def conjunctions(s):
    """ returns only the conjunctions in a text"""
    cleaned = clean_text(s)
    listwords = cleaned.split()
    conjunction = []
    for i in listwords:
        if(i == 'and'):
            conjunction += [i]
        elif(i == 'for'):
            conjunction += [i]
        elif(i == 'but'):
            conjunction += [i]
        elif(i == 'yet'):
            conjunction += [i]
        elif(i == 'so'):
            conjunction += [i]
        elif(i == 'or'):
            conjunction += [i]
        elif(i == 'nor'):
            conjunction += [i]
    return conjunction

def compare_dictionaries(d1, d2):
    """take two feature dictionaries d1 and d2 as inputs, and it should compute and return their log similarity score."""
    score = 0
    total = 0
    for i in d1:
        total += d1[i]



    """counters the divide by zero error if conjunctions dictionary is empty"""
    if(len(d1) == 0 or len(d2) == 0):
        return 0.0

    for w in d2:
        if(w in d1):
            score += math.log(d1[w]/total)*d2[w]
        else:
            score += math.log(0.5/total)*d2[w]
    return score

def test():
    """ test for function """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

def run_tests():
    """ test for comparasion between whitman's poems and shakespeare's poems """
    source1 = TextModel('shakespeare')
    source1.add_file('shakespeare.txt')
    source1.save_model()

    source2 = TextModel('whitman')
    source2.add_file('waltwhitman.txt')
    source2.save_model()

    new1 = TextModel('whitman1')
    new1.add_file('whitman1.txt')
    new1.save_model()
    new1.classify(source1, source2)

    new2 = TextModel('shakespeare1')
    new2.add_file('shakespeare1.txt')
    new2.save_model()
    new2.classify(source1, source2)

    new3 = TextModel('edgar')
    new3.add_file('edgar.txt')
    new3.save_model()
    new3.classify(source1, source2)

    new4 = TextModel('maya')
    new4.add_file('maya.txt')
    new4.save_model()
    new4.classify(source1, source2)

