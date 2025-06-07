import os

os.environ["USER_AGENT"] ="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"

from langchain_community.document_loaders import AsyncChromiumLoader, AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer, Html2TextTransformer

# # Load HTML
# loader = AsyncChromiumLoader(["https://www.hondaindiapower.com/product-detail/wb40xd"])
# html = loader.load()

# # Transform
# bs_transformer = BeautifulSoupTransformer()
# # print(html)
# docs_transformed = bs_transformer.transform_documents(html)

# print(docs_transformed[0].page_content)

# print("Done")

links = [
    "https://www.hondaindiapower.com/product-detail/wb40xd",
    "https://www.hondaindiapower.com/product-detail/wb30xd",
    "https://www.hondaindiapower.com/product-detail/wb20xd",
    "https://www.hondaindiapower.com/product-detail/ws20x",
    "https://www.hondaindiapower.com/product-detail/wb15x"
]
print(links)
loader = AsyncChromiumLoader(links)
# loader = ScrapingAntLoader(
#     [worker_state["link"]],
#     api_key="e5745f8589af4611abb4ca2778a224b7",  # Get your API key from https://scrapingant.com/
#     continue_on_failure=True,  # Ignore unprocessable web pages and log their exceptions
# )
html = loader.load()

soup_transformer = Html2TextTransformer()
docs_transformed = soup_transformer.transform_documents(html)

for doc in docs_transformed:
    print(doc.page_content)
    print("\n   -------------------   \n\n\n\n\n")