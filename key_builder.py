"""
生成秘钥，同时以文件的形式存下来。
存好的文件是给加密方向用的。
运行过一次以后就不要再运行了。
"""


import os
import pickle
from setting import Setting


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
	else:
		print('已经有秘钥了，不能再覆盖了。请删除秘钥后重试。')


def build_new_user(setting):
	if not os.path.exists(setting.new_user_name):
		model_all = "web_name = \nnickname = \nuser_name = \npassword1 = \npassword2 = \nremark = \n" \
					"[---------------split_line,don't_change---------------]\n" \
					"web_name = \nnickname = \nuser_name = \npassword1 = \npassword2 = \nremark = \n" \
					"[---------------split_line,don't_change---------------]\n"
		with open(setting.new_user_name, 'w') as f:
			f.write(model_all)


def main():
	setting = Setting()
	secret_key_dict = build_clear_to_cipher_dict()
	save_dict(secret_key_dict, setting.secret_key_name)
	build_new_user(setting)


if __name__ == '__main__':
	main()
