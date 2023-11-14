# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy


def write_to_log(data: list) -> None:
    log_name = bpy.context.preferences.addons["render-stats"].preferences.log_name
    log_path = bpy.utils.user_resource("SCRIPTS", path="addons/render-stats/logs") + f"/{log_name}.txt"
    
    with open(log_path, "a+") as file:
        file.write("".join(data))