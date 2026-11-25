import datetime
from dateutil import relativedelta
import requests
import os
from lxml import etree

# GANTI TANGGAL LAHIR DI BAWAH INI (Format: Tahun, Bulan, Tanggal)
BIRTHDAY = datetime.date(2004, 5, 15)

HEADERS = {'Authorization': 'token ' + os.environ['ACCESS_TOKEN']}
USER_NAME = os.environ.get('USER_NAME', 'XTripsy')


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
        headers=HEADERS
    )
    if request.status_code == 200:
        return request.json()
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
    while True:
        data = simple_request(query, {'login': username, 'cursor': cursor})['data']['user']['repositories']
        repos = data['totalCount']
        for edge in data['edges']:
            stars += edge['node']['stargazers']['totalCount']
        if not data['pageInfo']['hasNextPage']:
            break
        cursor = data['pageInfo']['endCursor']
    return repos, stars


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


def loc_query(username, user_id):
    query = '''
    query ($login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 50, after: $cursor, ownerAffiliations: OWNER, isFork: false) {
                edges {
                    node {
                        name
                        defaultBranchRef {
                            target {
                                ... on Commit {
                                    history(first: 100, author: {id: "%s"}) {
                                        edges {
                                            node {
                                                additions
                                                deletions
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }''' % user_id

    additions = 0
    deletions = 0
    cursor = None
    try:
        while True:
            data = simple_request(query, {'login': username, 'cursor': cursor})['data']['user']['repositories']
            for edge in data['edges']:
                branch = edge['node'].get('defaultBranchRef')
                if branch and branch.get('target') and branch['target'].get('history'):
                    for commit in branch['target']['history']['edges']:
                        additions += commit['node']['additions']
                        deletions += commit['node']['deletions']
            if not data['pageInfo']['hasNextPage']:
                break
            cursor = data['pageInfo']['endCursor']
    except Exception as e:
        print(f"Warning LOC fetch: {e}")

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
    justify_format(root, 'repo_dots', 'repo_data', f"{repos:,} {{Contributed: {contributed:,}}}", 26)
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
    repos, stars = graph_repos_stars(USER_NAME)
    commits = commit_counter(USER_NAME)
    loc = loc_query(USER_NAME, user_id)
    uptime = daily_readme(BIRTHDAY)

    for svg_file in ['dark_mode.svg', 'light_mode.svg']:
        if os.path.exists(svg_file):
            svg_overwrite(svg_file, uptime, repos, contributed, stars, commits, followers, loc)
            print(f"Updated {svg_file}")
