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

Thoughts on supporting more languages
----
Pseudo-compiling the sources of interpreted languages, which means appending
shebang at the start of the sources and `chmod`ing the sources to make them
executable, and then `./a.out`. This should work for most interpreted languages.

For compiled languages, it's even simpler.

I should admit that there are no clear distinction between CLs and ILs (e.g.
Java compiles and interpretes). Maybe I'll fuse the two classes in `_fundamental.py`
in the future.

#### 2014.12.28
I've just ACed "The A + B Problem" in Python and Ruby!!! If only I could gain
access to the server and update with this extension.

However, I do notice that the RF Table method for restricting system calls may
not be practical for Python and Ruby, of which the mechanism of running a
simple program like "A + B" is basically overwhelming.

**TODO** find a method other than RF Table to restrict system calls. Maybe AST?
**MODIFY 2015/3/23** AST may be a lot of work and eventually lead to a dead end.
Something related to runtime environment is mandatory here.

#### 2015.3.23
After **SO MUCH** refactor, I finally managed to have my solution to the
"A + B Problem" accepted in C/C++/Java/Pascal/Clojure/Python2/Python3 via the web
interface.

And of course, I have left future maintainer with interfaces to adding new languages
to WOJ. Instruction will be ready later.

**TODO** Add a tool that automatically determines the RF table for each language.
And I'll try to export a patch and apply it to upstream server.

#### 2015.3.27
A tool named `syscall_recorder` is ready. Check out `syscall_recorder -h` for more
details. This tools utilizes `strace.py` from `python-ptrace` to record all the
syscalls your target calls. An example call to `syscall_recorder` would be

    ./syscall_recorder python3 /home/user/woj/data/ . target1.py target2.py -n 1001
     1002 -l langs/ -f 5 -w read write close

After running this, `syscall_recorder` will record all the syscalls during the
execution of target1.py running 1001 and target2.py running 1002. And a syscall table
will be generated, in which each syscall will be assigned a number which shows how
many times this syscall has been called. If this number exceeds a threshold of 5 (given
by `-f`), it will be changed to -1, which means this syscall can be called infinite
times without triggering the `RF` alarm. Syscalls on white list will automatically
be given -1. `syscall_recorder` will generate a `your_lang_rf.py` according to the
information it has gathered. And users can directly `from your_lang_rf import rf` to
facilitate their security settings.

Contact
----
For anything with regard to enhancements of woj-land, please file an issue.

