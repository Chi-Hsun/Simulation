import itertools
import numpy as np
from copy import copy, deepcopy
from random import randrange

rev = []
co = []
accep = []
rc = []
cpu_u = []
bw_u = []

print("jjjjjjjjjjjj")
for rr in range(1,11): 
    print("rr = ", rr)
    filename_sub = 'small substrate 10 nodes cap20-40.txt'
    filename_vir = 'small_arbitrary_virtual_1lifetime_nodenum6-12.txt'
    nodenum, cpu_substrate, bw_substrate = read_Inp_substrate(filename_sub)
    VNR_list = read_virtual(filename_vir)

    bw_substrate = SN_transform_random_add_links(cpu_substrate, bw_substrate, rr)

    Inp1_nodenum = nodenum
    Inp2_nodenum = 0

    num_of_timeslots = 100
    total_cpu = sum(cpu_substrate)
    total_bw = sum(sum(bw_substrate))/2
    #print("total cpu = ",total_cpu)
    #print("total bw = ",total_bw)
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
        #print("time = ", time)
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
                [arr_time, life_time, node_num, node_cap, bw_cap] = take_an_arbitrary_virtual(VNR_list, time) #pop one VNR from the VNR_list
                #print("arr time: ", arr_time)
                #print("life_time: ", life_time)
                #print("node_num: ", node_num)
                #print("node_cap: ", node_cap)
                #print("bw_cap: ", bw_cap)
                total_VNR = total_VNR+1
                #del VNR_list[0:2*node_num+2] #lineVNR
                del VNR_list[0:node_num*node_num+node_num+3]
                #print("VNR_list: ",VNR_list)

                subnodes = list(range(0,len(cpu_substrate)))
                #virlinks = list(range(0,len(node_cap)-1))


                SP_budget, SP_best_sol, SP_link_opt = PSO_fast_version(Inp1_nodenum, Inp2_nodenum, cpu_substrate, bw_substrate, node_num, node_cap, bw_cap, 800, 1, 1)
                #print("SP budget: ", SP_budget)
                #print("SP best sol: ", SP_best_sol)
                #print("SP link opt: ", SP_link_opt)

                if SP_budget!=100000000 and SP_best_sol!=[]:
                    acceptance = acceptance+1
                    total_cost = total_cost + SP_budget
                    total_revenue = total_revenue + sum(sum(bw_cap))/2

                    for i in range(len(node_cap)):  #紀錄node資源什麼時候可以釋出，並且扣掉node資源
                        cpu_substrate[SP_best_sol[i]] = cpu_substrate[SP_best_sol[i]]-node_cap[i] #扣掉substrate node資源
                        node_resource_table[SP_best_sol[i]].append(arr_time+life_time)
                        node_resource_table[SP_best_sol[i]].append(node_cap[i])


                    #紀錄link資源什麼時候可以釋出，並且扣掉link資源
                    r = -1
                    for i in range(len(node_cap)):
                        for s in range(i+1,len(node_cap)):
                            if  bw_cap[i][s] != 0:
                                r = r+1
                                for j in range(len(SP_link_opt[r])-1):
                                    bw_substrate[SP_link_opt[r][j]][SP_link_opt[r][j+1]] = bw_substrate[SP_link_opt[r][j]][SP_link_opt[r][j+1]] - bw_cap[i][s] #扣掉頻寬資源
                                    bw_substrate[SP_link_opt[r][j+1]][SP_link_opt[r][j]] = bw_substrate[SP_link_opt[r][j]][SP_link_opt[r][j+1]]
                                    a = SP_link_opt[r][j]
                                    b = SP_link_opt[r][j+1]
                                    if a<b:
                                        bw_resource_table[link_pairs.index([a,b])].append(arr_time+life_time)
                                        bw_resource_table[link_pairs.index([a,b])].append(bw_cap[i][s])
                                    else:
                                        bw_resource_table[link_pairs.index([b,a])].append(arr_time+life_time)
                                        bw_resource_table[link_pairs.index([b,a])].append(bw_cap[i][s])

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

    #print("revenue =", revenue_array[num_of_timeslots-1])
    #print("cost =", cost_array[num_of_timeslots-1])
    #print("acceptance ratio =", acceptance_array[num_of_timeslots-1])
    #print("RC ratio = ", RC_array[num_of_timeslots-1])
    #print("CPU utilization =", cpu_utilization_array[num_of_timeslots-1])
    #print("BW utilization =", bw_utilization_array[num_of_timeslots-1])
    
    rev.append(revenue_array[num_of_timeslots-1])
    co.append(cost_array[num_of_timeslots-1])
    accep.append(acceptance_array[num_of_timeslots-1])
    rc.append(RC_array[num_of_timeslots-1])
    cpu_u.append(cpu_utilization_array[num_of_timeslots-1])
    bw_u.append(bw_utilization_array[num_of_timeslots-1])

print("revenue =", rev)
print("cost =", co)
print("acceptance ratio =", accep)
print("RC ratio = ", rc)
print("CPU utilization =", cpu_u)
print("BW utilization =", bw_u)
