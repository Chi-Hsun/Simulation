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

# build candidate list for each virtual node
def build_candidate(node_list, substrate_node):
    candidate = np.zeros((len(node_list), len(substrate_node)))
    for i in range(len(node_list)):                     
        for j in range(len(substrate_node)):
            if substrate_node[j]>=node_list[i]:
                candidate[i][j] = 1
    return candidate


def node_mapping(ithnode, node_cap, substrate, candidate):
    flag = 0
    for i in range(len(substrate)):
        if candidate[ithnode][i] == 1:
            substrate[i] = substrate[i] - node_cap[ithnode]
            print('virtual node', ithnode, 'is mapped onto susbtrate node', i)
            flag = 1    
            for j in range(len(node_cap)):
                candidate[j][i] = 0
            break;
    if flag == 0:
        print('node mapping fail!')
    return substrate, candidate, flag


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
