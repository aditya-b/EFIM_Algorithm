import numpy
from collections import defaultdict

def preprocess_data(ipfile,opfile,minimumutil,transfile):
        inputfile=open(ipfile,"r")
        data_dict=defaultdict(list)
        print(ipfile,opfile,minimumutil,transfile,sep="\n")
        tot_utility=dict()
        line=inputfile.readline()
        i=0
        while True:
            line=inputfile.readline()
            if line=="":
                  break
            linelist=line.split(",")
            tranid=linelist[0].strip()
            itemid=linelist[1].strip()
            quantity=int(linelist[2])
            unit=float(linelist[3])
            try:
                  data_dict[tranid][0].append(itemid)
                  data_dict[tranid][1].append(abs(quantity))
                  data_dict[tranid][2].append(round(unit,2))
                  data_dict[tranid][3]+=round(abs(quantity)*unit,2)
            except IndexError:
                  data_dict[tranid]=list()
                  data_dict[tranid].append([itemid])
                  data_dict[tranid].append([abs(quantity)])
                  data_dict[tranid].append([round(unit,2)])
                  data_dict[tranid].append(round(abs(quantity)*unit,2))
            i=i+1
        for tranid in data_dict.keys():
            items=data_dict[tranid][0]
            quants=data_dict[tranid][1]
            profits=data_dict[tranid][2]
            item_len=len(items)
            for i in range(item_len):
                    try:
                        tot_utility[items[i]] = round((tot_utility[items[i]] + (abs(quants[i]) * profits[i])), 2)
                    except KeyError:
                        tot_utility[items[i]] = round((abs(quants[i]) * profits[i]), 2)
        filtereditems=filterbytwu(data_dict,tot_utility,minimumutil)
        filtereditems.sort(key=lambda x:x[1])
        database=get_final_database(data_dict,filtereditems,transfile)
        alpha=[]
        primary=[]
        secondary=[]
        for item in filtereditems:
            if local_utility(database,[item[1]])>=float(minimumutil):
                secondary.append(item[1])
            if sub_tree_utility(database,[item[1]])>=float(minimumutil):
                primary.append(item[1])
        result=[]
        result_file=open(opfile,"w")
        result_file.write("Itemsets,Profit\n")
        EFIMalgorithm(database,primary,secondary,alpha,result,0,len(filtereditems),result_file,minimumutil)
        result_file.close()
        
def filterbytwu(data_dict,tot_utility,minutility):
        twu_dict=dict()
        min_utility=float(minutility)
        for item in tot_utility.keys():
                twu=0
                for values in data_dict.values():
                    setofitems=values[0]
                    if item in setofitems:
                        twu+=values[3]
                if twu>=min_utility:
                    twu_dict[item]=round(twu,2)
        twu_list=[]
        for i in twu_dict.keys():
                twu_list.append((twu_dict[i],i))
        return twu_list

def get_final_database(data_dict,filtered_items,transfile):
        print(transfile)
        database=defaultdict(list)
        for tranid in data_dict.keys():
                for item in filtered_items:
                        try:
                                itemid=item[1]
                                index=data_dict[tranid][0].index(itemid)
                                quantity=data_dict[tranid][1][index]
                                unit=data_dict[tranid][2][index]
                                try:
                                        database[tranid][0].append(itemid)
                                        database[tranid][1].append(quantity)
                                        database[tranid][2].append(unit)
                                        database[tranid][3]+=round(quantity*unit,2)
                                except IndexError:
                                        database[tranid]=list()
                                        database[tranid].append([itemid])
                                        database[tranid].append([quantity])
                                        database[tranid].append([unit])
                                        database[tranid].append(round(quantity*unit,2))
                        except ValueError:
                                pass
        for tranid in database.keys():
            z=zip(database[tranid][0],database[tranid][1],database[tranid][2])
            z=sorted(z)
            l1=[]
            l2=[]
            l3=[]
            for item in z:
                l1.append(item[0])
                l2.append(item[1])
                l3.append(item[2])
            database[tranid][0]=l1.copy()
            database[tranid][1]=l2.copy()
            database[tranid][2]=l3.copy()
        transactions=open(transfile,"w")
        transactions.write("Transaction ID,Items,Quantity,Unit Profit,Transaction utility\n")
        for key in database.keys():
            transactions.write(str(key)+',"'+str(database[key][0])+'","'+str(database[key][1])+'","'+str(database[key][2])+'",'+str(database[key][3])+'\n')
        transactions.close()
        return database

def local_utility(database,itemset):
    lu=0
    for tranid in database.keys():
        set1=set(itemset)
        set2=set(database[tranid][0])
        if set1.issubset(set2):
            lu+=database[tranid][3]
    lu=round(lu,2)
    return lu

def sub_tree_utility(database,itemset):
    su=0
    itemset.sort()
    for tranid in database.keys():
        set1=set(itemset)
        set2=set(database[tranid][0])
        index=0
        if set1.issubset(set2):
            for item in itemset:
                index=database[tranid][0].index(item)
                su+=round(database[tranid][1][index]*database[tranid][2][index],2)
            try:
                quan=numpy.array(database[tranid][1][index+1:])
                unit=numpy.array(database[tranid][2][index+1:])
                su+=sum(quan*unit)
            except IndexError:
                pass
    return su

def get_utility(database,itemset):
    util=0
    for tranid in database.keys():
        set1=set(itemset)
        set2=set(database[tranid][0])
        if set1.issubset(set2):
            for item in itemset:
                index=database[tranid][0].index(item)
                util+=round(database[tranid][1][index]*database[tranid][2][index],2)
    util=round(util,2)
    return util

def EFIMalgorithm(database,primary,secondary,alpha,result,iteration,max_iter,result_file,minutility):
    if iteration>max_iter:
        return
    try:
        primary.sort()
        secondary.sort()
        len_prim=len(primary)
        for i in range(len_prim):
            beta=alpha.copy()
            try:
                x=beta.index(primary[i])
            except ValueError:
                beta.append(primary[i])
            util=get_utility(database,beta)
            if util>=float(minutility):
                beta.sort()
                if not beta in result:
                    result.append(beta)
                    result_file.write('"'+str(beta)+'",'+str(util)+"\n")
            prim=[]
            sec=[]
            len_sec=len(secondary)
            for it in range(len_sec):
                l=beta.copy()
                try:
                    l.index(secondary[it])
                except ValueError:
                    l.append(secondary[it])
                    if local_utility(database,l)>=float(minutility):
                        sec.append(secondary[it])
                    if sub_tree_utility(database,l)>=float(minutility):
                        prim.append(secondary[it])
            EFIMalgorithm(database,prim,sec,beta,result,iteration+1,max_iter,result_file,minutility)
    except IndexError:
        return
