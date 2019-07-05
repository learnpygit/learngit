Git is a distributed version control system.
Git is free software distributed under the GPL.
Git has a mutable index called stage.
Git tracks changes of files.
Creating a new branch is quick.

一、初始化一个Git仓库，使用git init命令。
二、添加文件到Git仓库，分两步：
    1、使用命令git add <file>，注意，可反复多次使用，添加多个文件；
    2、使用命令git commit -m <message>，完成。
三、1、要随时掌握工作区的状态，使用git status命令。
    2、如果git status告诉你有文件被修改过，用git diff <file>可以查看修改内容。
四、Git基本操作
    <一>、版本回退
        1、HEAD指向的版本就是当前版本，（上一个版本就是HEAD^，上上一个版本就是HEAD^^，
           当然往上100个版本写100个^比较容易数不过来，所以写成HEAD~100）
           因此，Git允许我们在版使用命令git reset --hard commit_id。
        
        2、穿梭前，用git log可以查看提交历史，以便确定要回退到哪个版本。
        3、要重返未来，用git reflog查看命令历史，以便确定要回到未来的哪个版本。
    <二>、管理修改
        用git diff HEAD -- readme.txt命令可以查看工作区和版本库里面最新版本的区别.
        每次修改，如果不用git add到暂存区，那就不会加入到commit中。
    <三>、撤销修改  
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
    <四>、删除文件
        一般情况下，你通常直接在文件管理器中把没用的文件删了，或者用rm命令删了：rm test.txt
        现在你有两个选择，
        1、是确实要从版本库中删除该文件，那就用命令git rm删掉，并且git commit
            （小提示：先手动删除文件，然后使用git rm <file>和git add <file>效果是一样的。）(注：教程是不是说错了，手动跟命令删除都可以用git add <file>)
        2、是删错了，因为版本库里还有呢，所以可以很轻松地把误删的文件恢复到最新版本：
            git checkout -- file
            git checkout其实是用版本库里的版本替换工作区的版本，无论工作区是修改还是删除，都可以“一键还原”。
        注意：从来没有被添加到版本库就被删除的文件，是无法恢复的！
        命令git rm用于从版本库中删除一个文件。如果一个文件已经被提交到版本库，那么你永远不用担心误删，但是要小心，你只
        能恢复文件到最新版本，你会丢失最近一次提交后你修改的内容。
五、远程仓库
    <一>、添加远程库
        1、关联一个远程库。
            在本地的仓库下运行命令：(关联出错的话，可能要配置下系统etc下的hosts文件，如：13.250.177.223 github.com)
                git remote add origin git@server-name:path/repo-name.git
                例子：
                git remote add origin git@github.com:michaelliao/learngit.git
        2、本地库的所有内容推送到远程库上
                (1)第一次推送
                    git push -u origin master
                第一次推送master分支时，加上了-u参数，Git不但会把本地的master分支内容推送到远程新的master分支，还会把本地
                的master分支和远程的master分支关联起来，在以后的推送或者拉取时就可以简化命令。
                (2)此后的推送
                    git push origin master
    <二>、从远程库克隆
        git clone git@server-name:path/repo-name.git

六、分支管理
    <一>、创建与合并分支
        1、在Git里，这个分支叫主分支，即master分支。HEAD严格来说不是指向提交，而是指向master，master才是指向提交的，所以，
           HEAD指向的就是当前分支。
        2、当我们创建新的分支，例如dev时，Git新建了一个指针叫dev，指向master相同的提交，再把HEAD指向dev，就表示当前分支在dev上。
           你看，Git创建一个分支很快，因为除了增加一个dev指针，改改HEAD的指向，工作区的文件都没有任何变化！
        3、从现在开始，对工作区的修改和提交就是针对dev分支了，比如新提交一次后，dev指针往前移动一步，而master指针不变。
        4、Git怎么合并呢？最简单的方法，就是直接把master指向dev的当前提交，就完成了合并。
           所以Git合并分支也很快！就改改指针，工作区内容也不变！
        5、删除dev分支就是把dev指针给删掉，删掉后，我们就剩下了一条master分支。
        
        Git鼓励大量使用分支：
        查看分支：git branch
        创建分支：git branch <name>
        切换分支：git checkout <name>
        创建+切换分支：git checkout -b <name>
        合并某分支到当前分支：git merge <name>
        删除分支：git branch -d <name>
一、git init
二、git add <file>
    git commit -m <message>
三、git status
    git diff <file>
四、Git基本操作
    1、版本回退
        git reset --hard commit_id【或者：（上一个版本：git reset --hard HEAD^)】
        git log  （注：查看提交历史）
        git reflog  （注：查看命令历史）
    2、管理修改
        git diff HEAD -- <file>
    3、撤销修改
        git checkout -- file  （注：丢弃工作区的修改）
        git reset HEAD <file>   （注：丢弃暂存区的修改）
    4、删除文件
        rm <file>
        (1)确实要删除：
            git rm <file>
            git commit -m <message>
        (2)删错了,恢复到最新版本
            git checkout -- file
五、远程仓库
    1、添加远程库  
       (1) 关联一个远程库
           git remote add origin git@server-name:path/repo-name.git
       (2)推送到远程库
           第一次推送：
           git push -u origin master
           此后的推送：
           git push origin master
    2、从远程库克隆
        git clone git@server-name:path/repo-name.git
            如:git clone git@github.com:learnpygit/gitskills.git
