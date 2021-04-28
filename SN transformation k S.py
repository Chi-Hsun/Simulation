def SN_transform(k, cpu, bw, S):
    
    pseudo_nodes = []
    for i in range(len(cpu)):
        pseudo_nodes.append(cpu[i])
    #print(pseudo_nodes)
    
    additional_nodes_index = []
    for i in range(S):
        additional_nodes_index.append(len(cpu)+S-1)
        pseudo_nodes.append(300)   #random a number
    
    
    pseudo_SN = [[] for i in range(len(cpu)+S)]
    for i in range(len(cpu)+S):
        for j in range(len(cpu)+S):
            if(i<len(cpu)):
                if(j<len(cpu)):
                    pseudo_SN[i].append(bw[i][j])
                else:
                    pseudo_SN[i].append(0)
            else:
                pseudo_SN[i].append(0)
    print("pseudo SN = ", pseudo_SN)
    #pseudo_SN = deepcopy(bw)
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
    #print("type of sorted index = ", type(sorted_index))
    
    link_num_list = list(link_num)
    for i in range(S):
        link_num_list.append(0)
    
        
    goal_degree = max(link_num)
    #select nodes
    #counting 
    #計算每個degree共有幾個nodes
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
    while t1<k-S:
        t2 = t1
        print("current s = ",s)
        t1 =  t1 + counting_result[s]
        print("current t1 = ",t1)
        print("current t2 = ",t2)
        s = s+1
                
    thres_degree = goal_degree-s+1
    num_of_least_degree_nodes = k-t2-S
    print("num of least degree nodes = ",num_of_least_degree_nodes)
    
    # list all candidate sets
    
    candidate_set = []
    for j in range(len(link_num)):
        if link_num[j]==thres_degree:
            candidate_set.append(j)
        
    all_combinations = list(itertools.combinations(candidate_set,num_of_least_degree_nodes))  
    print("all combinations = ", all_combinations)
    candidate = np.zeros((len(all_combinations),k-S))
    for i in range(len(all_combinations)):
        for j in range(k-S):
            if j<t2:
                candidate[i][j] = sorted_index[j]
            else:
                candidate[i][j] = all_combinations[i][j-t2]
    
    print("candidate = ", candidate)
    
    # decide which k nodes are selected
    subgroup_links = np.zeros(len(candidate))
    print("bw = ", bw)
    for i in range(len(candidate)):
        for j in range(k-1-S):
            for h in range(j+1,k-S):
                print("bw[",int(candidate[i][j]),"][", int(candidate[i][h]),"] = ", bw[int(candidate[i][j])][int(candidate[i][h])])
                if (bw[int(candidate[i][j])][int(candidate[i][h])]!=0 and link_num[int(candidate[i][j])]!=goal_degree and link_num[int(candidate[i][h])]!=goal_degree ):
                    subgroup_links[i] += 1
    
    print("subgroup connectivity = ",subgroup_links)
    
    selected_nodes = candidate[np.argmax(-subgroup_links)]
    print("selected nodes = ", selected_nodes)
    
    queue = []
    add_additional_nodes_yet = 0
    for i in selected_nodes:
        if link_num[int(i)]== goal_degree:   #max degree的放在queue的最前面
            queue.append(int(i))
        else:
            if(S!=0 and add_additional_nodes_yet==0):
                for j in additional_nodes_index:    #再放新增的node
                    queue.append(int(j))
                    add_additional_nodes_yet = 1
            if(S==0 or add_additional_nodes_yet==1):
                queue.append(int(i))
            
            
    for i in sorted_index:
        print("i = ",i)
        print("i in queue", i in queue)    #先把被選的排在queue的前面
        if i not in queue:
            queue.append(i)    #剩下沒選到的排在後面
            
    print("queue = ", queue)
    current_max_degree_nodes = 0
    current_number_of_nodes = len(queue)
    i = 0
    while current_max_degree_nodes<k:
        s = 1
        while link_num_list[queue[i]]<goal_degree:
            if (i+s>=len(queue)):
                current_number_of_nodes += 1
                pseudo_nodes.append(current_number_of_nodes-1) #隨便random一個值
                queue.append(current_number_of_nodes-1)
                pseudo_SN.append([])
                link_num_list.append(0)
                
                for h in range(len(queue)-1):
                    pseudo_SN[h].append(0)
                    pseudo_SN[len(queue)-1].append(0)
                pseudo_SN[len(queue)-1].append(0)
                print("current pseudo nodes = ", pseudo_nodes)
                print("current queue = ", queue)
                print("current queue len = ", len(queue))
                print("current pseudo SN = ", pseudo_SN)
            
            print("current i = \n",i)
            print("current s = \n",s)
            
            if pseudo_SN[queue[i]][queue[i+s]] == 0:
                pseudo_SN[queue[i]][queue[i+s]] = 100
                pseudo_SN[queue[i+s]][queue[i]] = 100
                link_num_list[queue[i]]+=1
                link_num_list[queue[i+s]]+=1
                if (link_num_list[queue[i+s]]==goal_degree and i+s>=k):
                    current_max_degree_nodes += 1
                    if current_max_degree_nodes==k:
                        break
                    
            s+=1
        i += 1
        current_max_degree_nodes += 1
    return pseudo_SN, pseudo_nodes
