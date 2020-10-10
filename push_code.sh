if [ $(git diff HEAD | wc -l) -gt 30 ]
then
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git config user.name "GitHub Actions"
git status
git commit -a --amend --no-edit || true
git push --force | true
fi
