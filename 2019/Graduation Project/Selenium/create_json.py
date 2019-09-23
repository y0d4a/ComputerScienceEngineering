import json
from collections import OrderedDict

file_data = OrderedDict()

file_data['user_name'] = 'Haewoong Kwak'
file_data['user_email'] = 'kimsc@koreatech.ac.kr'
file_data['curr_url'] = 'https://ko.wikipedia.org/wiki/%EA%B0%80%EC%83%81%ED%99%94%ED%8F%90'
file_data['prev_url'] = 'https://www.google.com/search?sxsrf=ACYBGNQ-aJ7w60PlhyklEkVcu8b2UJOYSg%3A1569245513830&source=hp&ei=ScmIXfDHMKO0mAXv-ZrIDg&q=%EA%B0%80%EC%83%81%ED%99%94%ED%8F%90&oq=&gs_l=psy-ab.1.7.35i362i39l10.0.0..4415...0.0..0.115.115.0j1......0......gws-wiz.....10.UcK6Mci5BiE'
file_data['paths'] = ['ko.wikipedia.org', '/wiki', '/%EA%B0%80%EC%83%81%ED%99%94%ED%8F%90']
file_data['level'] = 2
file_data['tagged'] = 'Important'
file_data['memo'] = 'Virtual_Currency Wikipedia'
file_data['project_name'] = 'first_project'

with open('5.json', 'w', encoding='utf-8') as make_file:
    json.dump(file_data, make_file, ensure_ascii=False, indent='\t')