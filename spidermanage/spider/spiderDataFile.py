#coding=utf-8
import os


def filemanage():
    # here_dir = os.path.abspath('.') + '/spidermodule/' #　测试用
    here_dir = os.path.abspath('.') + '/spider/spidermodule/'

    # 顺序　本目录遍历　目录下目录遍历　广度＋深度
    # (遍历的路径，路径下的文件夹，路径下的文件)
    # 策略：拿出本目录的文件夹，即是　所有文件夹列表　[0][1] 顺序对应于 所有文件列表　[1:][2]

    # root, dirs, files
    all_dir_file = list(os.walk(here_dir))

    spider_dirs = all_dir_file[0][1]
    all_dir_file.remove(all_dir_file[0])

    items = []
    for i in range(len(all_dir_file)):
        item={}
        item['dir'] = spider_dirs[i]
        item['fileList'] = all_dir_file[i][2]
        item['fileList'].sort()
        items.append(item)
    return items


def main():
    for i in filemanage():
        print i

if __name__ == '__main__':
    main()
