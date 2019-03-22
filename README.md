# 密码管理器  

## 项目介绍  

本项目是一个用python写的密码管理器，支持Windows和Android（搭配qpython使用）。  
基于python3.6写的，python3应该通用，没有使用第三方库。  
目前没有编译成程序。  

## 使用方法  

### Windows  
#### 1.点击右上角“Clone or download”把代码下载到本地。  
#### 2.运行‘key_builder.py’生成秘钥。秘钥是‘password_manager_files/secret_key.csy’文件。  
- 秘钥是解密的唯一办法，如果通过此秘钥加密以后秘钥遗失了，那就丢失了数据，无论如何也解不开的。***所以请妥善保管秘钥***。  
- 秘钥与数据文件对应，如果不匹配解密出来的是乱码。  
- 运行过一遍后无法再次运行，需要在files文件夹中删除秘钥，方可再次生成。  
- 如果追求高安全性，推荐将秘钥保存到一台未联网的电脑中。  
#### 3.再打开‘password_manager_files/new_user.txt’输入要添加的账户信息。**保存**后关闭。  
	-web_name 网站名。描述当前账户是哪个网站的。必填。是程序识别不同账户的唯一标识符，支持中文。  
	-nickname 昵称。可空缺。支持中文。  
	-user_name 用户名。可空缺。支持中文。  
	-password1 密码一。一般为登录密码。可空缺。只支持ASCII码为33到122之间（包含）的字符。  
	-password2 密码二。一般为支付密码。可空缺。只支持ASCII码为33到122之间（包含）的字符。  
	-remark 备注。随便什么说明都可以往这扔，比如密保问题等。可空缺。支持中文。  
  默认设计了两个账户空位，实际上可以随意增减，可以空缺不填，也可以自行复制批量添加（请同时复制分割线）。  
***一定不要自行修改分割线内的内容***，包括两个中括号以及括号内的内容，这里是字符串匹配的。  
#### 4.运行‘add_user.py’文件。  
>此时程序把new_user.txt中的文件添加到数据库中，同时覆写new_user.txt文件。  
#### 5.运行‘show_user.py’文件。  
>查看所有账户信息。***以后如果仅仅是查看数据，那只需要运行这个即可。***    
#### 6.其他py文件说明：  
	-delete_account.py：删除账户。输入网站名（也就是web_name这条属性，这是账户的唯一标识）即可。  
	-output_all_data.py：输入明文账户信息。一般用不着，而且设备储存过明文数据没有覆写的话会有风险。  
	-edit_namemapping.py：把数据迁移到不同平台的补丁。先留个坑吧，操作说明有点麻烦，以后有时间再写。  
	-setting.py：各种设置。不要动，先留坑，以后再写吧。  

---------------------------
### Android  
#### 1.在手机上安装QPython3  
>请自行下载安装，我的是GooglePlay下的。  
#### 2.把整个项目文件夹移动到手机的/storage/emulated/0/qpython/projects3/文件夹中  
>如果没有project3那就放到project之类的都行，反正要在手机上用qpython运行时找的到。  
#### 3.其他步骤请参考windows下运行的第2、3、4、5条。  
>***注意new_user.txt和secret_key.csy文件的位置在'/sdcard/password_manager_files/'*** ，我用MIUI自带的文件管理打开看到的是‘/storage/emulated/0/password_manager_files/’，这是绝对文件路径。  
>这是因为读写权限的问题，只能放到sdcard的根目录，所以这里要麻烦一点。  

--------------------------
### 文件迁移  
>如果之前在PC上运行过，已经有了数据，想要搬移到手机，那么请在执行完Android的第1、2步以后，看接下来的操作。  
#### 1.把‘password_manager_files’文件夹移动到手机sdcard根目录  
>手机上的文件路径为'/sdcard/password_manager_files/'，或者是‘/storage/emulated/0/password_manager_files/’结果应该是一样的。  
#### 2.在QPython3中运行‘edit_namemapping.py’文件  
>‘edit_namemapping.py’文件在/storage/emulated/0/qpython/projects3/password_manager/文件夹，  
>如果之前没有在PC上添加过用户，那么应该会报错，请直接跳过这一步。  
#### 3.在QPython3中运行‘show_user.py’文件  

