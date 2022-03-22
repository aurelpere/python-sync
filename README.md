[![Test-Lint-Format](https://github.com/aurelpere/python-sync/actions/workflows/main.yml/badge.svg)](https://github.com/aurelpere/python-sync/actions/workflows/main.yml) ![test-coverage badge](./coverage-badge.svg) <a href="https://codeclimate.com/github/aurelpere/python-sync/test_coverage">  [![Maintainability](https://api.codeclimate.com/v1/badges/134ac26217ff8421bdf1/maintainability)](https://codeclimate.com/github/aurelpere/python-sync/maintainability)
  
# sync
a script to synchronize and encrypt data in different folders

## usage in command line:<br>
`python script_copy_fichiers.py -o origin_folder -d destination_folder`<br>

                      options :   -k keyword: will copy files only if keyword included in filenames
                                  -c password will cypher with 7zip with the password provided
                                  -dc password will decypher with 7zip with the password provided

## usage in python:<br>
  
`Sync('origin_folder','destination_folder',keyword='your_keyword').copy()`
>will copy files including keyword in their names from origin_folder to desination_folder 
   
    
`Sync('origin_folder','destination_folder',keyword='your_keyword').cypher('password')`
>will cypher with 7zip and copy files including keyword in their names from origin_folder to desination_folder 
    
    
`Sync('origin_folder','destination_folder',keyword='your_keyword').decypher('password')`
>will decypher with 7zip and copy files including keyword in their names from origin_folder to desination_folder 

