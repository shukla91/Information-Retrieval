import sys




pr = {}                 #dictionary for storing page rank of a particular page
npr = {}                #dictionary for storing new page rank calculated
inLinks = {}            #dictionary for storing inliks of a page
outLinks = {}           #dictionary for storing outlinks of a page
countInLinks = {}       #count of inLinks
sinks={}                #dictionary for storing sink pages
#pageCount = {}
N = 0
sourceList={}
tPages={}



def open_file(fi):
    global sinks
    f= open(fi,"r")
    for line in f:
        lineList =  line.strip().split(" ")
        print(lineList)
        destination = lineList.pop(0)
        tPages[destination] = 0
        if len(lineList) > 0:
            inLinks[destination] = lineList
#             pageCount[destination] = len(lineList)
#         else:
#             pageCount[destination] = 1

    for i in inLinks:
        for l in inLinks[i]:
            try:
                outLinks[l] = outLinks[l] + 1
            except KeyError:
                outLinks[l] = 1
    
    sinks = set(tPages.keys()) - set(outLinks.keys())

    f.close()
d = 0.85

def page_rank_calculate():
    n = len(tPages)
    N = float(n)
    i = 1      
    
    while i <= 100:
        if not pr:
            for p in tPages.keys():
                pr[p] = float(1/N)
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
        
        if i==1 or i==10 or i == 100:
            
            print("Page rank A %s"%(pr['A']))
            print("Page rank B %s"%(pr['B']))
            print("Page rank C %s"%(pr['C']))
            print("Page rank D %s"%(pr['D']))
            print("Page rank E %s"%(pr['E']))
            print("Page rank F %s"%(pr['F']))
        i = i+1
            
    


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
