weiboimg-crawler
===
微博相册爬虫
---

> 基于Python3，需要 BeautifulSoup 和 requests 库支持:  
sudo -H pip install BeautifulSoup4 requests  

> BeautifulSoup 用了 lxml 来解析网页，你可能需要安装 lxml 库：  
sudo -H pip install lxml  

> 但是 pip 安装 lxml 速度奇慢而且很可能报错，如果你是 Ubuntu 或者 Debian，推荐：  
sudo apt-get install python-lxml  
> 
> 如果你是 Windows 用户：  
请去 [这里](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml) 下载对应版本的whl来安装

使用方法
---

在nickname.txt里，一行一个微博昵称，保存。然后执行
> python main.py

That's all.

P.S.
---
通过 m.weibo.cn 实现单个用户的全部微博内容抓取（然而并没有真的全保存下来）。  
只下载原创微博的配图，所以严格来说并不是相册下载器。  

写完了以后发现其实可以扩展更多用途，比如按照微博的话题进行筛选之类的。  

总之你可以用它来下载coser和摄影微博的那些照片（虽然写脚本的本意不是为了这个  

← ← 也可以用来爬那些职业发车的老司机的微博内容（发现好像这个挺实用