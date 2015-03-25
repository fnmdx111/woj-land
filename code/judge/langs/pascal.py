from ._fundamental import def_compiled_lang, RFTable

rf = RFTable()
rf.close = -1
rf.execve = 1
rf.exit_group = -1
rf.futex = -1
rf.gettimeofday = -1
rf.ioctl = -1
rf.mmap = -1
rf.mremap = -1
rf.munmap = -1
rf.lseek = -1
rf.read = -1
rf.readlink = -1
rf.rf_sigaction = -1
rf.ugetrlimit = -1
rf.uname = -1
rf.write = -1
rf.writev = -1

def_compiled_lang(id_=4,
                  canonical_name='Pascal',
                  ext='pas',
                  compile_cmd=['fpc', '{source}', '-o{target}',
                               '-Co', '-Cr', '-Ct', '-Ci'],
                  **rf)
