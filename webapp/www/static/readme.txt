Git is a distributed version control system.
Git is free software distributed under the GPL.

一、初始化一个Git仓库，使用git init命令。
二、添加文件到Git仓库，分两步：
    1、使用命令git add <file>，注意，可反复多次使用，添加多个文件；
    2、使用命令git commit -m <message>，完成。
三、1、要随时掌握工作区的状态，使用git status命令。
    2、如果git status告诉你有文件被修改过，用git diff <file>可以查看修改内容。
四、版本回退
    1、HEAD指向的版本就是当前版本，（上一个版本就是HEAD^，上上一个版本就是HEAD^^，
       当然往上100个版本写100个^比较容易数不过来，所以写成HEAD~100）
       因此，Git允许我们在版使用命令git reset --hard commit_id。
    
    2、穿梭前，用git log可以查看提交历史，以便确定要回退到哪个版本。
    3、要重返未来，用git reflog查看命令历史，以便确定要回到未来的哪个版本。
    
    
1、git init
2、git add <file>
   git commit -m <message>
3、git status
   git diff <file>
4、版本回退
   git reset --hard commit_id【或者：（上一个版本：git reset --hard HEAD^)】
   git log
   git reflog
   