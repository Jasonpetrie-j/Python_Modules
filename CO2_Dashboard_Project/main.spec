# -*- mode: python ; coding: utf-8 -*-
import sys
import os
import shutil
from PyInstaller.utils.hooks import collect_all

# -----------------------------------------------------------------------------
# 1. AUTOMATED DEPENDENCY COLLECTION
# CustomTkinter has non-code assets (json themes, images) that PyInstaller 
# often misses. This helper grabs them all securely.
# -----------------------------------------------------------------------------
datas = []
binaries = []
hiddenimports = []

# Collect all customtkinter hooks (themes, images, etc.)
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# Add any other hidden imports if your src/ modules aren't found
hiddenimports += ['src.model', 'src.view', 'src.sensor_interface']

# -----------------------------------------------------------------------------
# 2. BUILD DEFINITION
# -----------------------------------------------------------------------------
block_cipher = None

a = Analysis(
    ['main.py'],                 # Your Entry Point
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='CO2_Dashboard',         # The name of your final .exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                # Set to True if you want to see print() output for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='monitor.ico'            # Optional: Add an icon if you have one (e.g., 'assets/icon.ico')
)

# -----------------------------------------------------------------------------
# 3. POST-BUILD AUTOMATION (The "L4" Touch)
# This script runs AFTER the build to ensure your deployment folder is ready.
# It copies config.json to the dist folder so it sits NEXT TO the exe.
# -----------------------------------------------------------------------------
print("\n--- STARTING POST-BUILD AUTOMATION ---")
dist_path = os.path.join(os.getcwd(), 'dist')
config_src = os.path.join(os.getcwd(), 'config.json')
config_dst = os.path.join(dist_path, 'config.json')

if os.path.exists(config_src):
    print(f"Detected config.json. Copying to: {config_dst}")
    shutil.copyfile(config_src, config_dst)
    print("SUCCESS: Config file bundled externally for easy editing.")
else:
    print("WARNING: config.json not found in root. Please copy manually.")

print("--- BUILD COMPLETE ---\n")