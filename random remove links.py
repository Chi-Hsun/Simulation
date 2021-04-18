def SN_transform_random_remove_links(cpu, bw, operations):
    pseudo_SN = deepcopy(bw)
    num_of_candidate_removed_links = 0
    candidate_removed_links = []
    for i in range(len(cpu)):  #check how many links in original SN
        for j in range(i+1,len(cpu)):
            if bw[i][j]!=0:
                num_of_candidate_removed_links += 1
                candidate_removed_links.append([i,j])
    #print("num_of_candidate_added_links", num_of_candidate_added_links)
    #print("candidate_added_links = ", candidate_added_links)
    #candidate_added_links = list(range(1,num_of_candidate_added_links+1))
    if num_of_candidate_removed_links>=operations:    
        removed_links = list(itertools.combinations(candidate_removed_links, operations))
        #print("added links", added_links)
        for i in removed_links[0]:
            #print("i = ", i)
            pseudo_SN[i[0]][i[1]] = 0
            pseudo_SN[i[1]][i[0]] = pseudo_SN[i[0]][i[1]]
        #print("pseudoSN = ", pseudo_SN)
        
    return pseudo_SN
    
