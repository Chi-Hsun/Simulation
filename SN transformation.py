def SN_transform(k, cpu, bw):
    pseudo_SN = deepcopy(bw)
    #calculate links
    link_num = np.zeros(np.size(bw,0))
  
    for i in range(np.size(bw,0)):
        for j in range(np.size(bw,1)):
            if bw[i][j]!=0:
                link_num[i] += 1
    print("link num = ",link_num)
    #sort index form large to small
    sorted_index = np.argsort(-link_num)
    print("sorted index = ", sorted_index)
    print("type of sorted index = ", type(sorted_index))
    goal_degree = max(link_num)
    #select nodes
    #counting 
    counting_result = []
    for i in range(int(goal_degree),-1,-1):
        s = 0
        for j in link_num:
            if j==i:
                s += 1
        counting_result.append(s)    
    print("counting result =", counting_result)
    
    # calculate threshold degree
    t1 = 0
    t2 = t1
    s = 0
    while t1<k:
        t2 = t1
        print("current s = ",s)
        t1 =  t1 + counting_result[s]
        #print("current t1 = ",t1)
        #print("current t2 = ",t2)
        s = s+1
                
    thres_degree = goal_degree-s+1
    num_of_least_degree_nodes = k-t2
    print("num of least degree nodes = ",num_of_least_degree_nodes)
    
    # list all candidate sets
    
    candidate_set = []
    for j in range(len(link_num)):
        if link_num[j]==thres_degree:
            candidate_set.append(j)
        
    all_combinations = list(itertools.combinations(candidate_set,num_of_least_degree_nodes))  
    print("all combinations = ", all_combinations)
    candidate = np.zeros((len(all_combinations),k))
    for i in range(len(all_combinations)):
        for j in range(k):
            if j<t2:
                candidate[i][j] = sorted_index[j]
            else:
                candidate[i][j] = all_combinations[i][j-t2]
    
    print("candidate = ", candidate)
    # decide which k nodes are selected
    subgroup_links = np.zeros(len(candidate))
    print("bw = ", bw)
    for i in range(len(candidate)):
        for j in range(k-1):
            for h in range(j+1,k):
                print("bw[",int(candidate[i][j]),"][", int(candidate[i][h]),"] = ", bw[int(candidate[i][j])][int(candidate[i][h])])
                if bw[int(candidate[i][j])][int(candidate[i][h])]!=0:
                    subgroup_links[i] += 1
    
    print("subgroup connectivity = ",subgroup_links)
    
    selected_nodes = candidate[np.argmax(-subgroup_links)]
    print("selected nodes = ", selected_nodes)
    
    queue = []
    for i in selected_nodes:
        queue.append(int(i))
    for i in sorted_index:
        print("i = ",i)
        print("i in queue", i in queue)
        if i not in queue:
            queue.append(i)
            
    print("queue = ", queue)
    for i in range(k):
        s = 1
        while link_num[queue[i]]<goal_degree:
            if bw[queue[i]][queue[i+s]] == 0:
                pseudo_SN[queue[i]][queue[i+s]] = 1
                pseudo_SN[queue[i+s]][queue[i]] = 1
                link_num[queue[i]]+=1
                link_num[queue[i+s]]+=1
            s += 1
    return pseudo_SN
