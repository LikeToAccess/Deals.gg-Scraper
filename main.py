# -*- coding: utf-8 -*-
# filename          : main.py
# description       : Deals.gg Scraper
# author            : Ian Ault
# email             : liketoaccess@protonmail.com
# date              : 06-24-2023
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.11.1 (must run on 3.6 or higher)
#==============================================================================
import discord
from time import perf_counter
from cachetools import TTLCache
from discord.ext import commands

from settings import *
from scraper import DealsGG


cache = TTLCache(maxsize=100, ttl=300)
intents = discord.Intents.default()
intents.message_content = True
number_of_results = 3
bot = commands.Bot(command_prefix=
	[
		"-",
		"please "
	],
	intents=intents,
	help_command=None,
	case_insensitive=True
)
scraper = DealsGG()


# def timer(f):
# 	def wrapper(*args, **kwargs):
# 		tic = perf_counter()
# 		result = f(*args, **kwargs)
# 		toc = perf_counter()
# 		print(f"{toc-tic:.4f}s")
# 		return result
# 	return wrapper

def embed_builder(title, description, url, image_url=None, color=0x00b0f4):
	embed = discord.Embed(
		title=title,
		url=url,
		description=description,
		colour=color
	)

	embed.set_author(
		name="LikeToAccess",
		url="https://discord.com/users/796577504130891798",
		icon_url="https://cdn.discordapp.com/avatars/796577504130891798/11808659f50314abd095cbfd4353dffd.webp?size=256"
	)

	if image_url is not None:
		embed.set_image(url=image_url)

	return embed

async def send_embed(channel, embed):
	await channel.send(embed=embed)

@bot.command(name="search")
async def search_deals(ctx, *query):
	query = " ".join(query)
	await ctx.send(f"Searching for \"{query}\"...")
	tic = perf_counter()
	results = cache.get(query)
	if results is None:
		results = scraper.search(query)
		cache[query] = results
	top_results = results[:number_of_results] if number_of_results > 0 else results
	toc = perf_counter()

	if len(results) == 0:
		await ctx.send(f"No results found for \"{query}\".")
	else:
		await ctx.send(f"Found {len(results)} result{'s' if len(results) > 1 else ''} in {toc-tic:.8f}s.")
		if top_results != results:
			await ctx.send(f"Returning top {len(top_results)} result{'s' if len(top_results) > 1 else ''}.")
		else:
			await ctx.send("Returning all results.")
		for result in top_results:
			game_info = scraper.get_game_info(result)
			title = game_info["title"]
			description = f"Official Price: {game_info['official_price']}\n" + \
				          f"Keyshop Price: {game_info['keyshop_price']}"
			url = game_info["url"]
			embed = embed_builder(
				title=title,
				description=description,
				url=url
			)
			await send_embed(ctx, embed)

def main():
	bot.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
	main()
