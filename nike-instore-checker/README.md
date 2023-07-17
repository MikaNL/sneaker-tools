# Nike instore Bot

The Nike instore bot is a Discord bot designed to provide information about Nike products available in physical stores near a specific location. It utilizes the `/nikeinstore` command with three parameters: PID (Product ID), address, and max distance.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/MikaNL/sneaker-tools.git
```

2. Install dependencies:

```bash
cd nike-instore-checker
```

Windows:
```bash
py -m pip install -r requirements.txt
```

Mac/Linux:
```bash
pip3 install requirements.txt
```

3. Set up a Discord bot:

   - Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
   - Under the "Bot" tab, click on "Add Bot" to create a bot for your application.
   - Copy the bot token for later use.

4. Configure the bot:

   - Open the `config.json` file.
   - Adjust any other settings as desired (e.g. distance unit and country code).

   Country | 2 Letter Country Code | Language Code
   --------|-----------------------|--------------
   United Kingdom | GB | en
   United States | US | en
   Australia | AU | en
   Austria | AT | en / de
   Belgium | BE | en / nl / de / fr
   Bulgaria | BG | en
   Canada | CA | en / fr
   Chile | CL | es
   China | CN | zh
   Croatia | HR | en
   Czechia | CZ | en / cs
   Denmark | DK | en / da
   Egypt | EG | en
   Finland | FI | en
   France | FR | fr
   Germany | DE | de
   Hungary | HU | en
   India | IN | en
   Indonesia | ID | en
   Ireland | IE | en
   Italy | IT | it
   Malaysia | MY | en
   Mexico | MX | es
   Morocco | MA | en / fr
   Netherlands | NL | en / nl 
   New Zealand | NZ | en
   Norway | NO | en / no
   Philippines | PH | en 
   Poland | PL | pl
   Portugal | PT | en / es
   Puerto Rico | PR | es
   Romania | RO | en
   Russia | RU | ru
   Saudi Arabia | SA | en
   Singapore | SG | en
   Slovenia | SI | en   
   South Africa | ZA | en
   Spain | ES | es / ca
   Sweden | SE | en / sv
   Switzerland | CH | en / fr / de / it 
   Turkey | TR | tr
   UAE | AE | en
   Vietnam | VN | en
   
   <sub><sup>Thanks to yasserqureshi1 for the table.</sup></sub>

5. Run the bot:

Windows:
```bash
py main.py
```

Mac/Linux:
```bash
pip3 main.py
```

## Usage

The bot uses the following command format:

```
/nikeinstore <PID> <address> <max_distance>
```

- `<PID>`: The Product ID of the Nike product you want to search for.
- `<address>`: The address or location around which to search for Nike stores.
- `<max_distance>`: The maximum distance (in the pre-described unit) within which to search for stores.

Example command:

```
/nikeinstore pid:12345 address:Kalverstraat 1 Amsterdam max_distance:10
```

## Features

- Retrieves information about Nike products available in physical stores.
- Searches for stores based on location and maximum distance.
- Provides details such as store names, addresses, and product availability.

## Contributing

Contributions are welcome! If you have any ideas, bug reports, or feature requests, please submit them as issues or make a pull request.

## License

Distributed under the GNU General Public License v3.0 License. See LICENSE for more information. Selling this code without my consent is strictly prohibited. If sharing this or an updated copy of this repo requires this repo to be made freely available.