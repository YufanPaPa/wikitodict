#coding=utf-8
import json
import sys
import wikitodict
from multiprocessing import Pool,Manager
import multiprocessing

manager = Manager()
infobox_dict = manager.dict()
count=manager.Value("d",0)

def process_data(data_path):
    item_all=[]
    with open(data_path) as f_read:
        line=f_read.readline().strip()
        while line:
            item_all.append(line)
            line=f_read.readline().strip()
    return item_all

def get_infos(items,infobox_dict,count):
    for item in items:
        count.value+=1
        result = wikitodict.search(item)
        if len(result)>=2:
            cur_dict = infobox_dict[item] = dict()
            for key in result:
                try:
                    cur_dict[key.encode("utf-8")] = result[key].encode("utf-8")
                except:
                    cur_dict[key] = result[key]
            infobox_dict[item]=cur_dict
        print(count.value)

def save_data(save_path,infobox_dict):
    with open(save_path,"w") as f_write:
        json.dump(infobox_dict.copy(), f_write, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    items=process_data(sys.argv[1])
    each_length = len(items)/25
    sub_item = []
    for i in range(24):
        sub_item.append(items[i*each_length:(i+1)*each_length])
    sub_item.append(items[24*each_length:])
    p = Pool(25)
    for i in range(25):
        p.apply_async(get_infos, args=(sub_item[i],infobox_dict,count))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    save_data(sys.argv[2],infobox_dict)
    
