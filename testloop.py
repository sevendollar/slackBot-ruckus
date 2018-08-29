from wifidb import  InsertData
word =[]
for Z in range(11, 20):
    new_words = {
            'team_name':'小熊隊',
            'team_user': '陳小花',
            'customer_name':'王小明',
            'customer_id':'L123456789',
            'mac':(f'ff:ff:cc:bb:aa:{Z}'),
        }
    word.append(new_words)

for new_word in word:
    print(new_word)
    # InsertData(new_word)
