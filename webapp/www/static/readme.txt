Git is a distributed version control system.
Git is free software distributed under the GPL.
Git has a mutable index called stage.
Git tracks changes of files.

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
五、

六、撤销修改  
    1、 丢弃工作区的修改
        命令git checkout -- readme.txt意思就是，把readme.txt文件在工作区的修改全部撤销，这里有两种情况：

            一种是readme.txt自修改后还没有被放到暂存区，现在，撤销修改就回到和版本库一模一样的状态；

            一种是readme.txt已经添加到暂存区后，又作了修改，现在，撤销修改就回到添加到暂存区后的状态。
        总之，就是让这个文件回到最近一次git commit或git add时的状态。
        git checkout -- file命令中的--很重要，没有--，就变成了“切换到另一个分支”的命令。
    2、丢弃暂存区的修改（重新放回工作区）
       用命令git reset HEAD <file>可以把暂存区的修改撤销掉（unstage），重新放回工作区。
       git reset命令既可以回退版本，也可以把暂存区的修改回退到工作区。当我们用HEAD时，表示最新的版本。
    3、丢弃版本库的修改
       已经提交了不合适的修改到版本库时，想要撤销本次提交，参考版本回退一节，不过前提是没有推送到远程库。
    
1、git init
2、git add <file>
   git commit -m <message>
3、git status
   git diff <file>
4、版本回退
   git reset --hard commit_id【或者：（上一个版本：git reset --hard HEAD^)】
   git log
   git reflog
5、

6、撤销修改
   git checkout -- file
   git reset HEAD <file>
   
   