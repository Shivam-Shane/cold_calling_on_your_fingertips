from langchain_community.document_loaders import WebBaseLoader

def posting_fetcher(url):
    loader=WebBaseLoader(url)
    documents=loader.load().pop().page_content
    return documents