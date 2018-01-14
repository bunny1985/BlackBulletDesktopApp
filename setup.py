#!/usr/bin/python3

import os, sys, site
from setuptools import setup, find_packages
from setuptools.command.install import install as _install


def get_installation_prefix(install_dir):
    py_version = '%s.%s' % (sys.version_info[0], sys.version_info[1])
    if '--user' in sys.argv:
        path = site.getusersitepackages()
        prefix = path.split("/lib/python%s/site-packages" % py_version)[0]
        if (os.path.exists(prefix)):
            return prefix
    else:
        for directory in ["dist-packages", "site-packages"]:
            py_dir = "/lib/python%s/%s" % (py_version, directory)
            if py_dir in install_dir:
                prefix = install_dir.split(py_dir)[0]
                if os.path.exists(prefix):
                    return prefix
    return ""


def _post_install(install_dir):
    prefix = get_installation_prefix(install_dir)
    print("compiling schemas")
    os.system('glib-compile-schemas %s/share/glib-2.0/schemas' % prefix)
    print("updating icon cache")
    os.system('gtk-update-icon-cache -f -t %s/share/icons/hicolor/' % prefix)


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="Running post install task")


my_data_files = [
    ('share/icons/hicolor/scalable/apps/', ['boilerplate/data/icons/scalable/boilerplate.svg']),
    ('share/icons/hicolor/16x16/apps/', ['boilerplate/data/icons/16x16/boilerplate.png']),
    ('share/icons/hicolor/24x24/apps/', ['boilerplate/data/icons/24x24/boilerplate.png']),
    ('share/icons/hicolor/32x32/apps/', ['boilerplate/data/icons/32x32/boilerplate.png']),
    ('share/icons/hicolor/48x48/apps/', ['boilerplate/data/icons/48x48/boilerplate.png']),
    ('share/icons/hicolor/64x64/apps/', ['boilerplate/data/icons/64x64/boilerplate.png']),
    ('share/applications/', ['boilerplate.desktop']),
    ('share/glib-2.0/schemas/', ['boilerplate.gschema.xml']),
    ]

setup(
    name = "BlcakBullet",
    version = "0.1",
    author = "Michał Banaś",
    author_email = "mb.michal.banas@gmail.com",
    description = "Blacbullet desktop App",
    license = "GPL3",
    keywords = "Android communication",
    url = "bmideas.pl",
    cmdclass={'install': install},
    scripts = ['boilerplate/boilerplate'],
    data_files = my_data_files,
    packages = find_packages(),
)
