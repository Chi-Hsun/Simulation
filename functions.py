def read_substrate(filename):
    with open(filename, 'r') as f:#with語句自動呼叫close()方法
        Inp1_nodenum = int(f.readline())
        Inp2_nodenum = int(f.readline())
        link = np.zeros((Inp1_nodenum+Inp2_nodenum,Inp1_nodenum+Inp2_nodenum))
        CPU = np.zeros(Inp1_nodenum+Inp2_nodenum)
        
        for i in range(2):
            line = f.readline()
            temp = line.split()
            for j in range(len(temp)):
                CPU[i*len(temp)+j] = int(temp[j])
        for i in range(Inp1_nodenum+Inp2_nodenum):
            line = f.readline()
            link[i] = line.split()
            
    return CPU,link

def read_virtual(filename):
    VNR_list = np.genfromtxt(filename)
    VNR_list = list(VNR_list)
    return VNR_list

def take_a_VNR(VNR_list, time):
    if int(VNR_list[0]) == time:
        arr_time = int(VNR_list[0])
        life_time = int(VNR_list[1])
        node_num = int(VNR_list[2])
        node_cap = np.zeros(node_num)
        bw_cap = np.zeros(node_num-1)
        for i in range(node_num):
            node_cap[i] = VNR_list[3+i]
        for i in range(node_num+3, 2*node_num+2):
            bw_cap[i-node_num-3] = VNR_list[i]
        return arr_time, life_time, node_num, node_cap, bw_cap
    else:
        arr_time = -1
        life_time = -1
        node_num = 1
        node_cap = np.zeros(node_num)
        bw_cap = np.zeros(node_num-1)
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
        print("unreachable!")
        path = -1
    
    return path
