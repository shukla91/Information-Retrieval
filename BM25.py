import sys
import json
from math import log
import operator
from _collections import defaultdict

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0

def calculate_bm25score(id1,tf,len1,averagec,doc1,qf):
    # calculate bm25 score for every document
    n = len(tf)
    f= tf.get(id1)
    rk = 0
    K = k1 * ((1 - b) + b * (float(doc1) / float(averagec)))
    first = log(((rk + 0.5) / (R - rk + 0.5)) / ((n - rk + 0.5) / (len1 - n - R + rk + 0.5)))
    second = ((k1 + 1) * f) / (K + f)
    third = ((k2 + 1) * qf) / (k2 + qf)
    score = first * second * third
    return score

def queryParser(query_file,tokens,index):
    
    result_dict = defaultdict(int)
    query_id = 0
    len1 = len(tokens)
    total = sum(tokens.values())            #total tokens
    #average length of doc
    averagec = float(total)/float(len1)  
    
    with open(query_file) as q_file:
        queries = q_file.readlines()
    for query in queries:
        query_id += 1
        result_dict.clear()
        terms = query.split()
        for t in terms:
            tf =  index.get(t)
            for id1 in tf:
                doc1 = tokens.get(id1)
                qf = query.count(t)
                score = calculate_bm25score(id1,tf,len1,averagec,doc1,qf)
                result_dict[id1] += score
        sorted_x = sorted([(v,k) for k,v in result_dict.iteritems()],reverse=True)
        output_print(sorted_x[0:max_doc],query_id)

def output_print(top_scores,query_id):
    #displaying sorted result
    rk = 0
    for score, id1 in top_scores:
        rk +=1
        tmp = (query_id, id1, rk, score)
        print '{:>1}\tQ0\t{:>4}\t{:>2}\t{:>12}\tSHUKLA'.format(*tmp)

def load_file(index_file, query_file, max_doc):
    #reading the inverted index and token count from the given input file
    with open(index_file) as f:
        getResult = json.load(f)
        index = getResult[0]
        tokens = getResult[1]
        queries = queryParser(query_file,tokens,index)

if __name__ == '__main__':
    if len(sys.argv) == 4:
        index_file = str(sys.argv[1])
        query_file = str(sys.argv[2])
        max_doc = int(sys.argv[3])
        load_file(index_file, query_file, max_doc)
    else:
        print " Incorrect number of arguments"
