#!/bin/bash
rm json/*
for file in `ls yaml`; do
  output_file=$(echo $file | gsed 's/\.yaml/\.json/g')
  yq yaml/$file -o json > json/$output_file
done

for file in `ls json`; do
  gsed -i 's/\.yaml/\.json/g' json/$file
done


datamodel-codegen --input-file-type jsonschema  --input json --output ../robocode_event_models/