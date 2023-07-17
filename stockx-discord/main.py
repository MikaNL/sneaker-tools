import discord, os, json
from discord import app_commands
from discord.ext import commands
from classes import stockx

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

with open("config.json", "r") as f:
    config = json.load(f)

for keys, value in config.items():
    if not value:
        print(f"{keys} is not set in config.json")
        exit()

sx = stockx.StockX()

class Select(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder="Select a product",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):
        productInfo = sx.getProductInfo(self.values[0])['data']['product']
        embed = discord.Embed(title=f"{productInfo['title']}", url=f"https://stockx.com/{productInfo['urlKey']}", color=config['embed_color'])
        embed.set_thumbnail(url=productInfo['media']['imageUrl'])
        embed.set_author(name="https://stockx.com/", url="https://stockx.com/")
        embed.add_field(name="Colorway", value=f"{productInfo['traits'][1]['value']}", inline=True)
        embed.add_field(name="SKU", value=f"{productInfo['styleId']}", inline=True)
        embed.add_field(name="Retail Price", value=f"${productInfo['traits'][2]['value']}", inline=True)
        embed.add_field(name="Last Sale", value=f"{productInfo['market']['salesInformation']['lastSale']}", inline=True)
        embed.add_field(name="Sales past 72 hours", value=f"{productInfo['market']['salesInformation']['salesLast72Hours']}", inline=True)
        embed.add_field(name="Highest Bid", value=f"${productInfo['market']['bidAskData']['highestBid']}", inline=True)
        embed.add_field(name="Lowest Ask", value=f"${productInfo['market']['bidAskData']['lowestAsk']}", inline=True)
        embed.add_field(name="Number of asks", value=f"{productInfo['market']['bidAskData']['numberOfAsks']}", inline=True)
        embed.add_field(name="Number of bids", value=f"{productInfo['market']['bidAskData']['numberOfBids']}", inline=True)
        embed.set_footer(text="• Made by @bontje34", icon_url="https://bontes.net/assets/img/logo.png")
        await interaction.response.send_message(embed=embed)
        

class SelectView(discord.ui.View):
    def __init__(self, options, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select(options))

@tree.command(name="stockx", description="Search for a product on StockX", guild=discord.Object(id=config["guild_id"]))
@app_commands.describe(query="The product you want to search for")
async def stockx(interaction: discord.Interaction, query: str):
    global sx
    products = []
    results = sx.search(query)
    if results['data']['browse']['results']['edges'] == []:
        await interaction.response.send_message("No products found", ephemeral=True)
        return
    for result in results['data']['browse']['results']['edges']:
        products.append(discord.SelectOption(label=f"{result['node']['primaryTitle']} {result['node']['secondaryTitle']}", value=f"{result['node']['urlKey']}"))
    await interaction.response.send_message(view=SelectView(products), ephemeral=True)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=config["guild_id"]))
    print("Bot is online!")

client.run(config['bot_token'])