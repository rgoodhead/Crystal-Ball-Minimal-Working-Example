#!/bin/bash

FILES=data/data_MWE/mate_parsed_corpus/parsed/*.txt
OUTPUTDESTINATION1=data/data_MWE/tmv/raw/
OUTPUTDESTINATION2=data/data_MWE/tmv/xml/

LANG="en"
for f in $FILES
do
	
	#echo "$INFILENAME"
	#echo "$OUTFILENAME"
	
	INPUT=${f}
	OUTPUT=$(basename $INPUT) 
	
	FILENAME=`basename ${f}`
	echo "Applying TMV Tool to file: $FILENAME"
	
	python tmv_tool/tmv-annotator-tool/TMV-EN_ecb_test_david.py $INPUT $OUTPUT $OUTPUTDESTINATION1
    
	python tmv_tool/tmv-annotator-tool/TMVtoHTML_ecb.py $OUTPUTDESTINATION1$OUTPUT $INPUT $LANG $OUTPUTDESTINATION2$OUTPUT
    
	#python -c "import sys; sys.stdout.write(open(sys.argv[1]).read())" $OUTFILENAME > $OUTFILENAME
	
done