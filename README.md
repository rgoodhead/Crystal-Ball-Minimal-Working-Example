# Crystal-Ball-Minimal-Working-Example

[David Byrne](https://sites.google.com/view/davidbyrneecon), [Robert Goodhead](https://sites.google.com/site/robertgoodhead/), [Michael McMahon](http://mcmahonecon.com/), Conor Parle

This is a readme file, designed to allow researchers to apply the approach of Byrne et al. (2022a). The files here represent a minimal working example (MWE) and will parse 9 text files containing policy statements by the Federal Reserve in 2019.

You will need the following programmes on your system, and accessible from your system path: Python, Java JDK, Maeven, Git Bash.

Our approach benefits from the use of multiple algorithms from the natural language processing (NLP) literature. In particular,

- the TMV algorithm of Ramm et al. (2017);
- the SUTime algorithm of Chang and Manning (2012);
- the MATE parser of Björkelund et al. (2010).

We explain clearly how and where to apply the codes of other researchers in the present readme. However, we do not provide access to these tools in the present repository, and refer users of our codes to the respective websites of these authors for relevant codes.

## Step 1: Ensure the file structure is correct

The file structure for the working directory needs to be as follows:
-	./data
-	./mate_tools_working
-	./stanford-corenlp-4.0.0
-	./tmv_tool

The file structure for ./data/data_MWE needs to be as follows:
- ./data/data_MWE
  - /corpus
  - /corpus_prepared_for_mate
  - /mate_parsed_corpus
  - /mate_parsed_corpus_backup
  - /sent_corpus
  - /sent_dates_corpus
  - /sent_sutime_corpus
  - /tmv

The correct file structures for ./mate_tools_working, ./stanford-corenlp-4.0.0, and ./tmv_tool will be discussed subsequently.

Ensure the folder ./data/data_MWE/corpus includes the 9 text files of interest. However, any text file containing English language sentences, will be parsed if they are placed in this folder. It is necessary that they follow the naming convention “filename_YYYYMMDD.txt” however, where YYYYMMDD indicates the reference date of the document.

## Step 2: Pre-process the textual data

You will need to run the following python codes in sequence to pre-process the data:
-	run_MWE_1a_preprocessing_minimal.py
-	run_MWE_1c_preprocessing_for_mate.py
-	run_MWE_1ca_dates_preprocessing_for_sutime.py

## Step 3: Set up the TMV tool

Before one can run the TMV tool, one needs to set up the MATE parser.

### 3a) Set up MATE

-	Download the file anna-3.61.jar from [here](https://code.google.com/archive/p/mate-tools/downloads) and put it in a folder called ./mate_tools_working/anna.
-	Download transition-1.30.jar from [here](https://code.google.com/archive/p/mate-tools/wikis/ParserAndModels.wiki) and put it in a folder called ./mate_tools_working/transition.
-	Download the parser + tagger from [here](https://code.google.com/archive/p/mate-tools/wikis/ParserAndModels.wiki), under “English Models”, which is a .mdl file called per-eng-S2b-40.mdl and put it in a folder called ./mate_tools_working/parser_tagger/.
-	Download the parser .csh script from [here](https://code.google.com/archive/p/mate-tools/wikis/ParserAndModels.wiki), which is a tiny example script called parse-eng, and put it in ./mate_tools_working/parser_tagger/.

### 3b) Set up TMV

-	Download the TMV tools (from the GitHub repository [here](https://github.com/aniramm/tmv-annotator)) into this folder and unzip inside ./tmv_tool. There should be folders called europarl, example-outputs, and tmv-annotator-tool. There should also be .gitignore, LICENSE, README.md.
-	Note that you need the de-bugged version of the English variant of the tool. You should place the file TMV-EN_ecb_test_david.py (found in ./supplements) in the directory (./data/tmv-annotator-tool).
-	You also need to add the file TMVtoHTML_ecb.py (found in ./supplements) in the directory (./data/tmv-annotator-tool).

## Step 4: Getting SUTime working

You will need a version of Stanford CoreNLP on your system. In our applications, we used version 4.0.0, which is available [here](https://stanfordnlp.github.io/CoreNLP/history.html). While our codes may function with more recent versions, we cannot guarantee this will be the case.

The folder ./stanford-corenlp-4.0.0 should have the following file structure:
- ./stanford-corenlp-4.0.0
   - /.idea
   - /jars
   - /patterns
   - /sutime
   - /target
   - /tokensregex

Next one needs to add two additional rules files, that are bespoke to this paper and are not included in the core distribution of SUTime. To do this, move the files defs2.sutime.txt and english2.sutime.txt (found in ./supplements) to the folder ./stanford-corenlp-4.0.0/sutime.

One now needs to add a .java file, designed to run extract the reference date from text file names, before applying SUTime to this reference date. To do this move the two files run_sutime_on_MWE.java and run_sutime_on_MWE.class into ./stanford-corenlp-4.0.0. These two files are both found in ./supplements.

## Step 5: Parse the data

To parse the data with TMV, one needs to run the following two files in sequence:
-	bash_run_mate_on_MWE.sh
-	bash_run_tmv_on_MWE.sh

To parse the data with SUTime, one needs to run the following file:
-	bash_run_sutime_on_MWE.sh

## Step 6: Additional preparation routines

These routines apply a few cleaning operations, as detailed in Byrne et al. (2022a). These routines are specific to our investigations, and any individual cleaning decision we leave for future researchers to remove or modify as they please.
-	run_MWE_2a_tmv_1_data_input 
-	run_MWE_2a_tmv_1a_tempoword
-	run_MWE_2b_sutime_datainput
-	run_MWE_3a_tmv_preparation
-	run_MWE_3b_sutime_preparation

The cleaned SUTime and TMV parsed data can be respectively found stored in the following .pkl files:
-	./data/data_MWE/data_TMV_cleaned.pkl
-	./data/data_MWE/data_SUTime_cleaned.pkl

## References

Björkelund, Anders, Bernd Bohnet, Love Hafdell and Pierre Nuges (2010), "A High-Performance Sytactic and Semantic Dependency Parser", Coling 2010, Demonstrations.

Byrne, David, Robert Goodhead, Michael McMahon, and Conor Parle (2022a), "Measuring the Temporal Dimension of Text: An Application to Policymaker Speeches", *mimeo*

Byrne, David, Robert Goodhead, Michael McMahon, and Conor Parle (2022b), "Measuring the Temporal Dimension of Text: An Application to Policymaker Speeches", *mimeo*

Chang, Angel X. and Christopher D. Manning (2012), "SUTime: A Library for Recognizing and Normalizing Time Expressions", 8th International Conference on Language Resources and Evaluation

Ramm, Anita, Sharid Loáiciga, Annemarie Friedrich, and Alexander Fraser (2017), "Annotating Tense, Mood and Voice for English, French and German", Proceedings of ACL 2017, System Demonstrations.
