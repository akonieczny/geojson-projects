#!/bin/bash

cd ./requirements
pip-compile requirements.in
pip-compile requirements.dev.in
