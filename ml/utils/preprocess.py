import re
import html
import unicodedata

URL_RE = re.compile(r'https?://\S+|www\.\S+')
EMAIL_RE = re.compile(r'\S+@\S+')
HTML_TAG_RE = re.compile(r'<.*?>')
SMART_QUOTES_RE = re.compile(r'[“”«»„‟`´]')
MULTI_WHITESPACE_RE = re.compile(r'\s+')

def clean_text(text: str) -> str:
    """
    Normalize text for both training & serving:
    - unescape HTML entities
    - normalize unicode (remove emojis/non-ascii)
    - replace smart quotes with normal quotes
    - remove URLs/emails/HTML tags
    - remove @mentions and hash symbol
    - keep basic punctuation (. , ? ! : ; - ' ")
    - collapse repeated punctuation and whitespace
    """
    if not text:
        return ""

    # 1) Unescape HTML entities and normalize unicode
    text = html.unescape(text)
    text = unicodedata.normalize('NFKD', text)

    # 2) Replace smart quotes with normal double-quote
    text = SMART_QUOTES_RE.sub('"', text)

    # 3) Remove URLs and emails
    text = URL_RE.sub(' ', text)
    text = EMAIL_RE.sub(' ', text)

    # 4) Remove HTML tags
    text = HTML_TAG_RE.sub(' ', text)

    # 5) Remove mentions (@username) and separate hashtags (#word -> word)
    text = re.sub(r'@\w+', ' ', text)
    text = re.sub(r'#', ' ', text)

    # 6) Remove characters outside basic set (keep letters, digits, basic punctuation)
    #    This will strip emojis and other exotic unicode characters.
    text = re.sub(r'[^0-9A-Za-z\s\.\,\?\!\:\;\-\'"]+', ' ', text)

    # 7) Collapse repeated punctuation (e.g., "!!!" -> "!")
    text = re.sub(r'([!?.,;:\-\'"])\1+', r'\1', text)

    # 8) Collapse whitespace
    text = MULTI_WHITESPACE_RE.sub(' ', text).strip()

    return text