# This module defines various classes for multiple language support.

import os
import subprocess
import io
import sys


def _lp(*p):
    return os.path.join(os.path.dirname(__file__), *p)

_TMP_FILE_PATH = _lp('conf', '.tmp', '.tmp.c')


class RFTable(dict):
    def __init__(self):
        super(RFTable, self).__init__()

    def __setattr__(self, attr, value):
        if not attr.startswith('SYS_'):
            attr = 'SYS_%s' % attr

        self[attr] = value

    def export(self, stream=None):
        if not stream:
            stream = io.StringIO()
            ret = True
        else:
            ret = False

        for k, v in self.items():
            stream.write('%s %s\n' % (k, v))

        if ret:
            return stream.getvalue() # Ugly method name.


class Language:

    """Lang code is a constant of unsigned integer designed as following
       to represent specific settings for a unique language.

       bit ... | 15 14 13 12 | 11 10 09 08 | 07 06 05 04 | 03 02 01 00
                 UU UU UU UU   UU UU UU UU   UU UU UU UU   UU UU CR RF

       CR: chroot Before Execution
       RF: Restricted by RF Table
    """

    MASK_CHROOT_BEFORE_EXECUTION = 0x2
    MASK_RESTRICTED_BY_RF_TABLE = 0x1

    def __init__(self, id_, canonical_name, suffix, code_name=None,
                 default_src_filename='',
                 default_exec_filename='',
                 memory_limit_multiplier=1,
                 time_limit_multiplier=1,
                 is_interpreted_language=False,
                 is_compiled_language=False,
                 exec_cmd=None,
                 chroot_enabled=True,
                 rf_enabled=True):
        self.id = id_

        self.chroot_enabled = chroot_enabled

        self.rf_enabled = rf_enabled
        self.rf = RFTable()

        self.canonical_name = canonical_name
        self.suffix = suffix
        self.code_name = code_name or canonical_name
        self.code_name = self.code_name.lower()
        self.default_src_filename = default_src_filename
        self.default_exec_filename = default_exec_filename

        self.is_interpreted_language = is_interpreted_language
        self.is_compiled_language = is_compiled_language

        self.memory_limit_multiplier = memory_limit_multiplier
        self.time_limit_multiplier = time_limit_multiplier

        self.exec_cmd = exec_cmd or []

        self.code = 0

        if rf_enabled:
            self.code |= self.MASK_RESTRICTED_BY_RF_TABLE & 0xffffffff
        if chroot_enabled:
            self.code |= self.MASK_CHROOT_BEFORE_EXECUTION & 0xffffffff

    def do(self, source, target, temp_dir_path):
        pass

    def exec_(self, source, target, temp_dir_path):
        if self.exec_cmd:
            _ = self.exec_cmd.format(source=source, target=target,
                                     temp_dir_path=temp_dir_path).split()
            os.execlp(_[0], *_)

    def add_rf(self, key, value):
        self.rf[key] = value

    def export_rf(self, path=None):
        with open(_TMP_FILE_PATH, 'w') as f:
            f.write('#include <sys/syscall.h>\n')
            self.rf.export(f)

        ret = subprocess.check_output(['gcc', '-E', _TMP_FILE_PATH],
                                      universal_newlines=True)

        with open(_lp('conf', '%s_rf.conf' % self.code_name), 'w') as f:
            for _ in ret.split('\n'):
                if not _ or _.startswith('#'):
                    # Ignore lines with `#' in the front.
                    pass
                else:
                    f.write('%s\n' % _)


class CompiledLanguage(Language):
    def __init__(self, id_,
                 canonical_name, suffix, code_name,
                 compile_cmd,
                 memory_limit_multiplier=1,
                 time_limit_multiplier=1,
                 default_src_filename='',
                 default_exec_filename='',
                 exec_cmd=None,
                 rf_enabled=False,
                 chroot_enabled=True):
        super(CompiledLanguage, self).__init__(
            id_=id_,
            canonical_name=canonical_name,
            memory_limit_multiplier=memory_limit_multiplier,
            time_limit_multiplier=time_limit_multiplier,
            suffix=suffix,
            code_name=code_name,
            default_src_filename=default_src_filename,
            default_exec_filename=default_exec_filename,
            exec_cmd=exec_cmd,
            is_compiled_language=True,
            chroot_enabled=chroot_enabled,
            rf_enabled=rf_enabled
        )

        self.compile_cmd = compile_cmd

    def before_compile(self, source, target, temp_dir_path=''):
        pass

    def after_compile(self, source, target, temp_dir_path=''):
        # It seems that call to execlp, if any, does not succeed
        pass

    def compile(self, source, target, temp_dir_path=''):
        pass

    def do(self, source, target, temp_dir_path=''):
        self.before_compile(source, target, temp_dir_path)
        self.compile(source, target, temp_dir_path)
        self.after_compile(source, target, temp_dir_path)


