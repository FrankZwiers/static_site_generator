import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_paragraph1(self):
        text = "This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph2(self):
        text = "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_block_to_block_type_ul_one_item(self):
        text = "- This is a list with one item"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ul_multiple_items(self):
        text = "- This is a list\n- with multiple\n- items"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ol_one_item(self):
        text = "1. This is a list with one item"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ol_multiple_items(self):
        text = "1. This is a list\n2. with multiple\n3. items"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_block_to_block_type_empty(self):
        text = ""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        text = ">This is a\n>beautiful quote"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_block_to_block_type_quote_wrong(self):
        text = ">This is a\n >incorrectly formatted\n> quote"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_ordered_list(self):
        md = """
1. List
2. With
3. Multiple
4. Items
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>List</li><li>With</li><li>Multiple</li><li>Items</li></ol></div>",
        )

    def test_ordered_list_bold_part(self):
        md = """
1. **An Unnecessary Interlude**: The encounter with Tom, while quaint and endearing, serves as a temporal diversion that detracts from the urgency of the Fellowship's quest.
2. **An Outlier in Purpose**: His escapades, while rich in mirth, add little to the central narrative, raising questions about their relevance in the grand design of Middle-earth.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>An Unnecessary Interlude</b>: The encounter with Tom, while quaint and endearing, serves as a temporal diversion that detracts from the urgency of the Fellowship's quest.</li><li><b>An Outlier in Purpose</b>: His escapades, while rich in mirth, add little to the central narrative, raising questions about their relevance in the grand design of Middle-earth.</li></ol></div>",
        )

    def test_unordered_list(self):
        md = """
- List
- With
- Multiple
- Items
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>List</li><li>With</li><li>Multiple</li><li>Items</li></ul></div>",
        )

    def test_image(self):
        md = """
![JRR Tolkien sitting](/images/tolkien.png)
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p><img src=\"/images/tolkien.png\" alt=\"JRR Tolkien sitting\"></img></p></div>",
        )

    def test_link(self):
        md = """
[Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p><a href=\"/blog/glorfindel\">Why Glorfindel is More Impressive than Legolas</a></p></div>",
        )

    def test_h1(self):
        md = """
# Test title
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Test title</h1></div>",
        )

    def test_h2(self):
        md = """
## Test title
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Test title</h2></div>",
        )

    def test_blockquote(self):
        md = """
> Nice quote
> Said by
> Someone
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Nice quote Said by Someone</blockquote></div>",
        )
    def test_blockquote_with_empty_line(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>\"I am in fact a Hobbit in all but size.\"  -- J.R.R. Tolkien</blockquote></div>",
        )