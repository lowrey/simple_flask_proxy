simple_flask_proxy
==================

This is a simple, straight forward proxy done in the Python.  It uses 
the Flask framework to accept requests and responses to and from the 
callee and forwards them with the Requests library.

It is intended to be used by redirecting traffic that to it and supplying
its destination via the header "Forwarding-Address".  Only the host is
required in this field; it will use the path it was call with as part
of the forwarding request.

It has several limitations in its current form.  It currently only 
supports text data in the request and does not support any streaming.
It also will strip out all headers from the response except its mime-
type.

It can be easily extended to add and modify headers, data, and other 
information to any request that passes through it.  

License
---

MIT   
