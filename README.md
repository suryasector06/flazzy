# Flazzy - Currency CLI Tool

**Flazzy** is a simple and powerful Command-Line Interface (CLI) tool that allows you to check real-time currency exchange rates and perform currency conversions directly from your terminal.

---

##  Features

- Fetch real-time exchange rates from an external API
- Convert between different currencies with ease
- Display historical exchange rate line charts
- List all supported currencies

---

##  Installation

### Using pip

```bash
pip install flazzy
```

### Using pipx (recommended for CLI tools)

```bash
pipx install flazzy
```

---

##  Usage

```bash
flazzy [OPTIONS] COMMAND [ARGS]...
```

### Global Options

| Option      | Description                |
| ----------- | -------------------------- |
| `--version` | Show the version and exit  |
| `--help`    | Show help message and exit |

### Available Commands

| Command      | Description                                                                 |
| ------------ | --------------------------------------------------------------------------- |
| `chart`      | Generate a historical line chart showing exchange rate trends               |
| `currencies` | List all available currencies retrieved from the API                        |
| `exchange`   | Convert a specific amount from one currency to another                      |
| `rates`      | Display a table of current exchange rates based on a selected base currency |

---

##  Examples

### List all available currencies

```bash
flazzy currencies --list-all
```

### Convert 100 USD to EUR

```bash
flazzy exchange --from USD --to EUR --amount 100
```

### Show exchange rates from IDR to other currencies

```bash
flazzy rates --base IDR
```

### Display historical chart from USD to JPY

```bash
flazzy chart --from USD --to JPY
```

##  License

This project is licensed under the **GNU Lesser General Public License v2.1 or later (LGPL-2.1-or-later)**.

See the `LICENSE` file for full license text.

---

##  Contributing

Contributions, issues, and feature requests are welcome!

- Fork this repository
- Create a new branch for your changes
- Submit a pull request

 Feel free to open issues or discussions on [GitHub Repository](https://github.com/suryasector06/flazzy)

---

##  Related Links

-  PyPI: [https://pypi.org/project/flazzy/](https://pypi.org/project/flazzy/)
-  Source Code: [https://github.com/suryacluster06/flazzy](https://github.com/suryasector06/flazzy)
