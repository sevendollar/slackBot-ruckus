#!/usr/local/bin/python3

from slackclient import SlackClient
import time
import re
import os
from ruckus import Ruckus
from getpass import getpass
import bank
import misc
import json

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN') or input('slack bot token: ')
RUCKUS_USER = os.environ.get('RUCKUS_USER') or input('ruckus username: ')
RUCKUS_PASS = os.environ.get('RUCKUS_PASS') or getpass('ruckus password: ')


slack_client = SlackClient(SLACK_BOT_TOKEN)  # instantiate Slack client
starterbot_id = None  # starterbot's user ID in Slack: value is assigned after the bot starts up

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = 'add MAC'
MENTION_REGEX = "^<@(|[WU].+?)>((.|\s)*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # TODO: do something when got bad words.

    # TODO: count how many MACs one have related to.

    # Default response is help text for the user
    default_response = f'''
    im just a baby-bot who r still learning & exploring the world, be nice to me plz...:slightly_smiling_face:\n
    Try *{EXAMPLE_COMMAND}* or *help* for more detail.
    '''
    response = None  # Finds and executes the given command, filling in response
    attachment = None
    greeting = ('Hello',
                'it\'s nice to meet you',
                'it\'s a pleasure to meet you',
                'Hi!',
                'What\'s up?',
                'How\'s it going?',
                'Yo!',
                'What\'s happenin\'?',
                )
    parsed_command = misc.parser(command)

    currency_rate = parsed_command.get('currency_rate')
    currency = parsed_command.get('currency')
    currency_intent = parsed_command.get('currency_intent')

    if True in (bool(currency_rate), bool(currency), bool(currency_intent)):
        mess_around_response = f'sorry dude, dont really know what u what...but good try though.'
        miss_currency_response = 'u missed the currency, try that again!'
        currency = currency or ''
        currency_intent = currency_intent or ''
        if len(currency) > 1 or len(currency_intent) > 1:
            response = mess_around_response
        else:
            currency = currency[0] if currency else None
            currency_intent = currency_intent[0] if currency_intent else None
            r = bank.interest_rate(currency, currency_intent)
            time = bank.interest_rate().get('time')
            response = miss_currency_response if r == 'unknown' else \
                (
                    f'{time}\n\nyou buy: {r[1]}\nyou sell: {r[0]}' if currency_intent is None and currency else \
                        (
                            f'{time}\n\n{r}' if currency_intent and currency else bank.interest_rate_table()
                        )
                )

    elif command in ('jef', 'who made this app?', 'show me the author', 'author'):
        image_jef = 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTA5MjMyMzUwNDheQTJeQWpwZ15BbWU3MDU4NTE3MjQ@._CR95,52,361,361_UX402_UY402._SY201_SX201_AL_.jpg'
        attachment = [{'title': None,
                       'image_url': image_jef}]
        response = ' '

    elif command in ('cat', 'cats'):
        response = ' '
        image_cat = 'https://www.merriam-webster.com/assets/mw/static/newsletter/subscribe-overlay-cat.jpg'
        attachment = [{'title': None,
                       'image_url': image_cat}]

    elif parsed_command.get('bad_words'):
        response = 'language!!!'

    elif command.startswith('add mac'):
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text='Working on it...:slightly_smiling_face:'
        )
        print(parse_user_words(command))
        mac = parse_user_words(command).get('mac')
        r = Ruckus(RUCKUS_USER, RUCKUS_PASS)
        if r.add_mac(mac):
            response = f'successfully added *{mac}*...:tada:'
        else:
            response = 'Oops, MAC existed...:cry:'
        del r
    elif command in ('hi', 'hello', 'how'):
        import random
        response = random.choice(greeting)
    elif command == 'help':
        response = 'gotcha...there\'s not thing i can help with...:grin:'
    else:
        response = default_response
        # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response,
        attachments=attachment or None,
    )


def parse_user_words(words):
    team_name = words.replace('\n', ' ').split(' ')[2]
    team_user = words.replace('\n', ' ').split(' ')[3]
    customer_name = words.replace('\n', ' ').split(' ')[4]
    customer_id = words.replace('\n', ' ').split(' ')[5]
    mac = words.replace('\n', ' ').split(' ')[6]
    new_words = {
        'team_name': team_name,
        'team_user': team_user,
        'customer_name': customer_name,
        'customer_id': customer_id,
        'mac': mac,
    }
    return new_words or None


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
