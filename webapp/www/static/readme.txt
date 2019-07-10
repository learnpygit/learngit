Git is a distributed version control system.
Git is a free software distributed under the GPL.
Git has a mutable index called stage.
Git tracks changes of files.
Creating a new branch is quick and simple.
分支管理策略

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
        6、git checkout命令加上-b参数表示创建并切换。
        7、git branch命令会列出所有分支，当前分支前面会标一个*号。
        8、git merge命令用于合并指定分支到当前分支。Fast-forward信息，Git告诉我们，这次合并是“快进模式”，也就是直接把master
           指向dev的当前提交，所以合并速度非常快。当然，也不是每次合并都能Fast-forward，我们后面会讲其他方式的合并。
        9、创建、合并和删除分支非常快，所以Git鼓励你使用分支完成某个任务，合并后再删掉分支，这和直接在master分支上工作效果是
           一样的，但过程更安全。
    <二>、解决冲突
        1、当Git无法自动合并分支时，就必须首先解决冲突。解决冲突后，再提交，合并完成。
            解决冲突就是把Git合并失败的文件，手动编辑为我们希望的内容，再提交。
        2、用git log --graph命令可以看到分支合并图。
           用带参数的git log也可以看到分支的合并情况：git log --graph --pretty=oneline --abbrev-commit
    <三>、分支管理策略      
        1、通常，合并分支时，如果可能，Git会用Fast forward模式，但这种模式下，删除分支后，会丢掉分支信息。
        2、如果要强制禁用Fast forward模式，Git就会在merge时生成一个新的commit，这样，从分支历史上就可以看出分支信息。
        3、下面我们实战一下--no-ff方式的git merge。
            例：   git merge --no-ff -m "merge with no-ff" dev
            注意--no-ff参数，表示禁用Fast forward
            因为本次合并要创建一个新的commit，所以加上-m参数，把commit描述写进去。            
        4、分支策略
            在实际开发中，我们应该按照几个基本原则进行分支管理：
                （1）首先，master分支应该是非常稳定的，也就是仅用来发布新版本，平时不能在上面干活；
                （2）那在哪干活呢？干活都在dev分支上，也就是说，dev分支是不稳定的，到某个时候，比如1.0版本发布时，再把dev分支
                     合并到master上，在master分支发布1.0版本；
                （3）你和你的小伙伴们每个人都在dev分支上干活，每个人都有自己的分支，时不时地往dev分支上合并就可以了。
        5、 小结
            Git分支十分强大，在团队开发中应该充分应用。
            合并分支时，加上--no-ff参数就可以用普通模式合并，合并后的历史有分支，能看出来曾经做过合并，
            而fast forward合并就看不出来曾经做过合并。 
    <四>、Bug分支
            当你接到一个修复一个代号101的bug的任务时，很自然地，你想创建一个分支issue-101来修复它，但是，等等，当前正在dev上进行
        的工作还没有提交。并不是你不想提交，而是工作只进行到一半，还没法提交，预计完成还需1天时间。但是，必须在两个小时内修
        复该bug，怎么办？
            Git还提供了一个stash功能，可以把当前工作现场“储藏”起来，等以后恢复现场后继续工作：
                git stash
        1、确定要在哪个分支上修复bug，假定需要在master分支上修复，就从master创建临时分支：
                git checkout master
                git checkout -b issue-101
        2、现在修复bug，然后提交：
                例：   git add readme.txt
                       git commit -m "fix bug 101"
        3、修复完成后，切换到master分支，并完成合并，最后删除issue-101分支：
                例：   git checkout master
                       git merge --no-ff -m "merged bug fix 101" issue-101
                       git branch -d issue-101
        4、现在，是时候接着回到dev分支干活了！
            用git stash list命令看看刚才的工作现场存到哪去了。
            
        5、需要恢复一下，有两个办法：
            一是：用git stash apply恢复，但是恢复后，stash内容并不删除，你需要用git stash drop来删除。
            另一种方式是：用git stash pop，恢复的同时把stash内容也删了。
            
        6、你可以多次stash，恢复的时候，先用git stash list查看，然后恢复指定的stash，用命令：
            git stash apply stash@{0}
            
        7、小结
            修复bug时，我们会通过创建新的bug分支进行修复，然后合并，最后删除。
            当手头工作没有完成时，先把工作现场git stash一下，然后去修复bug，修复后，再git stash pop，回到工作现场。
    <五>、Feature分支
        每添加一个新功能，最好新建一个feature分支，在上面开发，完成后，合并，最后，删除该feature分支。
        如果要丢弃一个没有被合并过的分支，可以通过git branch -D <branch-name>强行删除。
    <六>、多人协作
        1、查看远程库的信息
            git remote 或者，用git remote -v显示更详细的信息。
        2、推送分支
            git push origin <branch-name>
                但是，并不是一定要把本地分支往远程推送，那么，哪些分支需要推送，哪些不需要呢？
                (1)、master分支是主分支，因此要时刻与远程同步；
                (2)、dev分支是开发分支，团队所有成员都需要在上面工作，所以也需要与远程同步；
                (3)、bug分支只用于在本地修复bug，就没必要推到远程了，除非老板要看看你每周到底修复了几个bug；
                (4)、feature分支是否推到远程，取决于你是否和你的小伙伴合作在上面开发。
                总之，就是在Git中，分支完全可以在本地自己藏着玩，是否推送，视你的心情而定！
        3、抓取分支
            (1)、多人协作时，当你的小伙伴从远程库clone时，默认情况下，你的小伙伴只能看到本地的master分支。
                 现在，你的小伙伴要在dev分支上开发，就必须创建远程origin的dev分支到本地，于是他用这个命令创建本地dev分支：
                    git checkout -b dev origin/dev
            (2)、你的小伙伴的最新提交和你试图推送的提交有冲突，推送失败。用git pull把最新的提交从origin/<branch-name>抓下来，然后，
                 在本地合并，解决冲突，再推送。
                 如果git pull也失败了，原因是没有指定本地branch-name分支与远程origin/branch-name分支的链接，
                 根据提示，设置branch-name和origin/branch-name的链接：
                 例： git branch --set-upstream-to=origin/dev dev
                 git pull成功，但是合并有冲突，需要手动解决，解决的方法和分支管理中的解决冲突完全一样。解决后，提交，再push。
        4、小结
            多人协作的工作模式通常是这样：
                首先，可以试图用git push origin <branch-name>推送自己的修改；
                如果推送失败，则因为远程分支比你的本地更新，需要先用git pull试图合并；
                如果合并有冲突，则解决冲突，并在本地提交；
                没有冲突或者解决掉冲突后，再用git push origin <branch-name>推送就能成功！
                如果git pull提示no tracking information，则说明本地分支和远程分支的链接关系没有创建，
                用命令git branch --set-upstream-to <branch-name> origin/<branch-name>。
    <七>、Rebase
        1、 Git有一种称为rebase的操作，有人把它翻译成“变基”。看看怎么把分叉的提交变成直线。
            输入命令git rebase，原本分叉的提交现在变成一条直线了。
            rebase操作的特点：把分叉的提交历史“整理”成一条直线，看上去更直观。缺点是本地的分叉提交已经被修改过了。
        2、小结：
            rebase操作可以把本地未push的分叉提交历史整理成直线；
            rebase的目的是使得我们在查看历史提交的变化时更容易，因为分叉的提交需要三方对比。
