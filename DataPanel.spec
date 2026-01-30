# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata, collect_data_files
import streamlit
import os

block_cipher = None

# Collect metadata for packages that need it
datas = [('DataPanel.py', '.')]

# Try to copy metadata, skip if not available
for pkg in ['streamlit', 'altair', 'pandas', 'numpy', 'plotly']:
    try:
        datas += copy_metadata(pkg)
    except Exception:
        pass

# Add Streamlit's static files
streamlit_path = os.path.dirname(streamlit.__file__)
datas += [(os.path.join(streamlit_path, 'static'), 'streamlit/static')]
datas += [(os.path.join(streamlit_path, 'runtime'), 'streamlit/runtime')]

# Collect all streamlit data files
try:
    datas += collect_data_files('streamlit')
except Exception:
    pass

# Collect plotly data files
try:
    datas += collect_data_files('plotly')
except Exception:
    pass

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.web.bootstrap',
        'streamlit.runtime',
        'streamlit.runtime.scriptrunner',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.components.v1',
        'streamlit.logger',
        'requests',
        'requests.packages',
        'requests.packages.urllib3',
        'pandas',
        'numpy',
        'plotly',
        'plotly.express',
        'plotly.graph_objs',
        'plotly.graph_objects',
        'plotly.io',
        'plotly.subplots',
        'plotly.validators',
        'plotly.colors',
        'plotly.data',
        'plotly.figure_factory',
        '_plotly_utils',
        '_plotly_utils.basevalidators',
        'json',
        'altair',
        'pyarrow',
        'pydeck',
        'click',
        'toml',
        'validators',
        'watchdog',
        'tornado',
        'packaging',
        'protobuf',
        'pympler',
        'blinker',
        'cachetools',
        'gitpython',
        'pillow',
        'tzlocal',
        'tenacity',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DataPanel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console window to see streamlit output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
