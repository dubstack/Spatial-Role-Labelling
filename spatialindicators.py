#This is the place where all the shit REALLY HAPPENS
import xml.dom.minidom
import nltk
from pprint import pprint
from random import shuffle
from sklearn import svm
def generate_dataset():
    doc = xml.dom.minidom.parse("SItrain.xml")
    preps = doc.getElementsByTagName("PREPOSITION")
    instances = []
    for prep in preps:
        multiword=0
        features = []
        sis = prep.parentNode.parentNode.getElementsByTagName("SPATIAL_INDICATOR")
        for si in sis:
            sitext = si.childNodes[0].data.split() # split to delete spureous white spaces
            if len(sitext) > 1:
                multiword=1

            sitext = " ".join(sitext)
        head1 = prep.getElementsByTagName("HEAD1")[0].childNodes[0].data
        head1_lemma = prep.getElementsByTagName("HEAD1_LEMMA")[0].childNodes[0].data
        head1_pos = prep.getElementsByTagName("HEAD1_POS")[0].childNodes[0].data
        head2 = prep.getElementsByTagName("HEAD2")[0].childNodes[0].data
        head2_lemma = prep.getElementsByTagName("HEAD2_LEMMA")[0].childNodes[0].data
        head2_pos = prep.getElementsByTagName("HEAD2_POS")[0].childNodes[0].data
        prepos = prep.getElementsByTagName("PREP")[0].childNodes[0].data
    
        prepos_pos = prep.getElementsByTagName("PREP_POS")[0].childNodes[0].data
        prepos_spatial = prep.getElementsByTagName("PREP_SPATIAL")[0].childNodes[0].data
        tag = prep.getElementsByTagName("CLASS")[0].childNodes[0].data
        if tag == "SI": 
            tag = 1
        else: 
            tag = 0 
        features = {}
        features["head1"] = head1
        features["head1_lemma"] = head1_lemma
        features["head1_pos"] = head1_pos
        features["head2"] = head2
        features["head2_lemma"] = head2_lemma
        features["head2_pos"] = head2_pos
        features["prep"] = prepos
        features["prep_pos"] = prepos_pos
        features["prep_spatial"] = prepos_spatial
        if multiword==0:
            instances.append([features, tag])
    return instances
def get_multiwords_preps():
    doc = xml.dom.minidom.parse("tpp.xml")
    entries = doc.getElementsByTagName("hw")
    multiword_preps=[entry.childNodes[0].data for entry in entries if len(entry.childNodes[0].data.split())>1]
    #print multiword_preps
    return multiword_preps

def generate_testdata():
    doc = xml.dom.minidom.parse("input_data.xml")
    preps = doc.getElementsByTagName("PREPOSITION")
    instances = []
    for prep in preps:
        features = []
        head1 = prep.getElementsByTagName("HEAD1")[0].childNodes[0].data
        head1_lemma = prep.getElementsByTagName("HEAD1_LEMMA")[0].childNodes[0].data
        head1_pos = prep.getElementsByTagName("HEAD1_POS")[0].childNodes[0].data
        head2 = prep.getElementsByTagName("HEAD2")[0].childNodes[0].data
        head2_lemma = prep.getElementsByTagName("HEAD2_LEMMA")[0].childNodes[0].data
        head2_pos = prep.getElementsByTagName("HEAD2_POS")[0].childNodes[0].data
        prepos = prep.getElementsByTagName("PREP")[0].childNodes[0].data
        prepos_pos = prep.getElementsByTagName("PREP_POS")[0].childNodes[0].data
        prepos_spatial = prep.getElementsByTagName("PREP_SPATIAL")[0].childNodes[0].data
        tag =-1
        features = {}
        features["head1"] = head1
        features["head1_lemma"] = head1_lemma
        features["head1_pos"] = head1_pos
        features["head2"] = head2
        features["head2_lemma"] = head2_lemma
        features["head2_pos"] = head2_pos
        features["prep"] = prepos
        features["prep_pos"] = prepos_pos
        features["prep_spatial"] = prepos_spatial
        sentence_id=prep.parentNode.parentNode.getAttribute("id")
        sentence_id=sentence_id[1:]
        dependencies=prep.parentNode.parentNode.getElementsByTagName("DEPENDENCIES")[0]
        all_dependencies=[]
        for depen in dependencies.childNodes:
            #Cast to dict
            stringdepen = depen.childNodes[0].data
            listdepen = stringdepen.split(" ")
            name = listdepen[0].split(":")[1]
            specific = listdepen[1].split(":")[1]                                                                                      
            gov = listdepen[2].split(":")[1]                                                                                   
            dep = listdepen[3].split(":")[1]
            dictdepen = {'name': name, 'specific': specific, 'gov': gov, 'dep': dep}
            all_dependencies.append(dictdepen)
        taggedwords = prep.parentNode.parentNode.getElementsByTagName("POSTAGS")[0].childNodes[0].data
        taggedwords = taggedwords.split(" ")
        tw = []
        for pair in taggedwords:
            tw.append([pair.split("/")[0], pair.split("/")[1]])
        taggedwords = tw
        sentence=prep.parentNode.parentNode.getElementsByTagName("CONTENT")[0].childNodes[0].data
        instances.append([features, tag,sentence_id,all_dependencies,taggedwords,sentence])
        
    return instances

