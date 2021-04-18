def read_virtual(filename):
    VNR_list = np.genfromtxt(filename)
    VNR_list = list(VNR_list)
    return VNR_list

def read_Inp_substrate(filename):
    with open(filename, 'r') as f:#with語句自動呼叫close()方法
        nodenum = int(f.readline())
        CPU = np.zeros(nodenum)
        line = f.readline()
        temp = line.split()
        for i in range(nodenum):
            CPU[i] = int(temp[i])
        link = np.zeros((nodenum,nodenum))
        for i in range(nodenum):
            line = f.readline()
            link[i] = line.split()
    return nodenum, CPU, link

def take_an_arbitrary_virtual(VNR_list, time):
    if int(VNR_list[0]) == time:
        arr_time = int(VNR_list[0])
        life_time = int(VNR_list[1])
        node_num = int(VNR_list[2])
        node_cap = np.zeros(node_num)
        bw_cap = np.zeros((node_num, node_num))
        for i in range(node_num):
            node_cap[i] = VNR_list[3+i]
        k = node_num+3
        for i in range(node_num):
            for j in range(node_num):
                bw_cap[i][j] = VNR_list[k]
                k = k+1
    else:
        arr_time = -1
        life_time = -1
        node_num = 1
        node_cap = np.zeros(node_num)
        bw_cap = np.zeros((node_num, node_num))
    return arr_time, life_time, node_num, node_cap, bw_cap            

def find_all_links(substrate_link):
    links = []
    for i in range(len(substrate_link)):
        for j in range(i+1, len(substrate_link)):
            if substrate_link[i][j]!=0:
                links. append([i,j])
    return links


#link mapping
def shortest_path(source, des, virtual_link, substrate_link):
    # build adjanjency list
    adjanjency_list = np.ones((len(substrate_link), len(substrate_link)))*(-1)
    for i in range(len(substrate_link)):
        temp = -1
        for j in range(len(substrate_link)):
            if substrate_link[i][j]>=virtual_link:
                temp = temp + 1
                adjanjency_list[i][temp] = j
                
    queue = [source]
    path = [des]
    dis = np.ones(len(substrate_link))*(-1)
    last_hop = np.ones(len(substrate_link))*(-1)
    marked = np.zeros(len(substrate_link))
    marked[source] = 1
    while queue!=[]:
        u = queue[0]
        del queue[0]
        for i in adjanjency_list[int(u)]:
            if int(i)==-1:
                break
            else:
                if marked[int(i)]==0:
                    marked[int(i)] = 1
                    queue.append(i)
                    dis[int(i)] = dis[int(u)]+1
                    last_hop[int(i)] = u
    index = des
    while last_hop[int(index)]!=-1:
        path.append(int(last_hop[int(index)]))
        index = last_hop[int(index)]
    if last_hop[int(index)]==-1 and int(index)!=source:
        #print("unreachable!")
        path = -1
    
    return path

def build_graph(bw_substrate, bw_cap):
    graph = {}
    for i in range(len(bw_substrate)):
        addnode = []
        for j in range(len(bw_substrate)):
            if bw_substrate[i][j]>=bw_cap:
                addnode.append(j)
        graph[i] = addnode
    return graph



def depthFirst(graph, currentVertex, visited, visitedList):
    visited.append(currentVertex)
    for vertex in graph[currentVertex]:
        if vertex not in visited:
            depthFirst(graph, vertex, visited.copy(), visitedList)
            
    visitedList.append(visited)
    return visitedList

def find_all_path(src,des,visitedList):
    path = []
    for i in visitedList:
        if i[-1] == des:
            path.append(i)
    return path



def list_all_comb(test,all_comb):
    out = []
    if len(all_comb)==0:
        for i in range(len(test[0])):
            all_comb.append(test[0][i])
        del test[0]
        return list_all_comb(test, all_comb) 
    for i in range(len(all_comb)): 
        for j in range(len(test[0])):
            temp = []
            temp = all_comb[i].copy()
            temp.append(j)
            out.append(temp)
    if len(test)==1:
        return out
    else:
        del test[0]
        return list_all_comb(test, out)
        
