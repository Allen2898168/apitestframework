
# 安装
- 前提

    已安装好64位 python3.7+, [点击下载](https://www.python.org/downloads/windows/)
- 步骤

    - `git clone `
    - `cd ApiFramework`
    - `pip install -r requirements.txt`
    - 用[Pycharm](https://www.jetbrains.com/pycharm/), `File > Open`, 选择此目录
    
# 使用
 - 目录简介
 ```
ApiFramework
├── Common  …………全局通用方法
│   ├── Case.py …………基础用例
│   ├── Common.py   …………加解密处理,公共变量池
│   ├── Configure.py    …………配置读取
│   ├── DB.py   …………数据库控制器
│   ├── LoggingMap.py   …………日志打印控制
│   ├── Mailer.py   …………邮件发送器
│   └── Reporter.py …………报告生成器
├── Conf   …………全局级配置文件
│   └── Conf.yml   …………运行哪个项目、日志级别、是否自动发送邮件(用例跑完后)、数据库连接信息、邮件服务器及账户信息
├── Projects   …………此目录下包含所有项目
│   ├── __init__.py   …………Python的模块标识文件(内容默认为空但不可缺少，不用理会)，下同
│   └── dss_system   …………dss系统 示例项目  
│       ├── Base   …………该项目的基础用例，放置该项目的通用方法
│       │   ├── Base.py   …………见上
│       │   └── __init__.py
│       ├── Cases   …………模块测试用例文件夹
│       │   ├── TestCustomer.py   …………客户管理模块用例
│       │   └── __init__.py
│       ├── Conf
│       │   ├── Conf.yml   …………项目级配置文件，如要url、headers、data等测试数据
│       │   └── __init__.py
│       └── Modules   …………模块方法文件夹
│           ├── CaseMethod.py   …………测试方法，存储整个系统中的测试方法，实现测试代码和测试用例分离
│           └── __init__.py
├── README   …………本文档
├── Report   …………HTML格式的报告目录
│   └── Report.html   …………可直接在浏览器打开，再次运行后的结果可直接刷新浏览器查看
├── main.py   …………入口文件，类似于Java的main函数
└── requirements.txt   …………本框架涉及到的Python包及其版本
 ```
 - 快速开始
    
    本框架的设计思想是端到端的校验Api接口的正确性，一般的写法思维是：从数据库中选出数据，通过Api的返回校验数据校验正确性，或直接查询DB经过Api处理后的数据是否跟期望的一致。
    
    假设一个查询客户列表接口地址为:`https://testcardboard.ininin.com/crm/customer/pc_customer_list` 数据库(db_g_user.customer表)中已经存在一个客户为`'ep_name'(深圳市法本信息技术股份有限公司)`,则我们的用例可以这样写：       
    - 配置Api地址及sql

        在`project > Conf > Conf.yml`中, 添加`url`: `customer_list: "https://testcardboard.ininin.com/crm/customer/pc_customer_list"`, `data`: `customer_list: {"searchKey":"深圳市法本信息技术股份有限公司"}`  , 查询客户数据的`sql`: `SELECT ep_name FROM customer WHERE ep_name = '深圳市法本信息技术股份有限公司'`
        
    - 封装通用`CaseMethod`方法
    
        从用例设计的思想来说，查询会出现多种情况，如①正确的搜索条件、②无效的搜索条件、③模糊搜索  等情况，现在第一阶段优先①情况(先只考虑这种情况)，所以我们要先封装一个查询客户方法，示例如下：
        
        在`CaseMethod.py`中添加：
      
        def customer_list(self, data: str):
            url_customer_list = self.url.get("customer_list")
            r = self.client.get(url=url_customer_list, params=data, headers=self.token_headers(), verify=False)
            return r
  
        解释：
        第一行定义一个方法`customer_list`, 此方法接收类型为`str`的两个参数; 第二行读取名为`customer_list`的`url`(参考上一步的配置); 第三行通过`client`发起对服务器的请求; 第四行返回这个响应(这个响应我们要到用例里去校验, 校验的规则可能有很多，所以在这里需要返回这个响应对象)。
        
        在`TestCustomer`里添加测试代码：

        def test_customer_list(self):
        """ 查询客户列表 """
        with self.setUp():
            data = self.data.get("customer_list")

        with self.steps():
            resp = self.customer_list(data)
            resp_json = json.loads(resp.text)
            resp_name = ''.join(jsonpath.jsonpath(resp_json, "$..epName"))
            sql = self.sql.get("find_customer" ) % data.get("searchKey")
            expect = self.select_sql(sql)[0].get("ep_name")

        with self.verify():
            assert resp_name == expect, "错误，预期%s，实际%s" % (expect, resp_name)                  
      
      解释：
      
      第一行：我们定义一个`test_customer_list`的方法 ,必须以test开头，这样才能被框架识别的测试用例；

      第二行：是一个三引号的注释，因为英文名称的测试用例(`test_customer_list`)可能较长或直译得不太好，在查看报告的时候就会比较头疼，因此这个相当于是对中文理解报告的一个补充，不写也行，写上最好，方便看报告,在测试报告中会体现。
      
      第三行~最后的逻辑：python的通过`with`关键字编写的代码是一个安全的处理方案，可以有效防止如数据库连接未关闭、文件未关闭等情况；逻辑上，`setUp()`表示预处理，`steps()`表示步骤，`verify()`表示验证。当然，你也可以嵌套使用，这里的三个名称只是方便理清思路，纯属好看。
      
      第三行~最后的具体代码解释：
      
        ①: 通过`self.data.get("customer_list")`配置(详见`Conf.yml`)，获取Conf.yml里data下customer_list参数;
        
        ②: 发起请求(调用`customer_list`)并传入参数,;
      
        ③、④: 转换成json格式数据，获取响应体的`epName`值，jsonpath 支持完整解析json数据，在响应返回参数多的时候可用jsonpath--$..data匹配参数;
        ⑤、⑥ sql 查询数据结果是否跟API结果的一致
        ⑦: 校验`resp_name`和`expect` 是否一直，否则打印错误结果
    - 运行
        
        直接运行`main.py`文件
 
 
# 其他用法
- 新建其他项目

    直接复制dss_system目录，粘贴为自己的项目名(注意修改`Cases`文件夹和`Conf`文件夹下的相关信息), 运行时修改全局级配置文件的`PROJECT_TO_RUN`为自己的项目名;
- 只运行某几个(1个)模块
    
    在项目级配置文件里，`MODULES_TO_RUN`默认为空，表示运行所有模块的所有用例，如果要运行某几个(1个)模块则分别添加即可(用`,`<1个逗号+1个空格>分割), 若只有一个模块，则无需添加多余逗号;
- 备注
    
    示例代码默认是运行不起来的，为了防止密码泄露，我们隐藏了服务器密码(见全局级配置文件)，请咨询质量组或修改为自己的数据库密码进行测试。
      