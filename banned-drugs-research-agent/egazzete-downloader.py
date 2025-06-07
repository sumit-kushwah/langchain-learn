from playwright.sync_api import sync_playwright
main_website = "https://egazette.gov.in/"
import pandas as pd
from bs4 import BeautifulSoup


def tbody_html_to_df(tbody_html):
    """
    Converts the tbody HTML of a table into a Pandas DataFrame and saves it as a CSV file.

    Args:
        tbody_html (str): The HTML content of the <tbody> tag.
        csv_filename (str): The name of the CSV file to save the data.
    """
    # Parse the tbody HTML with BeautifulSoup
    soup = BeautifulSoup(tbody_html, "html.parser")
    
    # Extract rows and columns
    rows = soup.find_all("tr", class_=lambda x: x != "pager")
    data = []
    for row in rows:
        cols = row.find_all(["td", "th"])  # Include both <td> and <th> for headers
        data.append([col.get_text(strip=True) for col in cols])
    
    # Convert to Pandas DataFrame
    df = pd.DataFrame(data[1:-1], columns=data[0])
    
    # Save to CSV
    # df.to_csv(csv_filename, index=False, header=False)
    return df
    # print(f"Data saved to {csv_filename}")
    
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto(main_website)
    # page url after redirection
    page_url = page.url.replace("default.aspx", "Default.aspx")
    page.goto(page_url)
    page.click("a#sgzt")
    page.wait_for_load_state("networkidle")
    page.click("input#btneSearch")
    page.wait_for_load_state("networkidle")
    print(page.url)
    page.fill("input#txtGazetteText", "Ministry of Health")
    page.select_option("select#ddlMinistry", value="Ministry of Health and Family Welfare")
    page.select_option("select#ddlDepartment", value="Department of Health and Family Welfare")
    page.click("input#Img_SubmitText")
    page.wait_for_load_state("networkidle")
    print("Form submitted successfully!")
    result_text = page.text_content("span#lbl_Result")
    print("Result Text:", result_text)
    print("Current URL:", page.url)
    
    # get table html with id "gvGazetteList"
    table_html = page.inner_html("table#gvGazetteList")
    # print("Table HTML:", table_html)
    
    df = tbody_html_to_df(table_html)
    
    pagination_links = page.locator("tr.pager td a")
    page_numbers = pagination_links.count() + 1  # Include the current page (1)

    print(f"Total pages: {page_numbers}")
    
    for i in range(2, page_numbers + 1):
        print(f"Processing page {i}...")
        page.click(f"a[href=\"javascript:__doPostBack('gvGazetteList','Page${i}')\"]")
        page.wait_for_load_state("networkidle")
        table_html = page.inner_html("table#gvGazetteList")
        # concat header is same only
        df1 = tbody_html_to_df(table_html)
        # print(df1.columns)
        df = pd.concat([df, df1], axis=0)

    print("Dataframe shape:", df.shape)
    df.to_csv("egazette_data.csv", index=False)
    
    
    
    
    