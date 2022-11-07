#!/usr/bin/env python3

from dataclasses import dataclass
import json
import os
import sys


@dataclass
class Voting:
  name: str
  title: str
  votes: dict[str, list[str]]


def reversed_dict(d: dict[str, list[str]]) -> dict[str, list[str]]:
  r = {}
  for k, vs in d.items():
    for v in vs:
      if v not in r:
        r[v] = []
      r[v].append(k)
  return r


def render(voting: Voting) -> None:
  print('#', voting.title)
  print()
  votew = max(len(vote) for vote in voting.votes.keys())
  for vote, voters in voting.votes.items():
    try:
      vote = int(vote)
    except ValueError:
      pass
    print(f'- {vote:{votew}}:', ', '.join(voters))
  print()
  print('## Голоса')
  print()
  votes_by_voter = reversed_dict(voting.votes)
  voterw = max(len(voter) + 1 for voter in votes_by_voter.keys())
  for voter, votes in votes_by_voter.items():
    voter += ':'
    print(f'- {voter:{voterw}}', ', '.join(votes))


def render_readme(votings: list[Voting]) -> None:
  print('# Голосования')
  print()
  for voting in votings:
    print(f'- [{voting.title}](votes/{voting.name}.md)')

def main():
  votings = []
  for voting_name in os.listdir('data'):
    voting_name = voting_name.removesuffix('.json')
    source_fname = os.path.join('data', voting_name + '.json')
    target_fname = os.path.join('votes', voting_name + '.md')
    with open(source_fname, 'r') as source:
      voting = Voting(name=voting_name, **json.load(source))
      votings.append(voting)
    with open(target_fname, 'w') as sys.stdout:
      render(voting)
  with open('README.md', 'w') as sys.stdout:
    render_readme(votings)


if __name__ == '__main__':
  main()
