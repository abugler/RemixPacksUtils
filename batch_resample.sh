#!/bin/sh
# Take two arguments, $1 is the src, $2 is dst
shopt -s globstar nocaseglob
dest=$2

if [$# -gt 2]
then
  num_workers=$3
else
  num_workers=20
fi
tsp -S $num_workers

for input in find $1 -L -name "*"
do
  indir=$(dirname "$input")
  outdir=${indir/music_separated/$dest}
  [ ! -d "$outdir" ] && mkdir -p "$outdir"
  infile=$(basename "$input")
  outfile=${infile%.???}.wav
  tsp ffmpeg -i "$input" -ar 16000 -ac 1 "${outdir}/${outfile}"
done
# set it back to something reasonable
tsp -S 5