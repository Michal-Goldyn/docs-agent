from app.loader import split_into_chunks
from textwrap import dedent

def test_splits_on_h2_headers():
    content = """## First\nThis section explains something important and is long enough to survive the 
        merge rule, long text.\n\n## Second\nAnother section with enough text to stay a separate chunk on its own. Text text text text text text text text"""
    chunks = split_into_chunks(content)
    assert len(chunks) == 2

def test_hash_comment_in_code_block_is_not_a_header():
    content = '''
        ## First section
        text long enough to exceed 100 characters, text long enough to exceed 100 characters, text long enough to exceed 100 characters
        ```python
        # normal comment
        ## looks like a markdown header, but it's python comment
        This text also exceeds 100 characters, long enough text to test whether split function works correctly or not
        print("Hi")
        ```
        '''
    content = dedent(content)
    chunks = split_into_chunks(content)
    assert len(chunks) == 1
