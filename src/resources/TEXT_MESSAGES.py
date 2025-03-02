HELLO_MESSAGE = """
*🍀 ツ  Hi\\! This is the tech support bot\\. 🍀*

_If you have found bugs and errors in our programs\\, or you have suggestions for the development of the project\\, you can send information to our team using the bot\\._

*✅ Select the desired item ✅\\:*
"""

IDEA_TEXT = """
💫 *Now you can write your idea or suggestion for our team\\.*\n\n_Please indicate at the beginning the project to which your proposal relates\\._
"""

BUG_TEXT = """
🍁 *Now specify what error you encountered\\.*\n\n_If necessary\\, you can attach screenshot or log of the error\\.\n\nOur team will fix this error if possible and contact you if necessary\\._
"""

DONE_TEXT = """
🍀 _Your request has been successfully sent to the team and will be fixed soon\\. If we have any questions\\, you will be contacted by our administration \\(\\@Night3098\\) When your issue is fixed\\, you will be notified\\. The ticket will be automatically closed_ 🍀\\.
"""

DEVS_TEXT = """
💬 *Contacts of main developer*\n

"""

OUR_PRODUCTS_TEXT = """
"""

SUPPORT_TEXT = """
🏦 You can support our project through TON 🏦

`UQCF-sPDO0QqkNtvy5CKSvYWEsZS6l7vzaytV36oYM0SNhKt`

"""

INCORRECT_INPUT_FORMAT_ERROR = "Incorrect input format"

HELP_MESSAGE = """
🛠️ *This is a brief documentation on how to use the TechSupportBot* 🛠️

⬢ *ADMIN COMMANDS* ⬢

🟢 _Set ticket status \\(user will be notified\\)_
🚀 `\\/set_ticket_status \\| ticket id \\| ticket category \\| ticket status`

🟢 _View the category of a certain ticket_
🚀 `\\/get_ticket_status \\| ticket id \\| ticket category`

🟢 _Send notification to user_
🚀 `\\/admin_answer \\| user id \\(can be taken from the database\\) \\| message for user`

🟢 _Get all tickets from the database_
🚀 `\\/get_all_tickets`

🟢 _Get DB file_
🚀 `\\/get_db`

"""
