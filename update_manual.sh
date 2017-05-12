#!/bin/bash
cd /home/vlabs/sbhs_vlabs/sbhs/sbhs_server/production_static_files/manual

wget https://github.com/rupakrokade/sbhs-manual/blob/master/sbhs-new-manual.pdf?raw=true

mv sbhs-new-manual.pdf?raw=true sbhs-new-manual.pdf

cd /home/vlabs/sbhs_vlabs/sbhs/sbhs_server
