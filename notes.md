# Development Notes

## The tale of git and remote logging
git cannot retrieve remote logs natively.
Procedure for getting remote logs without a checkout is thus:

1. `mkdir reponame && cd reponame`
2. `git init && git remote add origin [repo_url]`
3. `git fetch`
4. `git log origin/master`