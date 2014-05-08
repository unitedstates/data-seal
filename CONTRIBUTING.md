# Contributing

* Documentation on how to bootstrap the project -- among other things --
  can be found [in the `/doc` directory](https://github.com/unitedstates/authentication/tree/master/doc).
* Check out [the project wiki](https://github.com/unitedstates/authentication/wiki)
  for some architecture information.
* Bugs and other concerns should be filed in a
  [GitHub issue](https://github.com/unitedstates/authentication/issues)
  so that anyone can help answer it.

## Code style

This project will use a *loose* variation of
[PEP8](http://legacy.python.org/dev/peps/pep-0008/).

Basically:

* Use **4 spaces** to indent. This is a bit old-school, but is highly recommended
  since most other Python projects use four spaces; abiding by this makes it
  easier to copy code in from other projects.
* **No hard restriction on line length**, though 70 to 100 chars is probably good.
* Files should **use UTF-8** and include a `# coding=utf-8` header if they contain
  non-ASCII charcters.
* PEP8 is basically just there for guidance, it is not the law of the land.
  Just make sure you don’t do anything crazy (and if you do, comment your code)
  and leave it generally readable.

If you’re super ambitious, you should try [PyLint](http://www.pylint.org/),
which will check your code for style AND also analyze your code for syntax
errors and bad imports and other things. A good sanity check that goes way
beyond code style.
