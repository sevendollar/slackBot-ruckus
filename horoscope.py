import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import datetime
from slackclient import SlackClient

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)
day7 = today + datetime.timedelta(days=6)


def luck(star=None, day=today):
    star = star or '0'
    payload = {
        'iAstro': star,
        'iAcDay': day,
    }
    url_base = 'http://astro.click108.com.tw/daily_1.php?'
    url_bind = url_base + urlencode(payload)
    res = requests.get(url_bind)
    soup = BeautifulSoup(res.text, 'lxml')
    today_word = soup.find('div', {'class': 'TODAY_WORD'}).text.strip()
    today_word = f'今日短評：{today_word}'
    today_content = soup.find('div', {'class': 'TODAY_CONTENT'}).text.strip().split('\n')
    star_sign = f'<{today_content[0][2:5]}>'
    stars_part1 = '   '.join([ x.split('：')[0] for x in today_content[1:3] ]).replace('☆', '　').replace('勢', '')
    stars_part2 = '   '.join([ x.split('：')[0] for x in today_content[3:] ]).replace('☆', '　').replace('勢', '')
    analyse1 = f'整體運分析：\n{today_content[1].split("：")[1]}'
    analyse2 = f'愛情運分析：\n{today_content[2].split("：")[1]}'
    analyse3 = f'事業運分析：\n{today_content[3].split("：")[1]}'
    analyse4 = f'財運運分析：\n{today_content[4].split("：")[1]}'
    return f'{star_sign}\n{stars_part1}\n{stars_part2}\n{today_word}\n\n{analyse1}\n\n{analyse2}\n\n{analyse3}\n\n{analyse4}'


if __name__ == '__main__':
    SLACK_TOKEN = ''
    sc = SlackClient(SLACK_TOKEN)

    user_lst = {i.get('name'): {'id': i.get('id')} for i in sc.api_call('users.list').get('members')}
    [user_lst.get(k).update({'dm_id': i.get('id')}) for k, v in user_lst.copy().items() for i in sc.api_call('im.list').get('ims') if v.get('id') == i.get('user')]

    channel_lst = {i.get('name'): {'id': i.get('id')} for i in sc.api_call('channels.list').get('channels')}
    group_lst = {i.get('name'): {'id': i.get('id')} for i in sc.api_call('groups.list').get('groups')}
    [channel_lst.update({k: v}) for k, v in group_lst.items()]

    print(sc.api_call('chat.postMessage',
                      channel=user_lst.get('sevendollar').get('dm_id'),
                      text=f'{luck(1)}').get('ok'))
