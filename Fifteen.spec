# -*- mode: python -*-
a = Analysis(['fifteen.py'],
             pathex=['/home/killerdigby/python-game-project/fifteen'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas+=[('data/bg3.png', 'data/bg3.png', 'DATA')]
a.datas+=[('data/loadscreen.png','data/loadscreen.png', 'DATA')]
a.datas += [('data/fifteen2.png', 'data/fifteen2.png', 'DATA')]             
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Fifteen',
          debug=False,
          strip=None,
          upx=True,
          console=True )
