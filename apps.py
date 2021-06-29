# -*- coding: utf-8 -*-
""" Apps.py. Parsl Application Functions (@) 2021

This module encapsulates all Parsl configuration stuff in order to provide a
cluster configuration based in number of nodes and cores per node.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

# COPYRIGHT SECTION
__author__ = "Diego Carvalho"
__copyright__ = "Copyright 2021"
__credits__ = ["Diego Carvalho", "etc"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Diego Carvalho"
__email__ = "d.carvalho@ieee.org"
__status__ = "Research"

#
# Parsl Bash and Python Applications
#
import parsl

#
# Strategy: list of apps to be implemented
#
# octave_app
# KFS2d
# mpca_app


@parsl.bash_app()
def KFS2d(spec_flags: str,
          stderr=parsl.AUTO_LOGNAME,
          stdout=parsl.AUTO_LOGNAME,
          outputs=[]):
    """ Kalman Filter
    """
    return f"cd kfs2d_rna_mirror; ./run-KFS2d.sh {spec_flags}"


@parsl.bash_app()
def model_normalize(inputs=[],
                    outputs=[],
                    stderr=parsl.AUTO_LOGNAME,
                    stdout=parsl.AUTO_LOGNAME):
    with open(inputs[0], 'r') as f:
        with open("octave/qAnalysisExpA.out", "w") as w:
            w.write(f.read())
    with open(inputs[1], 'r') as f:
        with open("octave/qModelExpA.out", "w") as w:
            w.write(f.read())
    with open(inputs[2], 'r') as f:
        with open("octave/qObservExpA.out", "w") as w:
            w.write(f.read())

    return "cd octave; spack load octave; octave ../scripts/kfs_normalize.m"


@parsl.bash_app()
def mpca_ann(inputs=[],
             outputs=[],
             stderr=parsl.AUTO_LOGNAME,
             stdout=parsl.AUTO_LOGNAME):
    with open(inputs[0], 'r') as f:
        with open("mpca-ann/data/x.txt", "w") as w:
            w.write(f.read())
    with open(inputs[1], 'r') as f:
        with open("mpca-ann/data/x_gen.txt", "w") as w:
            w.write(f.read())
    with open(inputs[2], 'r') as f:
        with open("mpca-ann/data/x_valid.txt", "w") as w:
            w.write(f.read())
    with open(inputs[3], 'r') as f:
        with open("mpca-ann/data/y.txt", "w") as w:
            w.write(f.read())
    with open(inputs[4], 'r') as f:
        with open("mpca-ann/data/y_gen.txt", "w") as w:
            w.write(f.read())
    with open(inputs[5], 'r') as f:
        with open("mpca-ann/data/y_valid.tx", "w") as w:
            w.write(f.read())

    return "cd mpca-ann; ../scripts/sed-mpca-src; ./runMPCA 1 4; ./annMLP 1 4"
