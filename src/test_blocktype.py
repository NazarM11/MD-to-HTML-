import unittest

from blocktype import *

class TestBlockType(unittest.TestCase):
    def test_heading(self):
        block = "## Hello World"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_no_space(self):
        block = "##Hello World"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote\n> still a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unlist(self):
        block = "- apples\n- bananas\n- cherries"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_orlist(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

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