def cvtrain(train, K):

    shuffle(train)
    total_accuracy = 0

    for k in xrange(K):
        training = [x for i, x in enumerate(train) if i % K != k]
        validation = [x for i, x in enumerate(train) if i % K == k]
        classifier = nltk.NaiveBayesClassifier.train(training)
        #print(classifier.classify(validation))
        accuracy =  nltk.classify.accuracy(classifier, validation)
        total_accuracy += accuracy

    avg_accuracy = float(total_accuracy)/K
    #print ("Naive Bayes accuracy on CV: ",str(avg_accuracy))
    return avg_accuracy
    
def getPOS(word, tagged):
    if word is None: return None
    try:
        pos = filter(lambda t: t[0] == word, tagged)
        if len(pos) > 0:
            return pos[0][1]
        else:
            return None

    except Exception as e:
        print "Error getting POS of:", word
        print e
def isObject(tag):
    if tag=="NN" or tag=="NNS" or tag=="NNP" or tag=="NNPS" or tag=="PRP" or tag=="PRP$":
        return 1
    else:
        return 0

def test():
    filer= open('output.txt','w')
    instances=generate_dataset()
    test_instances=generate_testdata()
    multiword_preps=get_multiwords_preps()
    classifier= nltk.NaiveBayesClassifier.train(instances)
    for x in test_instances:
        checker=0
        for prep in multiword_preps:
            if prep in x[5]:
                checker=1
                sentence=x[5].split()
                for word in sentence:
                    if isObject(getPOS(word,x[4]))==1:
                        object1=word
                        break
                for word in reversed(sentence):
                    if isObject(getPOS(word,x[4]))==1:
                        object2=word
                        break
                filer.write(x[2]+'. \"'+prep+'\" \"'+object1+ '\" \"' +object2+'\"\n')
                break
        if checker == 1 :
            continue
        predicted=classifier.classify(x[0])
        object1="none"
        object2="none"
        if x[0]['prep']=="beneath" :
            predicted=1
        if(predicted==1):
            if isObject(getPOS(x[0]["head1"],x[4]))==1 and isObject(getPOS(x[0]["head2"],x[4]))==1 : 
                filer.write(x[2]+'. \"'+x[0]["prep"]+'\" \"'+x[0]["head1"]+ '\" \"' +x[0]["head2"]+'\"\n')
            else:
                if isObject(getPOS(x[0]["head1"],x[4]))==0 :
                    for i in x[3]:
                        if i['dep']==x[0]["head1"]:
                            if isObject(getPOS(i['gov'],x[4]))==1:
                                object1=i['gov']
                                break
                        elif i['gov']==x[0]["head1"]:
                            if isObject(getPOS(i['dep'],x[4]))==1:
                                object1=i['dep']
                                break
                    else:
                        object1=x[0]["head1"]
                if isObject(getPOS(x[0]["head2"],x[4]))==0 :
                    for i in x[3]:
                        if i['gov']==x[0]["head2"]:
                            if isObject(getPOS(i['dep'],x[4]))==1:
                                object2=i['dep']
                                break
                        elif i['dep']==x[0]["head2"]:
                            if isObject(getPOS(i['gov'],x[4]))==1:
                                object1=i['gov']
                                break
                else:
                    object2=x[0]["head2"]
                filer.write(x[2]+'. \"'+x[0]["prep"]+'\" \"'+object1+ '\" \"' +object2+'\"\n')
    filer.close()

if __name__ == "__main__":
    """
    instances = generate_dataset()
    size = len(instances)
    cut = int(size*0.7)
    train = instances[:cut]
    test = instances[cut:]
    examples=0
    counter=0
    classifier = nltk.NaiveBayesClassifier.train(train)
    for x in test:
        pred = classifier.classify(x[0])
        gold = x[1]
        if(pred==gold):
            counter+=1
        else:
            print x[0]
            print "___________"
            print x[1]
        examples+=1
    print(float(counter)/examples)
    print(len(instances))"""
    test()
    get_multiwords_preps()