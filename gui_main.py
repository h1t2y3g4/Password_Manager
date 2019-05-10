import os
import easygui


if __name__ == '__main__':
    while True:
        msg = '请选择希望运行的程序:\n' \
              '注意事项：\n' \
              '1、初次运行请先点击“生成秘钥”。\n' \
              '2、添加新账户之前请在“password_manager_files/new_user.csy”中填写新用户信息。\n' \
              '3、详情请查看Github：https://github.com/h1t2y3g4/Password_Manager'
        duty_result = easygui.indexbox(title='密码管理器', msg=msg, choices=['生成密钥', '添加新账户', '查看所有账户', '删除账户', '退出程序'])
        path = os.path.split(os.path.realpath(__file__))[0]
        # print(path)
        if duty_result == 0:
            os.system(r'python ' + path + r'\key_builder.py')
        elif duty_result == 1:
            os.system(r'python ' + path + r'\add_user.py')
        elif duty_result == 2:
            os.system(r'python ' + path + r'\show_users.py')
        elif duty_result == 3:
            os.system(r'python ' + path + r'\delete_account.py')
        elif duty_result == 4:
            break

