#!/usr/bin/env bash

if [[ $# -lt 1 ]]; then
    echo 'Usage: mktar.sh <folder>'
    exit 0
fi

FOLDER="$1"

if [[ ! -d "$FOLDER" ]]; then
    echo "Folder $FOLDER does not exist"
    exit 0
fi

for lang in $(ls "$FOLDER"); do
    if [[ -d "$FOLDER/$lang" ]]; then
        files=()
        for file in $(cat "$FOLDER/$lang/.tarfiles"); do
            file_fp="$FOLDER/$lang/$file"
            if [[ -f "$file_fp" ]]; then
                files+=("$file_fp")
            fi
        done
        tar -czf "$FOLDER/$lang.tar.gz" ${files[@]}
    fi
done
