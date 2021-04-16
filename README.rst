=======
NetCHOS
=======

NetCHOS = Network, Connectivity and Hierarchically Organized Structures

Description
-----------

`NetCHOS <https://brainets.github.io/netchos/>`_ is a Python toolbox dedicated to network plotting, potentially with interactions, using standard plotting libraries (matplotlib, seaborn or plotly).

Documentation
-------------

NetCHOS documentation is available online at https://brainets.github.io/netchos/

Installation
------------

Run the following command into your terminal to get the latest stable version :

.. code-block:: shell

    pip install -U netchos


You can also install the latest version of the software directly from Github :

.. code-block:: shell

    pip install git+https://github.com/brainets/netchos.git


For developers, you can install it in develop mode with the following commands :

.. code-block:: shell

    git clone https://github.com/brainets/netchos.git
    cd netchos
    python setup.py develop
    # or : pip install -e .

Dependencies
++++++++++++

The main dependencies of Frites are :

* `Numpy <https://numpy.org/>`_
* `Xarray <http://xarray.pydata.org/en/stable/>`_
* `Joblib <https://joblib.readthedocs.io/en/latest/>`_

<!-- In addition to the main dependencies, here's the list of additional packages that you might need :

* `Numba <http://numba.pydata.org/>`_ : speed up the computations of some functions
* `Matplotlib <https://matplotlib.org/>`_, `Seaborn <https://seaborn.pydata.org/>`_ and `Networkx <https://networkx.github.io/>`_ for plotting the examples -->
