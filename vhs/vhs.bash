#!/bin/sh
for file in *.tape; do
    if [ -f "$file" ]; then
        vhs < "$file"
    fi
done
