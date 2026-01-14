# 🚀 MCP Server - RajaOngkir Komerce V2

<p align="center">
  <a href="README.md">🇬🇧 English</a> •
  <a href="README.id.md">🇮🇩 Bahasa Indonesia</a>
</p>

Production-ready **MCP (Model Context Protocol)** server for **RajaOngkir Komerce V2 API**.

> ✅ Complete with input validation, error handling, and standardized responses.

---

## 📦 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env → add your RAJAONGKIR_API_KEY

# Run server
python server.py

# Test with MCP Inspector
npx -y @modelcontextprotocol/inspector .venv\Scripts\python server.py
```

---

## 🔧 Available Tools (10 Tools)

### 🔍 Method 1: Search (Direct Search)

#### `search_domestic_destination(query: str)`
Search for domestic locations (cities/districts) in Indonesia.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>query</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Location name to search (min 1 character)</td>
    </tr>
  </tbody>
</table>

**Example:**
```python
await search_domestic_destination("Jakarta")
await search_domestic_destination("Surabaya")
await search_domestic_destination("Bandung")
```

---

#### `search_international_destination(query: str)`
Search for international locations (countries).

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>query</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Country name to search</td>
    </tr>
  </tbody>
</table>

**Example:**
```python
await search_international_destination("Singapore")
await search_international_destination("Malaysia")
await search_international_destination("Japan")
```

---

#### `calculate_domestic_cost(origin, destination, weight, courier)`
Calculate domestic shipping cost using IDs from search results.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>origin</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Origin location ID (from search_domestic)</td>
    </tr>
    <tr>
      <td><code>destination</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Destination location ID (from search_domestic)</td>
    </tr>
    <tr>
      <td><code>weight</code></td>
      <td><code>int</code></td>
      <td align="center">✅</td>
      <td>Package weight in grams (1 - 500,000)</td>
    </tr>
    <tr>
      <td><code>courier</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Courier code: jne, sicepat, jnt, pos, tiki, etc</td>
    </tr>
  </tbody>
</table>

**Example:**
```python
await calculate_domestic_cost("12345", "67890", 1000, "jne")
await calculate_domestic_cost("12345", "67890", 2500, "sicepat")
```

---

#### `calculate_international_cost(origin, destination, weight, courier)`
Calculate international shipping cost.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>origin</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Origin location ID (Indonesia)</td>
    </tr>
    <tr>
      <td><code>destination</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Destination country ID</td>
    </tr>
    <tr>
      <td><code>weight</code></td>
      <td><code>int</code></td>
      <td align="center">✅</td>
      <td>Package weight in grams</td>
    </tr>
    <tr>
      <td><code>courier</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Courier code: pos, jne, tiki, pcp, ems</td>
    </tr>
  </tbody>
</table>

**Example:**
```python
await calculate_international_cost("12345", "108", 1000, "pos")
```

---

### 🗂️ Method 2: Step-by-Step (Hierarchical)

Perfect for **cascading dropdowns**: Province → City → District → Subdistrict

#### `get_provinces()`
Get list of all Indonesian provinces.

<table>
  <thead>
    <tr>
      <th>Return Field</th>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>province_id</code></td>
      <td><code>str</code></td>
      <td>Province ID</td>
    </tr>
    <tr>
      <td><code>province</code></td>
      <td><code>str</code></td>
      <td>Province name</td>
    </tr>
  </tbody>
</table>

**Example:**
```python
provinces = await get_provinces()
# Output: [{"province_id": "1", "province": "Bali"}, ...]
```

---

#### `get_cities(province_id: str)`
Get list of cities/regencies within a province.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>province_id</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Province ID from get_provinces()</td>
    </tr>
  </tbody>
</table>

**Example:**
```python
cities = await get_cities("6")   # DKI Jakarta
cities = await get_cities("9")   # West Java
cities = await get_cities("11")  # Central Java
```

---

#### `get_districts(city_id: str)`
Get list of districts within a city.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>city_id</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>City ID from get_cities()</td>
    </tr>
  </tbody>
</table>

**Example:**
```python
districts = await get_districts("152")  # Central Jakarta
districts = await get_districts("22")   # Bandung
districts = await get_districts("444")  # Surabaya
```

---

#### `get_subdistricts(district_id: str)`
Get list of subdistricts within a district (optional, for maximum precision).

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>district_id</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>District ID from get_districts()</td>
    </tr>
  </tbody>
</table>

**Example:**
```python
subdistricts = await get_subdistricts("2096")
subdistricts = await get_subdistricts("2097")
```

---

#### `calculate_district_cost(origin, destination, weight, courier)`
Calculate shipping cost using district IDs. Supports **multiple couriers**.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>origin</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Origin district ID</td>
    </tr>
    <tr>
      <td><code>destination</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Destination district ID</td>
    </tr>
    <tr>
      <td><code>weight</code></td>
      <td><code>int</code></td>
      <td align="center">✅</td>
      <td>Package weight in grams (1 - 500,000)</td>
    </tr>
    <tr>
      <td><code>courier</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Courier code (multiple with <code>:</code>)</td>
    </tr>
  </tbody>
</table>

**Single Courier Example:**
```python
await calculate_district_cost("1391", "1376", 1000, "jne")
await calculate_district_cost("1391", "1376", 1500, "sicepat")
```

**Multiple Couriers Example:**
```python
await calculate_district_cost("1391", "1376", 1000, "jne:sicepat:jnt")
await calculate_district_cost("1391", "1376", 1000, "jne:sicepat:anteraja:pos:tiki")
```

---

### 📦 Tracking

#### `track_package(awb: str, courier: str)`
Track package by tracking number.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>awb</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Tracking/AWB number (5-50 characters)</td>
    </tr>
    <tr>
      <td><code>courier</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Courier code</td>
    </tr>
  </tbody>
</table>

**Example:**
```python
await track_package("JNE1234567890", "jne")
await track_package("SICEPAT001234567", "sicepat")
await track_package("JP1234567890", "jnt")
```

---

## 📋 Step-by-Step Flow

```
┌──────────────────────────────────────────────────────────────┐
│  STEP 1: get_provinces()                                     │
│  → Select province, get province_id                          │
└──────────────────────────────────────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────┐
│  STEP 2: get_cities(province_id)                             │
│  → Select city, get city_id                                  │
└──────────────────────────────────────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────┐
│  STEP 3: get_districts(city_id)                              │
│  → Select district, get district_id                          │
└──────────────────────────────────────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────┐
│  STEP 4 (Optional): get_subdistricts(district_id)            │
│  → Select subdistrict for maximum precision                  │
└──────────────────────────────────────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────┐
│  STEP 5: calculate_district_cost(origin, dest, weight, ...)  │
│  → Get shipping costs from various couriers                  │
└──────────────────────────────────────────────────────────────┘
```

---

## ✅ Response Format

All tools return consistent response format.

### Success Response
```json
{
    "success": true,
    "data": [...],
    "message": "Found 34 provinces",
    "meta": {
        "count": 34
    }
}
```

### Error Response
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Weight must be greater than 0",
        "detail": "Please provide a positive weight in grams."
    }
}
```

