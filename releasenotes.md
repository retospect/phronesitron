# Maintainer's build notes

```
rm -r build dist phronesitron.egg-info 
./phronesitron/ph # test
./phronesitron/paper2txt
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
pip uninstall openai pyperclip phronesitron pdfminer.six
python -m pip cache purge

pip install phronesitron
```
