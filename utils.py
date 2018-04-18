import sys
import csv
import pandas as pd

def jaccard(str1, str2):
    str1 = replacing(str1)
    str2 = replacing(str2)
    if str1 == str2:
        return 1
    chars = jaccard_chars(str1, str2)
    lista = str1.split()
    listb = str2.split()
    try:
        if lista[0].isdigit() and listb[0].isdigit():
            if abs(int(lista[0]) - int(listb[0])) > 10:
                return False
    except IndexError:
        return 0
    setA = set(lista)
    setB = set(listb)
    words = jaccard_words(setA, setB)
    ji = chars if chars > words else words
    return ji


def jaccard_words(s1, s2):
    count1 = 0
    count2 = 0
    for x in s1 & s2: count1 += 1
    for x in s1 | s2: count2 += 1
    jaccard_index = count1 * 1.0 / count2
    # if jaccard_index > 0:
    #     print(str1, str2, jaccard_index)
    return jaccard_index


def jaccard_chars(s1, s2):
    i = 0
    j = 0
    like = 0
    unlike = 0
    while True:
        if i >= len(s1) or j >= len(s2):
            break
        if s1[i] == " " and s2[j] != " ":
            j += 1
        elif s2[j] == " " and s1[i] != " ":
            i += 1
        elif s1[i] == s2[j]:
            like += 1
            i += 1
            j += 1
        else:
            unlike += 1
            i += 1

    return like/(len(s1) + len(s2) - (2*like) + like)


def address_refine(str1):
    str1 = str1.lower()
    str1 = address_replace(str1)
    ad = str1.split()
    s = ""
    try:
        for x in ["st", "dr", "ave", "pl", "pky", "blvd", "ct"]:
            if x in ad[2].lower().strip():
                for n in range(0, 3):
                    s += ad[n] + " "
            elif x in ad[3].lower().strip():
                for n in range(0, 4):
                    s += ad[n] + " "
    except IndexError:
        return str1

    return s


def replacing(a):
    a = a.lower()
    a = address_replace(a)
    a = a.replace('\'', '')
    a = a.replace('and', '&')
    a = a.replace('express', 'exp')
    a = a.replace('pizzeria', 'pizza')
    a = a.replace('academy', 'ady')
    a = a.replace('union station', 'usn')
    a = a.replace('cafe', 'cf')
    a = a.replace('  ', ' ')
    return a


def address_replace(a):
    a = a.replace('avenue', 'ave')
    a = a.replace('street', 'st')
    a = a.replace('court', 'ct')
    a = a.replace('boulevard', 'blvd')
    a = a.replace('parkway', 'pky')
    a = a.replace('place', 'pl')
    a = a.replace('drive', 'dr')
    return a


def progress(progress, total, status=''):
    length = 40  # modify this to change the length
    block = int((progress/total)*40)
    percent = (block/length)*100
    msg = "\r[{0}] {1}%({2}/{3}) - {4}".format("#" * block + "-" * (length - block), round(percent, 2), progress, total, status)
    if progress >= total: msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()


def data_preprocessing():
    review_file = open("Data/reviews_60601-60606.csv", "r")
    clean_reviews_file = open("Data/clean_reviews_60601-60606.csv", "w")
    review_reader = csv.reader(review_file)
    row_count = len(list(review_reader))
    review_file.seek(0)
    i = 0
    review_writer = csv.writer(clean_reviews_file)
    count = 0
    total_count = 0
    for line in review_reader:
        i += 1
        if len(line) > 10:
            str = line[3]
            initial = 4
            while initial < (len(line) - 6):
                str = str + (line[initial])
                del line[initial]
            line[3] = str
            count = count + 1
        review_writer.writerow(line)
        total_count = total_count + 1
        progress(i, row_count, status='Cleaning reviews dataset')
    reviews_pd = pd.read_csv("Data/clean_reviews_60601-60606.csv")
    final_pd = reviews_pd[['reviewContent', 'rating']]
    final_pd.to_csv("Data/preprocessed_reviews_file.csv")
    clean_reviews_file.close()

#print(jaccard("kfc express", "panda express"))
#print(jaccard("bacci pizzeria", "bacci's pizza italy"))
