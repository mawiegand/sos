# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

import os
from sos.policies.distros.redhat import RedHatPolicy, OS_RELEASE


class AnolisPolicy(RedHatPolicy):

    distro = "Anolis OS"
    vendor = "The OpenAnolis Project"
    vendor_urls = [('Distribution Website', 'https://openanolis.org/')]

    def __init__(self, sysroot=None, init=None, probe_runtime=True,
                 remote_exec=None):
        super().__init__(sysroot=sysroot, init=init,
                         probe_runtime=probe_runtime,
                         remote_exec=remote_exec)

    @classmethod
    def check(cls, remote=''):

        if remote:
            return cls.distro in remote

        # Return False if /etc/os-release is missing
        if not os.path.exists(OS_RELEASE):
            return False

        # Return False if /etc/anolis-release is missing
        if not os.path.isfile('/etc/anolis-release'):
            return False

        with open(OS_RELEASE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('NAME'):
                    if 'Anolis OS' in line:
                        return True
        return False

# vim: set et ts=4 sw=4 :
