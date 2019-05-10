"""
从文件中读取数据，把数据加密后储存，然后把原文件删除
现在存的都还没有经过秘钥，再写两个函数来加解密吧
"""


import os
import pickle
import random
from setting import Setting, User, Status


def if_changed(setting):
	"""
	检查是否有新增加的账户。如果有就返回模板的数据和新增加的文件的数据，如果没有就直接退出了。
	:param setting:
	:return: 模板的数据, 新增加的文件的数据
	"""
	model_all = "web_name = \nnickname = \nuser_name = \npassword1 = \npassword2 = \nremark = \n" \
				"[---------------split_line,don't_change---------------]\n" \
				"web_name = \nnickname = \nuser_name = \npassword1 = \npassword2 = \nremark = \n" \
				"[---------------split_line,don't_change---------------]\n"
	try:
		with open(setting.new_user_name, 'r', encoding='utf-8') as f:
			new_all = f.read()
	except FileNotFoundError:
		print("new_user.txt文件丢失。已修复问题，请重新添加。")
		with open(setting.new_user_name, 'w') as f:
			f.write(model_all)
			new_all = model_all
	model_all_2 = model_all.replace('\n', '')
	model_all_2 = model_all_2.replace(' ', '')
	new_all_2 = new_all.replace('\n', '')
	new_all_2 = new_all_2.replace(' ', '')
	if model_all_2 == new_all_2:
		print('没有发现新增账户，请在files文件夹下的new_user.txt文件夹中填写新账户。')
		os._exit(0)
	else:
		return model_all, new_all


def status_init(setting):
	"""
	初始化映射关系表
	:param setting:
	:return:
	"""
	status = Status()
	try:
		with open(setting.name_mapping_file, 'rb') as f:
			mapping_relation = pickle.load(f)
		status.name_mapping = mapping_relation
		# 自检。如果有账户数据文件丢失，则从name_mapping中删除这一项。并且给提醒。
		# 这样后面在储存文件的时候有一个判断账户文件是否丢失try语句就永远无法执行。不过没影响。
		file_list = os.listdir(setting.files_dir)
		for key, value in status.name_mapping.copy().items():
			if value.split('/')[-1] not in file_list:
				status.name_mapping.pop(key)
				print('{}账户文件丢失，已从name_mapping中删除'.format(key))
	except FileNotFoundError:
		print('没有找到name_mapping文件。可能是第一次运行。')
		pass
	# 加载秘钥
	try:
		with open(setting.secret_key_name, 'rb') as f:
			status.secret_key = pickle.load(f)
	except FileNotFoundError:
		print('没有找到秘钥，请先生成秘钥。')
	return status


def encryption(string, secret_key):
	"""
	将str加密
	:param string: 明文密码。字符串
	:param secret_key: 加密秘钥。字典
	:return: 密文密码。字符串
	"""
	cipher_code = ''
	for char_clear in string:
		char_cipher = secret_key[char_clear]
		cipher_code += char_cipher
	return cipher_code


def decryption(cipher_code, secret_key):
	"""
	解密
	:param cipher_code: 密文密码。字符串
	:param secret_key: 加密秘钥。字典
	:return: 明文密码。字符串
	"""
	decrypt_key = {}  # 解密秘钥
	for key, value in secret_key.items():
		decrypt_key[value] = key
	string = ''
	for char_secret in cipher_code:
		char_clear = decrypt_key[char_secret]
		string += char_clear
	return string


def deal_with_data(new_all, status):
	"""
	处理新添加账户数据
	:param new_all:
	:return: 一个装有很多User类实例的列表
	"""
	new_users = new_all.split("[---------------split_line,don't_change---------------]")
	users = []
	for new_user in new_users:
		new_user = new_user.strip()
		if new_user == '':
			break
		else:
			user = User()
		for property in new_user.split('\n'):
			property = property.strip()
			key_and_value = list(i.strip() for i in property.split('='))
			user.properties[key_and_value[0]] = key_and_value[1]
		users.append(user)
	return users


