def SN_transform_random_remove_nodes(cpu, bw, operations, removed_nodes):
    pseudo_cpu = deepcopy(cpu)
    pseudo_SN = deepcopy(bw)
    current_operations = 0
    current_removed_nodes = 0
    
    if (len(cpu)>removed_nodes):
        while current_removed_nodes<removed_nodes:
            f = randrange(len(cpu))
            if ((cpu[f]!= 0 and pseudo_cpu[f]!=0) or (cpu[f]==0)): #avoid to remove same substrate nodes
                pseudo_cpu[f] = 0
                current_removed_nodes += 1
                current_operations += 1
                for s in range(len(cpu)):
                    if pseudo_SN[s][f]!=0:
                        pseudo_SN[s][f] = 0
                        pseudo_SN[f][s] = pseudo_SN[s][f]
                        current_operations += 1
                        
        if current_operations < operations: #keep removing links
            num_of_candidate_removed_links = 0
            candidate_removed_links = []
            for i in range(len(pseudo_cpu)):  #check how many links in current SN
                for j in range(i+1,len(pseudo_cpu)):
                    if pseudo_SN[i][j]!=0:
                        num_of_candidate_removed_links += 1
                        candidate_removed_links.append([i,j])
            
            if num_of_candidate_removed_links>=operations-current_operations:    
                removed_links = list(itertools.combinations(candidate_removed_links, operations))
                #print("added links", added_links)
                for i in removed_links[0]:
                    #print("i = ", i)
                    pseudo_SN[i[0]][i[1]] = 0
                    pseudo_SN[i[1]][i[0]] = pseudo_SN[i[0]][i[1]]
            else: # remove all left links
                pseudo_SN = np.zeros((len(cpu), len(cpu)))
                
    
    return pseudo_cpu, pseudo_SN
