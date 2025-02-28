import os

os.environ["USER_AGENT"] ="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"

from langchain_community.document_loaders import AsyncChromiumLoader, AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

# Load HTML
loader = AsyncChromiumLoader(["https://www.amazon.in/Hero-PLEASURE-Scooter-Booking-Ex-Showroom/dp/B0D9DM8X6C/"])
html = loader.load()

# Transform
bs_transformer = BeautifulSoupTransformer()
# print(html)
docs_transformed = bs_transformer.transform_documents(html)

print(docs_transformed[0].page_content)

print("Done")