---

## 🛡️ Input Validation

All inputs are validated before API requests:

<table>
  <thead>
    <tr>
      <th>Input</th>
      <th>Type</th>
      <th>Rules</th>
      <th>Valid Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>query</code></td>
      <td><code>string</code></td>
      <td>Cannot be empty, min 1 character</td>
      <td><code>"Jakarta"</code></td>
    </tr>
    <tr>
      <td><code>ID</code></td>
      <td><code>string</code></td>
      <td>Must be numeric</td>
      <td><code>"152"</code>, <code>"1391"</code></td>
    </tr>
    <tr>
      <td><code>weight</code></td>
      <td><code>int</code></td>
      <td>Range: 1 - 500,000 grams</td>
      <td><code>1000</code>, <code>2500</code></td>
    </tr>
    <tr>
      <td><code>courier</code></td>
      <td><code>string</code></td>
      <td>Must be from valid courier list</td>
      <td><code>"jne"</code>, <code>"jne:sicepat"</code></td>
    </tr>
    <tr>
      <td><code>awb</code></td>
      <td><code>string</code></td>
      <td>Length: 5 - 50 characters</td>
      <td><code>"JNE1234567890"</code></td>
    </tr>
  </tbody>
</table>

---

## 📦 Supported Couriers

### Domestic Couriers

