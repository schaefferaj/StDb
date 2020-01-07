Dump Database to .csv
=====================

Program ``dump_stdb.py``
------------------------

Description
-----------
Program to dump a Station Database into ``.csv`` format. If an output file is 
specified, file is dumped there (with ``.csv`` extension). 
Otherwise output is directed to standard output.

This program is useful when you make edits to an existing ``.pkl`` database
merge two databases, or append a new station to a database, without 
automatically creating a corresponding ``.csv`` file.

Usage
-----

.. code-block::

    $ dump_stdb.py -h
    Usage: dump_stdb.py [options] <station pickle file>

    Program to dump the contents of a station database (.pkl) as csv. By default
    the output is directed to standard out. If a filename is optionally included,
    then the contents are also dumped to file.

    Options:
      -h, --help            show this help message and exit
      --keys=KEYS           Specify a comma separated list of keys to dump. Any
                            key not specified by this search is not included in
                            the output.
      -O OFILE, --output-file=OFILE
                            Specify an output file name for the dumped csv format
                            data. If no .csv extenion is included, one is added.
      -a, --ascii           Specify to write ascii Pickle files instead of binary.
                            Ascii are larger file size, but more likely to be
                            system independent.

Example
-------

In the example in :ref:`merge`, the database ``merged_list.pkl`` is not automatically
saved in ``.csv`` format:

.. code-block::

    $ ls -l merged_list.*
    -rw-r--r--  1 username  staff  2038  3 Oct 10:44 merged_list.pkl

You can save it as ``.csv`` by executing:

.. code-block::

    $ dump_stdb.py merged_list.pkl -O merged_list.csv

.. code-block::

    $ ls -l merged_list.*
    -rw-r--r--  1 username  staff   403  4 Oct 11:51 merged_list.csv
    -rw-r--r--  1 username  staff  2038  3 Oct 10:44 merged_list.pkl
