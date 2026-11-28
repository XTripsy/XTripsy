import datetime
from dateutil import relativedelta
import requests
import os
from lxml import etree

BIRTHDAY = datetime.date(2004, 8, 1)

HEADERS = {'Authorization': 'token ' + os.environ['ACCESS_TOKEN']}
USER_NAME = os.environ.get('USER_NAME', 'XTripsy')

# Filter ekstensi kode murni & folder library/auto-generated yang diabaikan
VALID_EXTENSIONS = (
    '.cpp', '.h', '.hpp', '.c', '.cs', '.gd',
    '.py', '.js', '.hlsl', '.glsl', '.vert', '.frag'
)
IGNORED_PATHS = (
    'libraries/', 'thirdparty/', 'third_party/', 'plugins/',
    'intermediate/', 'library/', 'binaries/', 'saved/',
    'builds/', 'build/', 'bin/', 'obj/', 'packages/',
    'glad.c', 'imgui', 'nlohmann', 'stb_'
)
IGNORE_REPOS = set()  # Tambahkan nama repo jika ada repo tertentu yang ingin dilewati seluruhnya


def is_valid_code_file(filepath):
    path_lower = filepath.lower()
    if not path_lower.endswith(VALID_EXTENSIONS):
        return False
    return not any(ignored in path_lower for ignored in IGNORED_PATHS)


def daily_readme(birthday):
    diff = relativedelta.relativedelta(datetime.date.today(), birthday)
    return '{} {}, {} {}, {} {}'.format(
        diff.years, 'year' + ('s' if diff.years != 1 else ''),
        diff.months, 'month' + ('s' if diff.months != 1 else ''),
        diff.days, 'day' + ('s' if diff.days != 1 else '')
    )


def simple_request(query, variables):
    request = requests.post(
        'https://api.github.com/graphql',
        json={'query': query, 'variables': variables},
        headers=HEADERS,
        timeout=30
    )
    if request.status_code == 200:
        data = request.json()
        if 'errors' in data:
            raise Exception(f"GraphQL errors: {data['errors']}")
        return data
    raise Exception(f"Query failed with status {request.status_code}: {request.text}")


def user_getter(username):
    query = '''
    query($login: String!) {
        user(login: $login) {
            id
            createdAt
            followers {
                totalCount
            }
            repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
                totalCount
            }
        }
    }'''
    res = simple_request(query, {'login': username})['data']['user']
    return (
        res['id'],
        res['createdAt'],
        res['followers']['totalCount'],
        res['repositoriesContributedTo']['totalCount']
    )


def graph_repos_stars(username):
    query = '''
    query ($login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, isFork: false) {
                totalCount
                edges {
                    node {
                        name
                        stargazers {
                            totalCount
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }'''
    cursor = None
    stars = 0
    repos = 0
    repo_names = []
    while True:
        data = simple_request(query, {'login': username, 'cursor': cursor})['data']['user']['repositories']
        repos = data['totalCount']
        for edge in data['edges']:
            repo_names.append(edge['node']['name'])
            stars += edge['node']['stargazers']['totalCount']
        if not data['pageInfo']['hasNextPage']:
            break
        cursor = data['pageInfo']['endCursor']
    return repos, stars, repo_names


def commit_counter(username):
    years_query = '''
    query($login: String!) {
        user(login: $login) {
            contributionsCollection {
                contributionYears
            }
        }
    }'''
    years = simple_request(years_query, {'login': username})['data']['user']['contributionsCollection']['contributionYears']
    total_commits = 0
    for year in years:
        query = '''
        query($login: String!, $from: DateTime!, $to: DateTime!) {
            user(login: $login) {
                contributionsCollection(from: $from, to: $to) {
                    totalCommitContributions
                    restrictedContributionsCount
                }
            }
        }'''
        variables = {
            'login': username,
            'from': f'{year}-01-01T00:00:00Z',
            'to': f'{year}-12-31T23:59:59Z'
        }
        cc = simple_request(query, variables)['data']['user']['contributionsCollection']
        total_commits += cc['totalCommitContributions'] + cc['restrictedContributionsCount']
    return total_commits


