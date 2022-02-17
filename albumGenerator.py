import requests
import discord
import json

from bs4 import BeautifulSoup

class AlbumGenerator:
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
        self.url = 'https://1001albumsgenerator.com/swiftarrow4'

    # Create a user from discord...
    def JoinGroup(ctx):                     
        ctx.send('https://1001albumsgenerator.com/?joinGroup=discord-bot')
        return

    def GetAlbumOTD(username='swiftarrow4'):
        # response object is given to you
        request = requests.get(f'https://1001albumsgenerator.com/api/v1/projects/{username}')
        requestData = json.loads(request.text)
        currentAlbum = requestData['currentAlbum']

        albumData = {}

        albumData['albumName'] =  currentAlbum['name']
        albumData['albumArtist'] = currentAlbum['artist']
        albumData['albumImage'] = currentAlbum['images'][1]['url']
        albumData['albumSpotifyLink'] = currentAlbum['spotifyId']

        return albumData

    # async def vote(ctx, rating):
    #     if rating < 1 or rating > 5:
    #         return ctx.send('Please input a number between 1 and 5')
    #     await ctx.send(f'Please register to give a rating at {COMMAND_PREFIX}joinGroup')

    async def GetUserSummary(ctx, user='swiftarrow4'):
        response = requests.get(f'https://1001albumsgenerator.com/api/v1/projects/{user}')
        soup = BeautifulSoup(response.content, 'html.parser')
        # TODO: Parse html page for summary data
        responseData = json.loads(response.text)
        summary = responseData['shareableUrl']
        await ctx.send(f'Summary page for {user}: {summary}')