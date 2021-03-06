# passwordz
Password manager and generator written in Python

## Features
* generate random passwords using a master-key without saving them on disk
* custom char-space and password length
* save passwords to clipboard for easy entry
* automatic clipboard clearing (on exit, after x seconds)
## Security
* password generation using hashes (One-Way!)
* security by transparency:
    * a hacker would need a generated password (online breach), find the source code to this software, hack the users configuration (password length and char-space) and reverse engineer the entire password generation process JUST to end up with a hash that he would still need to crack
    * even with all information available its hard to breach the master-key/hash

## TODO:
* rotate passwords
* override char-space for single password

## Dependencies
-   hashlib
-   numpy
-   win32clipboard

