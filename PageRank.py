import sys
import math
import operator



pr = {}
temp ={}
npr = {}
inLinks = {}
out = {list}
outLinks = {}
countInLinks = {}
sinks=[]
pageCount = {}
N = 0
sourceList={}
tPages={}
perplexityList =list()
Perplexity = []
d = 0.85
count =0
distinct_page ={}


def open_file(fi):
    count =0
    global sinks
    f= open(fi,"r")
    for line in f:
        lineList =  line.strip().split(" ")
        #print(lineList)
        destination = lineList.pop(0)
        
        tPages[destination] = 0

        if len(lineList)>0 and (destination not in inLinks):
            inLinks[destination] = lineList
            pageCount[destination] = len(lineList)
        else:
            pageCount[destination] = 0
            
        
        for i in inLinks:
            for l in inLinks[i]:
                try:
                    if l in outLinks:
                        del outLinks
                    outLinks[l] = outLinks[l]+1
                except KeyError:
                    if l in outLinks:
                        del outLinks
                        outLinks[l] = 1

    sinks = set(tPages.keys()) - set(outLinks.keys())

    f.close()

def convergence_calculate():   
    lengthPrep = len(Perplexity)
    Perplexity.append(perplexity_calculate())
    if lengthPrep < 4:
        return True 
    else:
        v1 = Perplexity[-1]
        v2 = Perplexity[-2]
        v3 = Perplexity[-3]
        v4 = Perplexity[-4]
        if (v1 == v2 and v1 == v3 and v1 == v4):
            return False
    return True


#Function to Calculate the perplexity value
def perplexity_calculate():
    global tPages, inLinks, pr
    perplexity = 0
    entropy = 0
    for k in tPages.keys():
        entropy +=  (pr[k] * (math.log(1/pr[k],2)))
    perplexity = math.pow (2,entropy)
    perplexityList.append(perplexity)
    return int(perplexity)
    
 
def page_rank_calculate():
    global pr, tPages, outLinks, sinks
    n = len(tPages)
    N = float(n)
    count=0
    if not pr:
        for p in tPages.keys():
            pr[p] = float(1/N)
            temp[p] = pr[p]
    while convergence_calculate():
        sinkPageRank = 0
        for p in sinks:                                       
            sinkPageRank += pr[p]
        for p in tPages:
            npr[p] = (1.0 - d) / N
            npr[p] += (d * sinkPageRank) / N                           
            if p in inLinks:           
                for inPage in inLinks[p]:      
                    npr[p] += d * pr[inPage] / outLinks[inPage]          
        for np in tPages:
            pr[np] = npr[np]
    for p in tPages:
        if pr[p] < temp[p]:
            count = count + 1
    print("Total Pages whose page rank is less than their initial value %d",count)
            
    
def sorted_inlinks_print():
    sorted_inlinks = sorted(inLinks,key = lambda i : len(inLinks[i]), reverse = True)
    f2 = open("inlink_sorted.txt", 'w')
    for i in range(0,50):
        f2.write("SNo. {} {} count = {} \n " .format(str(i) ,str(sorted_inlinks[i]), str(len(inLinks[sorted_inlinks[(i)]]))))
    f2.close()

#Sort the page rank and print
def sorted_page_rank_print():
    sorted_pagerank = (sorted(pr.items(),key=operator.itemgetter(1), reverse=True))
    f1 = open("pagerank_sorted.txt", 'w')
    for i in range(0,50):
        f1.write("%s\n" % str(sorted_pagerank[i]))
    f1.close()

def PrintPerplexity():
    global perplexityList
    f3 = open("perplexity.txt",'w')
    for k , v  in enumerate(perplexityList):
        f3.write("SNo. is {} and perplexity is {} \n ".format(str(k),str(v)))
    f3.close()
    
    print("Total Pages present = {} , Inlinks count = {} , Outlinks Count = {} , Sinkpages count = {}".format(len(tPages),len(inLinks),len(outLinks),len(sinks)))


if __name__ == "__main__":
    check_stat = False
 
    if len(sys.argv) == 2:
        fi = str(sys.argv[1])
        check_stat = False
    else:
        check_stat = True
        print " No. of arguments incorrect"
 
 
    if not check_stat:
        # calculate_page_rank Function
        open_file(fi)
        page_rank_calculate()
        sorted_page_rank_print()
        sorted_inlinks_print()
        PrintPerplexity()