<table>
  <thead>
    <tr>
      <th>Code</th>
      <th>Courier Name</th>
      <th>Code</th>
      <th>Courier Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>jne</code></td>
      <td>JNE Express</td>
      <td><code>ninja</code></td>
      <td>Ninja Xpress</td>
    </tr>
    <tr>
      <td><code>sicepat</code></td>
      <td>SiCepat Express</td>
      <td><code>lion</code></td>
      <td>Lion Parcel</td>
    </tr>
    <tr>
      <td><code>jnt</code></td>
      <td>J&T Express</td>
      <td><code>ide</code></td>
      <td>ID Express</td>
    </tr>
    <tr>
      <td><code>pos</code></td>
      <td>POS Indonesia</td>
      <td><code>sap</code></td>
      <td>SAP Express</td>
    </tr>
    <tr>
      <td><code>tiki</code></td>
      <td>TIKI</td>
      <td><code>ncs</code></td>
      <td>NCS Cargo</td>
    </tr>
    <tr>
      <td><code>anteraja</code></td>
      <td>AnterAja</td>
      <td><code>rex</code></td>
      <td>REX Express</td>
    </tr>
    <tr>
      <td><code>rpx</code></td>
      <td>RPX</td>
      <td><code>wahana</code></td>
      <td>Wahana</td>
    </tr>
    <tr>
      <td><code>sentral</code></td>
      <td>Sentral Cargo</td>
      <td><code>dse</code></td>
      <td>DSE</td>
    </tr>
    <tr>
      <td><code>star</code></td>
      <td>Star Cargo</td>
      <td><code>first</code></td>
      <td>First Logistics</td>
    </tr>
    <tr>
      <td><code>indah</code></td>
      <td>Indah Cargo</td>
      <td><code>pandu</code></td>
      <td>Pandu Logistics</td>
    </tr>
  </tbody>
</table>

### International Couriers

<table>
  <thead>
    <tr>
      <th>Code</th>
      <th>Courier Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>pos</code></td>
      <td>POS Indonesia</td>
    </tr>
    <tr>
      <td><code>jne</code></td>
      <td>JNE International</td>
    </tr>
    <tr>
      <td><code>tiki</code></td>
      <td>TIKI International</td>
    </tr>
    <tr>
      <td><code>pcp</code></td>
      <td>Priority Cargo</td>
    </tr>
    <tr>
      <td><code>ems</code></td>
      <td>Express Mail Service</td>
    </tr>
  </tbody>
</table>

---

## 🔴 Error Codes

<table>
  <thead>
    <tr>
      <th>Code</th>
      <th>HTTP</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>CONFIG_ERROR</code></td>
      <td align="center">-</td>
      <td>API key not configured</td>
    </tr>
    <tr>
      <td><code>VALIDATION_ERROR</code></td>
      <td align="center">-</td>
      <td>Invalid input</td>
    </tr>
    <tr>
      <td><code>API_ERROR_400</code></td>
      <td align="center">400</td>
      <td>Bad request - invalid parameters</td>
    </tr>
    <tr>
      <td><code>API_ERROR_401</code></td>
      <td align="center">401</td>
      <td>Invalid API key</td>
    </tr>
    <tr>
      <td><code>API_ERROR_403</code></td>
      <td align="center">403</td>
      <td>API key has no access</td>
    </tr>
    <tr>
      <td><code>API_ERROR_404</code></td>
      <td align="center">404</td>
      <td>Data not found</td>
    </tr>
    <tr>
      <td><code>API_ERROR_429</code></td>
      <td align="center">429</td>
      <td>Rate limit exceeded</td>
    </tr>
    <tr>
      <td><code>NETWORK_ERROR</code></td>
      <td align="center">-</td>
      <td>Connection failed / timeout</td>
    </tr>
    <tr>
      <td><code>UNEXPECTED_ERROR</code></td>
      <td align="center">-</td>
      <td>Unexpected error</td>
    </tr>
  </tbody>
