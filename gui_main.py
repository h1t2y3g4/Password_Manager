import os
import easygui
import pickle
import random
from platform import system


class Setting:
	def __init__(self):
		# path = os.path.split(os.path.realpath(__file__))[0]
		self.windows_files_dir = 'password_manager_files/'  # Windows下的根目录
		self.android_files_dir = '/sdcard/password_manager_files/'  # Linux下的根目录

		# 判断是windows还是linux
		plt = system()
		if 'Windows' == plt:
			self.files_dir = self.windows_files_dir
		elif 'Linux' == plt:
			self.files_dir = self.android_files_dir

		# 创建所需文件夹
		if not os.path.exists(self.files_dir):
			os.makedirs(self.files_dir)

		self.secret_key_name = self.files_dir + 'secret_key.csy'  # 秘钥文件
		self.new_user_name = self.files_dir + 'new_user.txt'  # 添加新用户的文件
		self.name_mapping_file = self.files_dir + 'name_mapping.csy'  # 一个记录明文账户名与账户文件文件名的映射关系文件
		self.all_user_name = self.files_dir + 'all_account.txt'  # 记录当前存了哪些账户


class User:
	def __init__(self):
		self.properties = {
			'web_name': None,  # 这是什么东西的账号。
			'nickname': None,  # 昵称，一般会空缺吧。
			'user_name': None,  # 用户名。
			'password1': None,  # 一般为登录密码
			'password2': None,  # 如果有，一般就是支付密码。
			'remark': None,  # 注释。有什么密保问题安全密码之类的直接往这里里面丢。
		}


class Status:
	def __init__(self):
		self.name_mapping = dict()  # 明文的账户与密文的账户之间对应关系的映射表。
		self.secret_key = dict()  # 加密秘钥


def build_clear_to_cipher_dict():
	"""
	生成秘钥，用了强伪随机数
	:return: 加密方向用的字典
	"""
	clear_text_set = set()
	cipher_text_set = set()  # 装密文的集合。cipher：n.暗号
	while len(clear_text_set) < 90:
		chr_num1 = ord(os.urandom(1))  # 这个函数返回的是强伪随机数，这才可用于密码
		if chr_num1 < 33 or chr_num1 > 122:  # ASCII字符里面从数字到小写英文字母，还有一些乱七八糟的符号
			continue
		clear_text = chr(chr_num1)
		clear_text_set.add(clear_text)
	while len(cipher_text_set) < 90:
		chr_num2 = ord(os.urandom(1))  # 这个函数返回的是强伪随机数，这才可用于密码
		chr_num2 = 255 - chr_num2
		if chr_num2 < 33 or chr_num2 > 122:  # ASCII字符里面从数字到小写英文字母，还有一些乱七八糟的符号
			continue
		cipher_text = chr(chr_num2)
		cipher_text_set.add(cipher_text)
		# set(集合)类型不能重排序，但是出于某种我未知的原因，这两个set直接生成字典会发现两个set中元素的排序几乎相同。
		# 所以接下来的这一行强行转换成list然后改变其中一个list的顺序
		cipher_text_list = sorted(list(cipher_text_set), reverse=True)
	clear_to_cipher_dict = dict(zip(clear_text_set, cipher_text_list))
	return clear_to_cipher_dict


def save_dict(dict1, filename):
	"""
	用二进制的方式储存密码字典，用到了pickle模块
	:param dict1:
	:param filename:
	:return:
	"""
	try:
		with open(filename, 'rb'):
			pass
	except FileNotFoundError:
		with open(filename, 'wb') as f:
			pickle.dump(dict1, f)
		print("秘钥生成成功。")
		print(dict1)
		easygui.msgbox(title='密码管理器', msg="秘钥生成成功。" + str(dict1), ok_button='确定')
	else:
		print('已经有秘钥了，不能再覆盖了。请删除秘钥后重试。')
		easygui.msgbox(title='密码管理器', msg='已经有秘钥了，不能再覆盖了。请删除秘钥后重试。', ok_button='确定')


def build_new_user(setting):
	if not os.path.exists(setting.new_user_name):
		model_all = "web_name = \nnickname = \nuser_name = \npassword1 = \npassword2 = \nremark = \n" \
					"[---------------split_line,don't_change---------------]\n" \
					"web_name = \nnickname = \nuser_name = \npassword1 = \npassword2 = \nremark = \n" \
					"[---------------split_line,don't_change---------------]\n"
		with open(setting.new_user_name, 'w') as f:
			f.write(model_all)


