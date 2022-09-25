#!/bin/bash

SCRIPT_DIR=$(realpath $(dirname ${BASH_SOURCE[0]}))
pushd $SCRIPT_DIR
mkdir -p generated/
protoc -I ./ ./*.proto --python_out ./generated
popd
