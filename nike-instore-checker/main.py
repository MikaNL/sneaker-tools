import discord, json
from discord import app_commands
from discord.ext import commands
from classes import Geocode
from classes import Nike

with open("config.json", "r") as f:
    config = json.load(f)

for keys, value in config.items():
    if not value:
        print(f"{keys} is not set in config.json")
        exit()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="nikeinstore", description="Check the availability for Nike stores", guild=discord.Object(id=config["guild_id"]))
@discord.app_commands.describe(pid="Product ID like: DD1871-001")
@discord.app_commands.describe(address="Address like: Kalverstraat 1 Amsterdam")
@discord.app_commands.describe(max_distance=f"Distance in {config['metrics_units']}")
async def nikeinstore(interaction, pid: str, address: str, max_distance: int):
    await interaction.response.defer()
    await interaction.delete_original_response()
    geocode = Geocode.Geocode(address)
    longitude, latitude = geocode.getCoordinates()
    if longitude == None or latitude == None:
        embed = discord.Embed(
            color=config['embed_color'],
            title="Location not found, please be more specific."
        )
        await interaction.followup.send(embed=embed)
        return
    nike = Nike.Nike()
    stores = nike.getStoreDetails(longitude, latitude, max_distance)
    if stores == None:
        embed = discord.Embed(
            color=config['embed_color'],
            title="No Nike-stores found in this area."
        )
        await interaction.followup.send(embed=embed)
        return
    name, slug, image = nike.getProductDetails(pid)
    for store_id, store_name, store_country, store_url in stores:
        availabilities = []
        sizes = nike.getAvailability(store_id, pid)
        if sizes == None:
            embed = discord.Embed(
                color=config['embed_color'],
                title=name,
                url=slug
            )
            embed.set_thumbnail(url=image)
            embed.set_author(name="https://www.nike.com/", url=f"https://www.nike.com/{config['country_code']}/")
            embed.add_field(name="Country", value=store_country)
            embed.add_field(name="Style code", value=pid.upper())
            embed.add_field(name="Store", value=f"[{store_name}]({store_url})")
            embed.add_field(name="Availability", value="Sold out at this store.")
            continue
        for gtin, level, modification_date in sizes:
            size = nike.getSize(gtin, pid)
            availabilities.append([size,level, modification_date])
        embed = discord.Embed(
            color=config['embed_color'],
            title=name,
            url=slug
        )
        embed.set_thumbnail(url=image)
        embed.set_author(name="https://www.nike.com/", url=f"https://www.nike.com/{config['country_code']}/")
        embed.add_field(name="Country", value=store_country)
        embed.add_field(name="Style code", value=pid.upper())
        embed.add_field(name="Store", value=f"[{store_name}]({store_url})")
        embed.add_field(name="Sizes", value="\n".join([size for size, level, modification_date in availabilities]))
        embed.add_field(name="Stock", value="\n".join([level for size, level, modification_date in availabilities]))
        embed.add_field(name="Last change", value="\n".join([modification_date for size, level, modification_date in availabilities]))
        embed.add_field(name="Links", value=nike.getFooterLinks(pid))
        embed.set_footer(text="• Made by @bontje34", icon_url="https://bontes.net/assets/img/logo.png")
        await interaction.followup.send(embed=embed)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=config["guild_id"]))
    print("Bot is online!")

client.run(config['bot_token'])