# SPDX-FileCopyrightText: 2021 Michael Webster
# SPDX-FileCopyrightText: Western Digital Corporation or its affiliates
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 
# I extended this example from BoxExtension in https://python-markdown.github.io/extensions/api/
import pkg_resources
import re
import subprocess
import xml.etree.ElementTree as etree

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension


class MCellGridTableBlockProcessor(BlockProcessor):
    RE_CODE_BLK_START = r'^ *`{3,}mcgtable *\n'  # For example: '```mcgtable'
    RE_CODE_BLK_END = r'\n *`{3,}\s*$'  # For example: '```\n\n'
    SCRIPT_PATH = pkg_resources.resource_filename(__package__,
                                                  'mcell-grid-table.lua')
    SCRIPT_CMD = f"lua {SCRIPT_PATH} -t html".split()

    def test(self, parent, block):
        return re.match(self.RE_CODE_BLK_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]

        # Remove code block's opening marker
        blocks[0] = re.sub(self.RE_CODE_BLK_START, '', blocks[0])

        # Find code block with closing marker
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_CODE_BLK_END, block):

                # Remove code block's closing marker
                blocks[block_num] = re.sub(self.RE_CODE_BLK_END, '', block)

                # Render code block as table

                e = self.invoke_script(blocks[:block_num + 1])
                parent.append(e.getroot())
                self.process_cell_contents(e)

                # Remove consumed blocks
                for _ in range(0, block_num + 1):
                    blocks.pop(0)
                return True

        # Something went wrong!  Restore original blocks.
        blocks[0] = original_block
        return False

    def process_cell_contents(self, e):
        for cell in e.findall('thead/tr/th'):
            txt = cell.text
            cell.text = ""
            self.parser.parseChunk(cell, txt)
        for cell in e.findall('thead/tr/td'):
            txt = cell.text
            cell.text = ""
            self.parser.parseChunk(cell, txt)
        for cell in e.findall('tbody/tr/th'):
            txt = cell.text
            cell.text = ""
            self.parser.parseChunk(cell, txt)
        for cell in e.findall('tbody/tr/td'):
            txt = cell.text
            cell.text = ""
            self.parser.parseChunk(cell, txt)
        for cell in e.findall('tfoot/tr/th'):
            txt = cell.text
            cell.text = ""
            self.parser.parseChunk(cell, txt)
        for cell in e.findall('tfoot/tr/td'):
            txt = cell.text
            cell.text = ""
            self.parser.parseChunk(cell, txt)
        # TODO: if just one paragraph found reduce it to just the td/th text?

    def invoke_script(self, blocks):
        proc = subprocess.Popen(
              self.SCRIPT_CMD,
              shell=False,
              stdin=subprocess.PIPE,
              stdout=subprocess.PIPE,
              universal_newlines=True
        )
        with proc.stdin as stdin:
            for block in blocks:
                stdin.write(block)
                stdin.write("\n")

        proc.wait(timeout=1)
        with proc.stdout as stdout:
            return etree.parse(stdout)


class MCellGridTableExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(
              MCellGridTableBlockProcessor(md.parser), 'mcgtable', 175)


def makeExtension(**kwargs):
    return MCellGridTableExtension(**kwargs)
