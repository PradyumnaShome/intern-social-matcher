#!/bin/bash

export S3_API_URL="https://nyhg428bs7.execute-api.us-east-1.amazonaws.com/default/fetchInterns"
export FLASK_APP="src/render_matches.py"
flask run