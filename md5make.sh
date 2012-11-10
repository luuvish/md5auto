#!/usr/bin/sh

#openssl dgst -md5 *

PATH=/volume1/share

nohup python md5auto.py --make --path $PATH --out ./md5s/collection-anime-best.md5     collection/anime/best
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-anime-ghibli.md5   collection/anime/ghibli
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-anime-gundam.md5   collection/anime/gundam
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-anime-mecanic.md5  collection/anime/mecanic
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-game-console.md5   collection/game/console
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-game-hentai.md5    collection/game/hentai
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-game-mame-roms.md5 collection/game/mame-roms.co.uk
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-game-windows.md5   collection/game/windows
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-movie-foreign.md5  collection/movie/foreign
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-movie-korean.md5   collection/movie/korean
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-music-image.md5    collection/music/image
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-software.md5       collection/software
nohup python md5auto.py --make --path $PATH --out ./md5s/collection-text.md5           collection/text

nohup python md5auto.py --make --path $PATH --out ./md5s/nominate-anime-best.md5       nominate/anime/best
nohup python md5auto.py --make --path $PATH --out ./md5s/nominate-anime-ghibli.md5     nominate/anime/ghibli
nohup python md5auto.py --make --path $PATH --out ./md5s/nominate-anime-gundam.md5     nominate/anime/gundam
nohup python md5auto.py --make --path $PATH --out ./md5s/nominate-anime-mecanic.md5    nominate/anime/mecanic
nohup python md5auto.py --make --path $PATH --out ./md5s/nominate-game-hentai.md5      nominate/game/hentai
nohup python md5auto.py --make --path $PATH --out ./md5s/nominate-game-windows.md5     nominate/game/windows
nohup python md5auto.py --make --path $PATH --out ./md5s/nominate-movie-foreign.md5    nominate/movie/foreign
nohup python md5auto.py --make --path $PATH --out ./md5s/nominate-movie-korean.md5     nominate/movie/korean

nohup python md5auto.py --make --path $PATH --out ./md5s/private.md5                   private
