# Maintainer's build notes

```
git commit 
git push
python setup.py sdist bdist_wheel
twine upload dist/*
```
gpg sign soon!

## test:
```
pip uninstall openai pyperclip phronesitron
pip uninstall phronesitron
python -m pip cache purge

pip install phronesitron
```
