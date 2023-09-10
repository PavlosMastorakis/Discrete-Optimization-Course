#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])


def sec():
    return 1


paths = [[]]
ans_path = []
lpath = []
rpath = []


def expectation(new_node, n, w, items):
    # breakpoint()
    if new_node[2] > w:
        return 0
    val_bound = new_node[1]
    j = new_node[0]
    totalweight = new_node[2]
    while j < n and totalweight+items[j].weight <= w:
        totalweight += items[j].weight
        val_bound += items[j].value
        j += 1
    if j < n:
        val_bound += (w-totalweight)*items[j].value/items[j].weight
    return val_bound


# n: item_count, w: capacity
def body(n, w, items):
    b = 0
    nodes = []
    # node = [level, value, room, expectation]
    node = [0, 0, 0, 0]
    nodes.append(node)
    global paths
    global rpath
    global lpath
    global ans_path
    while len(nodes) != 0:
        # breakpoint()
        node = nodes.pop(0)
        if node[0] == n:
            if node[1] >= b and node[2] <= w:
                b = node[1]
                ans_path = paths.pop(0)
            else:
                del paths[0]
        else:
            new_node = [node[0]+1, node[1]+items[node[0]].value, node[2]+items[node[0]].weight]
            if new_node[2] <= w and new_node[1] > b:
                b = new_node[1]
                # breakpoint()
                ans_path = paths[0].copy()
                ans_path.append(1)
            new_node.append(expectation(new_node, n, w, items))
            rpath = paths.pop(0)
            lpath = rpath.copy()
            if new_node[3] >= b:
                nodes.append(new_node)
                lpath.append(1)
                paths.append(lpath)
            new_node = [node[0]+1, node[1], node[2]]
            new_node.append(expectation(new_node, n, w, items))
            if new_node[3] >= b:
                nodes.append(new_node)
                rpath.append(0)
                paths.append(rpath)
    while len(ans_path) < n:
        ans_path.append(0)
    return b


# vre will be a vector with: Value, Room and Estimate
"""value = 0
prob = []
prob2 = []


def right_step(h_vre, item):
    h_vre[2] -= item.value
    return h_vre


def left_step(h_vre, item):
    h_vre[0] += item.value
    h_vre[1] -= item.weight
    return h_vre


def bins(vre, item_count, path, best_path, i, items):
    if i == item_count:
        global value
        global prob
        global prob2
        sl_obj = slice(len(prob))
        if len(prob) != 0 and prob == path[sl_obj]:
            return
        if len(prob2) != 0 and prob2 == path[sl_obj]:
            return
        h_vre = []
        for el in vre:
            h_vre.append(el)
        for j in range(0, item_count):
            if path[j] == 0:
                h_vre = right_step(h_vre, items[j])
            else:
                if h_vre[1] >= items[j].weight:
                    h_vre = left_step(h_vre, items[j])
                else:
                    for k in range(0, j+1):
                        prob.append(path[k])
                    break  # Does not continue for the rest of the items (rest of j)
            if h_vre[2] < value:
                for k in range(0, j + 1):
                    prob2.append(path[k])
                break
            # breakpoint()
            if j == item_count-1 and h_vre[1] >= 0 and h_vre[0] > value:
                best_path.clear()
                value = h_vre[0]
                for el in path:
                    best_path.append(el)
        return

    path[i] = 1
    bins(vre, item_count, path, best_path, i+1, items)
    # breakpoint()
    path[i] = 0
    bins(vre, item_count, path, best_path, i+1, items)
    # breakpoint()
    # return best_path"""


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    global paths
    global ans_path
    global lpath
    global rpath

    paths = [[]]
    ans_path = []
    lpath = []
    rpath = []

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # My solution
    if item_count == 200:
        taken = [0] * len(items)
        results = [[0 for i in range(item_count + 1)] for j in range(capacity + 1)]
        # breakpoint()
        for j in range(1, item_count + 1):
            for i in range(1, capacity + 1):
                if items[j - 1].weight <= i:
                    h = results[i - items[j - 1].weight][j - 1] + items[j - 1].value
                else:
                    h = 0
                    # breakpoint()
                results[i][j] = max(results[i][j - 1], h)
            # breakpoint()

        value = results[capacity][item_count]
        row = capacity
        for i in range(item_count, 0, -1):
            if results[row][i] == results[row][i - 1]:
                continue
            else:
                row -= items[i - 1].weight
                taken[i - 1] = 1
            # breakpoint()
        fin_ans = taken
        answer = value
    else:
        # My solution 2
        # To find the best estimation, v and create and sort value/weight array vpw
        vpw = []
        for i in range(0, item_count):
            h = items[i].value / items[i].weight
            vpw.append([i, h])
        vpw.sort(key=lambda x: x[1], reverse=True)
        v = 0
        cap_h = capacity
        i = 0
        while cap_h - items[vpw[i][0]].weight >= 0:
            v += items[vpw[i][0]].value
            cap_h -= items[vpw[i][0]].weight
            i += 1
        if cap_h > 0:
            v += (cap_h / items[vpw[i][0]].weight) * items[vpw[i][0]].value
        # breakpoint()
        items_sorted = []
        for i in range(0, item_count):
            items_sorted.append(items[vpw[i][0]])
        # breakpoint()
        answer = body(item_count, capacity, items_sorted)
        # breakpoint()
        temp = []
        for i in range(0, item_count):
            temp.append([items_sorted[i], ans_path[i]])
        temp.sort()
        # breakpoint()
        fin_ans = []
        for i in range(0, item_count):
            fin_ans.append(temp[i][1])
    # breakpoint()
    # prepare the solution in the specified output format
    output_data = str(answer) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, fin_ans))
    # breakpoint()
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

