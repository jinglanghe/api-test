# api-test
aiarts的接口测试框架

## 目录

- [上手指南](#上手指南)
  - [使用步骤](#使用步骤)
- [文件目录说明](#文件目录说明)
- [开发的架构](#开发的架构)
  
### 上手指南

###### 使用前的配置要求
执行机器上安装了
1. python3.6及以上版本
2. jdk8 & allure(若不使用allure生成报告，则可以不安装)

allure 安装方式 https://github.com/allure-framework/allure2/releases/

###### **使用步骤**

```sh
1. Clone the repo
2. cd apt-test
3. vim config/config.yaml  # 修改测试环境的url、用户名、密码（账号需提前创建好）
4. pip install -r requirements.txt
5. pytest -sv ./testcase --alluredir=./allure-results  # 执行测试
6. allure server ./allure-results  # 查看报告
```

### 文件目录说明


```
api-test
├── /api/
│  ├── /aiarts/             # 封装待测试的接口
│  └──base.py               # base类，处理配置、session、token等
├── /config/                # 配置文件 
│  ├── api_path_list.yaml   # api路径汇总
│  ├── config.yaml          # 测试环境的url及测试使用的账号
│  └── token.txt            # 执行测试时，token暂时会存在这里
├── /log/                   
├── test_assert             # 断言用的配置
├── test_data               # 测试时使用的数据
├── testcase                # 测试用例
├── /tools/                 # 工具类，日志等
├── README.md
└── requirements.txt
```

### 使用到的的架构 

pytest   
https://docs.pytest.org/en/6.2.x/

allure   
https://docs.qameta.io/allure/#_pytest