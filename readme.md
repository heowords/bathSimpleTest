# 一个简单的批量测试脚本

 - 可插拔通过curl_use快速切换测试用例
 - 持久化测试脚本输入，下次直接用，输出日志目前没有需求就不写了
 - 批量测试
 - yaml配置文件更灵活测试

环境安装
````
    python3 install requests
    python3 install yaml
````

执行命令
````
    python3 test.py
````

Mac可能存在SSL兼容问题
````
  brew install pyenv
  brew install openssl@1.1
````