#! /usr/bin/bash
set -eou pipefail

export OPENSSL_CONF=$(realpath openssl.cnf)

partial_download_path="./downloads.partial"
finished_download_path="/mnt/wd500GB/CSC500/Downloads"
download_list="./all_downloads"

mkdir -p $partial_download_path
mkdir -p $finished_download_path

./steves_downloader.py $partial_download_path $finished_download_path $download_list | tee steves_downloader.stdout.log
