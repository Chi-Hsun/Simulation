#import VNE_func as fc
import itertools
import numpy as np

filename_sub = 'substrate1130.txt'
filename_vir = 'virtual1130.txt'
cpu_substrate, bw_substrate = read_substrate(filename_sub)
VNR_list = read_virtual(filename_vir)


num_of_timeslots = 5000
acceptance = 0
total_cost = 0
total_revenue = 0
total_VNR = 0
node_resource_table = [[] for i in range(len(cpu_substrate))]
revenue_array = []
cost_array = []
acceptance_array = []
RC_array = []

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
            virlinks = list(range(0,len(node_cap)-1))


            # test all permutations
            all_combinations = list(itertools.permutations(subnodes))
            all_link_combinations = list(itertools.permutations(virlinks)) #列出所有找link的順序
            #print("all_link_combinations = ", all_link_combinations)
            #print(all_combinations)
            opt_cost = sum(bw_cap)
            temp_best_cost = 100000000
            temp_opt = -1  #node是第幾個組合最好
            opt_link = -1  #link是第幾個組合最好
            for i in range(len(all_combinations)):
                cost = 100000000
                node_check = 1
                bw_check = 1
                path_num = np.zeros(len(node_cap)-1)
                for k in range(len(node_cap)):
                    if node_cap[k]>cpu_substrate[all_combinations[i][k]]:    #先測試這組解是否都滿足node constraints
                        node_check = 0
                        break
                       
                if node_check==1:   #node測試過再測試link                    
                    link_cost = np.zeros(len(all_link_combinations))
                    for x in range(len(all_link_combinations)):                        
                        copy_bw_substrate = bw_substrate
                        for s in range(len(node_cap)-1):
                            path = shortest_path(all_combinations[i][all_link_combinations[x][s]], all_combinations[i][all_link_combinations[x][s]+1], bw_cap[all_link_combinations[x][s]], copy_bw_substrate)
                            #print("path = ",path)
                            if path == -1:
                                link_cost[x] = 100000000
                                break
                            else:
                                for j in range(len(path)-1):
                                    copy_bw_substrate[path[j]][path[j+1]] = copy_bw_substrate[path[j]][path[j+1]] - bw_cap[all_link_combinations[x][s]]  #扣掉頻寬資源
                                    copy_bw_substrate[path[j+1]][path[j]] = copy_bw_substrate[path[j]][path[j+1]]
                                    hop = len(path)-1
                                    link_cost[x] = link_cost[x] + bw_cap[s]*hop
                                #print("link_cost", x, "=", link_cost[x])
                #print("link cost = ", link_cost)
                #print("min link cost")
                if node_check==1 and min(link_cost)<temp_best_cost:
                    opt_link = all_link_combinations[list(link_cost).index(min(link_cost))]
                    temp_best_cost = min(link_cost)
                    temp_opt = i
                    if temp_best_cost == opt_cost:   #找到最佳解就停止
                        #print("Find the opt solution ", i)
                        break
            #print("temp opt = ", temp_opt)
            #print("opt link = ", opt_link)
            #print("the solution is ", all_combinations[temp_opt])

            if temp_opt!=-1:
                acceptance = acceptance+1
                total_cost = total_cost + temp_best_cost
                total_revenue = total_revenue + opt_cost

                for i in range(len(node_cap)):  #紀錄node資源什麼時候可以釋出，並且扣掉node資源
                    cpu_substrate[all_combinations[temp_opt][i]] = cpu_substrate[all_combinations[temp_opt][i]]-node_cap[i] #扣掉substrate node資源
                    node_resource_table[all_combinations[temp_opt][i]].append(arr_time+life_time)
                    node_resource_table[all_combinations[temp_opt][i]].append(node_cap[i])

            
                #紀錄node資源什麼時候可以釋出，並且扣掉node資源
                for i in range(len(node_cap)-1):
                    path = shortest_path(all_combinations[temp_opt][opt_link[i]], all_combinations[temp_opt][opt_link[i]+1], bw_cap[opt_link[i]], bw_substrate)
                                                   
                
               
                    for j in range(len(path)-1):
                        bw_substrate[path[j]][path[j+1]] = bw_substrate[path[j]][path[j+1]] - bw_cap[opt_link[i]] #扣掉頻寬資源
                        bw_substrate[path[j+1]][path[j]] = bw_substrate[path[j]][path[j+1]]
                        a = path[j]
                        b = path[j+1]
                        if a<b:
                            bw_resource_table[link_pairs.index([a,b])].append(arr_time+life_time)
                            bw_resource_table[link_pairs.index([a,b])].append(bw_cap[opt_link[i]])
                        else:
                            bw_resource_table[link_pairs.index([b,a])].append(arr_time+life_time)
                            bw_resource_table[link_pairs.index([b,a])].append(bw_cap[opt_link[i]])
            if VNR_list!=[]:
                arr_time = VNR_list[0]  
            else:
                break

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
