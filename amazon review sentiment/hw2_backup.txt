def readAndDivideBySentiment(fileName):
    location = "C:\\Users\\Linsu\\Documents\\[PURDUE]\\CS 380\\"
    f = open(location + fileName, "r")
    pos = list()
    neg = list()
    s = f.read()
    lines = 0
    for i in s:
        if i == "\n":
            lines += 1
    f.seek(0)
    for i in range(0, lines):
        a = f.readline()
        string = a.split("\t")[0]
        rating = a[-2]
        if int(rating) == 0:
            neg.append(string)
        else:
            pos.append(string)
    f.close()
    return neg, pos


def cleanData(myData):
    import re
    cleaned = list()
    for i in range(0, len(myData)):
        s = myData[i].lower().strip()

        s = s.lower()
        s = s.replace("--", " ")
        s = s.replace("-", "")
        s = re.sub(r"[^a-z0-9_']", " ", s)

        a = re.compile("\s[0-9]+[a-z]+")
        b = re.compile("[a-z]+[0-9]+\s")
        # todo: case c: 123abc123 in beginning of a string

        if bool(a.search(s)):
            found = a.findall(s)
            spaced = list()
            for i in range(0, len(found)):
                for j in range(0, len(found[i])):
                    if found[i][j].isalpha():
                        spaced.append(found[i][:j] + ' ' + found[i][j:])
                        break
            for i in range(0, len(found)):
                s = s.replace(found[i], spaced[i])

        if bool(b.search(s)):
            found = b.findall(s)
            spaced = list()
            for i in range(0, len(found)):
                for j in range(0, len(found[i])):
                    if found[i][j].isdigit():
                        spaced.append(found[i][:j] + ' ' + found[i][j:])
                        break
            for i in range(0, len(found)):
                s = s.replace(found[i], spaced[i])

        s = re.sub(r"[0-9]+\s+", "# ", s)
        s = re.sub(r"\s+[0-9]", " #", s)
        s = re.sub(r"(# )\1+", r"\1", s)
        s = re.sub(r" +", " ", s).strip()
        cleaned.append(s)
    return cleaned


def calculateUniqueWordFreq(trainData, cutOff):
    count = {}
    dict = {}
    for i in range(0, len(trainData)):
        words = trainData[i].split(" ")
        for word in words:
            if word in count:
                count[word] += 1
            else:
                count.update({word: 1})
    for word in count:
        if count[word] >= cutOff:
            dict.update({word: count[word]})
    return dict


def calculateClassProbability(posTrain, negTrain):
    total = float(len(posTrain) + len(negTrain))
    posProb = len(posTrain) / total
    negProb = float(len(negTrain) / total)
    return posProb, negProb


def calculateScores(classProb, uniqueVocab, testData):
    scores_w = []
    wordsInDict = len(uniqueVocab)
    wordsCumFreq = 0
    scores = []
    p = float(classProb)
    for word in uniqueVocab:
        wordsCumFreq += uniqueVocab[word]
    for i in range(0, len(testData)):
        words = testData[i].split(" ")
        for word in words:
            try:
                w_count = float(uniqueVocab[word])
            except KeyError:
                w_count = float(0)
            w_score = (w_count + 1) / (wordsInDict + wordsCumFreq)
            scores_w.append(w_score)
        score = p
        for i in scores_w:
            score *= i
        scores.append(score)
        scores_w = []
    return scores


def calculateAccuracy(postitiveTestDataPostitiveScores, positiveTestDataNegativeScores,
                      negativeTestDataPositiveScores, negativeTestDataNegativeScoes):
    tp = int()
    fp = int()
    tn = int()
    fn = int()
    for i in range(0, len(postitiveTestDataPostitiveScores)):
        if postitiveTestDataPostitiveScores[i] > positiveTestDataNegativeScores[i]:
            tp += 1
        else:
            fp += 1
    for i in range(0, len(negativeTestDataNegativeScoes)):
        if negativeTestDataNegativeScoes[i] > negativeTestDataPositiveScores[i]:
            tn += 1
        else:
            fn += 1
    return tp, fp, tn, fn


def main():
    negR = readAndDivideBySentiment("TRAINING.txt")[0]
    posR = readAndDivideBySentiment("TRAINING.txt")[1]
    negT = readAndDivideBySentiment("TESTING.txt")[0]
    posT = readAndDivideBySentiment("TESTING.txt")[1]
    negRC = cleanData(negR)
    posRC = cleanData(posR)
    negTC = cleanData(negT)
    posTC = cleanData(posT)
    cutOff = 2
    negRCDict = calculateUniqueWordFreq(negRC, cutOff)
    posRCDict = calculateUniqueWordFreq(posRC, cutOff)
    negRP = calculateClassProbability(posR, negR)[1]
    posRP = calculateClassProbability(posR, negR)[0]
    ptps = calculateScores(posRP, posRCDict, posTC)
    ptns = calculateScores(negRP, negRCDict, posTC)
    ntps = calculateScores(posRP, posRCDict, negTC)
    ntns = calculateScores(negRP, negRCDict, negTC)
    print "dictionary cutoff:", cutOff
    print "respective values for:\ntp, fp, tn, fn"
    print calculateAccuracy(ptps, ptns, ntps, ntns)


main()
