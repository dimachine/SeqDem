import csv, itertools
csvfile=open('for Sequence_mining (full).csv', 'r')
# отркрытие файла с данными опросника для формирования последовательностей
sreader = csv.reader(csvfile, delimiter=';', quotechar='|')
names=sreader.next()# stores attributes' names
#cnt=0
dataList=[]
for row in sreader:
    # reads all lines in the csv file
    # and stores them in a dictionary with the value of an attribute
    dataDic={}
    attrInd=0
    for cell in row:
        if cell<>'':
            dataDic[names[attrInd]]=int(cell)
        attrInd+=1

    dataList.append(dataDic)
    #cnt+=1
    #if cnt==20: break

    
csvfile.close()



def DataListToPairsList(DataList, names):
    #converts dictionaries with values to values 1 or 0 for pairs
    # (a,b) depending on whether a precedes b
    PairsList=[]
    attrs=[]
    for pair in itertools.product(names,names):
        if pair[0]<>pair[1]: attrs.append(pair)
    
    
    for row in DataList:
        lst=[]
        for attr in attrs:
            if attr[0] in row.keys() and attr[1] in row.keys() and row[attr[0]]<=row[attr[1]]:
                lst.append(attr)
        PairsList.append(lst)
        
            

    return PairsList

def DataListToSequenceList(DataList, names):
    #maps attributes to a sequence based on sorting them by age in an ascending order
    SequenceList=[]

    for row in DataList:
        SequenceList.append(sorted(row.keys(), key=row.get))
    
    return SequenceList


def DataListToSequenceList2(DataList, names):
    # maps attributes to a sequence based on sorting them by age in an ascending order
    # taking into account equal ages
    SequenceList=[]
    #names=sorted(names)

    for row in DataList:
        tempSeq=sorted(row.keys(), key=row.get)
        sequence=[]
        prevEv=''
        for ev in tempSeq:
            if prevEv=='':
                sequence.append([ev])
                #print row
            elif row[prevEv]==row[ev]:
                #print row
                sequence[-1].append(ev)
            else:
                #print row
                sequence.append([ev])
            prevEv=ev
        SequenceList.append(sequence)
                
   
    return SequenceList

def PairsToContext(pairs, names, filename):

    outfile=open(filename+'.txt', 'w')

    attrs=[]
    for pair in itertools.product(names,names):
        if pair[0]<>pair[1]: attrs.append(pair)

    outfile.write('\t'.join([str(attr) for attr in attrs])+'\n\n')
      
        

    for el in pairs:
        line=[]
        for attr in attrs:
            if attr in el:
                line.append('1')
            else: line.append('0')
        outfile.write('\t'.join(line)+'\n')        
        
    

    outfile.close()

    return []

def SequenceToSPMF(SequenceList, filename):

    outfile=open(filename+'.txt', 'w')

    for seq in SequenceList:
        for el in seq:
            if len(el)==1:
                outfile.write(el[0]+' -1 ')
            else:
                for el2 in el:
                    outfile.write(el2+' ')
                outfile.write('-1 ')
        outfile.write('-2\n')
            
    print filename               

    outfile.close()


    return []

def AttrAndSeqFusion(SequenceList, AttrFileName):
    csvfile=open(AttrFileName, 'rb')
    areader = csv.reader(csvfile, delimiter=';', quotechar='|')
    names=areader.next()# stores attributes' names
    #cnt=0
    dataList=[]
    for row in areader:
        # reads all lines in the csv file
        # and stores in a list the value of an attribute
        attrList=[]
        attrInd=0
        for cell in row:
            attrList.append([str(names[attrInd])+'='+str(cell)])
            attrInd+=1

        dataList.append(attrList)
        #cnt+=1
        #if cnt==20: break

        
    csvfile.close()

    [dataList[i].extend(SequenceList[i])  for i in  range(len(dataList))]

    return dataList
    


def exp1():

    #dl= DataListToPairsList(dataList, names)
    ds= DataListToSequenceList2(dataList, names)
    #PairsToContext(dl, names, 'pairs_context')
    #SequenceToSPMF(ds, 'sequence_context(p_and_m)')
    fl=AttrAndSeqFusion(ds,'SocialAttributes.csv')
    SequenceToSPMF(fl, 'socAttrAndSeqFusion(full)')

def exp2():
    ds= DataListToSequenceList2(dataList, names)
    SequenceToSPMF(ds, 'Seq')

exp2()



