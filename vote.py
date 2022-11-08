#!/usr/bin/env python3

import git
import os
import pick
from tqdm import tqdm

repo = git.Repo('.', search_parent_directories=True)
os.chdir(repo.working_tree_dir)

def git_pbar_hook(pbar, def_msg=None):
  last = [0]

  def hook(op, curr, total=None, message=None):
    if total is not None:
      pbar.total = total
    if message is not None:
      print(message, file=pbar)
    pbar.update(curr - last[0])
    last[0] = curr

  return hook

with tqdm() as pbar:
  p = git_pbar_hook(pbar)
  repo.remotes.origin.pull(progress=p, verbose=True)
