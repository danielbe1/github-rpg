[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/danielbe1/github-rpg)
# github-rpg


Issues <--> Tasks in a nutshell
==============================
* When opening a new Github issue, a new `todo` task will be created on your Habitica account.
* When closing an existing Github issue, the corresponding Habitica `todo` task will be completed, if the task does not exist it will be recreated.
* When reopening a closed Github issue, the corresponding Habitica `todo` task will be uncompleted, if it does not exist it will be recreated.

Task hints in Github issues
===========================
It is possible to specify certain hints on the Github issue to specify task parameters:
* Difficulty: 
    - `Difficulty: trivial`
    - `Difficulty: easy`
    - `Difficulty: medium`
    - `Difficulty: hard`

Excluding Github issues
=======================
Specific issues can be excluded from being synced by adding a label, defined in the `LABEL_TO_IGNORE` env variable (set to `github-rpg-ignore` by default).
Adding or removing this label from existing issues will acuse the corresponding `todo` tasks to be deleted or recreated accordingly.
