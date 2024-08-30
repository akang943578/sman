## sman
```
  ___ _ __ ___   __ _ _ __  
 / __| '_ ` _ \ / _` | '_ \ 
 \__ \ | | | | | (_| | | | |
 |___/_| |_| |_|\__,_|_| |_|
```

* sman is a script management repository designed to collect and share high-quality scripts developed by different individuals, with the goal of "developed by one, benefiting all."
* sman usage environment: `MacOS`, `git`, `Python 2.x.x`, `bash/zsh`.

### Installation:

#### Method 1: (Only applicable in a proxy environment)
```
curl -s https://raw.githubusercontent.com/haojiakang/sman/master/install.py | python
```

#### Method 2:
Open [install.py](https://github.com/haojiakang/sman/blob/master/install.py), copy the entire content, save it locally as `install.py`, and then run:
```
python install.py
```
Alternatively, copy the script entirely and then in the Mac terminal run:
```
pbpaste | python
```

#### After the first installation:
* Please follow the instructions at the end and add `source ${install_dir}/sman/gen/sman-complete` to your `.bash_profile` or `.bashrc` to enable sman's command auto-completion feature.
* Then, immediately run `source .bash_profile` or `source .bashrc` to activate the auto-completion feature.
* If typing `sman` brings you to the sman git repository folder, it indicates that zsh's AUTO_CD feature is enabled. In this case, run `unsetopt AUTO_CD` to disable it.
* No further action is needed for repeat installations.

### Usage:
```
Usage:
    1. sman list: List the scripts recorded locally by sman.
    2. sman update: Update sman itself and the scripts recorded.
    3. sman add username/project: Add custom scripts locally.
        eg: If you have a custom script located at `https://github.com/haojiakang/custom_scripts`,
            use `sman add haojiakang/custom_scripts` to include it in your local sman.
        For the rules on writing custom scripts, please refer to `How to Develop and Add Custom Scripts` on https://github.com/haojiakang/sman.
    4. sman rm username/project: Remove custom scripts locally. The rules are the same as `sman add username/project`.
    5. sman uninstall: Uninstall the sman tool.
    6. sman reinstall: Reinstall the sman tool.
    7. sman any_other_options: Execute the recorded scripts.
        eg: Typing `sman test` will find and execute the locally recorded `test` script.
```
* sman supports operations including meta-operations and call operations.
* Meta-operations are actions on sman itself, including list, update, add, rm, uninstall, and reinstall.
* Call operations are used to call and execute recorded scripts. The recorded scripts include core scripts and custom scripts.
    * Core scripts are found under the sman project.
        * In the sman installation directory, any executable scripts found in a directory (excluding the `gen`, `test`, `custom` directories, and hidden directories beginning with `.`) will be recorded by sman.
        * If a script contains `# sman_notes: Write some description here.`, this note will be visible when using `sman list`.
            * eg: The `test` file in the `others` directory has `# sman_notes: script to test whether sman works well.`. When you run `sman list`, you will see:
                ```
                ============== others ==============
                test : script to test whether sman works well.
                ```
        * Scripts must have executable permissions; otherwise, they will not be recorded by sman.
    * Custom scripts are independent of the sman project but will be recorded in the `custom` directory after being added with `sman add username/project`.
        * Custom scripts are stored under `custom/username_project_name/scripts`.
            * For example, adding a custom script from [https://github.com/haojiakang/custom_scripts](https://github.com/haojiakang/custom_scripts) using the command `sman add haojiakang/custom_scripts`:
                * The custom script can be found under `custom/haojiakang_sman_scripts/scripts`.
                * By running `sman list`, you will see:
                    ```
                    ============== haojiakang_custom_scripts ==============
                    motor : custom script 'motor'
                    ```
        * The rules for recording custom scripts are the same as for core scripts.
        * You can remove a custom script from sman by executing `sman rm username/project`.
* `sman list` lists the currently recorded scripts, including both core scripts and custom scripts.
* When the git repository code is updated, running `sman update` will update the local sman to the latest version, including the sman project itself and custom scripts.


### Currently Recorded Core Scripts:

* egit: Encapsulation and extension of git commands.
    * fpush: Quickly push to the git repository, including `git add .`, `git commit -am commit_msg`, `git push`.
    * fold: Used to merge multiple commits in the current branch into a single commit before submitting a PR.
    * fbranch: Quickly create or delete branches from master, including both remote and local branches.
    * fversion: Quickly set the version in the project's pom.xml and all submodule dependencies.
    * fdeploy: Quickly deploy a repository, always using the latest code from the master branch.
    * Details can be found at: [egit](egit)
* others: Collect small, precise scripts that do not warrant their own directory.
    * test: A test script. After installation, use `sman test anything` to verify that sman works correctly.
    * Details can be found at: [others](others)


### How to Develop and Add Custom Scripts:

* 1. Create your own project on GitHub.
* 2. Create a `scripts` directory in the root of the project, and develop your scripts within this directory.
* 3. If a script under the `scripts` directory is only for internal use and you do not want it to be recorded by the local sman, rename it with a prefix of `__` (two underscores).
* 4. Add `# sman_notes: Write some description here.` at the top of the script you wish to record, and grant it executable permissions.
* 5. Push the code to your git repository.
* 6. Add the script to sman using the `sman add username/project` command.
* 7. Use `sman list` to check whether the custom script was added successfully.
* 8. To remove a custom script from sman, run `sman rm username/project`.
* 9. If the custom script is updated in the future, execute `sman update` to update the local sman to the latest version.


### How to Contribute Your Custom Scripts to sman Core Scripts:

* 1. Core scripts should be widely applicable and have stable usage by everyone.
* 2. Core scripts should maintain good code quality since the source code is visible to everyone.
* 3. After gaining development permissions for the sman project, create the relevant directory in the root of the sman project, ensuring the directory name is clear and intuitive.
* 4. Rename scripts that are only for internal use and should not be recorded by sman with a prefix of `__` (two underscores).
* 5. Add `# sman_notes: Write some description here.` at the top of the scripts you wish to record, and grant them executable permissions.
* 6. Add a `README.md` file to the directory to provide detailed documentation.
* 7. Add a description of the newly added directory and its reference address to the `Currently Recorded Core Scripts:` section of this document, following the existing format.
* 8. Push the code to the GitHub repository.
* 9. Remind others to use `sman update` to update their local sman.

### Configurable Options

#### Auto-Update Strategy
* 1. sman attempts to update automatically by default. The configuration parameters are located in `~/.sman_config`. You can manually modify these parameters to adjust the update strategy.
* 2. `sman_auto_check_update = false`: Whether to automatically attempt to update when using sman.
    * false: sman will not update when used. You can manually update using `sman update`.
    * true: sman will check for updates every time a script is run.
    * Checking for updates requires interaction with the GitHub repository, which takes about 4-5 seconds, so it is disabled by default.
    * Even when disabled, sman will still check for updates every `sman_update_days_gap` days.
    * You can regularly use `sman update` to keep your local scripts in sync with the GitHub repository.
* 3. `sman_promt_update_verify = true`: Whether to prompt for confirmation when an update is available. (false: directly update when an update is available)
* 4. `sman_update_days_gap = 14`: The interval in days between update checks.
* 5. `sman_last_update_day = 17696`: The last update day, in days since January 1, 1970.


### About This Project:

* 1. The code is inspired by the open-source project `wtool` on GitHub, developed by `@蛋

二狗`, which focuses on managing small tool scripts. This project takes similar code and expands on it.
* 2. The project was developed and maintained by several contributors, each adding their own useful scripts.
* 3. The intention is to enable users to share scripts efficiently, reducing duplicated efforts.
* 4. sman is specifically designed for use in environments that comply with proxy standards, facilitating script management and sharing.
* 5. The code is open-source, and contributions are welcome to help grow and improve the collection of scripts.

### License:
This project is licensed under the MIT License. See the [LICENSE](https://github.com/haojiakang/sman/blob/master/LICENSE) file for more details.

### FAQ:
* 1. Where can I find more information or report issues?
    * Visit the [sman GitHub repository](https://github.com/haojiakang/sman).
* 2. Is there a way to undo an update?
    * Since sman is essentially a git repository, you can manually revert to a previous commit if necessary.
* 3. Can I run sman on Windows?
    * sman is designed for use on MacOS with bash/zsh. It may not work correctly on Windows.
* 4. How can I ensure my scripts are recognized by sman?
    * Make sure they are stored in the correct directory, have executable permissions, and include the required note format.
