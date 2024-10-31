#!/bin/bash

elasticdump --input="https://$ES_HOST/search-foundry-vtt" \
  --output=foundryvttv12.json --type=data \
  --headers="{\"Authorization\": \"ApiKey $ES_API_KEY\"}"