class InterpretedLanguage(Language):
    def __init__(self, id_,
                 canonical_name, suffix, code_name, shebang_name=None,
                 memory_limit_multiplier=1,
                 time_limit_multiplier=1,
                 default_src_filename='',
                 default_exec_filename='',
                 exec_cmd=None,
                 rf_enabled=False):
        super(InterpretedLanguage,
              self).__init__(id_=id_,
                             canonical_name=canonical_name,
                             memory_limit_multiplier=memory_limit_multiplier,
                             time_limit_multiplier=time_limit_multiplier,
                             suffix=suffix,
                             code_name=code_name,
                             default_src_filename=default_src_filename,
                             default_exec_filename=default_exec_filename,
                             exec_cmd=exec_cmd,
                             is_interpreted_language=True,
                             rf_enabled=rf_enabled,
                             chroot_enabled=False)

        self.shebang_name = shebang_name or self.code_name

        if not self.shebang_name:
            sys.exit(-1)

    def make_shebang(self, source, target, temp_dir_path=''):
        with open(source, 'r') as src, open(target, 'w') as tgt:
            tgt.write('#! /usr/bin/%s\n\n' % self.shebang_name)
            tgt.write(src.read())

            # Mimic the permission setting of executables compiled from gcc.
            os.chmod(target, 0o755)

    def do(self, source, target, temp_dir_path=''):
        self.make_shebang(source, target, temp_dir_path)


def anchor_variable_at(anchor, name='lang', value=None):
    setattr(sys.modules[anchor], name, value)

def package_address_of(name):
    return 'langs.%s' % name

def def_compiled_lang(id_,
                      canonical_name, suffix, compile_cmd, code_name=None,
                      memory_limit_multiplier=1, time_limit_multiplier=1,
                      default_src_filename='',
                      default_exec_filename='',
                      exec_cmd=None,
                      # some compiler hooks,
                      before_compilation_hook=lambda _1, _2, _3: None,
                      compilation_failed_hook=lambda _1, _2, _3: None,
                      # some security options
                      chroot_enabled=True,
                      **rf_table):
    class SomeCompiledLang(CompiledLanguage):
        # TODO modify the name of this class to reflect the language name
        def __init__(self):
            super(SomeCompiledLang, self).__init__(
                id_,
                canonical_name,
                suffix,
                code_name,
                compile_cmd=compile_cmd,
                memory_limit_multiplier=memory_limit_multiplier,
                time_limit_multiplier=time_limit_multiplier,
                default_src_filename=default_src_filename,
                default_exec_filename=default_exec_filename,
                exec_cmd=exec_cmd,
                chroot_enabled=chroot_enabled,
                rf_enabled=False
            )

            if rf_table:
                self.rf_enabled = True
                for key, val in rf_table.items():
                    self.add_rf(key, val)

        def compile(self, source, target, temp_dir_path=''):
            _ = map(lambda sub: sub.format(source=source, target=target,
                                           temp_dir_path=temp_dir_path),
                    self.compile_cmd)

            _ = list(_)
            os.execlp(_[0], *_)

        def before_compile(self, source, target, temp_dir_path=''):
            before_compilation_hook(source, target, temp_dir_path)

        def after_compile(self, source, target, temp_dir_path=''):
            compilation_failed_hook(source, target, temp_dir_path)

    obj = SomeCompiledLang()
    anchor_variable_at(package_address_of(obj.code_name),
                       value=obj)

    return obj


def def_interpreted_lang(id_,
                         canonical_name, suffix,
                         memory_limit_multiplier=1,
                         time_limit_multiplier=1,
                         code_name=None, shebang_name=None,
                         default_src_filename='',
                         default_exec_filename='',
                         exec_cmd=None,
                         **rf_table):
    class SomeInterpretedLang(InterpretedLanguage):
    # TODO modify the name of this class to reflect the language name
        def __init__(self):
            super(SomeInterpretedLang, self).__init__(
                id_,
                canonical_name, suffix, code_name, shebang_name,
                memory_limit_multiplier=memory_limit_multiplier,
                time_limit_multiplier=time_limit_multiplier,
                default_src_filename=default_src_filename,
                default_exec_filename=default_exec_filename,
                exec_cmd=exec_cmd,
                rf_enabled=False
            )

            if rf_table:
                self.rf_enabled = True
                for key, val in rf_table.items():
                    self.add_rf(key, val)

    obj = SomeInterpretedLang()
    anchor_variable_at(package_address_of(obj.code_name),
                       value=obj)

    return obj