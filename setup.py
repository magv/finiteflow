#! /usr/bin/env python3

import subprocess
import sys

from setuptools import setup
from setuptools.command.build_ext import build_ext

def write_config_hh():
    with open("include/fflow/config.hh.in") as f:
        text = f.read()
    text = text.replace("@FFLOW_VERSION@", "2")
    text = text.replace("@FFLOW_VERSION_MINOR@", "0")
    text = text.replace(
        f"#cmakedefine01 FFLOW_BIG_ENDIAN",
        f"#define FFLOW_BIG_ENDIAN {int(sys.byteorder == 'big')}",
    )
    text = text.replace(
        f"#cmakedefine01 FFLOW_THREAD_POOL",
        f"#define FFLOW_THREAD_POOL {int(sys.platform != 'darwin')}",
    )
    with open("include/fflow/config.hh", "w") as f:
        f.write(text)

def generate_cffi_source():
    """Generate pythonapi/_cffi_fflow.c via fflow_build.py --source-only."""
    subprocess.check_call(
        [sys.executable, "fflow_build.py", "--source-only"],
        cwd="pythonapi",
    )

class build_ext(build_ext):
    def run(self):
        subprocess.check_call(
            ["make", "-C", "hepware", "gmp.done", "flint-finiteflow.done",
             f"FETCH={sys.executable} bin/urlget"]
        )
        write_config_hh()
        generate_cffi_source()
        super().run()

    def build_extensions(self):
        extra_link_args = (
            ["-Wl,-dead_strip"] if sys.platform == "darwin" else ["-Wl,--gc-sections"]
        )
        for ext in self.extensions:
            ext.extra_link_args.extend(extra_link_args)
            if sys.platform.startswith("linux"):
                ext.libraries.append("pthread")
        super().build_extensions()

setup(cmdclass={"build_ext": build_ext})
