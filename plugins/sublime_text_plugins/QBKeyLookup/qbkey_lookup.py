import sublime
from sublime_plugin import TextCommand
import requests


# -------------------------------------------------------------------------------------------------
def tohex(val, nbits):
    return hex((val + (1 << nbits)) % (1 << nbits))


# -------------------------------------------------------------------------------------------------
def parse_checksum(content):
    checksum = content.lower().strip()
    if checksum.endswith('u'):
        # BAADF00Du
        checksum = str('0x' + checksum[:-1])
    if checksum.startswith('0x'):
        # 0xBAADF00D
        checksum = int(checksum, 0)
    else:
        # -1163005939, 3131961357
        checksum = int(checksum)
    return str(tohex(checksum, 32))


# -------------------------------------------------------------------------------------------------
def lookup_checksum(checksum, fmt=False):
    url = 'http://api.thmods.com/api/ScriptKey/getByChecksum/'
    try:
        r = requests.get(
            url='{0}{1}'.format(url, checksum),
            timeout=5 
        )
    except (requests.ConnectionError, requests.Timeout):
        sublime.error_message('Unable to reach the THMods API...')
    else:
        if r.ok:
            checksum_name = r.json().get('name', None)
            if checksum_name is not None:
                if fmt:
                    sublime.set_clipboard(
                        '/*0x{:08X}*/"{}"'.format(
                            int(checksum, 16),
                            checksum_name
                        )
                    )
                else:
                    sublime.set_clipboard(checksum_name)
            else:
                sublime.message_dialog('No match for: ' + str(checksum))
        else:
            sublime.error_message('API error. See console...')
            print(r.json())


# -------------------------------------------------------------------------------------------------
class qbkey_lookupCommand(TextCommand):

    def run(self, edit, fmt=False):
        if self.region_set_empty(self.view.sel()):
            self.parse_region(edit, sublime.Region(0, self.view.size()), fmt)
        else:
            region_set = self.view.sel()
            for region in region_set:
                self.parse_region(edit, region, fmt)

    def region_set_empty(self, region_set):
        for region in region_set:
            if not region.empty():
                return False
        return True

    def parse_region(self, edit, region, fmt):
        content = self.view.substr(region)
        try:
            checksum = parse_checksum(content)
        except Exception as e:
            sublime.error_message('Plugin error. See console...')
            print(str(e))
        else:
            lookup_checksum(checksum, fmt)
