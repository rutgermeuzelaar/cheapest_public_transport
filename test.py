test_dict = {'kaas': [], 'bier': ['what']}
test_list = ['jo', 'what']

for key, value in test_dict.items():
    if None in value:
        print('yes')
    if 'what' in value:
        print('s')