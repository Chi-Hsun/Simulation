import VNE_func as fc
import itertools
import numpy as np

from copy import copy, deepcopy
filename_sub = 'substrate1209_1.txt'
filename_vir = 'virtual1212.txt'
cpu_substrate, bw_substrate = read_substrate(filename_sub)
VNR_list = read_virtual(filename_vir)


num_of_timeslots = 5000
total_cpu = sum(cpu_substrate)
total_bw = sum(sum(bw_substrate))/2
print("total cpu = ",total_cpu)
print("total bw = ",total_bw)
acceptance = 0
total_cost = 0
total_revenue = 0
total_VNR = 0
node_resource_table = [[] for i in range(len(cpu_substrate))]
revenue_array = []
cost_array = []
acceptance_array = []
RC_array = []
cpu_utilization_array = []
bw_utilization_array = []

#先找出原本substrate network裡的所有link組合
link_pairs = list(find_all_links(bw_substrate))  
bw_resource_table = [[] for i in range(len(link_pairs))]
#print("all pairs: ", link_pairs)


for time in range(num_of_timeslots):
    print("time = ", time)
    if VNR_list!=[]:
        arr_time = VNR_list[0] 

        #先檢查是否有資源可以釋出
        for i in range(len(cpu_substrate)):   #node resource
            for j in range(0,len(node_resource_table[i]),2):
                if node_resource_table[i][j]==time:
                    cpu_substrate[i] = cpu_substrate[i]+ node_resource_table[i][j+1]

        for i in range(len(link_pairs)):    #link resource
            for j in range(0,len(bw_resource_table[i]),2):
                if bw_resource_table[i][j]==time:
                    which_link = link_pairs[i]
                    bw_substrate[which_link[0]][which_link[1]] = bw_substrate[which_link[0]][which_link[1]] + bw_resource_table[i][j+1]
                    bw_substrate[which_link[1]][which_link[0]] = bw_substrate[which_link[0]][which_link[1]]

        #print("node_resource_table: ", node_resource_table)
        #print("link_resource_table: ", bw_resource_table)
        #print("cpu substrate: ", cpu_substrate)
        #print("bw substrate: ", bw_substrate)




        while arr_time==time:   
            #print("take a VNR!")
            [arr_time, life_time, node_num, node_cap, bw_cap] = take_a_VNR(VNR_list, time) #pop one VNR from the VNR_list
            #print("arr time: ", arr_time)
            #print("life_time: ", life_time)
            #print("node_num: ", node_num)
            #print("node_cap: ", node_cap)
            #print("bw_cap: ", bw_cap)
            total_VNR = total_VNR+1
            del VNR_list[0:2*node_num+2]
            #print("VNR_list: ",VNR_list)

            subnodes = list(range(0,len(cpu_substrate)))
            #virlinks = list(range(0,len(node_cap)-1))


            # test all permutations
            all_combinations = list(itertools.permutations(subnodes, node_num))
            #print(all_combinations)
            opt_cost = sum(bw_cap)
            temp_best_cost = 100000000
            temp_opt = -1  #node是第幾個組合最好
            opt_link_index = -1  #link是第幾個組合最好
            #print("cpu substrate = ", cpu_substrate)
            #print("bw_substrate = ", bw_substrate)
            for i in range(len(all_combinations)):
                #print("i = ",i)
                cost = 100000000
                node_check = 1
                bw_check = 1
                path_num = np.zeros(len(node_cap)-1)
                for k in range(len(node_cap)):
                    if node_cap[k]>cpu_substrate[all_combinations[i][k]]:    #先測試這組解是否都滿足node constraints
                        node_check = 0
                        break
                       
                if node_check==1:   #node測試過再測試link         
                    #print("pass node check, for the ",i, "combinations")
                    bw_substrate_copy = deepcopy(bw_substrate)
                    graph = build_graph(bw_substrate_copy,1)
                    path_comb = []
                    for s in range(len(bw_cap)):
                        path = depthFirst(graph, all_combinations[i][s], [], [])
                        path = find_all_path(all_combinations[i][s], all_combinations[i][s+1], path)  #篩選出從source到destination的所有路境
                        path_comb.append(path)

                    #print("path_comb = ", path_comb)
                    total_path_comb = []
                    for s in range(len(bw_cap)):
                        each_path_num = list(range(0,len(path_comb[s])))
                        total_path_comb.append(each_path_num)
                    #print("total path comb = ", total_path_comb)                    
                    for k in range(len(bw_cap)):
                        if total_path_comb[k]==[]:
                            print("link mapping fail!")
                            bw_check = 0
                            break
                if node_check==1 and bw_check==1:
                    all_comb = [[]]
                    possible_path_comb = list_all_comb(total_path_comb, all_comb)
                    #print("possible path comb = ", possible_path_comb)
                    
                    # check whether each path candidate satisfies bw constraints, if yes, calculate the cost and compare with temp_best_cost.
                    for s in range(len(possible_path_comb)):
                        cost = 0
                        bw_copy = deepcopy(bw_substrate)
                        #print("bw_substrate_copy = ", bw_copy)
                        #print("turn to the ,", s, "possible_path_comb") 
                        flag = 0
                        for k in range(len(bw_cap)):
                            if flag ==-1:
                                break
                            else:
                                current_path = path_comb[k][possible_path_comb[s][k]]
                                #print("path for virtual link ",k, "is ", current_path)
                                for h in range(len(current_path)-1):
                                    bw_copy[current_path[h]][current_path[h+1]] = bw_copy[current_path[h]][current_path[h+1]] - bw_cap[k]
                                    bw_copy[current_path[h+1]][current_path[h]] = bw_copy[current_path[h]][current_path[h+1]]
                                    if bw_copy[current_path[h]][current_path[h+1]]>=0:
                                        cost = cost + bw_cap[k]
                                        #print("bw_copy = ",bw_copy)
                                        #print("cost = ", cost)
                                    else:
                                        cost = 100000000
                                        #print("link mapping fail!")
                                        flag = -1
                                        break
                        if cost<temp_best_cost:
                            #print("update current best!")
                            temp_best_cost = cost
                            temp_opt = i
                            opt_link_index = s   
                            link_opt = []
                            for x in range(len(bw_cap)):
                                link_opt.append(path_comb[x][possible_path_comb[opt_link_index][x]])
                            #print("current link opt = ", link_opt)
                                                                
                if temp_best_cost == opt_cost:   #找到最佳解就停止
                    print("Find the opt solution ", i, ", and the best path is ", link_opt )
                    break
            if temp_opt!=-1 and opt_link_index!=-1:
                #print("temp opt = ", temp_opt)
                #print("link opt = ", link_opt)
                print("the solution is ", all_combinations[temp_opt])
            else:
                print("reject this VNR!")

            if temp_opt!=-1:
                acceptance = acceptance+1
                total_cost = total_cost + temp_best_cost
                total_revenue = total_revenue + opt_cost

                for i in range(len(node_cap)):  #紀錄node資源什麼時候可以釋出，並且扣掉node資源
                    cpu_substrate[all_combinations[temp_opt][i]] = cpu_substrate[all_combinations[temp_opt][i]]-node_cap[i] #扣掉substrate node資源
                    node_resource_table[all_combinations[temp_opt][i]].append(arr_time+life_time)
                    node_resource_table[all_combinations[temp_opt][i]].append(node_cap[i])

            
                #紀錄link資源什麼時候可以釋出，並且扣掉link資源
                for i in range(len(node_cap)-1):
                    
                    for j in range(len(link_opt[i])-1):
                        bw_substrate[link_opt[i][j]][link_opt[i][j+1]] = bw_substrate[link_opt[i][j]][link_opt[i][j+1]] - bw_cap[i] #扣掉頻寬資源
                        bw_substrate[link_opt[i][j+1]][link_opt[i][j]] = bw_substrate[link_opt[i][j]][link_opt[i][j+1]]
                        a = link_opt[i][j]
                        b = link_opt[i][j+1]
                        if a<b:
                            bw_resource_table[link_pairs.index([a,b])].append(arr_time+life_time)
                            bw_resource_table[link_pairs.index([a,b])].append(bw_cap[i])
                        else:
                            bw_resource_table[link_pairs.index([b,a])].append(arr_time+life_time)
                            bw_resource_table[link_pairs.index([b,a])].append(bw_cap[i])
            if VNR_list!=[]:
                arr_time = VNR_list[0]  
            else:
                break
    cpu_utilization_array.append(1 - sum(cpu_substrate)/total_cpu)
    bw_utilization_array.append(1 - sum(sum(bw_substrate))/total_bw/2)
    revenue_array.append(total_revenue)
    cost_array.append(total_cost)
    if total_cost>0:
        RC_array.append(total_revenue/total_cost)
    else:
        RC_array.append(0)
  
    if total_VNR>0:
        acceptance_array.append(acceptance/total_VNR)
    else:
        acceptance_array.append(0)
#print all information

print("revenue =", revenue_array)
print("cost =", cost_array)
print("acceptance ratio =", acceptance_array)
print("RC ratio = ", RC_array)
print("CPU utilization =", cpu_utilization_array)
print("BW utilization =", bw_utilization_array)
