import unittest

from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):

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

    
class TestBlockToBlockType(unittest.TestCase):

    def test_code(self):
        md = """
```This is a code block```

``This is not a code block```

#``This is not a code block`

```This is a code block
This is still a code block
and this too```
"""
        blocks = markdown_to_blocks(md)
        blocktypes = []
        for block in blocks:
            blocktypes.append(block_to_block_type(block))
        self.assertEqual(blocktypes, 
            [BlockType.CODE, BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.CODE]
            )


    def test_heading(self):
        md = """
# This is a heading <h1>

## This is a heading <h2>

### This is a heaading <h3>

#### This is a heading <h4>

##### This is a heading <h5>

###### This is a heading <h6>

####### This is not a heading, so it defaults to a paragraph <p>

##!# This is not a valid heading, so it defaults to a paragraph <p>
"""
        blocks = markdown_to_blocks(md)
        blocktype = []
        for block in blocks:
            blocktype.append(block_to_block_type(block))
        self.assertListEqual(blocktype,
            [BlockType.HEADING, BlockType.HEADING, BlockType.HEADING,
             BlockType.HEADING, BlockType.HEADING, BlockType.HEADING,
             BlockType.PARAGRAPH, BlockType.PARAGRAPH]
        )

    def test_quote(self):
        md = """
>This is a quote

!>This is not a quote, so <p>

>This is a multi quote block
>Because each line starts with '>'
>This is another quote, which makes the total quote count 3 in this block
"""

        blocks = markdown_to_blocks(md)
        blocktypes = []
        for block in blocks:
            blocktypes.append(block_to_block_type(block))
        self.assertListEqual(blocktypes, 
            [BlockType.QUOTE, BlockType.PARAGRAPH,
             BlockType.QUOTE]
        )
    

    def test_unordered_list(self):
        md = """
- item 1
- item 2
- item 3

-item 
- item

-item
2. item
"""
        blocks = markdown_to_blocks(md)
        blocktypes = []
        for block in blocks:
            blocktypes.append(block_to_block_type(block))
        self.assertListEqual(blocktypes, 
            [BlockType.UNORDERED_LIST, BlockType.PARAGRAPH,
             BlockType.PARAGRAPH]
            )
        
    
    def test_ordered_list(self):
        md = """
1. item
2. item
3. item

a. item
b. item
c. item

..item
.item
1 item
"""
        blocks = markdown_to_blocks(md)
        blocktypes = []
        for block in blocks:
            blocktypes.append(block_to_block_type(block))
        self.assertListEqual(blocktypes, 
            [BlockType.ORDERED_LIST, BlockType.PARAGRAPH,
             BlockType.PARAGRAPH]
            )
        
    def test_mix(self):
        md = """
# This is the header title

### This is smaller header

Here is a list of some kind:

- item
- item
- item

Here is another list but ordered:

1. item
2. item
3. item

>This list is perfect -Olivier Gaudet

```Code for world domination
print(hello, world!)```

War, what is it good for?
"""
        blocks = markdown_to_blocks(md)
        blocktypes = []
        for block in blocks:
            blocktypes.append(block_to_block_type(block))
        self.assertListEqual(blocktypes, 
            [BlockType.HEADING, BlockType.HEADING, BlockType.PARAGRAPH, BlockType.UNORDERED_LIST,
             BlockType.PARAGRAPH, BlockType.ORDERED_LIST, BlockType.QUOTE, BlockType.CODE,
             BlockType.PARAGRAPH])