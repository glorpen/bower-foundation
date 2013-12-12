This repository is automatically updated from https://github.com/zurb/bower-foundation

=============
`Foundation`_
=============
.. _Foundation: http://foundation.zurb.com

Foundation is the most advanced responsive front-end framework in the world. You can quickly prototype and build sites or apps that work on any kind of device with Foundation, which includes layout constructs (like a fully responsive grid), elements and best practices.

To get started, check out http://foundation.zurb.com/docs


Installation
============

To get going with Foundation python module you can install it from `PyPi package`_:

.. _PyPi package: https://pypi.python.org/pypi/zurb-foundation

.. sourcecode:: sh

   pip install zurb-foundation

Documentation
=============

Foundation documentation pages are available at http://foundation.zurb.com/docs

Python package
==============

After installation you can use *pkg_resource* module to access assets:

.. sourcecode:: python

   import pkg_resources
   
   as_string = pkg_resources.resource_string("zurb_foundation", "js/vendor/custom.modernizr.js")
   full_path_to_file = pkg_resources.resource_filename("zurb_foundation", "js/vendor/custom.modernizr.js")
   file_like = pkg_resources.resource_stream("zurb_foundation", "js/vendor/custom.modernizr.js")


Package consists of: *js*, compiled *css* and *scss* files.
