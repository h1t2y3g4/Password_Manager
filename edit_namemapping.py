"""
删除name_mapping文件中的files/，算是从PC移植到Qpython打的补丁吧。只需运行一遍就行了。
突然发现这个程序也可以用在任何需要修改文件储存位置的时候。
"""

import pickle
from setting import Setting, User, Status


def main():
    setting = Setting()
    status = Status()
    with open(setting.name_mapping_file, 'rb') as f:
        status.name_mapping = pickle.load(f)  # 字典类型
    for (key, value) in status.name_mapping.items():
        new_value = value.split('/')[-1]
        status.name_mapping[key] = setting.files_dir + new_value
    with open(setting.name_mapping_file, 'wb') as f:
        pickle.dump(status.name_mapping, f)


if __name__ == '__main__':
    main()
