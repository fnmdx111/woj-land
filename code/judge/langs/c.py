from ._fundamental import def_compiled_lang, RFTable
import platform

rf = RFTable()
rf.brk                   = -1
rf.close                 = -1
rf.execve                = 1
rf.exit_group            = -1
rf.futex                 = -1
rf.gettimeofday          = -1
rf.mremap                = -1
rf.mprotect              = -1
rf.munmap                = -1
rf.lseek                 = -1
rf.read                  = -1
rf.set_thread_area       = -1
rf.uname                 = -1
rf.write                 = -1
rf.writev                = -1
rf.readlink              = -1

if platform.uname().machine == 'x86_64':
    rf.arch_prctl        = -1
    rf.mmap              = -1
    rf.fstat             = -1
else:   
    rf.access            = -1
    rf.mmap2             = -1
    rf.fstat64           = -1

def_compiled_lang(id_=1,
                  canonical_name='C',
                  suffix='c',
                  code_name='c',
                  compile_cmd=['gcc', '-o' '{target}',
                               '{source}', '-static', '-w',
                               '-lm', '-std=c99', '-O2', '-DOJ'],
                  **rf)
