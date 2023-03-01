# Maintainer's build notes

```
git commit 
git clean -fdx --dry-run
tox
bumpver update --patch
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD

```
gpg sign soon!

## test:
```
pip uninstall -y openai pyperclip phronesitron pdfminer.six termcolor
python -m pip cache purge

poetry build; pip install --force-reinstall dist/*.whl; rehash
```
