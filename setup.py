from setuptools import find_namespace_packages, setup


setup(name='xicam.myplugin',
      version='1.0.0',
      author='roberttk',
      install_requires='xicam',
      packages=find_namespace_packages(include=['xicam.*']),
      entry_points={
          # 'MyPlugin' can be found in package 'xicam.myplugin'
          # class is called 'MyPlugin'
          'xicam.plugins.GUIPlugin': [
              'MyPlugin=xicam.myplugin:MyGUIPlugin'
          ] ,
          'xicam.plugins.OperationPlugin': [
              'fft=xicam.myplugin.operations:fft'
              # 'random_noise=xicam.sampleplugin.operations.noise:random_noise'
          ]
      }
     )
