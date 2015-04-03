from ._fundamental import def_interpreted_lang
try:
    from .lua_rf import rf
except ImportError:
    rf = {}

def_interpreted_lang(id_=8,
                     canonical_name='Lua',
                     ext='lua',
                     **rf)
