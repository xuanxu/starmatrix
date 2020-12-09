Edge
====

If you want to play with the latest code present in this repository even if it has not been released yet, you can do it by cloning the repo locally and instructing pip to install it::

    $ git clone https://github.com/xuanxu/starmatrix.git
    $ cd starmatrix
    $ pip install -e .

Testing
-------

You can then run the test suite locally using `pytest`::

    $ pytest -v --cov=starmatrix
