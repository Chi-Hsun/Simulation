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
