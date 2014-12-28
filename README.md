woj-land
========

This is a fork of [woj-land on Google Code](https://code.google.com/p/woj-land ),
of which the creator and maintainer is [felix021](http://www.felix021.com/blog/ ).

Objectives
----
Enhancements to `woj-land` are planned.

Recently planned:
* Supports for interpreted languages (firstly, Python2, Python3 and Ruby)
* Supports for other languages requested (e.g. Scala, Clojure and Brainf**k)
* Distributed judging

Changes currently not in consideration:
* web (PHP IS THE BEST LANGUAGE IN THE WORLD!!!)


Thoughts on distributed judging
----
Replace `judge-all.exe` with a Python script which is in charge of distributing
judge tasks to `judge-all.exe` processes on slave machines to minimize changes
that have to be made.

Thoughts on supporting interpreted languages
----
Pseudo-compiling the sources, which means that appending shebang at the start
of the sources and `chmod`ing the sources to make them executable, and then
`./a.out`. This should work for most interpreted languages. (LINUX DAFA HAO)

#### 2014.12.28
I've just ACed "The A + B Problem" in Python and Ruby!!! If only I could gain
access to the server and update with this extension.

However, I do notice that the RF Table method for restricting system calls may
not be practical for Python and Ruby, of which the mechanism of running a
simple program like "A + B" is basically overwhelming.

**TODO** find a method other than RF Table to restrict system calls. Maybe AST?

Contact
----
For anything with regard to enhancements of woj-land, please file an issue.

