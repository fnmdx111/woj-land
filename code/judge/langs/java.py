from ._fundamental import def_compiled_lang

JAVA_SECURITY_POLICY_PATH = '/home/wo/land/code/judge/java.policy'

def_compiled_lang(id_=3,
                  canonical_name='Java',
                  suffix='java',
                  code_name='java',
                  compile_cmd=['javac', '{source}',
                               '-d', '{temp_dir_path}'],
                  exec_cmd=['java', '-Djava.security.manager',
                            '-Djava.security.policy=%s'
                            % JAVA_SECURITY_POLICY_PATH,
                            'Main'],
                  memory_limit_multiplier=2,
                  time_limit_multiplier=2,
                  default_src_filename='Main.java',
                  chroot_enabled=False)

