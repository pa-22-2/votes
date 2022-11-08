#!/usr/bin/env python3

from dataclasses import dataclass
from tqdm import tqdm
import git
import inquirer
from types import SimpleNamespace
import json
import os


@dataclass
class Voting(SimpleNamespace):
  name: str
  title: str
  votes: dict[str, list[str]]


def main():
  repo = git.Repo('.', search_parent_directories=True)
  os.chdir(repo.working_tree_dir)

  votings = []
  for voting_name in tqdm(os.listdir('data')):
    voting_name = voting_name.removesuffix('.json')
    with open(f'data/{voting_name}.json', 'r') as f:
      votings.append(Voting(name=voting_name, **json.load(f)))

  answer = inquirer.prompt([
    inquirer.Text('name', 'What\'s your name?'),
    inquirer.List('voting', 'What do you want to vote for?', choices=[(v.title, v) for v in votings]),
    inquirer.Checkbox('votes', 'What will you vote for?', choices=lambda answers: list(answers['voting'].votes.keys())),
  ])

  name = answer['name']
  voting = answer['voting']
  votes = answer['votes']

  for vote in votes:
    voting.votes[vote].append(name)

  with open(f'data/{voting.name}.json', 'w') as f:
    raw_voting = vars(voting)
    del raw_voting['name']
    json.dump(raw_voting, f)


if __name__ == '__main__':
  main()
