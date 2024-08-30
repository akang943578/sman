## sman
```
  ___ _ __ ___   __ _ _ __  
 / __| '_ ` _ \ / _` | '_ \ 
 \__ \ | | | | | (_| | | | |
 |___/_| |_| |_|\__,_|_| |_|
```
    
* sman是脚本管理仓库，其目的是收录各位开发的优秀脚本，实现一人开发、人人受益的宗旨。
* sman使用环境：`MacOS` `git` `Python 2.x.x` `bash/zsh`。


### 安装:

#### 方式一：（仅限fq环境使用）
```
curl -s https://raw.githubusercontent.com/haojiakang/sman/master/install.py | python
```

#### 方式二：
打开[install.py](https://github.com/haojiakang/sman/blob/master/install.py)，将文件内容全部复制保存到本地，文件名为install.py，然后执行
```
python install.py
```
，或者将脚本全文拷贝之后，在mac命令客户端输入
```
pbpaste | python
```

#### 首次安装完成后：
* 请根据最后面的提示，将`source ${install_dir}/sman/gen/sman-complete`添加到`.bash_profile`或`.bashrc`，以启用sman的命令自动补全功能。
* 然后立即执行一次`source .bash_profile`或`source .bashrc`以令自动补全功能立即生效。
* 如果输入sman是进入到了sman的git仓库文件夹，说明是开启了zsh的AUTO_CD功能，此时执行`unsetopt AUTO_CD`以关闭。
* 重复安装无需操作。


### 用法：
```
Usage:
    1. sman list: 列出sman本地收录的可执行脚本。
    2. sman update: 更新sman自身和所收录的脚本。
    3. sman add username/project: 本地添加自定义脚本。
        eg: 自己有一个自定义脚本地址为`https://github.com/haojiakang/custom_scripts`，
            则使用`sman add haojiakang/custom_scripts`将其收录到本地的sman。
        关于自定义脚本的编写规则请移步：https://github.com/haojiakang/sman 的`如何开发并添加自定义脚本`。
    4. sman rm username/project: 本地移除自定义脚本，规则同`sman add username/project`一致。
    5. sman uninstall: 卸载sman工具。
    6. sman reinstall: 重新安装sman工具。
    7. sman any_other_options: 执行所收录的脚本。
        eg: 输入`sman test`则会找到本地sman所收录的test脚本并执行。
```
* sman支持的操作包括元操作和调用操作。
* 元操作是对sman自身的操作，包括list、update、add、rm、uninstall、reinstall。
* 调用操作是调用收录的脚本并执行。收录的脚本也分为核心脚本和自定义脚本。
    * 核心脚本存在于smans项目下面。
        * 在sman安装目录下，每一个目录（去除gen、test、custom和以`.`开头的隐藏目录）下面的可执行脚本（去除以`_`开头的脚本，且不是`__init__.py`或`README.md`）都会被sman收录。
        * 如果脚本里面有`# sman_notes: Write some description here.`，则在使用`sman list`时可以看到关于脚本的说明。
            * eg: others目录的test文件里面有`# sman_notes: script to test whether sman works well.`这一行，则在执行`sman list`时，将会看到：
                ```
                ============== others ==============
                test : script to test whether sman works well.
                ```
        * 脚本必须具有可执行权限，否则将不会被sman收录。
    * 自定义脚本跟sman项目相互独立，但其通过`sman add username/project`添加到sman后，会存在于custom目录下。
        * 自定义脚本收录的地址为`custom/username_project_name/scripts`下。
            * 例如，通过`sman add haojiakang/custom_scripts`命令将[https://github.com/haojiakang/custom_scripts](https://github.com/haojiakang/custom_scripts)自定义脚本添加进来后:
                * 可以在`custom/haojiakang_sman_scripts/scripts`目录下看到自定义脚本。
                * 通过`sman list`可以看到：
                    ```
                    ============== haojiakang_custom_scripts ==============
                    motor : custom script 'motor'
                    ```
        * 对自定义脚本收录的规则如同核心脚本。
        * 可以通过`sman rm username/project`将自定义脚本从sman移除。
 * `sman list`会列出当前所收录的脚本，包括核心脚本和自定义脚本。
 * 当git仓库的代码更新后，调用`sman update`会更新本地sman到最新，包括sman自身项目和自定义脚本。

 
### 当前收录的核心脚本：

* egit: 对git的封装和扩展。
    * fpush: 快速push到git仓库，包括`git add .`, `git commit -am commit_msg`, `git push`三个操作。
    * fold: 用于在提交PR之前，将本分之的多个commit合并成1个commit。
    * fbranch: 快速从master创建分支或快速删除分支，包括远程和本地。
    * fversion: 快速设置项目pom.xml的version以及所有子module依赖的version。
    * fdeploy: 快速进行deploy一个仓库，总是使用master最新代码。
    * 详情可见: [egit](egit)
* others: 收录一些小而精，不必收录到一个单独目录的脚本。
    * test: 测试脚本，安装完成后，使用`sman test anything`用以测试sman是否正常工作。
    * 详情可见: [others](others)
    

### 如何开发并添加自定义脚本：

* 1.在github仓库创建自己的项目。
* 2.在项目根目录下面创建scripts目录，在scripts目录下面开发自己的脚本。
* 3.如果scripts下面的脚本只是内部调用，不希望被本地sman收录，则将其改名为以`__`（2个下划杠）开头。
* 4.为希望被本地sman收录的脚本文件的前部区域添加`# sman_notes: Write some description here.`脚本说明，并为其添加可执行权限。
* 5.将代码push到git仓库。
* 6.使用`sman add username/project`命令将其添加到sman。
* 7.使用`sman list`已查看自定义脚本是否添加成功。
* 8.如果希望将自定义脚本从sman移除，请执行`sman rm username/project`。
* 9.以后如果自定义脚本有更新，执行`sman update`即可更新本地sman为最新。


### 如何将自己开发的自定义脚本贡献到sman核心脚本：

* 1.核心脚本应该具有普适意义，即所有人都有稳定的使用频率。
* 2.核心脚本应该控制好代码质量，毕竟所有人都可以看到源码。
* 3.取得sman项目的开发权限后，在sman项目的根目录下创建相关目录，目录名应当清晰、直观。
* 4.将只是内部调用、不希望被sman收录的脚本改名以`__`（2个下划杠）开头。
* 5.将希望被sman收录的脚本文件的前部区域添加`# sman_notes: Write some description here.`脚本说明，并为其添加可执行权限。
* 6.在目录下面添加`README.md`文件，提供详细的说明文档。
* 7.将新添加的目录的说明和引用地址添加到本文档的`当前收录的核心脚本：`区域，参照现有的格式编辑。
* 8.将代码push到github仓库。
* 9.提醒他人使用`sman update`更新本地sman。


### 可配置项

#### 自动尝试更新策略
* 1.sman默认在使用时自动尝试更新，配置参数在`~/.sman_config`下。可以手动修改参数来调整更新策略。
* 2.`sman_auto_check_update = false` 是否在使用sman时自动尝试更新。
    * false：sman使用时不更新，可以使用`sman update`手动更新。
    * true：每次通过sman使用脚本时都先检查sman是否有更新。
    * 由于检查更新需要跟github仓库交互，耗时将近4-5秒，因此默认关闭。
    * 在关闭时，sman仍然会每`sman_update_days_gap`设置的天数进行一次更新检查。
    * 可以经常使用`sman update`手动更新，以尽量使本地脚本和git仓库保持一致。
* 3.`sman_promt_update_verify = true` 在可能需要更新时，是否弹出更新确认信息。（false：可能需要更新时直接更新）
* 4.`sman_update_days_gap = 14` 检查更新间隔天数。（即距离上次更新多久时，再次尝试更新）
* 5.`sman_last_update_day = 17696` 上一次更新的天数。（1970.1.1以来的天数值）


### 关于此项目：

* 1.代码参考github开源项目`wtool`，开发者为`@蛋疼的axb`：[https://github.com/qdaxb/wtool](https://github.com/qdaxb/wtool)


### FAQ:

* 1.为什么模块明明添加成功了，在对应的目录下可以看到。但无论是使用`sman list`、脚本自动补全、`sman 脚本名`都找不到脚本？
    * 因为对应的脚本没有可执行权限。请在对应的git项目中找到该脚本文件，为其添加可执行权限，push后使用`sman update`更新。
* 2.为什么执行`sman reinstall`的时候，会出现`installed dir contains cur work dir, can not be re installed`？
    * 不支持在sman当前的安装目录下执行`sman reinstall`，请跳出sman当前安装目录重新执行。
    * sman当前安装目录可以查看`/usr/local/bin/sman`，`sman_dir`即为安装目录。
* 3.脚本运行时出现了未知的错误，通过`sman uninstall`无法卸载，手动完全卸载应该怎么做？
    * 1.打开`/usr/local/bin/sman`，找到`sman_dir`所指向的目录，并删除。
    * 2.删除`/usr/local/bin/sman`。
    * 3.删除`~/.sman_config`。
    * 4.删除`.bash_profile`或`.bashrc`中已添加的source项。
* 4.为何脚本运行时抛出异常？
    * 1.请确认本机是否已经安装右侧命令：`git` `Python 2.x.x` `bash/zsh`，运行平台为MacOS，Linux未测试。
