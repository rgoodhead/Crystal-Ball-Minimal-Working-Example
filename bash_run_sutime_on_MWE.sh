#!/bin/bash

set -e

clear
echo "-------------------------"
echo "applying SUTime          "
echo "-------------------------"

cd stanford-corenlp-4.0.0

INPUTLOC=..//data//data_MWE//sent_dates_corpus//
OUTPUTLOC=..//data//data_MWE//sent_sutime_corpus//

# First, compile the Java programs into Java classes
javac -cp "*" run_sutime_on_MWE.java
  
# Now pass the arguments to the Java classes
java -cp "*" run_sutime_on_MWE.java "$INPUTLOC" "$OUTPUTLOC"