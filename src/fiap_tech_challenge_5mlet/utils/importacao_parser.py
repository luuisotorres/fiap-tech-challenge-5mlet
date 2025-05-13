from bs4 import BeautifulSoup
from fastapi import HTTPException

def parse_importacao(html: str) -> list[dict]:
    """
    Parses the HTML content for import data and returns a list of structured data.

    Args:
        html (str): Raw HTML content from the import page.

    Returns:
        list[dict]: A list of import data, including a total item.

    Raises:
        HTTPException: If the main data table is not found or all values are empty.
    """
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", class_="tb_base tb_dados")
    if not table:
        raise HTTPException(status_code=404, detail="Data table not found.")

    results = []

    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) != 3:
            continue

        country = cols[0].get_text(strip=True)
        quantity = cols[1].get_text(strip=True).replace(".", "").replace(",", ".")
        value = cols[2].get_text(strip=True).replace(".", "").replace(",", ".")

        if quantity == "-" and value == "-":
            continue

        results.append({
            "country": country,
            "quantity_kg": float(quantity) if quantity != "-" else None,
            "value_usd": float(value) if value != "-" else None,
            "subproducts": [] 
        })

    tfoot = table.find("tfoot", class_="tb_total")
    if tfoot:
        total_row = tfoot.find("tr")
        total_cols = total_row.find_all("td")
        if len(total_cols) == 3:
            total_quantity = total_cols[1].get_text(strip=True).replace(".", "").replace(",", ".")
            total_value = total_cols[2].get_text(strip=True).replace(".", "").replace(",", ".")
            results.append({
                "country": "Total",
                "quantity_kg": float(total_quantity),
                "value_usd": float(total_value),
                "subproducts": [] 
            })

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No import data available for the specified year."
        )

    return results