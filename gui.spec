# -*- mode: python -*-

block_cipher = None


a = Analysis(['gui.py'],
             pathex=['C:\\Users\\Dylan\\Desktop\\selene'],
             binaries=None,
             datas=[('se.py','se'),('modules.py','modules'),('__init__.py','__init__')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Selene',
          debug=False,
          strip=False,
          upx=True,
          console=False, 
		  icon='icon.ico')
