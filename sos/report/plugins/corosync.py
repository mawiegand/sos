# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

import re
from sos.report.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin


class Corosync(Plugin):

    short_desc = 'Corosync cluster engine'

    plugin_name = "corosync"
    profiles = ('cluster',)
    packages = ('corosync',)

    def setup(self):
        self.add_copy_spec([
            "/etc/corosync",
            "/var/lib/corosync/fdata",
            "/var/log/cluster/corosync.log*"
        ])
        self.add_cmd_output([
            "corosync-quorumtool -l",
            "corosync-quorumtool -s",
            "corosync-cpgtool",
            "corosync-cfgtool -s",
            "corosync-blackbox",
            "corosync-objctl -a",
            "corosync-cmapctl -m stats"
        ])
        self.add_cmd_output("corosync-cmapctl",
                            tags="corosync_cmapctl")
        self.exec_cmd("killall -USR2 corosync")

        corosync_conf = "/etc/corosync/corosync.conf"
        if not self.path_exists(corosync_conf):
            return

        # collect user-defined logfiles, matching either of pattern:
        # log_size: filename
        # or
        # logging.log_size: filename
        # (it isnt precise but sufficient)
        pattern = r'^\s*(logging.)?logfile:\s*(\S+)$'
        try:
            cconf = self.path_join("/etc/corosync/corosync.conf")
            with open(cconf, 'r', encoding='UTF-8') as file:
                for line in file:
                    if re.match(pattern, line):
                        self.add_copy_spec(re.search(pattern, line).group(2))
        except IOError as err:  # pylint: disable=broad-except
            self._log_warn(f"could not read from {corosync_conf}: {err}")

    def postproc(self):
        self.do_cmd_output_sub(
            "corosync-objctl",
            r"(.*fence.*\.passwd=)(.*)",
            r"\1******"
        )


class RedHatCorosync(Corosync, RedHatPlugin):
    """ Parent class Corosync's setup() will be called """


class DebianCorosync(Corosync, DebianPlugin, UbuntuPlugin):
    """ Parent class Corosync's setup() will be called """
    files = ('/usr/sbin/corosync',)

# vim: set et ts=4 sw=4 :
