import requests
from fastmcp import FastMCP

# Inisialisasi Server MCP Rick and Morty
mcp = FastMCP("RickAndMortyServer")

BASE_URL = "https://rickandmortyapi.com/api"

@mcp.tool()
def search_character(name: str) -> str:
    """Mencari informasi karakter Rick and Morty berdasarkan nama."""
    try:
        # Mengambil data dari API eksternal
        response = requests.get(f"{BASE_URL}/character/?name={name}", timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        char = data['results'][0]
        return f"Nama: {char['name']}\nStatus: {char['status']}\nSpesies: {char['species']}"
    except Exception as e:
        return f"Karakter '{name}' tidak ditemukan atau API sedang bermasalah."

@mcp.tool()
def get_location_info(location_id: int) -> str:
    """Mengambil detail lokasi/planet berdasarkan ID (1-126)."""
    try:
        response = requests.get(f"{BASE_URL}/location/{location_id}", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return f"Lokasi: {data['name']}\nTipe: {data['type']}\nDimensi: {data['dimension']}"
    except Exception as e:
        return f"Gagal mengambil data lokasi ID {location_id}."

if __name__ == "__main__":
    mcp.run()