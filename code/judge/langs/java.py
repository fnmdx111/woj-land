from ._fundamental import def_compiled_lang, RFTable
import platform

def_compiled_lang(id_=3,
                  canonical_name='Java',
                  suffix='java',
                  code_name='java',
                  compile_cmd=['javac', '{source}',
                               '-d', '{temp_dir_path}'],
                  exec_cmd=['java', '-Djava.security.manager',
                            '-Djava.security.policy=/home/wo/l'
                            'and/code/judge/java.policy',
                            'Main'],
                  memory_limit_multiplier=2,
                  time_limit_multiplier=2,
                  default_src_filename='Main.java',
                  chroot_enabled=False)

