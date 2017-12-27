import sys
import importlib
import json
from os.path import basename

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from docutils.parsers.rst import Directive
from docutils import nodes, statemachine
from sphinx.directives.code import CodeBlock


class ExecDirective(Directive):
    """Execute the specified python code and insert the output into the document"""
    has_content = True

    def run(self):
        oldStdout, sys.stdout = sys.stdout, StringIO()

        tab_width = self.options.get('tab-width', self.state.document.settings.tab_width)
        source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)

        try:
            exec('\n'.join(self.content))
            text = sys.stdout.getvalue()
            lines = statemachine.string2lines(text, tab_width, convert_whitespace=True)
            self.state_machine.insert_input(lines, source)
            return []
        except Exception:
            return [nodes.error(None, nodes.paragraph(text = "Unable to execute python code at %s:%d:" % (basename(source), self.lineno)), nodes.paragraph(text = str(sys.exc_info()[1])))]
        finally:
            sys.stdout = oldStdout

class DictDirective(CodeBlock):
    """ Pretty print dictionaries containing references to classes. """
    has_content = True
    required_arguments = 2

    def run(self):
        dict_obj = getattr(importlib.import_module(self.arguments[0]), self.arguments[1])
        new_dict = {}
        for k,v in dict_obj.items():
            new_dict[k] = '%s' % v.__name__
        string = self.arguments[0] + '.' + self.arguments[1] + ' = ' + json.dumps(new_dict, indent=2, sort_keys=True)

        self.arguments = ['Javascript']
        self.content = string.split('\n')
        return CodeBlock.run(self)


def setup(app):
    app.add_directive('exec', ExecDirective)
    app.add_directive('dict', DictDirective)
