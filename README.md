# alphamed-federated-playground
医学联邦学习计算平台

## 项目结构
```
.
├── README.md
├── config
│   ├── cert
│   │   ├── org.crt
│   │   ├── user.sign.crt
│   │   ├── user.sign.key
│   │   ├── user.tls.crt
│   │   └── user.tls.key
│   └── config.yml
├── docker-compose.yml
└── src
    ├── __init__.py
    ├── __pycache__
    │   ├── backend_client.cpython-39.pyc
    │   ├── cert_init.cpython-39.pyc
    │   └── subscribe.cpython-39.pyc
    ├── cert.py
    ├── client.py
    ├── main.py
    └── subscribe.py
```

## 快速开始
### 准备工作
#### 系统环境准备
##### 1. 推荐配置

| 配置 | 最低配置 | 推荐配置 |
| ---- | -------- | -------- |
| CPU  | 1.5GHz   | 2.4GHz   |
| 内存 | 8GB      | 16GB     |
| 核心 | 4核      | 8核      |
| 带宽 | 2Mb      | 10Mb     |

##### 2. 软件依赖
| 名称           | 版本       | 描述                 | 是否必须 |
| -------------- | ---------- | -------------------- | -------- |
| OS             | centos 8.4 | 操作系统             |          |
| git            | /          | 源码管理             | 是       |
| golang         | 1.16+      | 编译环境             | 是       |
| docker         | 18+        | 独立运行容器         | 否       |
| docker-compose | /          | 容器管理组件         | 否       |
| gcc            | 7.3+       | 编译环境依赖         | 是       |
| glibc          | 2.18       | 智能合约执行环境依赖 | 是       |
| tmux           | /          | 默认快速启动命令依赖 | 否       |

##### 3.主要依赖安装
##### 3.1 安装golang
 ```
wget https://go.dev/dl/go1.18.2.linux-amd64.tar.gz
tar -zxvf go1.18.2.linux-amd64.tar.gz
mv go /usr/local/
vim ~/.bash_profile
export PATH=$PATH:/usr/local/go/bin
[root@VM-11-35-centos ~]# go version
go version go1.18.2 linux/amd64

## 设置代理
go env -w GOPROXY=https://goproxy.cn
 ```
##### 3.2 安装docker
 ```
 sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum list docker-ce --showduplicates | sort -r
yum install docker-compose-plugin
 ```
###### 3.3 下载代码
```
git clone git@github.com:ssplabs/alphamed-federated-playground.git
```
#### 配置文件准备
##### 证书秘钥
1. 下载组织CA证书放入系统目录并重命名 `config/cert/org.crt`
2. 下载用户签名证书放入系统目录并重命名 `config/cert/user.sign.crt`
3. 下载用户签名私钥放入系统目录并重命名 `config/cert/user.sign.key`
4. 下载用户TLS证书放入系统目录并重命名 `config/cert/user.tls.crt`
5. 下载用户TLS私钥放入系统目录并重命名 `config/cert/user.tls.key`
##### 配置文件
```
backend:
  host: 127.0.0.1 # 默认不变
chain:
  chain_id: "sspchain1" # 默认不变
  org_id: "wx-org1.chainmaker.org" # 申请的组织ID
  org_name: "sspchain1org1" # 组织名称
  node_name: "sspchain1org1node1" # 订阅节点的名称
  node_id: "" # 订阅节点的ID
  user_name: "" # 用户名称
  node_host: "127.0.0.1" # 订阅节点的ip
  node_rpc_port: 12301 # 订阅节点rpc端口
  tls: true
  tls_host_name: "chainmaker.org" # CA颁发组织 默认不变
  contract:
  - name: "fact" # 订阅合约名称 默认
    version: "1.0" # 订阅合约版本 默认
  - name: "task" # 订阅合约名称 默认
    version: "2.0" # 订阅合约名称 默认
  cert:
    org_ca: ../config/cert/org.crt
    user_tls_cert: ../config/cert/user.tls.crt
    user_tls_key: ../config/cert/user.tls.key
    user_sign_cert: ../config/cert/user.sign.crt
    user_sign_key: ../config/cert/user.sign.key    
```
### 启动平台
#### 构建并启动系统
```
docker-compose up -d --build
```
#### 初始化链节点订阅
```
cd crc
// 初始化证书到系统
python3 main.py init_cert
// 初始化区块链订阅
python3 main.py subscribe_chain
// 进入系统观察区块链的区块同步完成
// 初始化区块合约订阅
python3 main.py subscribe_contract
```
#### 系统初始化完毕
### 开始第一个联邦学习任务 
    