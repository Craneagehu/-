准备工作
1.安装scrapy_redis包,打开cmd工具,执行命令pip install scrapy_redis



2.准备好一个没有BUG,没有报错的爬虫项目



3.准备好redis主服务器还有跟程序相关的mysql数据库

前提mysql数据库要打开允许远程连接,因为mysql安装后root用户默认只允许本地连接,详情请看此文章





部署过程
1.修改爬虫项目的settings文件
在下载的scrapy_redis包中,有一个scheduler.py文件,里面有一个Scheduler类,是用来调度url,还有一个dupefilter.py文件,里面有个类是RFPDupeFilter,是用来去重,所以要在settings任意位置文件中添加上它们



还有在scrapy_redis包中,有一个pipelines文件,里面的RedisPipeline类可以把爬虫的数据写入redis,更稳定安全,所以要在settings中启动pipelines的地方启动此pipeline



最后修改redis连接配置



2.修改spider爬虫文件
首先我们要引入一个scrapy_redis.spider文件中的一个RedisSpider类,然后把spider爬虫文件原来继承的scrapy.Spider类改为引入的RedisSpider这个类



接着把原来的start_urls这句代码注释掉,加入redis_key = '自定义key值',一般以爬虫名:urls命名



测试部署是否成功
直接运行我们的项目,



打开redis客户端在redis添加key为yunqi:start_urls的列表,值为地址



添加成功后,程序直接跑了起来



查看数据是否插入



分布式用到的代码应该是同一套代码
1） 先把项目配置为分布式
2） 把项目拷贝到多台服务器中
3） 把所有爬虫项目都跑起来
4） 在主redis-cli中lpush你的网址即可
5） 效果：所有爬虫都开始运行，并且数据还都不一样
