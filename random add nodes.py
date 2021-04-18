def SN_transform_random_add_nodes(cpu, bw, operations, added_nodes):
    if (operations>=added_nodes*2):
        pseudo_cpu = np.zeros(len(cpu)+added_nodes)
        pseudo_SN = np.zeros((len(cpu)+added_nodes, len(cpu)+added_nodes))
        

        for i in range(len(cpu)+added_nodes):
            if i <len(cpu):
                pseudo_cpu[i] = cpu[i]
            else:
                pseudo_cpu[i] = randrange(10,50)+1   #pseudo node cpu capacity
                f = randrange(len(cpu))
                pseudo_SN[f][i] = randrange(10,50)+1 # the pseudo nodes must connect to original SN with at least one link
                pseudo_SN[i][f] = pseudo_SN[f][i]

        num_of_candidate_added_links = 0
        candidate_added_links = []


        for i in range(len(pseudo_cpu)):
            for j in range(i+1, len(pseudo_cpu)):
                if (i<len(cpu) and j<len(cpu)):
                    pseudo_SN[i][j] = bw[i][j]

                else:
                    if pseudo_SN[i][j]==0:
                        num_of_candidate_added_links += 1
                        candidate_added_links.append([i,j])
                        
                pseudo_SN[j][i] = pseudo_SN[i][j]
                
                
                    

        #print("num_of_candidate_added_links", num_of_candidate_added_links)
        #print("candidate_added_links = ", candidate_added_links)
        #candidate_added_links = list(range(1,num_of_candidate_added_links+1))
        if num_of_candidate_added_links>=(operations - added_nodes*2):    
            added_links = list(itertools.combinations(candidate_added_links, operations - added_nodes*2))
            #print("added links", added_links)
            if(len(added_links)-1)>0:
                #print("SN modified!!!!!!")
                ran = randrange(0,len(added_links)-1)
                for i in added_links[ran]:
                    #print("i = ", i)
                    pseudo_SN[i[0]][i[1]] = randrange(10,50)+1
                    pseudo_SN[i[1]][i[0]] = pseudo_SN[i[0]][i[1]]

        else:
            for i in range(len(pseudo_cpu)):
                for j in range(i+1, pseudo_cpu):
                    if pseudo_SN[i][j] == 0:
                        pseudo_SN[i][j] = randrange(10,50)+1
                        pseudo_SN[j][i] = pseudo_SN[i][j]
                    
    else:
        pseudo_cpu = deepcopy(cpu)
        pseudo_SN = deepcopy(bw)
    
    #print("pseudocpu = ,", pseudo_cpu)
    #print("pseudoSN = ", pseudo_SN)
    
    
    return pseudo_cpu, pseudo_SN
    
