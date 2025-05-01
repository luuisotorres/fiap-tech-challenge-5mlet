from bs4 import BeautifulSoup
from fastapi import HTTPException


def parse_producao(html: str) -> list[dict]:
    """
    Parses the HTML content from Embrapa's 'Produção' page and returns
    a list of products and their related subproducts with quantities.

    Args:
        html (str): Raw HTML string from the Embrapa page.

    Returns:
        list[dict]: Structured production data with main
        products and subproducts.

    Raises:
        HTTPException: If the data table is not found or all values are empty.
    """
    # Convert HTML to BeautifulSoup object
    soup = BeautifulSoup(html, "html.parser")

    # Locate the main data table
    table = soup.find("table", class_="tb_base tb_dados")
    if not table:
        raise HTTPException(status_code=404,
                            detail="Produção table not found.")

    rows = table.find_all("tr")
    data = []
    current_product = None

    # Iterate through table rows
    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 2:
            continue  # Skip malformed rows

        name = cols[0].get_text(strip=True)
        quantity = cols[1].get_text(strip=True)

        # Identify main products
        if 'tb_item' in cols[0].get('class', []):
            current_product = {
                "product": name,
                "quantity_liters": quantity,
                "subproducts": []
            }
            data.append(current_product)

        # Identify subproducts linked to the current main product
        elif 'tb_subitem' in cols[0].get('class', []) and current_product:
            current_product["subproducts"].append({
                "product": name,
                "quantity_liters": quantity
            })

    # Check if all values are empty ("-")
    all_empty = all(
        item["quantity_liters"] == "-" and
        all(sub["quantity_liters"] == "-" for sub in item["subproducts"])
        for item in data
    )

    if all_empty:
        raise HTTPException(
            status_code=404,
            detail="No produção data available for the specified year."
        )

    # Look for the total value in the footer
    tfoot = table.find("tfoot")
    if tfoot:
        total_row = tfoot.find("tr")
        total_cols = total_row.find_all("td") if total_row else []
        if len(total_cols) == 2:
            total_value = total_cols[1].get_text(strip=True)
            data.append({
                "total_overall": total_value
            })

    return data