def PSO_fast_version(Inp1_nodenum, Inp2_nodenum, cpu_substrate, bw_substrate, node_num, node_cap, bw_cap, ite_times, particles, mode): # mode=1, InP; mode=0, SP
    link_num = 0; #calculate number of links
    virtual_links = []
    virtual_links_index = []
    
    
    # sort virtual links, from high to low requirements    
    for i in range(node_num):
        for j in range(i, node_num):
            if bw_cap[i][j] !=0:
                virtual_links.append(bw_cap[i][j])
                virtual_links_index.append([i,j])
                link_num += 1 
                
    #print("virrrrrtal links = ",virtual_links)
    #print("virtual links index = ", virtual_links_index)
    sorted_virtual_links = list(np.argsort(virtual_links))
    sorted_virtual_links.reverse()
    #print("sorted virtual links = ", sorted_virtual_links)
        
    if link_num==0:
        return 100000000, [], []
    
    temp_best_sol = []
    temp_best_cost = 100000000
    link_opt = []
    
    
    for i in range(ite_times):
        bw_substrate_copy = deepcopy(bw_substrate)
        cpu_substrate_copy = deepcopy(cpu_substrate)
        #print(i,"-th iteration")
        node_check = 1
        bw_check = 1
        temp_sol = []
        for j in range(node_num):
            temp = randrange(len(cpu_substrate)) 
            if(node_cap[j]>cpu_substrate_copy[temp]):
                cost = 100000000
                temp_sol = []
                node_check = 0
                break;
            else:
                temp_sol.append(temp)
                cpu_substrate_copy[temp] = cpu_substrate_copy[temp] - node_cap[j]
        #print("temp sol = ", temp_sol)
        
        if (mode==0 and temp_sol!=[]):
            temp_node_assigned_to_Inp1 = []
            temp_node_assigned_to_Inp2 = []
            for j in range(node_num):
                if(temp_sol[j]<Inp1_nodenum):
                    temp_node_assigned_to_Inp1.append(temp_sol[j])
                else:
                    temp_node_assigned_to_Inp2.append(temp_sol[j]) 
            if(len(temp_node_assigned_to_Inp1) ==0 or len(temp_node_assigned_to_Inp2) ==0):
                node_check = 0
                cost = 100000000
                temp_sol = []
                print("reject this VNR due to SP privacy")
        
        path_comb = []
        if node_check==1:
            
            #start finding path for each virtual link
            total_path = []
            cost = 0
            for j in sorted_virtual_links:
                
                #print("jjjjjj = ",j)
                #print("virtual link index[j] = ", virtual_links_index[j])
                #print("virtual link index[j][0] = ", virtual_links_index[j][0])
                
                path = shortest_path(temp_sol[virtual_links_index[j][0]], temp_sol[virtual_links_index[j][1]], virtual_links[j], bw_substrate_copy)
                #print("pathhhhhhhhhh = ", path)
                
                if path == -1:
                    bw_check = 0
                    cost = 100000000
                    break
                else:
                    total_path.append(path)                    
                    #calculate cost and occupied resource 
                    cost = cost + virtual_links[j]*(len(path)-1)
                    for s in range(len(path)-1):
                        bw_substrate_copy[path[s]][path[s+1]] = bw_substrate_copy[path[s]][path[s+1]]-virtual_links[j]
                        bw_substrate_copy[path[s+1]][path[s]] = bw_substrate_copy[path[s]][path[s+1]]
                     
        if node_check==1 and bw_check==1:
            
            if cost<temp_best_cost:
                #print("update current best!")
                temp_best_cost = cost
                temp_best_sol = temp_sol  
                #在這邊讓link_opt的順序變正確的
                link_opt = []
                    
                #print("temp best cost = ", temp_best_cost)
                #print("temp best sol = ", temp_best_sol)
                    
                for x in range(len(virtual_links)):
                    a = sorted_virtual_links.index(x)
                    link_opt.append(total_path[a])
                #print("current link opt = ", link_opt)
                    
                    
            if temp_best_cost == 0:   #找到最佳解就停止
                #print("Find the opt solution ", temp_best_sol, ", and the best path is ", link_opt )
                break
            
            
            
    #if temp_best_cost!=100000000 and temp_best_sol!=[]:
        #print("temp best cost = ", temp_best_cost)
        #print("temp best sol = ", temp_best_sol)
        #print("current link opt = ", link_opt)
    #else:
        #print("reject this VNR!")    
    

    return temp_best_cost, temp_best_sol, link_opt
