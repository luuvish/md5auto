#!/usr/bin/sh

#nohup md5make.sh
#openssl dgst -md5 *

#PATH=/volume1/share
PATH=..
MAKE=./md5auto/md5auto.py --make
MD5S=./md5auto/md5s
LOGS=./md5auto/logs

pushd $PATH

#python $MAKE --out $MD5S/md5make-all.md5 collection nominate private

python $MAKE --out $MD5S/collection-anime-best.md5     	collection/anime/best
python $MAKE --out $MD5S/collection-anime-ghibli.md5   	collection/anime/ghibli
python $MAKE --out $MD5S/collection-anime-gundam.md5   	collection/anime/gundam
python $MAKE --out $MD5S/collection-anime-mecanic.md5  	collection/anime/mecanic
python $MAKE --out $MD5S/collection-game-console.md5   	collection/game/console
python $MAKE --out $MD5S/collection-game-mame-roms.md5 	collection/game/mame-roms.co.uk
python $MAKE --out $MD5S/collection-game-windows.md5   	collection/game/windows
python $MAKE --out $MD5S/collection-movie-foreign.md5  	collection/movie/foreign
python $MAKE --out $MD5S/collection-movie-korean.md5   	collection/movie/korean
python $MAKE --out $MD5S/collection-music-image.md5    	collection/music/image
python $MAKE --out $MD5S/collection-software.md5       	collection/software
python $MAKE --out $MD5S/collection-text.md5       		collection/text

python $MAKE --out $MD5S/nominate-anime-best.md5       	nominate/anime/best
python $MAKE --out $MD5S/nominate-anime-ghibli.md5     	nominate/anime/ghibli
python $MAKE --out $MD5S/nominate-anime-gundam.md5     	nominate/anime/gundam
python $MAKE --out $MD5S/nominate-anime-mecanic.md5    	nominate/anime/mecanic
python $MAKE --out $MD5S/nominate-game-windows.md5     	nominate/game/windows
python $MAKE --out $MD5S/nominate-movie-foreign.md5    	nominate/movie/foreign
python $MAKE --out $MD5S/nominate-movie-korean.md5     	nominate/movie/korean

python $MAKE --out $MD5S/private.md5                   	private

popd
