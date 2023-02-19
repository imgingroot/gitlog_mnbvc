# gitlog_mnbvc

这是一个用于从Git仓库中提取提交日志的Python脚本。它使用GitPython库来克隆或拉取存储库，并使用diff方法来获取提交之间的差异。它还使用file-lang库来确定每个文件的语言。

脚本接受以下参数：

repo_url：Git存储库的URL。

start_time：要检查的时间段的起始时间，默认为1天之前。

end_time：要检查的时间段的结束时间，默认为1天之后。


脚本的主要功能是获取给定时间段内存储库的提交日志。对于每个提交，它获取差异列表，并对于每个差异，它提取文件扩展名，添加行数，删除行数，文件语言和差异内容。所有这些信息都被保存为一个JSON字符串。

需要安装 git
```
pip install GitPython
```

可以这样执行：
```
python main.py https://github.com/esbatmop/MNBVC.git 
```