def key_builder_main():
	setting = Setting()
	secret_key_dict = build_clear_to_cipher_dict()
	save_dict(secret_key_dict, setting.secret_key_name)
	build_new_user(setting)


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
		easygui.msgbox(title='密码管理器', msg="new_user.txt文件丢失。已修复问题，请重新添加。", ok_button='确定')

		with open(setting.new_user_name, 'w') as f:
			f.write(model_all)
			new_all = model_all
	model_all_2 = model_all.replace('\n', '')
	model_all_2 = model_all_2.replace(' ', '')
	new_all_2 = new_all.replace('\n', '')
	new_all_2 = new_all_2.replace(' ', '')
	if model_all_2 == new_all_2:
		print('没有发现新增账户，请在files文件夹下的new_user.txt文件夹中填写新账户。')
		easygui.msgbox(title='密码管理器', msg='没有发现新增账户，请在files文件夹下的new_user.txt文件夹中填写新账户。', ok_button='确定')
		return None, None
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
				easygui.msgbox(title='密码管理器', msg='{}账户文件丢失，已从name_mapping中删除'.format(key), ok_button='确定')
	except FileNotFoundError:
		print('没有找到name_mapping文件。可能是第一次运行。')
		easygui.msgbox(title='密码管理器', msg='没有找到name_mapping文件。可能是第一次运行。', ok_button='确定')
		pass
	# 加载秘钥
	try:
		with open(setting.secret_key_name, 'rb') as f:
			status.secret_key = pickle.load(f)
	except FileNotFoundError:
		key_builder_main()
		with open(setting.secret_key_name, 'rb') as f:
			status.secret_key = pickle.load(f)
		print('没有找到秘钥，已为您自动生成秘钥。')
		easygui.msgbox(title='密码管理器', msg='没有找到秘钥，已为您自动生成秘钥。', ok_button='确定')
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
					easygui.msgbox(msg='账户{}已存在,且内容无变化，自动跳过此项。\n'.format(user.properties['web_name']),
					               title='密码管理器',
					               ok_button='确定')
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
			# update_or_no = input('是否需要更新？(回车键继续/否请输入“n”)：'.format(user.properties['web_name']))
			update_or_no = easygui.ccbox(msg='{}账户已存在\n原{}账户信息：{}\n新{}账户信息：{}\n是否需要更新？'
			                             .format(user.properties['web_name'],
			                                     user.properties['web_name'], old_user_properties,
			                                     user.properties['web_name'], user.properties),
			                             choices=['是', '否'],
			                             title='密码管理器')
			if update_or_no == 1:
				# 这里如果选择是，则用映射表中的名字覆写文件。
				user.properties['password1'] = encryption(user.properties['password1'], status.secret_key)
				user.properties['password2'] = encryption(user.properties['password2'], status.secret_key)
				with open(status.name_mapping[user.properties['web_name']], 'wb') as f:
					pickle.dump(user.properties, f)
				print('添加成功\n')
				easygui.msgbox(msg='添加成功\n', title='密码管理器', ok_button='确定')
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
	easygui.msgbox(msg='新用户添加成功', title='密码管理器', ok_button='确定')


def add_user_main():
	setting = Setting()
	model_all, new_all = if_changed(setting)  # 检查是否有新增加的账户。如果有就返回模板的数据和新增加的文件的数据，如果没有就直接退出了。
	if not model_all and not new_all:
		return None
	status = status_init(setting)  # 初始化映射关系表
	users = deal_with_data(new_all, status)  # 处理新增加的数据，添加到文件里。
	save_data(users, setting, model_all, status)  # 保存账户文件、映射关系表，覆写新用户文件


def show_user_main():
	setting = Setting()
	status = Status()
	try:
		with open(setting.name_mapping_file, 'rb') as f:
			status.name_mapping = pickle.load(f)  # 字典类型
	except FileNotFoundError:
		print("请先添加账户后重试")
		easygui.msgbox(msg="请先添加账户后重试", title="出错", ok_button='确定')
		return None
	try:
		with open(setting.secret_key_name, 'rb') as f:
			status.secret_key = pickle.load(f)
	except FileNotFoundError:
		print("没有找到秘钥文件")
		easygui.msgbox(msg="没有找到秘钥文件", title="出错", ok_button='确定')
		return None
	all_txt = ''
	for value in status.name_mapping.values():
		user = User()
		with open(value, 'rb') as f:
			user.properties = pickle.load(f)
		user.properties['password1'] = decryption(user.properties['password1'], status.secret_key)
		user.properties['password2'] = decryption(user.properties['password2'], status.secret_key)
		account_data = output_properties(user)
		all_txt += account_data
	all_txt += '\n文件储存位置：'
	for k, v in status.name_mapping.items():
		print('{}:{}'.format(k, v))
		all_txt += '{}:{}\n'.format(k, v)
	easygui.msgbox(msg=all_txt, title='密码管理器', ok_button='确定')
	# input('请敲回车退出')


def output_properties(user):
	print('******************************')
	print('网站名:{}'.format(user.properties['web_name']))
	print('昵称:{}'.format(user.properties['nickname']))
	print('用户名:{}'.format(user.properties['user_name']))
	print('密码一:{}'.format(user.properties['password1']))
	print('密码二:{}'.format(user.properties['password2']))
	print('备注:{}\n'.format(user.properties['remark']))
	account_data = '******************************\n网站名:{}\n昵称:{}\n用户名:{}\n密码一:{}\n密码二:{}\n备注:{}\n'\
		.format(user.properties['web_name'], user.properties['nickname'], user.properties['user_name'],
	            user.properties['password1'], user.properties['password2'], user.properties['remark'])
	return account_data


