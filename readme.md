## README

This code is a Python script that utilizes the `telebot` library to create a Telegram bot. The bot performs various functions related to managing users in Telegram groups.

### Functions

1. `remove_user(gid, user)`: This function removes a user from a group. It takes the group ID (`gid`) and the user object (`user`) as parameters. It updates the status of the user in the corresponding worksheet to 'inactive'.

2. `welcome_user(gid, user)`: This function sends a welcome message to a new user in a group. It takes the group ID (`gid`) and the user object (`user`) as parameters. It sends a photo and a caption to the group.

3. `add_user(gid, user)`: This function adds a user to a group. It takes the group ID (`gid`) and the user object (`user`) as parameters. It updates the status of the user in the corresponding worksheet to 'active'.

4. `job()`: This function is a scheduled job that runs every day at 18:40. It performs actions based on the status of users in different groups. If a user is 'inactive', it bans the user from the group and logs the user. If a user is 'active', it unbans the user from the group and removes the user from the log.

5. `update_groups(gid, sid)`: This function adds a new group to the list. It takes the group ID (`gid`) and the sheet ID (`sid`) as parameters. It updates the `list.csv` file with the new group information.

6. `remove_group(gid)`: This function removes a group from the list. It takes the group ID (`gid`) as a parameter. It removes the group from the `list.csv` file.

7. `get_worksheet(sheet_id)`: This function retrieves a worksheet based on the sheet ID. It takes the sheet ID (`sheet_id`) as a parameter and returns the corresponding worksheet.

### Usage

To use this script, you need to have the following:

- Python installed on your system
- The necessary libraries (`telebot`, `schedule`, `csv`, `pygsheets`)
- A Telegram bot token
- A Google Sheets API service account file (`client.json`)
- A `list.csv` file to store the group information

You can run the script by executing the `main.py` file. Make sure to update the necessary variables such as the bot token, sheet ID, admin ID, and admin IDs list.

The script will run the Telegram bot and perform the defined functions based on user interactions and scheduled jobs.

Please refer to the code comments for more detailed explanations of each function and its usage.