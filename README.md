# python-flask B2C-分布式生鲜商城

### 项目实例地址：
flask版本: [http://flask.summerleaves.cn/](http://flask.summerleaves.cn/)    
django版本: [https://fresh.summerleaves.cn/](https://fresh.summerleaves.cn/)    

###  技术栈
* 语言：Python3.6.8  (flask==1.1.1)
* 数据库: MySql、 redis 
* 任务队列(异步处理): celery
* 分布式文件存储: FastDFS
* web服务器配置: Nginx+ uwsgi


###  安装和配置
* 安装python3.6
* 安装依赖包  
    * 进入项目根目录`pip install -r requeirtments.txt`
* 配置文件(config.py)
    * `DATABASE` mysql数据库
    * `REDIS_HOST`redis的地址
	* `REDIS_PASSWORD` redis密码
	* `EMAIL_HOST` 邮件的主机（qq邮箱:smtp.qq.com）
	* `EMAIL_USER` `EMAIL_PASS`
	*  `DOMAIN` 项目部署的ip和域名, 本地直接填写http://127.0.0.1:5000
	* `ALIPAY_APP_ID` # Alipay的id
	* `APP_PRIVATE_KEY_PATH` Alipay的私钥地址
	* `ALIPAY_PUBLIC_KEY_PATH` Alipay的公钥地址
* 配置eamil
    * `EMAIL_HOST_USER`
    * `EMAIL_HOST_PASSWORD`
    * `EMAIL_HOST_PASSWORD`
    * 参考链接：
        * https://www.cnblogs.com/ivy-blogs/p/10961494.html
        * https://www.cnblogs.com/ivy-blogs/p/11180271.html
* 修改DOMAIL
    * `DOMAIN` 修改为你的启动项目的ip地址或域名
* 修改IMG_URL
    * `IMG_URL` 修改为你的fast-dfs配置的nginx映射的ip和域名
* 修改fast-dfs的配置
* 修改`ALIPAY_APP_ID`为你的id
    * 参考链接
        * https://docs.open.alipay.com/200/105311/
* 安装fast-dfs和配置
    * 参考链接：
        * https://www.cnblogs.com/ivy-blogs/p/11237118.html
* uwsgi + nginx 项目部署
    * 参考链接
        * https://www.cnblogs.com/ivy-blogs/p/11162464.html

* 项目命令
	* `python manager.py db init`  初始化本地迁移环境
	* `python manager.py db migrate` 生成数据库迁移脚本
	* `python manager.py db upgrade` 运用生成的迁移脚本
	* `python manager.py runserver`  运行测试环境
	* `python manager.py admin startapp -n <your appname>`  在apps目录下创建app文件
		* 生成的应用需要到config的INSTALL_APP里面注册,不然项目初始化的时候找不到该app
	* `python manager.py admin createkey` 生成SECRET_KEY，可用于config文件的SECRET_KEY，一旦确定不可更改
	
	
	
	
	
	
	
	
	
	
	
	
