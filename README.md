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
  A <a href="https://modelcontextprotocol.io">Model Context Protocol (MCP)</a> server for <strong>RajaOngkir API</strong> integration.<br>
  Enable any MCP-compatible AI assistant, agent, or application to calculate Indonesian shipping costs and track packages.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="https://modelcontextprotocol.io"><img src="https://img.shields.io/badge/MCP-Compatible-purple.svg" alt="MCP Compatible"></a>
</p>

---

<details>
<summary><strong>📖 Table of Contents</strong></summary>

- [Example Interactions](#example-interactions)
- [Tools](#tools)
  - [Location Search](#location-search)
  - [Hierarchical Location](#hierarchical-location)
  - [Cost Calculation](#cost-calculation)
  - [Package Tracking](#package-tracking)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Integration](#integration)
- [Supported Couriers](#supported-couriers)
- [License](#license)

</details>

---

## Example Interactions

<table>
  <tr>
    <td>💬</td>
    <td>"Calculate shipping cost from Jakarta to Surabaya for a 1kg package"</td>
  </tr>
  <tr>
    <td>💬</td>
    <td>"Compare JNE, SiCepat, and J&T prices from Bandung to Yogyakarta"</td>
  </tr>
  <tr>
    <td>💬</td>
    <td>"Track my package with AWB number JNE1234567890"</td>
  </tr>
  <tr>
    <td>💬</td>
    <td>"Show me all districts in Jakarta Pusat"</td>
  </tr>
</table>

---

## Tools

### Location Search

<table>
  <thead>
    <tr>
      <th width="200">Tool</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>search_domestic_destination</code></td>
      <td>
        <strong>Search for cities/districts in Indonesia</strong><br>
        <em>Parameters:</em> <code>query</code> (string)<br>
        <em>Example:</em> <code>search_domestic_destination("Jakarta")</code>
      </td>
    </tr>
    <tr>
      <td><code>search_international_destination</code></td>
      <td>
        <strong>Search for international countries</strong><br>
        <em>Parameters:</em> <code>query</code> (string)<br>
        <em>Example:</em> <code>search_international_destination("Singapore")</code>
      </td>
    </tr>
  </tbody>
</table>

### Hierarchical Location

<table>
  <thead>
    <tr>
      <th width="200">Tool</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>get_provinces</code></td>
      <td>
        <strong>Get all Indonesian provinces</strong><br>
        <em>Parameters:</em> None<br>
        <em>Example:</em> <code>get_provinces()</code>
      </td>
    </tr>
    <tr>
      <td><code>get_cities</code></td>
      <td>
        <strong>Get cities within a province</strong><br>
        <em>Parameters:</em> <code>province_id</code> (string)<br>
        <em>Example:</em> <code>get_cities("6")</code> → DKI Jakarta
      </td>
    </tr>
    <tr>
      <td><code>get_districts</code></td>
      <td>
        <strong>Get districts within a city</strong><br>
        <em>Parameters:</em> <code>city_id</code> (string)<br>
        <em>Example:</em> <code>get_districts("152")</code> → Jakarta Pusat
      </td>
    </tr>
    <tr>
      <td><code>get_subdistricts</code></td>
      <td>
        <strong>Get subdistricts within a district</strong><br>
        <em>Parameters:</em> <code>district_id</code> (string)<br>
        <em>Example:</em> <code>get_subdistricts("2096")</code>
      </td>
    </tr>
  </tbody>
</table>

### Cost Calculation

<table>
  <thead>
    <tr>
      <th width="200">Tool</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>calculate_domestic_cost</code></td>
      <td>
        <strong>Calculate domestic shipping cost</strong><br>
        <em>Parameters:</em> <code>origin</code>, <code>destination</code>, <code>weight</code>, <code>courier</code><br>
        <em>Example:</em> <code>calculate_domestic_cost("12345", "67890", 1000, "jne")</code>
      </td>
    </tr>
    <tr>
      <td><code>calculate_district_cost</code></td>
      <td>
        <strong>Calculate cost using district IDs (multi-courier support)</strong><br>
        <em>Parameters:</em> <code>origin</code>, <code>destination</code>, <code>weight</code>, <code>courier</code><br>
        <em>Example:</em> <code>calculate_district_cost("1391", "1376", 1000, "jne:sicepat:jnt")</code>
      </td>
    </tr>
    <tr>
      <td><code>calculate_international_cost</code></td>
      <td>
        <strong>Calculate international shipping cost</strong><br>
        <em>Parameters:</em> <code>origin</code>, <code>destination</code>, <code>weight</code>, <code>courier</code><br>
        <em>Example:</em> <code>calculate_international_cost("12345", "108", 1000, "pos")</code>
      </td>
    </tr>
  </tbody>
</table>

### Package Tracking

<table>
  <thead>
    <tr>
      <th width="200">Tool</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>track_package</code></td>
      <td>
        <strong>Track package by AWB/tracking number</strong><br>
        <em>Parameters:</em> <code>awb</code>, <code>courier</code><br>
        <em>Example:</em> <code>track_package("JNE1234567890", "jne")</code>
      </td>
    </tr>
  </tbody>
</table>

---

## Setup

### Prerequisites

<ul>
  <li>Python 3.10+</li>
  <li>RajaOngkir Komerce API Key (<a href="https://rajaongkir.komerce.id">Get it here</a>)</li>
</ul>

### Installation

```bash
git clone https://github.com/Arseno25/rajaongkir-mcp-server.git
cd rajaongkir-mcp-server
pip install -r requirements.txt
```

### Configuration

<ol>
  <li>Copy the example config file:</li>
</ol>

```bash
cp .env.example .env
```

<ol start="2">
  <li>Edit the file with your credentials:</li>
</ol>

```env
RAJAONGKIR_API_KEY=your-api-key-here
RAJAONGKIR_BASE_URL=https://rajaongkir.komerce.id/api/v1
```

<details>
<summary><strong>📋 Getting a RajaOngkir API Key</strong></summary>

1. Go to [RajaOngkir Komerce](https://rajaongkir.komerce.id)
2. Create an account or log in
3. Subscribe to a plan (free tier available)
4. Copy your API key from the dashboard

</details>

---

## Integration

This MCP server can be integrated with **any MCP-compatible client**, including:

- 🤖 **AI Assistants** - Claude Desktop, ChatGPT (with MCP support)
- 💻 **Code Editors** - Cursor, VS Code (via Cline/Continue extensions)
- 🔧 **AI Agents** - LangChain, AutoGPT, custom agents
- 📱 **Applications** - Any app implementing MCP protocol

<details open>
<summary><strong>Claude Desktop</strong></summary>

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rajaongkir": {
      "command": "python",
      "args": ["path/to/rajaongkir-mcp-server/server.py"],
      "env": {
        "RAJAONGKIR_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

</details>

<details>
<summary><strong>Cursor</strong></summary>

Go to **MCP tab** in Cursor Settings. Add a server with this command:

```
python path/to/rajaongkir-mcp-server/server.py
```

</details>

<details>
<summary><strong>VS Code (Cline Extension)</strong></summary>

Add to your `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "rajaongkir": {
      "command": "python",
      "args": ["path/to/rajaongkir-mcp-server/server.py"],
      "env": {
        "RAJAONGKIR_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

</details>

<details>
<summary><strong>Other MCP Clients</strong></summary>

For other MCP-compatible clients, use the following configuration:

- **Command:** `python`
- **Args:** `["path/to/rajaongkir-mcp-server/server.py"]`
- **Environment:**
  - `RAJAONGKIR_API_KEY`: Your RajaOngkir API key

Refer to your client's documentation for specific integration steps.

</details>

---

## Supported Couriers

<table>
  <thead>
    <tr>
      <th>Type</th>
      <th>Couriers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Domestic</strong></td>
      <td>JNE, SiCepat, J&T, POS Indonesia, TIKI, AnterAja, Ninja Xpress, Lion Parcel, ID Express, SAP, NCS, REX, RPX, Wahana, Sentral, Star, DSE, First, Indah, Pandu</td>
    </tr>
    <tr>
      <td><strong>International</strong></td>
      <td>POS Indonesia, JNE, TIKI, EMS</td>
    </tr>
  </tbody>
</table>

---

## Credits

<p>
  This project uses the following services and technologies:
</p>

<ul>
  <li><a href="https://rajaongkir.com">RajaOngkir</a> - Indonesian shipping cost API provider</li>
  <li><a href="https://modelcontextprotocol.io">Model Context Protocol</a> - MCP specification by Anthropic</li>
</ul>

---

## License

<p>
  This project is licensed under the <strong>MIT License</strong> - see the <a href="LICENSE">LICENSE</a> file for details.
</p>

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/Arseno25">Arseno Kalam</a>
</p>
