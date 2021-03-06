from platform import system
import os


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

