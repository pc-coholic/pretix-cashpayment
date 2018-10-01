Pretix Cash Payment plugin
==========================

.. image:: https://img.shields.io/pypi/v/pretix-cashpayment.svg
   :target: https://pypi.python.org/pypi/pretix-cashpayment

.. image:: https://img.shields.io/badge/translations-POEditor.com-blue.svg
   :target: https://poeditor.com/join/project/5aFqmrdbz3

This is a plugin for `pretix`_.

Upon installation and activiation, you will be able to offer your clients a "Cash Payment"-option. This might be useful if you still want to sell tickets ahead of your event but the time to process payment transactions like SEPA-transfers is too long and/or payment via (credit) card processors is not possible or desired.

In the plugin settings you can set a custom text which will not only be displayed to your customers when selecting the payment method but also after checkout has occured and the payment is pending as well as in the order-confirmation emails that are being sent out.

Please note, that you will have to mark the orders as payed by hand using the pretix backend. You may also - at your own risk - use the `pretix-cashpoint`_ in conjunction with the `de.pccoholic.pretix.cashpoint`_ android app to mark tickets as payed.

Compatibility
-------------
As major versions in pretix tend to also include major changes, compatibility can be difficult to maintain.

In order to make things simpler, the versioning of this plugin is also orienting itself on the versioning of pretix.

On other words: If you are running pretix 1.x, you should only install this plugin in a 1.x-version. The 2.x-version *might* work just fine, but is implementing pretix 2.x-functionality, which might not be available on legacy systems or might even break it.

To install the latest 1.x-version, using ``pip``, please use ``pip install "pretix-cashpayment<2.0"``

Production setup - pip method
-----------------------------

1. Activate - if applicable your pretix `venv`

2. ``pip install pretix-cashpayment``

3. python3 -m pretix migrate

4. python3 -m pretix rebuild

5. Restart your pretix processes: ``systemctl restart pretix-web pretix-worker``


     Note for Docker users:
     There seems to be a problem, where running the ``pip install``-command in your Docker-file will result with a ``No module named 'production_settings'``-message. There are however `two available workarounds`_.

Production setup - installation from git
----------------------------------------

Follow the instructions of the development setup. But instead of ``python setup.py develop`` in the plugin directory, run ``pip install .`` instead. ``python setup.py setup`` will not work.

Development setup
-----------------

1. Make sure that you have a working `pretix development setup`_.

2. Clone this repository, eg to ``local/pretix-cashpayment``.

3. Activate the virtual environment you use for pretix development.

4. Execute ``python setup.py develop`` within this directory to register this application with pretix's plugin registry.

5. Execute ``make`` within this directory to compile translations.

6. Restart your local pretix server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.


License
-------

Copyright 2018 Martin Gross

Released under the terms of the Apache License 2.0


.. _pretix: https://github.com/pretix/pretix
.. _pretix development setup: https://docs.pretix.eu/en/latest/development/setup.html
.. _pretix-cashpoint: https://github.com/pc-coholic/pretix-cashpoint
.. _de.pccoholic.pretix.cashpoint: https://github.com/pc-coholic/de.pccoholic.pretix.cashpoint
.. _two available workarounds: https://github.com/pc-coholic/pretix-cashpayment/issues/5#issuecomment-382447489
