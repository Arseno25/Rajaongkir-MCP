<div align="center">
  <img src="https://storage.googleapis.com/komerce/rajaongkir/RO-by-Komerce.svg" alt="RajaOngkir by Komerce Logo" width="100">
  <br><br>
</div>

<h1 align="center">RajaOngkir MCP Server</h1>

<p align="center">
  <a href="README.md">🇬🇧 English</a> •
  <a href="README.id.md">🇮🇩 Bahasa Indonesia</a>
</p>

<p align="center">
  Server <a href="https://modelcontextprotocol.io">Model Context Protocol (MCP)</a> untuk integrasi <strong>RajaOngkir API</strong>.<br>
  Memungkinkan AI assistant, agent, atau aplikasi yang kompatibel dengan MCP untuk menghitung ongkir dan melacak paket di Indonesia.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="https://modelcontextprotocol.io"><img src="https://img.shields.io/badge/MCP-Compatible-purple.svg" alt="MCP Compatible"></a>
</p>

---

<details>
<summary><strong>📖 Daftar Isi</strong></summary>

- [Contoh Interaksi](#contoh-interaksi)
- [Tools](#tools)
  - [Pencarian Lokasi](#pencarian-lokasi)
  - [Lokasi Hierarkis](#lokasi-hierarkis)
  - [Kalkulasi Ongkir](#kalkulasi-ongkir)
  - [Lacak Paket](#lacak-paket)
- [Setup](#setup)
  - [Prasyarat](#prasyarat)
  - [Instalasi](#instalasi)
  - [Konfigurasi](#konfigurasi)
- [Integrasi](#integrasi)
- [Kurir yang Didukung](#kurir-yang-didukung)
- [Lisensi](#lisensi)

</details>

---

## Contoh Interaksi

<table>
  <tr>
    <td>💬</td>
    <td>"Hitung ongkir dari Jakarta ke Surabaya untuk paket 1kg"</td>
  </tr>
  <tr>
    <td>💬</td>
    <td>"Bandingkan harga JNE, SiCepat, dan J&T dari Bandung ke Yogyakarta"</td>
  </tr>
  <tr>
    <td>💬</td>
    <td>"Lacak paket saya dengan resi JNE1234567890"</td>
  </tr>
  <tr>
    <td>💬</td>
    <td>"Tampilkan semua kecamatan di Jakarta Pusat"</td>
  </tr>
</table>

---

## Tools

### Pencarian Lokasi

<table>
  <thead>
    <tr>
      <th width="200">Tool</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>search_domestic_destination</code></td>
      <td>
        <strong>Cari kota/kecamatan di Indonesia</strong><br>
        <em>Parameter:</em> <code>query</code> (string)<br>
        <em>Contoh:</em> <code>search_domestic_destination("Jakarta")</code>
      </td>
    </tr>
    <tr>
      <td><code>search_international_destination</code></td>
      <td>
        <strong>Cari negara tujuan internasional</strong><br>
        <em>Parameter:</em> <code>query</code> (string)<br>
        <em>Contoh:</em> <code>search_international_destination("Singapore")</code>
      </td>
    </tr>
  </tbody>
</table>

### Lokasi Hierarkis

<table>
  <thead>
    <tr>
      <th width="200">Tool</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>get_provinces</code></td>
      <td>
        <strong>Ambil semua provinsi Indonesia</strong><br>
        <em>Parameter:</em> Tidak ada<br>
        <em>Contoh:</em> <code>get_provinces()</code>
      </td>
    </tr>
    <tr>
      <td><code>get_cities</code></td>
      <td>
        <strong>Ambil kota dalam provinsi</strong><br>
        <em>Parameter:</em> <code>province_id</code> (string)<br>
        <em>Contoh:</em> <code>get_cities("6")</code> → DKI Jakarta
      </td>
    </tr>
    <tr>
      <td><code>get_districts</code></td>
      <td>
        <strong>Ambil kecamatan dalam kota</strong><br>
        <em>Parameter:</em> <code>city_id</code> (string)<br>
        <em>Contoh:</em> <code>get_districts("152")</code> → Jakarta Pusat
      </td>
    </tr>
    <tr>
      <td><code>get_subdistricts</code></td>
      <td>
        <strong>Ambil kelurahan dalam kecamatan</strong><br>
        <em>Parameter:</em> <code>district_id</code> (string)<br>
        <em>Contoh:</em> <code>get_subdistricts("2096")</code>
      </td>
    </tr>
  </tbody>
</table>

### Kalkulasi Ongkir

<table>
  <thead>
    <tr>
      <th width="200">Tool</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>calculate_domestic_cost</code></td>
      <td>
        <strong>Hitung ongkir domestik</strong><br>
        <em>Parameter:</em> <code>origin</code>, <code>destination</code>, <code>weight</code>, <code>courier</code><br>
        <em>Contoh:</em> <code>calculate_domestic_cost("12345", "67890", 1000, "jne")</code>
      </td>
    </tr>
    <tr>
      <td><code>calculate_district_cost</code></td>
      <td>
        <strong>Hitung ongkir pakai ID kecamatan (multi-kurir)</strong><br>
        <em>Parameter:</em> <code>origin</code>, <code>destination</code>, <code>weight</code>, <code>courier</code><br>
        <em>Contoh:</em> <code>calculate_district_cost("1391", "1376", 1000, "jne:sicepat:jnt")</code>
      </td>
    </tr>
    <tr>
      <td><code>calculate_international_cost</code></td>
      <td>
        <strong>Hitung ongkir internasional</strong><br>
        <em>Parameter:</em> <code>origin</code>, <code>destination</code>, <code>weight</code>, <code>courier</code><br>
        <em>Contoh:</em> <code>calculate_international_cost("12345", "108", 1000, "pos")</code>
      </td>
    </tr>
  </tbody>
</table>

### Lacak Paket

<table>
  <thead>
    <tr>
      <th width="200">Tool</th>
      <th>Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>track_package</code></td>
      <td>
        <strong>Lacak paket berdasarkan nomor resi</strong><br>
        <em>Parameter:</em> <code>awb</code>, <code>courier</code><br>
        <em>Contoh:</em> <code>track_package("JNE1234567890", "jne")</code>
      </td>
    </tr>
  </tbody>
</table>

---

## Setup

### Prasyarat

<ul>
  <li>Python 3.10+</li>
  <li>API Key RajaOngkir Komerce (<a href="https://rajaongkir.komerce.id">Daftar di sini</a>)</li>
</ul>

### Instalasi

```bash
git clone https://github.com/Arseno25/rajaongkir-mcp-server.git
cd rajaongkir-mcp-server
pip install -r requirements.txt
```

### Konfigurasi

<ol>
  <li>Copy file config contoh:</li>
</ol>

```bash
cp .env.example .env
```

<ol start="2">
  <li>Edit file dengan kredensial kamu:</li>
</ol>

```env
RAJAONGKIR_API_KEY=api-key-kamu
RAJAONGKIR_BASE_URL=https://rajaongkir.komerce.id/api/v1
```

<details>
<summary><strong>📋 Cara Mendapatkan API Key RajaOngkir</strong></summary>

1. Buka [RajaOngkir Komerce](https://rajaongkir.komerce.id)
2. Buat akun atau login
3. Subscribe ke paket (ada paket gratis)
4. Copy API key dari dashboard

</details>

---

## Integrasi

MCP server ini dapat diintegrasikan dengan **semua klien yang kompatibel dengan MCP**, termasuk:

- 🤖 **AI Assistant** - Claude Desktop, ChatGPT (dengan dukungan MCP)
- 💻 **Code Editor** - Cursor, VS Code (via Cline/Continue extensions)
- 🔧 **AI Agent** - LangChain, AutoGPT, custom agents
- 📱 **Aplikasi** - Aplikasi apapun yang mengimplementasikan protokol MCP

<details open>
<summary><strong>Claude Desktop</strong></summary>

Tambahkan ke `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rajaongkir": {
      "command": "python",
      "args": ["path/to/rajaongkir-mcp-server/server.py"],
      "env": {
        "RAJAONGKIR_API_KEY": "api-key-kamu"
      }
    }
  }
}
```

</details>

<details>
<summary><strong>Cursor</strong></summary>

Buka **MCP tab** di Cursor Settings. Tambahkan server dengan command:

```
python path/to/rajaongkir-mcp-server/server.py
```

</details>

<details>
<summary><strong>VS Code (Cline Extension)</strong></summary>

Tambahkan ke `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "rajaongkir": {
      "command": "python",
      "args": ["path/to/rajaongkir-mcp-server/server.py"],
      "env": {
        "RAJAONGKIR_API_KEY": "api-key-kamu"
      }
    }
  }
}
```

</details>

<details>
<summary><strong>Klien MCP Lainnya</strong></summary>

Untuk klien MCP lainnya, gunakan konfigurasi berikut:

- **Command:** `python`
- **Args:** `["path/to/rajaongkir-mcp-server/server.py"]`
- **Environment:**
  - `RAJAONGKIR_API_KEY`: API key RajaOngkir kamu

Lihat dokumentasi klien kamu untuk langkah integrasi spesifik.

</details>

---

## Kurir yang Didukung

<table>
  <thead>
    <tr>
      <th>Tipe</th>
      <th>Kurir</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Domestik</strong></td>
      <td>JNE, SiCepat, J&T, POS Indonesia, TIKI, AnterAja, Ninja Xpress, Lion Parcel, ID Express, SAP, NCS, REX, RPX, Wahana, Sentral, Star, DSE, First, Indah, Pandu</td>
    </tr>
    <tr>
      <td><strong>Internasional</strong></td>
      <td>POS Indonesia, JNE, TIKI, EMS</td>
    </tr>
  </tbody>
</table>

---

## Kredit

<p>
  Proyek ini menggunakan layanan dan teknologi berikut:
</p>

<ul>
  <li><a href="https://rajaongkir.com">RajaOngkir</a> - Penyedia API ongkos kirim Indonesia</li>
  <li><a href="https://modelcontextprotocol.io">Model Context Protocol</a> - Spesifikasi MCP oleh Anthropic</li>
</ul>

---

## Lisensi

<p>
  Proyek ini dilisensikan di bawah <strong>MIT License</strong> - lihat file <a href="LICENSE">LICENSE</a> untuk detail.
</p>

---

<p align="center">
  Dibuat dengan ❤️ oleh <a href="https://github.com/Arseno25">Arseno Kalam</a>
</p>
