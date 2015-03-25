from ._fundamental import def_interpreted_lang
from .java import JAVA_SECURITY_POLICY_PATH

CLJ_JAR_PATH = '/home/wo/clojure-1.6.0/clojure-1.6.0.jar'

def_interpreted_lang(id_=7,
                     canonical_name='Clojure',
                     ext='clj',
                     exec_cmd=['java', '-cp', CLJ_JAR_PATH,
                               'clojure.main', '{source}',
                               '-Djava.security.manager',
                               '-Djava.security.policy=%s' %
                               JAVA_SECURITY_POLICY_PATH],
                     memory_limit_multiplier=3,
                     time_limit_multiplier=3)
