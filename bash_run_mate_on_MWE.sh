#!/bin/bash

FILES=data/data_MWE/corpus_prepared_for_mate/*.txt
OUTLOCATION1=data/data_MWE/mate_parsed_corpus/split/
OUTLOCATION2=data/data_MWE/mate_parsed_corpus/parsed/
OUTLOCATION3=data/data_MWE/mate_parsed_corpus_backup/

for f in $FILES
do
	FILENAME=`basename ${f}`
	INFILENAME=${f}
	OUTFILENAME1=$OUTLOCATION1$FILENAME
	OUTFILENAME2=$OUTLOCATION2$FILENAME
	OUTFILENAME3=$OUTLOCATION3$FILENAME
	
	#echo "$INFILENAME"
	#echo "$OUTFILENAME"
	
	echo "Applying MATE parser to file: $FILENAME"
	
	java -cp mate_tools_working/anna/anna-3.61.jar is2.util.Split $INFILENAME > $OUTFILENAME1
	
	java -Xmx6g -classpath mate_tools_working/transition/transition-1.30.jar is2.transitionS2a.Parser  -model mate_tools_working/parser_tagger/per-eng-S2b-40.mdl -test $OUTFILENAME1 -out $OUTFILENAME2
	
	#python -c "import sys; sys.stdout.write(open(sys.argv[1]).read())" $OUTFILENAME > $OUTFILENAME
	
	cp $OUTFILENAME2 $OUTFILENAME3
	
done