七、标签管理
    发布一个版本时，我们通常先在版本库中打一个标签（tag），这样，就唯一确定了打标签时刻的版本。
    Git的标签虽然是版本库的快照，但其实它就是指向某个commit的指针（跟分支很像对不对？但是分支可以移动，标签不能移动），
    所以，创建和删除标签都是瞬间完成的。
    <一>、创建标签
        1、切换到需要打标签的分支上，默认标签是打在最新提交的commit上的。
        2、有时候，如果忘了打标签，比如，现在已经是周五了，但应该在周一打的标签没有打，怎么办？
           方法是找到历史提交的commit id，然后打上就可以了。
        3、还可以创建带有说明的标签，用-a指定标签名，-m指定说明文字：
           例： git tag -a v0.1 -m "version 0.1 released" 1094adb
        4、注意，标签不是按时间顺序列出，而是按字母排序的。可以用git show <tagname>查看标签信息。
        5、注意：标签总是和某个commit挂钩。如果这个commit既出现在master分支，又出现在dev分支，
                 那么在这两个分支上都可以看到这个标签。




一、git init
二、git add <file>
    git commit -m <message>
三、git status
    git diff <file>
四、Git基本操作
    1、版本回退
        git reset --hard commit_id【或者：（上一个版本：git reset --hard HEAD^)】
        git log  （注：查看提交历史） 
            嫌输出信息太多，看得眼花缭乱的，可以试试加上--pretty=oneline参数：git log --pretty=oneline
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
六、分支管理
    1、创建与合并分支
        Git鼓励大量使用分支：
            查看分支：git branch
            创建分支：git branch <name>
            切换分支：git checkout <name>
            创建+切换分支：git checkout -b <name>
            合并某分支到当前分支：git merge <name>
            删除分支：git branch -d <name>
    2、解决冲突
        用git log --graph命令可以看到分支合并图。
        用带参数的git log也可以看到分支的合并情况：git log --graph --pretty=oneline --abbrev-commit
    3、分支管理策略
        git merge --no-ff -m <message> <branchname>
    4、Bug分支
       把当前工作现场“储藏”起来：git stash
       恢复“储藏”起来的工作现场：(注：要回到“储藏”的分支中才能恢复)
            (1)恢复:  git stash apply
               删除:  git stash drop
            (2)恢复+删除:  git stash pop
    5、Feature分支
        强行删除没有被合并过的分支：git branch -D <name>
    6、多人协作 
        (1)、查看远程库信息：git remote 或 git remote -v
        (2)、从本地推送分支：git push origin branch-name
             如果推送失败，先用抓取远程的新提交：git pull
        (3)、在本地创建和远程分支对应的分支，本地和远程分支的名称最好一致：git checkout -b branch-name origin/branch-name   
        (4)、建立本地分支和远程分支的关联：git branch --set-upstream-to <branch-name> origin/<branch-name>   （错误： git branch --set-upstream branch-name origin/branch-name）
        (5)、从远程抓取分支：git pull
    7、Rebase 
        git rebase
七、标签管理   
    1、创建标签
        (1)、新建一个标签，默认为HEAD；  git tag <tagname> 
             也可以指定一个commit_id：   git tag <tagname> <commit_id>
             
        (2)、指定标签信息；  git tag -a <tagname> -m <message>
        (3)、查看所有标签:  git tag
        (4)、查看标签信息：git show <tagname>