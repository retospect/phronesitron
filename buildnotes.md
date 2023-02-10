# Maintainer's build notes

```
git commit 
git push
python setup.py sdist bdist_wheel
twine upload dist/*
git tag 0.0.x
git push origin 0.0.x
# Edit setup to inc rev 
```
gpg sign soon!

## test:
```
pip uninstall openai pyperclip phronesitron
pip uninstall phronesitron
python -m pip cache purge

pip install phronesitron
```
