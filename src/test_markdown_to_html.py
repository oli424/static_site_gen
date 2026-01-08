import unittest
from markdown_blocks import markdown_to_blocks
from markdown_html_node import extract_title, markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is the first paragraph.

This is the second paragraph.

This is the third paragraph.
"""
        expected_html = '<div><p>This is the first paragraph.</p><p>This is the second paragraph.</p><p>This is the third paragraph.</p></div>'
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        expected_html = '<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>'
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)

    def test_code_block(self):
        md = """
```python```
"""
        expected_html = '<div><pre><code>python</code></pre></div>'
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)

    def test_quote(self):
        md = """
> This is a blockquote.

> This is another blockquote line.
"""
        expected_html = '<div><blockquote>This is a blockquote.</blockquote><blockquote>This is another blockquote line.</blockquote></div>'
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)

    def test_ulist(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        expected_html = '<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>'
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)
    
    def test_olist(self):
        md = """
1. First item
2. Second item
3. Third item
"""
        expected_html = '<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>'
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)

    def test_mixed_content(self):
        md = """
# Heading
```print("Hello, World!")```
> This is a quote.
- List item 1
- List item 2
1. Ordered item 1
2. Ordered item 2

This is a paragraph.
"""
        expected_html = '<div><h1>Heading</h1><pre><code>print("Hello, World!")</code></pre><blockquote>This is a quote.</blockquote><ul><li>List item 1</li><li>List item 2</li></ul><ol><li>Ordered item 1</li><li>Ordered item 2</li></ol><p>This is a paragraph.</p></div>'
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)

    def test_paragraph_with_inline(self):
        md = """
This is **bold** and _italic_ and `code` in one paragraph
"""
        expected_html = ("<div><p>This is <b>bold</b> and <i>italic</i> and <code>code</code> in one paragraph</p></div>")
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)

    def test_multiline_code_block(self):
        md = """
```
line one
line **two**
```
"""
        expected_html = ("<div><pre><code>line one\nline **two**\n</code></pre></div>")
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)

    def test_empty_markdown(self):
        md = "   \n\n   "
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div></div>")

    def test_quote_with_inline(self):
        md = """
> A _quoted_ **line**
"""
        expected_html = ("<div><blockquote>A <i>quoted</i> <b>line</b></blockquote></div>")
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)

    def test_ulist_with_inline(self):
        md = """
- **Bold item**
- Item with `code`
- _Italic item_
"""
        expected_html = ("<div><ul><li><b>Bold item</b></li><li>Item with <code>code</code></li><li><i>Italic item</i></li></ul></div>")
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)

    def test_heading_with_inline(self):
        md = """
# This is a **bold** heading

## This is a smaller _italic_ heading
"""
        expected_html = ("<div><h1>This is a <b>bold</b> heading</h1><h2>This is a smaller <i>italic</i> heading</h2></div>")
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected_html)


class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        md = """
# My Document Title
Some paragraph text.
```print("Hello")```
> A quote here.
- List item
"""
        title = extract_title(md)
        self.assertEqual(title, "My Document Title")
    
    def test_no_title(self):
        md = """
Some paragraph text.
```print("Hello")```

> A quote here.
- List item
"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No heading found in markdown")

    def test_title_with_leading_spaces(self):
        md = """
   #   Title with Spaces
Some paragraph text.
"""
        title = extract_title(md)
        self.assertEqual(title, "Title with Spaces")

    def test_multiple_headings(self):
        md = """
# First Title
```print("Hello")```
## Second Title
Some paragraph text.
"""
        title = extract_title(md)
        self.assertEqual(title, "First Title")
    
    def test_no_h1(self):
        md = """
## Subtitle Only
```print("Hello")```
Some paragraph text.
"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No heading found in markdown")