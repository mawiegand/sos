# Copyright 2023 Marcel Wiegand <wiegand@linux.com>

# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from sos.report.plugins import ArchPlugin
from sos.report.plugins.kubernetes import Kubernetes


class K3s(Kubernetes, ArchPlugin):
    short_desc = "K3s - Lightweight Kubernetes"

    plugin_name = "k3s"

    packages = ("k3s",)
    files = ("/etc/rancher/k3s/k3s.yaml",)
    kube_cmd = "k3s kubectl"
