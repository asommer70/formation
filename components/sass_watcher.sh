#!/usr/bin/env bash
#
#

fswatch -0 scss/ | while IFS= read -r -d "" path
echo $path
do
    echo "Re-building CSS (due to change in ${path})"

    # Check the version of sassc (Ubuntu 18.04 uses 3.4.5 which doesn't require an argument after the -m).
    version=$(sassc -v | grep sassc)
    if [[ "$version" = "sassc: 3.4.5" ]]; then
       /usr/local/bin/sassc -m -t compressed scss/main.scss ../assets/css/main.css
    else
       /usr/local/bin/sassc -m auto -t compressed scss/main.scss ../assets/css/main.css
    fi
done
