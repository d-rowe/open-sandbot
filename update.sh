#!/usr/bin/env bash

git pull --rebase

# rebuild static content
cd client
npm run build
