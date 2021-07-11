# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


A=[("P:\\GITHUB\\Melody\\libmpg123-0.dll",'.'),
	("P:\\GITHUB\\Melody\\libvorbisfile-3.dll",'.'),
	("P:\\GITHUB\\Melody\\libvorbis-0.dll",'.'),
	("P:\\GITHUB\\Melody\\libopusfile-0.dll",'.'),
	("P:\\GITHUB\\Melody\\libopus-0.dll",'.'),
	("P:\\GITHUB\\Melody\\libogg-0.dll",'.')]
a = Analysis(['Melody.py'],
             pathex=['p:\\GITHUB\\Melody','.',
			'P:\MelodyProject\Lib\site-packages','.'],
             binaries=A,
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Melody',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='Melody.ico')