def delet_file(setting, status, delete_account):
	try:
		with open(setting.name_mapping_file, 'rb') as f:
			status.name_mapping = pickle.load(f)
	except FileNotFoundError:
		print('没有找到name_mapping文件。请先添加用户。')
		easygui.msgbox(msg='没有找到name_mapping文件。请先添加用户。', title='密码管理器', ok_button='确定')
		# os._exit(1234)
	else:
		try:
			os.remove(status.name_mapping[delete_account])
			print("账户{}删除成功".format(delete_account))
			easygui.msgbox(msg="账户{}删除成功".format(delete_account), title='密码管理器', ok_button='确定')
		except FileNotFoundError:
			print('{}的账户文件丢失，已删除记录。'.format(delete_account))
			easygui.msgbox(msg='{}的账户文件丢失，已删除记录。'.format(delete_account), title='密码管理器', ok_button='确定')
			status.name_mapping.pop(delete_account)
			with open(setting.name_mapping_file, 'wb') as f:
				print('当前name_mapping：{}'.format(status.name_mapping))
				# easygui.msgbox(msg='当前name_mapping：{}'.format(status.name_mapping), title='密码管理器', ok_button='确定')
				pickle.dump(status.name_mapping, f)
		except KeyError:
			print('没有找到{}账户，请检查输入是否正确。'.format(delete_account))
			easygui.msgbox(msg='没有找到{}账户，请检查输入是否正确。'.format(delete_account), title='密码管理器', ok_button='确定')
		else:
			status.name_mapping.pop(delete_account)
			with open(setting.name_mapping_file, 'wb') as f:
				print('当前name_mapping：{}'.format(status.name_mapping))
				# easygui.msgbox(msg='当前name_mapping：{}'.format(status.name_mapping), title='密码管理器', ok_button='确定')
				pickle.dump(status.name_mapping, f)


def delete_user_main():
	setting = Setting()
	status = Status()
	delete_account = easygui.enterbox(msg='请输入要删除的账户名', title='密码管理器')
	if delete_account:
		delet_file(setting, status, delete_account)
	# 存当前所有账户有哪些
	with open(setting.all_user_name, 'w') as f:
		for key, value in status.name_mapping.items():
			with open(value, 'rb') as f_user:
				properties = pickle.load(f_user)
			f.write('网站名：{}   账户名：{}\n'.format(key, properties['user_name']))
	print('all_account.txt文件已更新。\n退出。')
	# easygui.msgbox(msg='all_account.txt文件已更新。', title='密码管理器', ok_button='确定')


def add_single_user_main():
	setting = Setting()
	msg = "请填写新账户信息(其中带*号的项为必填项)"
	title = "密码管理器"
	fieldNames = ["*网站名", "昵称", "用户名", "密码一", "密码二", "备注"]
	fieldValues = easygui.multenterbox(msg=msg, title=title, fields=fieldNames)
	if not fieldValues:
		return None
	if not fieldValues[0]:
		easygui.msgbox(msg='带*号的项不能省略', title='密码管理器', ok_button='确定')
		return None
	new_all = "web_name = {}\nnickname = {}\nuser_name = {}\npassword1 = {}\npassword2 = {}\nremark = {}\n[---------------split_line,don't_change---------------]\n"\
		.format(fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3], fieldValues[4], fieldValues[5])
	status = status_init(setting)  # 初始化映射关系表
	users = deal_with_data(new_all, status)  # 处理新增加的数据，添加到文件里。
	model_all = "web_name = \nnickname = \nuser_name = \npassword1 = \npassword2 = \nremark = \n" \
	            "[---------------split_line,don't_change---------------]\n" \
	            "web_name = \nnickname = \nuser_name = \npassword1 = \npassword2 = \nremark = \n" \
	            "[---------------split_line,don't_change---------------]\n"
	save_data(users, setting, model_all, status)  # 保存账户文件、映射关系表，覆写新用户文件


if __name__ == '__main__':
	while True:
		msg = '请选择希望运行的功能:\n' \
		      '注意事项：\n' \
		      '1、初次运行请先点击“生成秘钥”。秘钥是解密的唯一办法，请妥善保管\n' \
		      '2、批量添加新账户之前请在“password_manager_files/new_user.csy”文件中填写新用户信息。\n' \
		      '3、详情请查看Github：https://github.com/h1t2y3g4/Password_Manager\n' \
		      'Copyright (c) 2019 陈守阳'
		duty_result = easygui.indexbox(title='密码管理器', msg=msg, choices=['生成密钥', '添加/修改单个新账户', '批量添加/修改新账户', '查看所有账户', '删除账户', '退出程序'])
		path = os.path.split(os.path.realpath(__file__))[0]
		if duty_result == 0:
			key_builder_main()
		elif duty_result == 1:
			add_single_user_main()
		elif duty_result == 2:
			add_user_main()
		elif duty_result == 3:
			show_user_main()
		elif duty_result == 4:
			delete_user_main()
		elif duty_result == 5:
			break

