# 电视
	由于2017/11/28北邮人TV改版，已经全换成清华IPTV。
	节目清单、电视截图以及视频源都是抓取清华IPTV。也可以修改源代码换成其他的视频源（如东北大学，北交等）
&#160; &#160; &#160; &#160;这是一个电视网站，可以在线观看转发的清华IPTV的电视节目，适合有如下需求的人（比如手机用户）：
![image](https://raw.githubusercontent.com/zhcong/traTV/master/net.png)<br />
&#160; &#160; &#160; &#160;部署改项目时可以使用代理服务器（该服务器可以接入IPv6网络），或是直接可以连接到IPv6网络，然后处于同一局域网下的设备就可以访问了。<br />
&#160; &#160; &#160; &#160;截图如下，专门为手机和平板适配的界面，另外也可以下载m3u8文件来使用本地的播放器观看节目：
<br /><br />
![image](https://raw.githubusercontent.com/zhcong/traTV/master/screenshot.png)<br />
	注意：添加了公告功能，在主页点击最上方电视图标进入(或者输入<地址:端口/tip>)，需要输入管理码(config.py文件设置)
## 配置
`python3 index.py`启动网站，python版本是3.0以上版本。`config.py`文件是配置文件，可以配置是否使用代理、代理配置等<br />
`proxy_enable`     是否使用代理<br />
`proxy_ip`         代理服务器地址<br />
`proxy_port`       代理服务端口<br />
`port`             traTV监听的端口<br />
`timeout`          连接视频源的超时时间<br />
`admin_code`       发布公告时填写的管理码，相当于密码<br />
`db_file`          数据库文件的名称<br />
## 依赖
使用`flask`构建的网站，`PIL`处理的截图，因此可能需要安装`flask`、`PIL`和`BeautifulSoup`，可以使用`pip`命令安装。
## 感谢
感谢清华IPTV提供的内容<br />
感谢video.js提供的视频播放器<br />
## 不足
受限于带宽和网站框架，不适合太多人同时使用。另外播放器的功能也需要完善。
## 联系
1011.0011@163.com