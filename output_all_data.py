"""
把数据库中所有的数据拿出来，输出成一个new_user.txt文件。
目的是为更换秘钥时明文备份用
"""

import pickle
from setting import Setting, User, Status
from add_user import decryption


def main():
    setting = Setting()
    status = Status()
    with open(setting.name_mapping_file, 'rb') as f:
        status.name_mapping = pickle.load(f)  # 字典类型
    with open(setting.secret_key_name, 'rb') as f:
        status.secret_key = pickle.load(f)
    for value in status.name_mapping.values():
        user = User()
        with open(value, 'rb') as f:
            user.properties = pickle.load(f)
        user.properties['password1'] = decryption(user.properties['password1'], status.secret_key)
        user.properties['password2'] = decryption(user.properties['password2'], status.secret_key)
        output_properties(user, setting)
    print('导出完成。')


def output_properties(user, setting):
    with open(setting.files_dir + 'data_backup.txt', 'a') as f:
        f.write('web_name = {}\n'.format(user.properties['web_name']))
        f.write('nickname = {}\n'.format(user.properties['nickname']))
        f.write('user_name = {}\n'.format(user.properties['user_name']))
        f.write('password1 = {}\n'.format(user.properties['password1']))
        f.write('password2 = {}\n'.format(user.properties['password2']))
        f.write('remark = {}\n'.format(user.properties['remark']))
        f.write("[---------------split_line,don't_change---------------]\n")


if __name__ == '__main__':
    main()
