# ----------------------------------------------------------------------------------------------------
import sublime_plugin
import base64
from pathlib import Path
from subprocess import Popen

# ----------------------------------------------------------------------------------------------------
RUNMENOW_PATH = Path('D:/Repos/thugpro-tools/runmenow.exe')


# ----------------------------------------------------------------------------------------------------
class RunMeNowCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            if region.size() > 2:
                selection = self.view.substr(region)
                encoded = base64.urlsafe_b64encode(selection.encode()).decode()
                Popen([str(RUNMENOW_PATH), encoded])

    def is_enabled(self):
        return True
