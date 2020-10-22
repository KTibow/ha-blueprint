if [ $(git diff HEAD | wc -l) -gt 30 ]
then
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git config user.name "GitHub Actions"
git pull
git add *.js
git add *.ts
git add *.py
git status
git commit --amend --no-edit || true
git status
git push --force || true
fi
