from bs4 import BeautifulSoup
from fastapi import HTTPException


def parse_processamento(html: str) -> list[dict]:
    """
    Parses the HTML from the Embrapa 'Processamento' tab and returns
    structured data of products and subproducts with their respective
    quantities.

    Args:
        html (str): Raw HTML content from the target Embrapa page.

    Returns:
        list[dict]: List of processed product data including subproducts.

    Raises:
        HTTPException: If the main data table is not found or all values are
        empty.
    """
    # Convert the HTML into a BeautifulSoup object
    soup = BeautifulSoup(html, "html.parser")

    # Locate the data table
    table = soup.find("table", class_="tb_base tb_dados")
    if not table:
        raise HTTPException(status_code=404,
                            detail="Data table not found.")

    results = []
    current_category = None
    category_qty = None
    subproducts = []

    # Iterate through each row in the table
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) != 2:
            continue  # Skip malformed rows

        name = cols[0].get_text(strip=True)
        quantity = cols[1].get_text(strip=True)
        cell_classes = cols[0].get("class", [])

        # Detect a main product row
        if "tb_item" in cell_classes:
            # Save the previous product if it exists
            if current_category:
                results.append({
                    "product": current_category,
                    "quantity_kg": category_qty,
                    "subproducts": subproducts
                })

            # Start tracking a new main product
            current_category = name
            category_qty = quantity
            subproducts = []

        # Detect a subproduct row linked to the current main product
        elif "tb_subitem" in cell_classes and current_category:
            subproducts.append({
                "product": name,
                "quantity_kg": quantity
            })

    # Append the last product collected
    if current_category:
        results.append({
            "product": current_category,
            "quantity_kg": category_qty,
            "subproducts": subproducts
        })

    # Check if all entries are empty (quantities are "-")
    all_empty = all(
        item["quantity_kg"] == "-" and
        all(sub["quantity_kg"] == "-" for sub in item["subproducts"])
        for item in results
    )

    if all_empty:
        raise HTTPException(
            status_code=404,
            detail="No processamento data available for the specified year."
        )

    # Look for footer to obtain the total
    tfoot = table.find("tfoot", class_="tb_total")
    if tfoot:
        total_row = tfoot.find("tr")
        total_cols = total_row.find_all("td")
        if len(total_cols) == 2:
            total_value = total_cols[1].get_text(strip=True)
            results.append({
                "total_overall": total_value
            })

    return results
