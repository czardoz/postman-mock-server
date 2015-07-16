Postman Mock Server
===================

Beta is down but you need to test your client? Use this! PostMocker
will take a `Postman Collection file <https://www.getpostman.com/docs/collections>`_ where the responses are saved, and serve
those up at the appropriate routes!

Installation
------------

You can install PostMocker using pip:

.. code-block::

    $ pip install git+https://github.com/czardoz/postmocker

Usage
-----

Locate your collection file, and let PostMocker do its job:

.. code-block::

    $ postmocker -c /path/to/collection/file.json
    
Disclaimer
----------

This is beta software. Some things might break, and some things are not 
implemented at all.

License
-------

Released under the MIT license.
