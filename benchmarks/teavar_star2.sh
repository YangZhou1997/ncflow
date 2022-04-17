#! /usr/bin/env bash

set -e
set -x

# topo_folder num_demand beta mcf path topo_file_name cutoff_downscale beginning_cutoff
julia ../ext/teavar/run_teavar_star.jl teal 20 0.99 x ECMP topology.txt 2 1 > teavar_star.txt