def loc_query(username, repo_names):
    sha_query = '''
    query ($login: String!, $name: String!, $cursor: String) {
        repository(owner: $login, name: $name) {
            defaultBranchRef {
                target {
                    ... on Commit {
                        history(first: 100, after: $cursor) {
                            nodes {
                                oid
                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }
            }
        }
    }'''

    additions = 0
    deletions = 0

    session = requests.Session()
    session.headers.update(HEADERS)

    for repo_name in repo_names:
        if repo_name in IGNORE_REPOS:
            continue

        cursor = None
        commit_shas = []
        try:
            while True:
                res = simple_request(sha_query, {'login': username, 'name': repo_name, 'cursor': cursor})
                branch = res['data']['repository'].get('defaultBranchRef')
                if not branch or not branch.get('target') or not branch['target'].get('history'):
                    break
                history = branch['target']['history']
                for node in history['nodes']:
                    commit_shas.append(node['oid'])
                if not history['pageInfo']['hasNextPage']:
                    break
                cursor = history['pageInfo']['endCursor']

            for sha in commit_shas:
                url = f"https://api.github.com/repos/{username}/{repo_name}/commits/{sha}"
                resp = session.get(url, timeout=30)
                if resp.status_code != 200:
                    continue
                for f in resp.json().get('files', []):
                    if is_valid_code_file(f.get('filename', '')):
                        additions += f.get('additions', 0)
                        deletions += f.get('deletions', 0)

        except Exception as e:
            print(f"Skipping {repo_name} due to error: {e}")
            continue

    return additions, deletions, additions - deletions


def find_and_replace(root, element_id, new_text):
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        element.text = new_text


def justify_format(root, dots_id, val_id, new_text, width):
    new_text = str(new_text)
    find_and_replace(root, val_id, new_text)
    dots_count = max(2, width - len(new_text) - 2)
    find_and_replace(root, dots_id, ' ' + ('.' * dots_count) + ' ')


def svg_overwrite(filename, uptime, repos, contributed, stars, commits, followers, loc):
    tree = etree.parse(filename)
    root = tree.getroot()

    justify_format(root, 'uptime_dots', 'uptime', uptime, 51)
    justify_format(root, 'repo_dots', 'repo_data', f"{repos:,} {{Contributed: {contributed:,}}}", 27)
    justify_format(root, 'star_dots', 'star_data', f"{stars:,}", 17)
    justify_format(root, 'commit_dots', 'commit_data', f"{commits:,}", 22)
    justify_format(root, 'follower_dots', 'follower_data', f"{followers:,}", 15)

    loc_total_str = f"{loc[2]:,}"
    loc_add_str = f"{loc[0]:,}++"
    loc_del_str = f"{loc[1]:,}--"
    find_and_replace(root, 'loc_data', loc_total_str)
    find_and_replace(root, 'loc_add', loc_add_str)
    find_and_replace(root, 'loc_del', loc_del_str)

    combined_len = len(loc_total_str) + len(loc_add_str) + len(loc_del_str) + 6
    dots_count = max(2, 34 - combined_len - 2)
    find_and_replace(root, 'loc_dots', ' ' + ('.' * dots_count) + ' ')

    tree.write(filename, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    user_id, _, followers, contributed = user_getter(USER_NAME)
    repos, stars, repo_names = graph_repos_stars(USER_NAME)
    commits = commit_counter(USER_NAME)
    loc = loc_query(USER_NAME, repo_names)
    uptime = daily_readme(BIRTHDAY)

    for svg_file in ['dark_mode.svg', 'light_mode.svg']:
        if os.path.exists(svg_file):
            svg_overwrite(svg_file, uptime, repos, contributed, stars, commits, followers, loc)
            print(f"Updated {svg_file} with LOC: {loc}")
