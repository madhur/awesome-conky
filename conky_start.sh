#!/bin/bash
conky -p 15 -c ~/.conky/.conkyrc-core &
conky -p 15 -c ~/.conky/.conkyrc-weather &
conky -p 15 -c ~/.conky/.conkyrc-social
