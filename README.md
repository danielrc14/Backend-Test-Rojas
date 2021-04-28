## cornershop-backend-test

### Running the development environment

* `make up`
* `dev up`

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`

### Hostnames for accessing the service directly

* Local: http://127.0.0.1:8000

### Configuration needed

* This project needs a user with the permission `'menus.add_menu'`, this user would correspond to "Nora" in the instructions. Only users with this permissions would be able to access the views of the `menus` app. To add this permission to a user, do the following:

```python
# Create and assign the permission
group = Group.objects.create(name='Admin Group') # Name doesn't matter
permission = Permission.objects.get(codename='add_menu')
group.permissions.add(permission)

# Assign the group to the desired user
user.groups.add(group)
```

* This project also needs to add the Slack oauth token of the Slack app to the local environment, in the `SLACK_SDK_OAUTH_TOKEN` variable. To create a Slack app and get the token, see https://github.com/slackapi/python-slack-sdk/blob/main/tutorial/01-creating-the-slack-app.md

### Project overview

This project has two Django apps, `menus` and `users`.

* The `menus` app has two models, `Menu` and `MenuOption`, that correspond to a menu for a date and it's meal options, respectively. This app also contains the views responsible for the listing, creation and edition of menus and options, as well as a view to list the user's selections for today's menu, and a view to send today's menu to all users via Slack.

* The `users` app has two models: `User`, a custom user model that replaces the default Django model, and adds additional fields (the user's Slack username and a uuid for the link sent to Slack); and `MenuOptionSelection`, a model that represents a user's selection for a certain menu. This app also contains the view where the user can select an option for today's menu. In addition, this app contains the Slack client, responsible of sending messages to users in Slack.

### Assumptions and limitations in the web app's flow

* Users are only allowed to select an option for today's menu, not for other dates.

* The menu's date and it's options have to be created and edited separately due to frontend limitations.

* Nora can only see the selectios for today's menu, not for other dates.

* There's no distinction between employees and other users, so the notification of today's menu is sent to every user with a `slack_username` configured.

* The slack integration wasn't tested, mainly because testing both Slack and Celery adds additional complexity.