</table>

---

## 📡 API Endpoints Reference

<table>
  <thead>
    <tr>
      <th>Tool</th>
      <th>Endpoint</th>
      <th>Method</th>
      <th>Payload</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>search_domestic_destination</code></td>
      <td><code>/destination/domestic-destination</code></td>
      <td align="center">GET</td>
      <td>Query</td>
    </tr>
    <tr>
      <td><code>search_international_destination</code></td>
      <td><code>/destination/international-destination</code></td>
      <td align="center">GET</td>
      <td>Query</td>
    </tr>
    <tr>
      <td><code>get_provinces</code></td>
      <td><code>/destination/province</code></td>
      <td align="center">GET</td>
      <td>-</td>
    </tr>
    <tr>
      <td><code>get_cities</code></td>
      <td><code>/destination/city/{id}</code></td>
      <td align="center">GET</td>
      <td>Path</td>
    </tr>
    <tr>
      <td><code>get_districts</code></td>
      <td><code>/destination/district/{id}</code></td>
      <td align="center">GET</td>
      <td>Path</td>
    </tr>
    <tr>
      <td><code>get_subdistricts</code></td>
      <td><code>/destination/sub-district/{id}</code></td>
      <td align="center">GET</td>
      <td>Path</td>
    </tr>
    <tr>
      <td><code>calculate_domestic_cost</code></td>
      <td><code>/calculate/domestic-cost</code></td>
      <td align="center">POST</td>
      <td>Form</td>
    </tr>
    <tr>
      <td><code>calculate_district_cost</code></td>
      <td><code>/calculate/district/domestic-cost</code></td>
      <td align="center">POST</td>
      <td>Form</td>
    </tr>
    <tr>
      <td><code>calculate_international_cost</code></td>
      <td><code>/calculate/international-cost</code></td>
      <td align="center">POST</td>
      <td>Form</td>
    </tr>
    <tr>
      <td><code>track_package</code></td>
      <td><code>/track/waybill</code></td>
      <td align="center">POST</td>
      <td>Query</td>
    </tr>
  </tbody>
</table>

---

## 🧪 Testing

### MCP Inspector (Recommended)
```bash
npx -y @modelcontextprotocol/inspector .venv\Scripts\python server.py
```

### Test Script
```bash
python test_tools.py
```

### Manual Python Test
```python
import asyncio
from src.tools import get_provinces, get_cities, calculate_district_cost

async def main():
    # Get provinces
    provinces = await get_provinces()
    print(provinces)
    
    # Get cities in DKI Jakarta
    cities = await get_cities("6")
    print(cities)
    
    # Calculate shipping cost
    cost = await calculate_district_cost("1391", "1376", 1000, "jne:sicepat")
    print(cost)

asyncio.run(main())
```

---

## ⚙️ Environment Variables

<table>
  <thead>
    <tr>
      <th>Variable</th>
      <th>Required</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>RAJAONGKIR_API_KEY</code></td>
      <td align="center">✅</td>
      <td>API key from RajaOngkir</td>
      <td>-</td>
    </tr>
    <tr>
      <td><code>RAJAONGKIR_BASE_URL</code></td>
      <td align="center">❌</td>
      <td>API Base URL</td>
      <td><code>https://rajaongkir.komerce.id/api/v1</code></td>
    </tr>
  </tbody>
</table>

---

## 📝 License

MIT License
