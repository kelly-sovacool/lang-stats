#!/Users/kelly/miniconda3/envs/lang-stats/bin/python
import collections
from github import Github
import os
import plotly
import yaml


class LangStat:
    def __init__(self, description, count_type, name):
        self.description = description
        self.count_type = count_type
        self.filename = f'figures/language_{name}.svg'
        self.counter = collections.Counter()

    def __repr__(self):
        return f"{self.__class__}({self.__dict__})"

    def add(self, key, value):
        self.counter[key] += value

    def update(self, iterable):
        self.counter.update(iterable)

    def make_plot(self):
        tuples = self.counter.most_common()
        x = [lang[0] for lang in tuples]
        y = [lang[1] for lang in tuples]
        figure = plotly.graph_objs.Figure(data=[plotly.graph_objs.Bar(x=x, y=y, text=y, textposition='auto')],
                                          layout=plotly.graph_objs.Layout(title=self.description,
                                                                          xaxis=dict(title='language'),
                                                                          yaxis=dict(title=self.count_type)))
        plotly.io.write_image(figure, self.filename)


def get_language_data(github):
    language_data = {'all_bytes': LangStat("My languages by bytes of code", 'bytes of code', 'all_bytes'),
                     'all_repos': LangStat('My languages by presence in repositories', '# of repos', 'all_repos'),
                     'top_bytes': LangStat("Top repo languages by bytes of code", 'bytes of code', 'top_bytes'),
                     'top_repos': LangStat("Top languages by repositories", '# of repos', 'top_repos')}
    with open('results/repos.txt', 'w') as outfile:
        user = github.get_user(github.get_user().login)
        for repo in github.get_user().get_repos():
            is_owner = repo.owner == user
            is_contributor = user in repo.get_contributors()
            # only include contributing repos
            if is_owner or is_contributor:
                outfile.write(f"{repo.owner.login}/{repo.name}\n")
                languages = repo.get_languages()  # excludes vendored languages from the repo's .gitattributes
                if languages:
                    for lang, bytes_count in languages.items():
                        language_data['all_bytes'].add(lang, bytes_count)
                    language_data['all_repos'].update(languages.keys())
                    top_language = max(languages, key=lambda k: languages[k])
                    language_data['top_repos'].add(top_language, 1)
                    language_data['top_bytes'].add(top_language, languages[top_language])
    return language_data


def main():
    for dir in ('figures', 'results'):
        if not os.path.exists(dir):
            os.mkdir(dir)
    credentials = yaml.load(open('credentials.yaml'), Loader=yaml.Loader)
    github = Github(credentials['login'], credentials['password'])
    language_data = get_language_data(github)
    for stats in language_data.values():
        stats.make_plot()



if __name__ == "__main__":
    main()
