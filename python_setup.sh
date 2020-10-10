echo "::group::Hassfest setup"
mkdir hassfest-temp
cd hassfest-temp
git init
git remote add -f origin https://github.com/home-assistant/actions.git
git config core.sparseCheckout true
echo 'hassfest' >> .git/info/sparse-checkout
git pull origin master
cd ..
ls
mv hassfest-temp/hassfest .
rm -r hassfest-temp
docker build -t hassfest -f hassfest/Dockerfile hassfest
echo "::endgroup::"
# Flake8
echo "::group::Flake8 setup"
python -m pip install --upgrade pip wheel
python -m pip install --upgrade flake8 wemake-python-styleguide
echo "::endgroup::"
# Formatting
echo "::group::Format setup"
python -m pip install --upgrade black
echo "::endgroup::"