def save_data(users, setting, model_all, status):
	"""
	保存账户文件、映射关系表，覆写新用户文件
	:param users:
	:param setting:
	:param model_all:
	:param status:
	:return:
	"""
	print('========================================')
	for user in users:
		# 这里是为了修复当new_user文件没有填满时，会生成一个空账户文件的BUG
		if user.properties['web_name'] == '':
			continue
		# 这里是先检测数据库里面有没有这个网站，再存。
		if user.properties['web_name'] in status.name_mapping.keys():
			# 此项判断还有问题，如果账户的数据文件丢失了，但是name_mapping文件还在，此时会直接跳过此项数据，更新都没办法？
			# 答：不会，因为我马上要打印原来的账户信息，此时会读取账户数据，找不到文件一报错就可以直接更新账户数据了嘛。
			# 这里打印出原来的和现在的账户信息，做一个对比。
			try:
				with open(status.name_mapping[user.properties['web_name']], 'rb') as f:
					old_user_properties = pickle.load(f)
				# 解密
				old_user_properties['password1'] = decryption(old_user_properties['password1'], status.secret_key)
				old_user_properties['password2'] = decryption(old_user_properties['password2'], status.secret_key)
				if old_user_properties == user.properties:
					# 如果新旧文件信息完全相等，则跳过此user
					print('账户{}已存在,且内容无变化，自动跳过此项。\n'.format(user.properties['web_name']))
					continue
				else:
					# 现在这个直接打印所有信息，眼睛都要看花，未来可能可以只打印变化了的信息。
					print('{}账户已存在'.format(user.properties['web_name']))
					print('原{}账户信息：{}'.format(user.properties['web_name'], old_user_properties))
					print('新{}账户信息：{}'.format(user.properties['web_name'], user.properties))
			except FileNotFoundError:
				# 直接更新数据，不询问
				user.properties['password1'] = encryption(user.properties['password1'], status.secret_key)
				user.properties['password2'] = encryption(user.properties['password2'], status.secret_key)
				with open(status.name_mapping[user.properties['web_name']], 'wb') as f:
					pickle.dump(user.properties, f)
				pass
			update_or_no = input('是否需要更新？(回车键继续/否请输入“n”)：'.format(user.properties['web_name']))
			if update_or_no == '':
				# 这里如果选择是，则用映射表中的名字覆写文件。
				user.properties['password1'] = encryption(user.properties['password1'], status.secret_key)
				user.properties['password2'] = encryption(user.properties['password2'], status.secret_key)
				with open(status.name_mapping[user.properties['web_name']], 'wb') as f:
					pickle.dump(user.properties, f)
				print('添加成功\n')
			else:
				# 这里如果选择否，则跳过此user。实际上不管输入的是不是n都会取消掉更新。
				continue
		else:

			# 此else后接的内容为当发现这是一个全新账户后，①把新账户存下来。②记录name_mapping文件。
			root_file_name = str(random.randrange(2**63, 2**64))
			file_name = setting.files_dir + root_file_name + '.csy'
			user.properties['password1'] = encryption(user.properties['password1'], status.secret_key)
			user.properties['password2'] = encryption(user.properties['password2'], status.secret_key)
			with open(file_name, 'wb') as f:
				pickle.dump(user.properties, f)
			status.name_mapping[user.properties['web_name']] = file_name
	print('这是新增数据处理完成时的name_mapping（马上要存入文件）:', end='')
	print(status.name_mapping)
	# 存映射关系文件
	with open(setting.name_mapping_file, 'wb') as f:
		pickle.dump(status.name_mapping, f)
	# 覆写new_user文件
	with open(setting.new_user_name, 'w') as f:
			f.write(model_all)
	# 存当前所有账户有哪些
	with open(setting.all_user_name, 'w') as f:
		for key, value in status.name_mapping.items():
			with open(value, 'rb') as f_user:
				properties = pickle.load(f_user)
			f.write('网站名：{}   账户名：{}\n'.format(key, properties['user_name']))
	print('新用户添加成功，new_user文件删除。')


def main():
	setting = Setting()
	model_all, new_all = if_changed(setting)  # 检查是否有新增加的账户。如果有就返回模板的数据和新增加的文件的数据，如果没有就直接退出了。
	status = status_init(setting)  # 初始化映射关系表
	users = deal_with_data(new_all, status)  # 处理新增加的数据，添加到文件里。
	save_data(users, setting, model_all, status)  # 保存账户文件、映射关系表，覆写新用户文件


if __name__ == '__main__':
	main()

