##egit

###说明：
* egit是对git的封装和扩展，将开发中常用到的git命令组合定制成脚本，简化重复操作。

###Usage
* fpush: 快速push到git仓库，包括`git add .`, `git commit -am commit_msg`, `git push`三个操作。
    * fpush 交互式，会有提示输入commit信息。
    * fpush add some commit message here 非交互式，直接将fpush后面的内容作为commit信息提交。
* fold: 用于在提交PR之前，将本分之的多个commit合并成1个commit。
    * fold 交互式，会有提示输入commit信息。
    * fold add some commit message here 非交互式，直接将fold后面的内容作为commit信息提交。
* fbranch: 快速从master创建分支或快速删除分支，包括远程和本地。
    * 快速从master创建分支，不支持创建master：
        * fbranch 交互式，会提示输入要创建的分支名。
        * fbranch branch_name 非交互式，将以'branch_name'作为要创建的分支名。注意分支名不可输入多个。
    * 快速删除分支，包括远程和本地，不支持删除master：
        * fbranch -rm 交互式，会提示输入要创建的分支名。
        * fbranch -rm branch_name 非交互式，将以'branch_name'作为要创建的分支名。注意分支名不可输入多个。
* fversion: 快速设置项目pom.xml的version以及所有子module依赖的version。
    * fversion 交互式，提示输入目标版本号。
    * fversion x.xx.xxx 非交互式，x.xx.xxx作为目标版本号。
    * fversion -a 自动模式，如果是SNAPSHOT版本，则不变；如果是正式版本（无后缀），则目标版本号为当前版本号末尾数字+1。
* fthrift: 快速根据thrift文件重新生成java源码，fpush和deploy。
    * fthrift -v: 快速根据thrift文件重新生成java源码，并将pom version如果正式版增加1，fpush和deploy。