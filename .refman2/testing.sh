#!/run/current-system/sw/bin/bash

# rm -r ../Papers_test 
# rm -r ../Books_test
# rm -r ../Websites_test 
rm ../citekeys_test.db 

# BCS superconductivity paper
./refman2_nixos.sh refman2.py add-doi 10.1103/PhysRev.106.162 \
  --database "../citekeys_test.db" 

# TBG Superconductivity paper
./refman2_nixos.sh refman2.py add-doi 10.1038/nature26160 \
  --citekey "TBG-SC-2018" \
  --database "../citekeys_test.db" 

# Perelman papers
./refman2_nixos.sh refman2.py add-doi math/0211159 \
  --database "../citekeys_test.db" 

./refman2_nixos.sh refman2.py rename "Perelman2002" "Perelman1" \
  --database "../citekeys_test.db"

./refman2_nixos.sh refman2.py add-doi math/0303109 \
  --database "../citekeys_test.db" 

./refman2_nixos.sh refman2.py rename "Perelman2003" "Perelman2" \
  --database "../citekeys_test.db"

./refman2_nixos.sh refman2.py add-doi math/0307245 \
  --database "../citekeys_test.db" 

./refman2_nixos.sh refman2.py rename "Perelman2003" "Perelman3" \
  --database "../citekeys_test.db"


# Peskin & Schroeder
./refman2_nixos.sh refman2.py add-isbn 0201503972 \
  --database "../citekeys_test.db" 

# Jackson Electrodynamics
./refman2_nixos.sh refman2.py add-isbn 0-471-30932-X \
  --database "../citekeys_test.db"

# Xiao Gang Wen Topological QFT 
./refman2_nixos.sh refman2.py add-isbn 019922725X \
  --database "../citekeys_test.db"

# Algebraic Topology by Hatcher 
./refman2_nixos.sh refman2.py add-isbn 0521795400 \
  --database "../citekeys_test.db"

# Org Chem by Czako and Kurti 
./refman2_nixos.sh refman2.py add-isbn 0123694833 \
  --database "../citekeys_test.db"

# Bernevig's superconductivity book
./refman2_nixos.sh refman2.py add-isbn 069115175X \
  --database "../citekeys_test.db"

#./refman2_nixos.sh refman2.py add-url "https://www.bibtex.org/" \
#  --database "../citekeys_test.db"


./refman2_nixos.sh refman2.py 'Bernevig2013' \
  --database "../citekeys_test.db"

./refman2_nixos.sh refman2.py remove 'Bernevig2013' \
  --database "../citekeys_test.db"

