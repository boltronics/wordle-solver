Wordle Solver
=============

This program helps you solve `Wordle`_ puzzles.

.. _`Wordle`: https://www.powerlanguage.co.uk/wordle/


How to use
----------

Usage example:

.. code-block:: console

 $ ./solver.py -1 r -5 l -a udiceny -s _o_a_
 === 2 ===
 lobar
 molar
 polar
 solar
 volar
 $


Installation
------------

Install Python 3.8+, and the WordNet dictionary. Other dictionaries
should also work, but you will need to edit the location of the file
in `solver.py`.

Here are a couple of examples:

Arch Linux (from AUR):

.. code-block:: console

    $ pikaur -S dict-wn

Debian GNU/Linux:

.. code-block:: console

    $ apt install dict-wn

The end result is that you shoud have `wn.index` installed under
`/usr/share/dictd/`.

Finally, you can just copy this script somewhere into your path and
give it executable permissions. Alternatively just run:

.. code-block:: console

   $ python3 solver.py
