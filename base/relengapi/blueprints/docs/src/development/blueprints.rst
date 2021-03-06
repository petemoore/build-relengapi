Writing a Blueprint
===================

If your blueprint will be meaty enough to deserve its own project, repo, and so forth, then start that now.
Otherwise, if it's just a small thing, add it to the relengapi project in a top-level directory.
Note that Releng Best Practices call for many well-delineated projects, so err on the former side.

Add a ``setup.py`` similar to that in ``docs/``.
Name the package with a ``relengapi-`` prefix, so it's easy to find.
The ``install_requires`` parameter should name both ``Flask`` and ``relengapi``, as well as any other dependencies.
The ``namespace_packages`` line allows multiple packages to share the same Python path::

    namespace_packages=['relengapi', 'relengapi.blueprints'],

Finally, include an entry point so that the base can find the blueprint::

    entry_points={
        "relengapi_blueprints": [
            'mypackage = relengapi.blueprints.mypackage:bp',
        ],
    },

The ``relengapi.blueprints.mypackage:bp`` in the above is an import path leading to the Blueprint object.

Now, create the directory structure

.. code-block:: none

    relengapi/__init__.py
    relengapi/blueprints/__init__.py
    relengapi/blueprints/mypackage/__init__.py

The first two of the ``__init__.py`` files must have *only* the following contents::

    __import__('pkg_resources').declare_namespace(__name__)

In the third, create your Blueprint::

    from flask import Blueprint, jsonify
    bp = Blueprint('docs', __name__)
    @bp.route('/some/path')
    def root():
        return jsonify("HELLO")

The ``root`` function in this example would be available at ``/mypackage/some/path``.  

