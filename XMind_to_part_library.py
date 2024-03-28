from xmindparser import xmind_to_dict
import read_dot
import pandas as pd
import os
import numpy as np

def visit_xmind_to_tree_plot(xmind_tree, f2, node_index= 0, edge_list=[]):
    # print(xmind_tree['title'])
    # print("node: %d, fidx= %s, f_val= %f" % (node_index, str(featurename[tree.f_idx]), tree.f_val))

    if 'topics' in xmind_tree.keys(): #非叶子结点
        #写入当前结点
        # line = "node: " + str(node_index) + ", " + str(xmind_tree['title']) + "\n"
        line = str(node_index) + " [label=\"" + str(xmind_tree['title']) + "\" color=balck" + " shape=ellipse]" + "\n"
        f2.write(line)
        line = str(node_index) + " -> " + str(node_index + 1) + "\n"
        f2.write(line)
        #如果当前结点下面还有子结点
        for i in range(len(xmind_tree['topics'])):
            # node_index = node_index + 1
            edge_list.append(node_index)
            title, node_index = visit_xmind_to_tree_plot(xmind_tree['topics'][i], f2, node_index + 1, edge_list)
            node_num2 = edge_list.pop()
            if i + 1 != len(xmind_tree['topics']):
                print(node_num2, "->", node_index + 1)
                line = str(node_num2) + "->" + str(node_index + 1) + "\n"
                f2.write(line)

    else:
        line = str(node_index) + " [label=\"val = " + str(xmind_tree['title']) + "\" color=green shape=rect]" + "\n"
        f2.write(line)
    return xmind_tree['title'], node_index

#将XMind的规则树，转化为部件
def visit_xmind_to_tree(xmind_tree, f2, columns, node_index= 0, edge_list=[]):

    if 'topics' in xmind_tree.keys(): #非叶子结点
        #写入当前结点
        split_fidx_f_val = str(xmind_tree['title']).split(' ')

        fidx = split_fidx_f_val[0]
        fidx = columns.index(fidx)
        if len(split_fidx_f_val) == 1:
            f_val = None
        else:
            f_val = float(split_fidx_f_val[-1])
        line = "node: " + str(node_index) + ", fidx= " + str(fidx) + ", f_val= " + str(f_val) + "\n"
        f2.write(line)
        line = str(node_index) + " -> " + str(node_index + 1) + "\n"
        f2.write(line)
        #如果当前结点下面还有子结点
        for i in range(len(xmind_tree['topics'])):
            edge_list.append(node_index)
            title, node_index = visit_xmind_to_tree(xmind_tree['topics'][i], f2, columns, node_index + 1, edge_list)
            node_num2 = edge_list.pop()
            if i + 1 != len(xmind_tree['topics']):
                print(node_num2, " -> ", node_index + 1)
                line = str(node_num2) + " -> " + str(node_index + 1) + "\n"
                f2.write(line)

    else:
        leaf = 0.0
        line = "node: " + str(node_index) + ", leaf_value= " + str(leaf) + "\n"
        f2.write(line)
    return xmind_tree['title'], node_index

if __name__ == '__main__':
    data_train = pd.read_csv('./prepare_data/task1/331new_train_data.csv')

    x = []
    for i in range(np.shape(data_train)[0]):
        a = np.random.normal(loc=0.0, scale=1.0, size=None)
        x.append(a)
    
    data_train['feature_a'] = x

    d = data_train.pop('feature_a')
    data_train.insert(3, 'feature_a', d)

    data_train.drop(columns=['RID', 'VISCODE', 'SavePath'], inplace=True)
    columns = data_train.columns.values.tolist()
    XMind_files_path = './test_none_threshold/'
    model_tree_path = './test_none_threshold_part_library/'
    file_names = os.listdir(XMind_files_path)
    for xmind_file in file_names:
        print(xmind_file)
        out = xmind_to_dict(XMind_files_path + xmind_file) #list
        ##将树模块转换成树结构
        filename_path = model_tree_path + xmind_file[:-5] +'txt'
        f2 = open(filename_path, 'w', encoding='UTF-8')
        begin_line = '{\n'
        f2.write(begin_line)
        visit_xmind_to_tree(out[0]['topic'], f2, columns)
        end_line = '}'
        f2.write(end_line)
        f2.close()
    # print(out)
    # print(type(out[0]))
    # filename_path = './ad_cn.gv'
    # f2 = open(filename_path, 'w', encoding='UTF-8')
    # begin_line = 'digraph {\n'
    # f2.write(begin_line)
    # visit_xmind_to_tree_plot(out[0]['topic'], f2)
    # end_line = '}'
    # f2.write(end_line)
    # f2.close()
    #
    # # 生成树图
    # read_dot.dot2png(dot_file_path=filename_path, img_path="./tree_ad_cn.png")





#实现了从XMind读取规则树，并将其进行可视化

