import markdown
import unittest
from mcgtable.extension import MCellGridTableExtension
import re


class TestExtension(unittest.TestCase):

    def test_simple_example_works(self):
        html = self.to_html(simple_example)
        self.html_compare(html, simple_expected)

    def test_text_before_preserved(self):
        html = self.to_html("before\n" + simple_example)
        self.html_compare(html, "<p>before</p>\n" + simple_expected)

    def test_text_after_preserved(self):
        html = self.to_html(simple_example + "\nafter")
        self.html_compare(html, simple_expected + "\n<p>after</p>")

    def to_html(self, raw_markdown):
        return markdown.markdown(raw_markdown,
                                 extensions=[MCellGridTableExtension()])

    def html_compare(self, actual, expected):
        a = self.normalize_html(actual)
        e = self.normalize_html(expected)
        # don't truncate diffs
        self.maxDiff = None
        self.assertEqual(a, e, 'HTML should not differ except for whitespace')

    def normalize_html(self, html):
        collapsed_whitespace = re.sub('\\s+', ' ', html, flags=re.MULTILINE)
        # <col style="width: 6em;" /> -> <col style="width: 6em;"/>
        cleaned_end_tags = re.sub('\\s/>', '/>', collapsed_whitespace)
        # <p> c </p> -> <p>c</p>
        removed_padding = re.sub('((?<=>)\\s|\\s(?=<))', '', cleaned_end_tags)
        return removed_padding


simple_example = """
```mcgtable
+-----+-----+
|h1   |h2   |
+=====+=====+
|c1   | c2  |
+abc  |-----+
|123  |c3   |
+-----+-----+
```
"""

# captured output and then visually inspected
simple_expected = """
<table>
  <col style="width: 6em;"/>
  <col style="width: 6em;"/>
  <thead>
  <tr>
    <th>
      <p>h1</p>
    </th>
    <th>
      <p>h2</p>
    </th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td rowspan="2">
      <p>
        c1
        abc
        123
      </p>
    </td>
    <td>
      <p>c2</p>
    </td>
  </tr>
  <tr>
    <td>
      <p>c3</p>
    </td>
  </tr>
  </tbody>
</table>

"""

# unused
complex_example = """
A paragraph of text before table.

```mcgtable
Table: Simple Merge Cell Example

+-----+------+------+------+
|h1          |h2    |h3    |
+============+======+======+
|c1   |c2    |c3    |c4    |
+abc  |------+------+------+
|xyz  |c5    | c6          |
+-----+------+ 123         |
|c7   |c8    | 456         |
|     |      |             |
|     |      | 789         |
|     |      |             |
|     |      | - Item A    |
|     |      | - Item B    |
|     |      | - Item C    |
+-----+------+-------------+
```

Another paragraph of text after table.
"""

if __name__ == '__main__':
    unittest.main()
