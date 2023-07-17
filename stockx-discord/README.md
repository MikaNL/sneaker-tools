# StockX Bot for Discord

The StockX Bot for Discord is a handy bot that allows users to quickly search for products on StockX directly within their Discord server. By utilizing the `/stockx <query>`-command, users can easily find relevant information about products, such as their current market value, recent sales, and more.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/MikaNL/sneaker-tools.git
```

2. Install dependencies:

```bash
cd stockx-discord
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
   - Adjust any other settings as desired (e.g. bot token and guild ID).

5. Run the bot:

Windows:
```bash
py main.py
```

Mac/Linux:
```bash
pip3 main.py
```

## Contributing

Contributions are welcome! If you have any ideas, bug reports, or feature requests, please submit them as issues or make a pull request.

## License

Distributed under the GNU General Public License v3.0 License. See LICENSE for more information. Selling this code without my consent is strictly prohibited. If sharing this or an updated copy of this repo requires this repo to be made freely available.