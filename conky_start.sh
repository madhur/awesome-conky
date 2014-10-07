#!/bin/bash
conky -p 15 -c ~/.conkyrc-core &
conky -p 15 -c ~/.conkyrc-weather &
conky -p 15 -c ~/.conkyrc-social
