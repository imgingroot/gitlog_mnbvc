# gitlog_mnbvc

用于mnbvc获取github commit diff的脚本，整个过程分为下面三个步骤：

1. Step 1 把原始仓库列表的 jsonl [(样本文件)](./repo_list/full_100l.jsonl) 精简，抽取出主要内容(仓库名、fork数、star数等等)，便于后续处理. [s1 处理代码](s1_repo_jsonl_lite.py)
2. Setp 2 把s1处理过的数据 [(s1样本)](./repo_list/full_100l.jsonl.s1) 做筛选、~~排重~~(还没做)，选出需要下载的仓库，导出成可以队列下载的仓库列表 [(s2样本)](./repo_list/full_100l.jsonl.s1.s2) 这部分现在只是简单的对fork、star、watch数做了筛选，并没有做排重，还需要汇总排重.[s2处理代码](s2_repo_filter.py)
3. Step 3 遍历列表  [(s2样本)](./repo_list/full_100l.jsonl.s1.s2)   clone 仓库，并把仓库中的commit记录导出成jsonl，因为github上号称2亿仓库（实际几百万），为了避免重名，和单目录下子目录过多（超过 3w 个 OS 已经很难处理），这里把仓库拆分到了3级目录，把导出的jsonl文件也同样的放入到了目录[最终样本](temp/mnbvc_git_diff_commit.jsonl)。 [s3处理代码](s3_repo_clone.py)
4. [主程序](main.py)，分别调用前面的三个步骤，输入为原始的jsonl文件，（目录或者文件，如果是目录则递归遍历目录下所有的jsonl逐个处理，如果是文件，则单个处理）输出为仓库文件和git diff commit 的 jsonl

使用：
- 需要安装git和python，并使用pip安装：
  ```shell
  pip install GitPython tqdm 
- 启动运行主程序出入文件和目录即可，主程序会分别调用各个步骤
  ```shell
  python main.py xxx.jsonl
  ```
  or 目录
  ```shell
  python main.py ./repo_list/
  ```
注意事项：
- 默认会把仓库下载到 **./repo/** 目录下的三级子目录生成的git commit_diff，也在同目录，默认文件名是 **mnbvc_git_diff_commit.jsonl**，在main.py中可以修改
- 全部执行完成可以把输出拼接在一起：
    ```shell
    find directory -name 'mnbvc_git_diff_commit.jsonl' -exec cat {} + > all.jsonl
    ```
- s1-s2的步骤都是本地文本处理，不会出现中断的情况。而s3中clone 仓库容易出现中断，程序会检查原有仓库是否存在来避免重复下载。当s3程序中断后，可以继续启动执行
- s1-s2步骤会在jsonl同目录产生临时文件(后缀 .s1 .s2)运行完s3可以删除
- 使用python的git库进行下载，无法估算文件大小，体验上有些不便

TODO：
- **仓库排重**，github列表中存在大量的fork空仓库，因为排重需要对所有数据汇总处理，在2亿的数量级，单机处理可能会比较困难，s1的步骤需要多做些出来
- **质量** 如何筛选出有价值的仓库数据，现在暂时只能按照star、fork等来做筛选，没有加入评分，这部分可以放到s2的步骤中
- **注释、实现抽取** 暂缺
- **代码排重** 需要大数据处理
- **过滤代码** 同上
- 小修改：
  - s3中如果仓库目录存在，则调用git pull更新代码，而没有检查仓库是否下载完整，这部分可能需要根据逻辑做修改
  - s3中根据扩展名获取代码语言的判断方法写的不全get_file_language
  - 可能还存在一些异常情况没有完全处理


[s1_repo_jsonl_lite.py](s1_repo_jsonl_lite.py) 代码说明
```
    #从输入的jsonl中，逐行遍历，在每行的json中的取出
    id\clone_url\stargazers_count\watchers_count\forks_count\language\open_issues_count\ 
    并导出成新的jsonl
    Usage: python s1_repo_jsonl_lite.py [input_file_path] [output_file_path]
```

[s2_repo_filter.py](s2_repo_filter.py) 代码说明
```
    # 逐行读取jsonl文件，加载成json，如果它的 stargazers_count watchers_count forks_count 都大于0 则把clone_url 保存到文本文件中。
    Usage: python s2_repo_filter.py input_file.jsonl output_file.txt
```

[s3_repo_clone.py](s3_repo_clone.py) 代码说明
```
    # 从Git仓库中提取提交日志的Python脚本。它使用GitPython库来克隆或拉取存储库，并使用diff方法来获取提交之间的差异。它还使用file-lang库来确定每个文件的语言。

    脚本接受以下参数：

    路径：Git存储库的URL。

    start_time：要检查的时间段的起始时间，默认为1天之前。

    end_time：要检查的时间段的结束时间，默认为1天之后。


    脚本的主要功能是获取给定时间段内存储库的提交日志。对于每个提交，它获取差异列表，并对于每个差异，它提取文件扩展名，添加行数，删除行数，文件语言和差异内容。所有这些信息都被保存为一个JSON字符串。

    parser.add_argument('--repo_set_dir', type=str,default="repo", help='DEST_REPO_DIR of the repository default=repo')
    parser.add_argument('--diff_filename', default=None,type=str, help='git diff commit jsonl,if null not save')
    parser.add_argument('--start', dest='start_time', type=str, default=(datetime.datetime.now() - datetime.timedelta(days=50*365)).strftime('%Y-%m-%dT%H:%M:%S'),
                        help='start time in the format of "YYYY-MM-DDTHH:MM:SS" (default: 50 years ago)')
    parser.add_argument('--end', dest='end_time', type=str, default=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S'),
                        help='end time in the format of "YYYY-MM-DDTHH:MM:SS" (default: tomorrow)')
```




