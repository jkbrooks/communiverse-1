import csv
import requests
import pandas as pd
import github

class MessagePuller():
    def __init__(self, repo_name, personal_token, issue_state, date_since = '2020-01-01T00:00:00Z', sort = 'updated'):
        self.repo_name = repo_name
        self.headers = {'Authorization': 'token %s' % personal_token }
        self.params_payload = {'state':issue_state, 'since':date_since, 'sort':sort}
        self.dict_with_output = {'id':[],'state':[],'title':[], 'body':[],'date':[]}
        self.gh = github.Github()

    def get_and_write_issues(self,response):
        r = response

        if r.status_code != 200:
            raise Exception(r.status_code, r.json())
        
        for issue in r.json():
            if 'pull_request' not in issue:
                listlabels = []

                for label in issue['labels']:
                    listlabels.append(label['name'])
                truncatebody = ''

                if issue['body']:
                    truncatebody = issue['body'][:10000]

                self.dict_with_output['id'].append(issue['number'])
                self.dict_with_output['state'].append(issue['state'])
                self.dict_with_output['title'].append(issue['title'])
                self.dict_with_output['body'].append(truncatebody)
                self.dict_with_output['date'].append(issue['created_at'])
                # csvout.writerow([issue['number'], issue['state'].encode('ascii', 'ignore'), issue['title'].encode('ascii', 'ignore'), truncatebody.encode('ascii', 'ignore'), ','.join(listlabels) , issue['created_at'], issue['closed_at']])

    def process_repo(self):
        issues_for_repo_url = 'https://api.github.com/repos/%s/issues' % self.repo_name
        response = requests.get(issues_for_repo_url, params = self.params_payload, headers = self.headers)

        print(f'Repo in process: {self.repo_name}')

        check = True
        csvfile = 'test-file.csv'

        # csvout = csv.writer(open(csvfile, 'w'), delimiter=',', quotechar='"')
        # csvout.writerow(['id', 'State' ,'Title', 'Body', 'Labels', 'Created At', 'Closed At'])
        self.get_and_write_issues(response)

        if 'Link' in response.headers:
            while check == True:
                # Create overview regarding the different Links, usually previous, first, last and next
                data = {}
                for links in response.headers['Link'].split(","):
                    raw = links.split(";")
                    data[raw[1][6:6+4]] = raw[0].strip()

                if "next" in data:
                    newlink = data["next"][1:-1]
                    response = requests.get(newlink, headers=self.headers)
                    print("Now processing page: " + newlink)
                    self.get_and_write_issues(response)
                    if data["next"] == data["last"]:
                        check = False
                        print("Done with Repository: " + self.repo_name)
                else:
                    check = False
                    print("Done with Repository: " + self.repo_name)
        
        output_df = pd.DataFrame(data = self.dict_with_output)
        output_df.to_csv(f'{self.repo_name}.csv')

    def get_comments(self, issue_id):
        repo = self.gh.get_repo(self.repo_name)

        issues = repo.get_issues()
        for issue in issues:
            issue_dict = {}
            if issue.number == issue_id:
                issue_dict['url'] = issue.url
                issue_dict['title'] = issue.title
                issue_dict['comments'] = [comment.body for comment in issue.get_comments()]
                break

        return issue_dict


        

#testing 
# MP = MessagePuller('UKPLab/EasyNMT', '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', 'open')

# MP.get_comments(95)



