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
import env
import discord
from discord.ext import tasks

from scraper import Scraper


bot = discord.Bot(intents=discord.Intents.all())
scraper = Scraper()

def main():
	bot.run(env.discord_token())


if __name__ == "__main__":
	main()
