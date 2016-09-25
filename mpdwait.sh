#!/bin/bash
while : ; do
        mpc idle &>/dev/null
        # the sed will exclude things between parenthesis like (feat. Pit Bull)
        SONG="$(mpc current | grep -v "player|mixer")"
        ./wallofsound.py $SONG 2>/dev/null
done
