Access tokens
=============

To use this marker, you will need to get an Access Token for your Canvas account, 
or an API key for your specific MarkUs instance. Here's how to get them:

- **Canvas:** Login, then ``Account > Settings > + New Access Token``.

- **MarkUs:** Login to the instance, scroll to the bottom of the page. On newer versions of MarkUs you may need to go to the *Settings* tab.

---

When using the marker for the first time with Canvas, or for the first time for 
the MarkUs instance, you will be prompted for the token on the command line, 
and be given the option to save them locally. The marker creates 
(and subsequently looks for):

- **Canvas:** A file in your home directory, ``~/.canvas.tokens``.
- **MarkUs:** A file in your home directory, ``~/.markus.tokens``.

Each of these files is simply a CSV file with 2 columns, storing a mapping 
between the ``base_url`` of each instance with the corresponding API key. 
For example, your ``.markus.tokens`` file might look something like:

.. code:: 

    https://markus.utsc.utoronto.ca/csca08f19,<APIKEY>
    https://markus.utsc.utoronto.ca/cscb07f19,<APIKEY>