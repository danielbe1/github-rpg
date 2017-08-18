[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/danielbe1/github-rpg)
====================================================================================================================================

This is a little service I've created to make organizing projects more rewarding by turning Github issues to Habitica tasks.
The service is intended to be deployed on the Heroku platform and you can try it by pressing the nice purple button above.

Service configuration
=====================
The service requireds only 3 configuration settings:
* USER_KEY - The Habitca user key.
* API_KEY - The Habitica API key.
* LABEL_TO_IGNORE - The name of a label that can be applied to issues that you want the service to ignore.

Setting up the Github repo
==========================
In your repo webhook settings set the webhook as follows:
* Payload URL - The URL for the heroku application you created.
* Content type - Set this to `application/json`
* Set the webhook events to `Send me everything.`

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
