import unittest

from inline_markdown import *

class TestInline(unittest.TestCase):
    def test_code(self):
        node = TextNode("Hello `code` world", TextType.TEXT)
        output = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(output, [
    TextNode("Hello ", TextType.TEXT),
    TextNode("code", TextType.CODE),
    TextNode(" world", TextType.TEXT),
    ])
        
        
    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(output, [
    TextNode("This is ", TextType.TEXT),
    TextNode("bold", TextType.BOLD),
    TextNode(" text", TextType.TEXT),
    ])
    
    def test_non_text(self):
        node = node = TextNode("already bold", TextType.BOLD)
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(output, [
    TextNode("already bold", TextType.BOLD),
    ])
        
    def test_no_delim(self):
        node = TextNode("Just plain text", TextType.TEXT)
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(output, [
    TextNode("Just plain text", TextType.TEXT),
    ])
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_empty_alt(self):
        matches = extract_markdown_images("An image with no alt text ![](https://storage.googleapis.com/qvault-webapp-wallet-artifacts/quest_authoring/confused_wizard.png)")
        self.assertListEqual([("", "https://storage.googleapis.com/qvault-webapp-wallet-artifacts/quest_authoring/confused_wizard.png")], matches)
    
    def test_extract_markdown_links_double(self):
        matches = extract_markdown_links(
            "I love [Boot.dev](https://www.boot.dev) and [Google](https://www.google.com)"
        )
        self.assertListEqual([("Boot.dev", "https://www.boot.dev"), ("Google", "https://www.google.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
        
    def test_final_conv(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        conv_node = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], conv_node
        )
