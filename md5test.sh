#!/usr/bin/sh

#nohup md5test.sh
#openssl dgst -md5 *

#PATH=/volume1/share
PATH=..
TEST=./md5auto/md5auto.py --test
MD5S=./md5auto/md5s
LOGS=./md5auto/logs

pushd $PATH

#python $TEST --log $LOGS/md5test-all.log $MD5S/*.md5

python $TEST --log $LOGS/collection-anime-best.log 	    $MD5S/collection-anime-best.md5
python $TEST --log $LOGS/collection-anime-ghibli.log 	$MD5S/collection-anime-ghibli.md5
python $TEST --log $LOGS/collection-anime-gundam.log 	$MD5S/collection-anime-gundam.md5
python $TEST --log $LOGS/collection-anime-mecanic.log 	$MD5S/collection-anime-mecanic.md5
python $TEST --log $LOGS/collection-game-console.log 	$MD5S/collection-game-console.md5
python $TEST --log $LOGS/collection-game-mame-roms.log 	$MD5S/collection-game-mame-roms.md5
python $TEST --log $LOGS/collection-game-windows.log 	$MD5S/collection-game-windows.md5
python $TEST --log $LOGS/collection-movie-foreign.log 	$MD5S/collection-movie-foreign.md5
python $TEST --log $LOGS/collection-movie-korean.log 	$MD5S/collection-movie-korean.md5
python $TEST --log $LOGS/collection-music-image.log 	$MD5S/collection-music-image.md5
python $TEST --log $LOGS/collection-software.log 	    $MD5S/collection-software.md5
python $TEST --log $LOGS/collection-test.log 	    	$MD5S/collection-test.md5

python $TEST --log $LOGS/nominate-anime-best.log 		$MD5S/nominate-anime-best.md5
python $TEST --log $LOGS/nominate-anime-ghibli.log 		$MD5S/nominate-anime-ghibli.md5
python $TEST --log $LOGS/nominate-anime-gundam.log 		$MD5S/nominate-anime-gundam.md5
python $TEST --log $LOGS/nominate-anime-mecanic.log 	$MD5S/nominate-anime-mecanic.md5
python $TEST --log $LOGS/nominate-game-windows.log 		$MD5S/nominate-game-windows.md5
python $TEST --log $LOGS/nominate-movie-foreign.log 	$MD5S/nominate-movie-foreign.md5
python $TEST --log $LOGS/nominate-movie-korean.log 		$MD5S/nominate-movie-korean.md5

python $TEST --log $LOGS/private.log  					$MD5S/private.md5

popd
