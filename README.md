<img src="docs/.static/logo-wide.png" alt="Logo" width="1000" />

_Basic Recipes for Annotations and Modeling_

[![Version][version-badge]][version-badge]
[![Pipeline][pipeline-badge]][pipeline-badge]
[![Coverage][coverage-badge]][coverage-report]

Brambox is a toolbox that contains unified tools for converting image data annotation sets,
computing statistics and more.  
It's main use is for object detection networks.


## Installing
```bash
# For usage only
pip install -r requirements.txt

# For development
pip install -r develop.txt
```
> This project is python 3.6 and higher so on some systems you might want to use 'pip3.6' instead of 'pip'


## Using
The toolbox contains both library packages and scripts.
If you installed brambox you can just run brambox scripts from anywhere on the commandline.
For more about their usage, run `some_brambox_script.py --help`.  
If you installed brambox you can also import brambox packages in your own python program with:
```python
import brambox
```
For more in-depth guides and the API documentation [click here][doc-url].


## Contributing
See [the contribution guidelines](CONTRIBUTING.md)

[version-badge]: https://img.shields.io/badge/version-1.0.0-blue.svg
[pipeline-badge]: https://gitlab.com/EAVISE/brambox/badges/master/pipeline.svg
[coverage-badge]: https://codecov.io/gl/EAVISE/brambox/branch/master/graph/badge.svg
[coverage-report]: https://codecov.io/gl/EAVISE/brambox/branch/master
[doc-url]: https://eavise.gitlab.io/brambox
