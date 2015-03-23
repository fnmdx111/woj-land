from ._fundamental import def_interpreted_lang, RFTable
from .c import rf

rf.clone = -1
rf.dup = -1
rf.execve = 6
rf.fcntl = -1
rf.getcwd = -1
rf.getdents = -1
rf.geteuid = -1
rf.getegid = -1
rf.getgid = -1
rf.getrlimit = -1
rf.getrusage = -1
rf.getuid = -1
rf.ioctl = -1
rf.lstat = -1
rf.open = -1
rf.openat = -1
rf.stat = -1
rf.pipe = -1
rf.rt_sigaction = -1
rf.rt_sigprocmask = -1
rf.sched_getaffinity = -1
rf.sched_setaffinity = -1
rf.set_robust_list = -1
rf.set_tid_address = -1
rf.sigaltstack = -1

def_interpreted_lang(id_=5,
                     canonical_name='Python2',
                     suffix='py',
                     memory_limit_multiplier=2,
                     time_limit_multiplier=2,
                     **rf)
