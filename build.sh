#! /bin/bash
echo "Packaging Radio for release..."
mkdir release
mkdir release/out
cp -r Radio modules README.md release
zip -r release/out/plugin.music.radio.zip modules Radio README.md
echo "Finished!"
