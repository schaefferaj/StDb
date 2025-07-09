project('stdb', 'c',
  version : '0.2.7',
  license: 'MIT',
  meson_version: '>=0.64.0',
)

py_mod = import('python')
py = py_mod.find_installation()
py_dep = py.dependency()

py.install_sources(
  'stdb/classes.py',
  'stdb/gui.py',
  'stdb/io.py',
  'stdb/kml.py',
  'stdb/__init__.py',
  'stdb/scripts/append_stdb.py',
  'stdb/scripts/dump_stdb.py',
  'stdb/scripts/edit_stdb.py',
  'stdb/scripts/gen_stdb.py',
  'stdb/scripts/ls_stdb.py',
  'stdb/scripts/merge_stdb.py',
  'stdb/scripts/query_fdsn_stdb.py',
  'stdb/scripts/stdb_to_kml.py',
  'stdb/scripts/__init__.py',
  pure: false,
  preserve_path: true,
  )
  