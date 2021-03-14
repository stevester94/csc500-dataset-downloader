#! /usr/bin/bash
set -eou pipefail

export OPENSSL_CONF=$(realpath openssl.cnf)

# This is the top level for Arena_Testbed_"in_the_wild" - Wireless_different_Antenna
top_level=https://repository.library.northeastern.edu/collections/neu:gm80j757w

# Input: The whole experiment       # Input: Each day in the experiment              # Input: each device in each day
./collection_finder.py $top_level | xargs --max-procs=10 -n1 ./collection_finder.py  | xargs --max-procs=10 -n1 ./download_finder.py
