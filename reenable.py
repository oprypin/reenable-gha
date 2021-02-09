import collections
import logging
import os

import requests

logging.basicConfig(level=logging.DEBUG)

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ses = requests.Session()
ses.headers['Authorization'] = f'token {GITHUB_TOKEN}'
ses.hooks['response'] = lambda r, *args, **kwargs: r.raise_for_status()

username = ses.get('https://api.github.com/user').json()['login']

results = ses.get('https://api.github.com/search/code', params={
    'q': f'user:{username} path:.github/workflows language:YAML schedule', 'per_page': 100
}).json()['items']

repo_files = collections.defaultdict(list)
for result in results:
    repo_files[result['repository']['url']].append(result['path'])

for repo, files in repo_files.items():
    workflows = ses.get(f'{repo}/actions/workflows').json()['workflows']
    for workflow in workflows:
        if workflow['path'] in files:
            ses.put('{url}/enable'.format_map(workflow))
