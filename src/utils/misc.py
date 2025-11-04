import os
import re


def get_root():
    current_file = os.path.abspath(__file__)
    api_dir = os.path.dirname(current_file)
    src_dir = os.path.dirname(api_dir)
    return os.path.dirname(src_dir)


def escape_markdown(text):
    special_chars = r'\`*_{}[]()#+\-\.!'
    return re.sub(f'([{re.escape(special_chars)}])', r'\\\1', text)

def escape_tag_and_username(text):
    match = re.match(r'^(\[[^\]]+\]\s+[^:]+:)\s(.*)$', text)
    if match:
        tag_and_user = match.group(1)
        message_content = match.group(2)
        escaped_tag = escape_markdown(tag_and_user)
        return escaped_tag + ' ' + message_content
    return escape_markdown(text)
