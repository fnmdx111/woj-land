Distributed Judging Extension to WOJ
====

This is an extension of supporting distributed judging to WOJ.

One thing notable currently is that the load balancing algorithm is random
selection, which may later be developed to a more advanced probablistic
one.

You can take advantage of multi-tasking to somewhat undergo heavy traffic.
If you have just one machine, you still are able to use this extension,
since you can start multiple instances of slaves on one single machine and
make good use of your multi-core CPU.

Requirements
----

* Python 3 (developed and tested under Python 3.4)
* libzmq 4.1.0 and pyzmq 14.5.0
* woj judge test suite


Howto
----

Firstly, configure `config.py` of initiator, master and heartbeatd
according to your local settings.

Secondly, deploy the judge suite (i.e. `judge_all.exe`, `pygent` and/or
anything locally related) and slave to your slave machines and configure
the `config.py` of slaves accordingly.

Finally, start master, heartbeatd and your slave nodes. Pay attention
to its logging. If nothing funny happens, try posting a judge request and
watch.

