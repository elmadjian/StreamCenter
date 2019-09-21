#!/bin/bash

if [[ "$1" != "app://" ]]; then 
    app=${1#app://}
    nohup "$app" &>/dev/null &
else 
    nohup termite &>/dev/null &
fi