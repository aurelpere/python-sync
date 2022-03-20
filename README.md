[![Test-Lint-Format](https://github.com/aurelpere/python-sync/actions/workflows/blank.yml/badge.svg)](https://github.com/aurelpere/python-sync/actions/workflows/blank.yml) ![test-coverage badge](./coverage-badge.svg) <a href="https://codeclimate.com/github/aurelpere/python-sync/test_coverage"><img src="https://api.codeclimate.com/v1/badges/134ac26217ff8421bdf1/test_coverage" /></a>
# sync
a script to synchronize and encrypt data in different folders

usage:<br>
`python script_copy_fichiers.py -o origin_folder -d destination_folder`<br>

                      options :   -k keyword: will copy files only if keyword included in filenames
                                  -c password will cypher with 7zip with the password provided
                                  -dc password will decypher with 7zip with the password provided

