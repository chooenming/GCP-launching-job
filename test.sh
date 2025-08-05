#!/bin/bash

SOMETHING='SOME-Text-Here'
SOMETHING=$(echo ${SOMETHING} | tr '[:upper:]' '[:lower:]')

echo "${SOMETHING}"