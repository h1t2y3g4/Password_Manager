"""
删除不要的账户的入口
"""


from setting import Setting, Status
import pickle
import os


def delet_file(setting, status, delet_account):
    try:
        with open(setting.name_mapping_file, 'rb') as f:
            status.name_mapping = pickle.load(f)
    except FileNotFoundError:
        print('没有找到name_mapping文件。请先添加用户。')
        os._exit(1234)
    else:
        try:
            os.remove(status.name_mapping[delet_account])
            print("账户{}删除成功".format(delet_account))
        except FileNotFoundError:
            print('{}的账户文件丢失，已删除记录。'.format(delet_account))
            status.name_mapping.pop(delet_account)
            with open(setting.name_mapping_file, 'wb') as f:
                print('当前name_mapping：{}'.format(status.name_mapping))
                pickle.dump(status.name_mapping, f)
        except KeyError:
            print('没有找到{}账户，请检查输入是否正确。'.format(delet_account))
        else:
            status.name_mapping.pop(delet_account)
            with open(setting.name_mapping_file, 'wb') as f:
                print('当前name_mapping：{}'.format(status.name_mapping))
                pickle.dump(status.name_mapping, f)


def main():
    setting = Setting()
    status = Status()
    while True:
        delet_account = input('请输入要删除的账户名(输出exit退出)：')
        if delet_account == 'exit':
            break
        delet_file(setting, status, delet_account)
    # 存当前所有账户有哪些
    with open(setting.all_user_name, 'w') as f:
        for key, value in status.name_mapping.items():
            with open(value, 'rb') as f_user:
                properties = pickle.load(f_user)
            f.write('网站名：{}   账户名：{}\n'.format(key, properties['user_name']))
    print('all_account.txt文件已更新。\n退出。')


if __name__ == '__main__':
    main()
