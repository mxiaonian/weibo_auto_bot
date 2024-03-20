请提前安装好python3.10.11
下载好chorme的绿色版本，已打包一份存百度云盘，虚拟环境也打包了，可在以下链接下载

链接：https://pan.baidu.com/s/16AbAhpq4ltrrLAMuCe9vIA?pwd=nian 
提取码：nian 


1.打开项目文件夹，设置虚拟环境
在终端中输入以下命令，在项目中设置虚拟环境：

python3 -m venv venv

或者点击设置-项目-python解释器，选择venv，然后点击确定。 项目终端中使用以下命令激活虚拟环境：

source venv\scripts\activate

2.导入依赖包（如已下载打包好的环境，可直接解压到项目目录下，不用引入依赖）
在终端中输入以下命令，在项目中引入依赖包：

pip install -r requirements.txt


3、运行程序
在终端中输入以下命令，运行程序：

python3 main.py

或者点击main.py文件，使用dbug模式运行程序。推荐使用pycharm进行调试。我没有尝试过vscode，不知道是否也可以。

这个项目的本意是为了工作流自动化，实现微博自动点赞评论指定条数，指定评论内容，自动私信发送，爬取指定博主微博，定时发送。然而仅完成了点赞评论和私信发送，便调离工作岗位，遂开源出来。项目为自学python3个月后写的，新手，能力有限，望各位大佬轻喷。
