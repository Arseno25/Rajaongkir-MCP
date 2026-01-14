# 🚀 MCP Server - RajaOngkir Komerce V2

<p align="center">
  <a href="README.md">🇬🇧 English</a> •
  <a href="README.id.md">🇮🇩 Bahasa Indonesia</a>
</p>

Production-ready **MCP (Model Context Protocol)** server untuk **RajaOngkir API Komerce V2**.

> ✅ Lengkap dengan validasi input, error handling, dan standardized responses.

---

## 📦 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env → tambahkan RAJAONGKIR_API_KEY

# Run server
python server.py

# Test dengan MCP Inspector
npx -y @modelcontextprotocol/inspector .venv\Scripts\python server.py
```

---

## 🔧 Daftar Tools (10 Tools)

### 🔍 Method 1: Search (Pencarian Langsung)

#### `search_domestic_destination(query: str)`
Cari lokasi domestik (kota/kabupaten/kecamatan) di Indonesia.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Tipe</th>
      <th>Wajib</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>query</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Nama lokasi yang dicari (min 1 karakter)</td>
    </tr>
  </tbody>
</table>

**Contoh:**
```python
await search_domestic_destination("Jakarta")
await search_domestic_destination("Surabaya")
await search_domestic_destination("Bandung")
```

---

#### `search_international_destination(query: str)`
Cari lokasi internasional (negara).

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Tipe</th>
      <th>Wajib</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>query</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Nama negara yang dicari</td>
    </tr>
  </tbody>
</table>

**Contoh:**
```python
await search_international_destination("Singapore")
await search_international_destination("Malaysia")
await search_international_destination("Japan")
```

---

#### `calculate_domestic_cost(origin, destination, weight, courier)`
Hitung ongkos kirim domestik menggunakan ID dari hasil pencarian.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Tipe</th>
      <th>Wajib</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>origin</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>ID lokasi asal (dari search_domestic)</td>
    </tr>
    <tr>
      <td><code>destination</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>ID lokasi tujuan (dari search_domestic)</td>
    </tr>
    <tr>
      <td><code>weight</code></td>
      <td><code>int</code></td>
      <td align="center">✅</td>
      <td>Berat paket dalam gram (1 - 500.000)</td>
    </tr>
    <tr>
      <td><code>courier</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Kode kurir: jne, sicepat, jnt, pos, tiki, dll</td>
    </tr>
  </tbody>
</table>

**Contoh:**
```python
await calculate_domestic_cost("12345", "67890", 1000, "jne")
await calculate_domestic_cost("12345", "67890", 2500, "sicepat")
```

---

#### `calculate_international_cost(origin, destination, weight, courier)`
Hitung ongkos kirim internasional.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Tipe</th>
      <th>Wajib</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>origin</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>ID lokasi asal (Indonesia)</td>
    </tr>
    <tr>
      <td><code>destination</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>ID negara tujuan</td>
    </tr>
    <tr>
      <td><code>weight</code></td>
      <td><code>int</code></td>
      <td align="center">✅</td>
      <td>Berat paket dalam gram</td>
    </tr>
    <tr>
      <td><code>courier</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Kode kurir: pos, jne, tiki, pcp, ems</td>
    </tr>
  </tbody>
</table>

**Contoh:**
```python
await calculate_international_cost("12345", "108", 1000, "pos")
```

---

### 🗂️ Method 2: Step-by-Step (Hierarkis)

Cocok untuk **cascading dropdowns**: Provinsi → Kota → Kecamatan → Kelurahan

#### `get_provinces()`
Ambil daftar semua provinsi di Indonesia.

<table>
  <thead>
    <tr>
      <th>Return Field</th>
      <th>Tipe</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>province_id</code></td>
      <td><code>str</code></td>
      <td>ID provinsi</td>
    </tr>
    <tr>
      <td><code>province</code></td>
      <td><code>str</code></td>
      <td>Nama provinsi</td>
    </tr>
  </tbody>
</table>

**Contoh:**
```python
provinces = await get_provinces()
# Output: [{"province_id": "1", "province": "Bali"}, ...]
```

---

#### `get_cities(province_id: str)`
Ambil daftar kota/kabupaten dalam provinsi.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Tipe</th>
      <th>Wajib</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>province_id</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>ID provinsi dari get_provinces()</td>
    </tr>
  </tbody>
</table>

**Contoh:**
```python
cities = await get_cities("6")   # DKI Jakarta
cities = await get_cities("9")   # Jawa Barat
cities = await get_cities("11")  # Jawa Tengah
```

---

#### `get_districts(city_id: str)`
Ambil daftar kecamatan dalam kota.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Tipe</th>
      <th>Wajib</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>city_id</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>ID kota dari get_cities()</td>
    </tr>
  </tbody>
</table>

**Contoh:**
```python
districts = await get_districts("152")  # Jakarta Pusat
districts = await get_districts("22")   # Bandung
districts = await get_districts("444")  # Surabaya
```

---

#### `get_subdistricts(district_id: str)`
Ambil daftar kelurahan dalam kecamatan (opsional, untuk presisi maksimal).

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Tipe</th>
      <th>Wajib</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>district_id</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>ID kecamatan dari get_districts()</td>
    </tr>
  </tbody>
</table>

**Contoh:**
```python
subdistricts = await get_subdistricts("2096")
subdistricts = await get_subdistricts("2097")
```

---

#### `calculate_district_cost(origin, destination, weight, courier)`
Hitung ongkos kirim menggunakan ID kecamatan. Mendukung **multiple couriers**.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Tipe</th>
      <th>Wajib</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>origin</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>ID kecamatan asal</td>
    </tr>
    <tr>
      <td><code>destination</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>ID kecamatan tujuan</td>
    </tr>
    <tr>
      <td><code>weight</code></td>
      <td><code>int</code></td>
      <td align="center">✅</td>
      <td>Berat paket dalam gram (1 - 500.000)</td>
    </tr>
    <tr>
      <td><code>courier</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Kode kurir (bisa multiple dengan <code>:</code>)</td>
    </tr>
  </tbody>
</table>

**Contoh Single Courier:**
```python
await calculate_district_cost("1391", "1376", 1000, "jne")
await calculate_district_cost("1391", "1376", 1500, "sicepat")
```

**Contoh Multiple Couriers:**
```python
await calculate_district_cost("1391", "1376", 1000, "jne:sicepat:jnt")
await calculate_district_cost("1391", "1376", 1000, "jne:sicepat:anteraja:pos:tiki")
```

---

### 📦 Tracking

#### `track_package(awb: str, courier: str)`
Lacak paket berdasarkan nomor resi.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Tipe</th>
      <th>Wajib</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>awb</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Nomor resi/AWB (5-50 karakter)</td>
    </tr>
    <tr>
      <td><code>courier</code></td>
      <td><code>str</code></td>
      <td align="center">✅</td>
      <td>Kode kurir</td>
    </tr>
  </tbody>
</table>

**Contoh:**
```python
await track_package("JNE1234567890", "jne")
await track_package("SICEPAT001234567", "sicepat")
await track_package("JP1234567890", "jnt")
```

---

## 📋 Flow Step-by-Step

```
┌──────────────────────────────────────────────────────────────┐
│  STEP 1: get_provinces()                                     │
│  → Pilih provinsi, dapatkan province_id                      │
└──────────────────────────────────────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────┐
│  STEP 2: get_cities(province_id)                             │
│  → Pilih kota, dapatkan city_id                              │
└──────────────────────────────────────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────┐
│  STEP 3: get_districts(city_id)                              │
│  → Pilih kecamatan, dapatkan district_id                     │
└──────────────────────────────────────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────┐
│  STEP 4 (Opsional): get_subdistricts(district_id)            │
│  → Pilih kelurahan untuk presisi maksimal                    │
└──────────────────────────────────────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────┐
│  STEP 5: calculate_district_cost(origin, dest, weight, ...)  │
│  → Dapatkan ongkos kirim dari berbagai kurir                 │
└──────────────────────────────────────────────────────────────┘
```

---

## ✅ Response Format

Semua tools mengembalikan response dengan format yang konsisten.

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

## 🛡️ Validasi Input

Semua input divalidasi sebelum request ke API:

<table>
  <thead>
    <tr>
      <th>Input</th>
      <th>Tipe</th>
      <th>Rules</th>
      <th>Contoh Valid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>query</code></td>
      <td><code>string</code></td>
      <td>Tidak boleh kosong, min 1 karakter</td>
      <td><code>"Jakarta"</code></td>
    </tr>
    <tr>
      <td><code>ID</code></td>
      <td><code>string</code></td>
      <td>Harus berupa angka</td>
      <td><code>"152"</code>, <code>"1391"</code></td>
    </tr>
    <tr>
      <td><code>weight</code></td>
      <td><code>int</code></td>
      <td>Range: 1 - 500.000 gram</td>
      <td><code>1000</code>, <code>2500</code></td>
    </tr>
    <tr>
      <td><code>courier</code></td>
      <td><code>string</code></td>
      <td>Harus dari daftar kurir valid</td>
      <td><code>"jne"</code>, <code>"jne:sicepat"</code></td>
    </tr>
    <tr>
      <td><code>awb</code></td>
      <td><code>string</code></td>
      <td>Panjang: 5 - 50 karakter</td>
      <td><code>"JNE1234567890"</code></td>
    </tr>
  </tbody>
</table>

---

## 📦 Kurir yang Didukung

### Kurir Domestik

<table>
  <thead>
    <tr>
      <th>Kode</th>
      <th>Nama Kurir</th>
      <th>Kode</th>
      <th>Nama Kurir</th>
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

### Kurir Internasional

<table>
  <thead>
    <tr>
      <th>Kode</th>
      <th>Nama Kurir</th>
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
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>CONFIG_ERROR</code></td>
      <td align="center">-</td>
      <td>API key tidak dikonfigurasi</td>
    </tr>
    <tr>
      <td><code>VALIDATION_ERROR</code></td>
      <td align="center">-</td>
      <td>Input tidak valid</td>
    </tr>
    <tr>
      <td><code>API_ERROR_400</code></td>
      <td align="center">400</td>
      <td>Bad request - parameter salah</td>
    </tr>
    <tr>
      <td><code>API_ERROR_401</code></td>
      <td align="center">401</td>
      <td>API key tidak valid</td>
    </tr>
    <tr>
      <td><code>API_ERROR_403</code></td>
      <td align="center">403</td>
      <td>API key tidak punya akses</td>
    </tr>
    <tr>
      <td><code>API_ERROR_404</code></td>
      <td align="center">404</td>
      <td>Data tidak ditemukan</td>
    </tr>
    <tr>
      <td><code>API_ERROR_429</code></td>
      <td align="center">429</td>
      <td>Rate limit exceeded</td>
    </tr>
    <tr>
      <td><code>NETWORK_ERROR</code></td>
      <td align="center">-</td>
      <td>Koneksi gagal / timeout</td>
    </tr>
    <tr>
      <td><code>UNEXPECTED_ERROR</code></td>
      <td align="center">-</td>
      <td>Error tidak terduga</td>
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
      <th>Wajib</th>
      <th>Deskripsi</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>RAJAONGKIR_API_KEY</code></td>
      <td align="center">✅</td>
      <td>API key dari RajaOngkir</td>
      <td>-</td>
    </tr>
    <tr>
      <td><code>RAJAONGKIR_BASE_URL</code></td>
      <td align="center">❌</td>
      <td>Base URL API</td>
      <td><code>https://rajaongkir.komerce.id/api/v1</code></td>
    </tr>
  </tbody>
</table>

---

## 📝 License

MIT License
