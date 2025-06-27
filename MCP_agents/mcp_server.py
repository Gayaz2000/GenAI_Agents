from mcp.server.fastmcp import FastMCP
import httpx

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

mcp = FastMCP("crypto-price-tracker")

@mcp.tool()
async def get_crypto_price(crypto_id: str, currency: str = "inr"):
    """
    Get the current price of a cryptocurrency in the specified currency.

    Parameters:
        crypto_id: The ID of the cryptocurrency (e.g., 'bitcoin', 'ethereum')
        currency: The currency in which to display the price (default='inr')

    Returns:
        Current price information as a formatted string.
    """
    url = f"{COINGECKO_BASE_URL}/simple/price"
    params = {
        "ids": crypto_id,
        "vs_currencies": currency
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, params=params)
            response.raise_for_status()
            data = await response.json()

            if crypto_id not in data or currency not in data[crypto_id]:
                return f"Price data for {crypto_id} in {currency} not found. Please check your input."

            price = data[crypto_id][currency]
            return f"The current price of {crypto_id.capitalize()} is {price} {currency.upper()}"

    except httpx.HTTPStatusError as e:
        return f"API error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error fetching price data: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
