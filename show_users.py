"""
在cmd中打印所有的账户信息
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
        output_properties(user)
    for k, v in status.name_mapping.items():
        print('{}:{}'.format(k, v))
    input('请敲回车退出')


def output_properties(user):
    print('******************************')
    print('网站名:{}'.format(user.properties['web_name']))
    print('昵称:{}'.format(user.properties['nickname']))
    print('用户名:{}'.format(user.properties['user_name']))
    print('密码一:{}'.format(user.properties['password1']))
    print('密码二:{}'.format(user.properties['password2']))
    print('备注:{}\n'.format(user.properties['remark']))


if __name__ == '__main__':
    main()
