# Maintainer's build notes

```
rm -r build dist phronesitron.egg-info 
./phronesitron/ph # test
./phronesitron/paper2txt
git commit 
git push
tox
bumpver
flit build
flit publish

```
gpg sign soon!

## test:
```
pip uninstall openai pyperclip phronesitron pdfminer.six termcolor
python -m pip cache purge

pip install phronesitron
```
