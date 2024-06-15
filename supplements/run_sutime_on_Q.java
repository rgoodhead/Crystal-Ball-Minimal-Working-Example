import edu.stanford.nlp.pipeline.CoreDocument;
import edu.stanford.nlp.pipeline.CoreEntityMention;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.time.TimeAnnotations;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.Scanner;

public class run_sutime_on_Q {

    public static void main(String[] args) throws IOException {

        // create token1
        String token1 = "";
		String inputFile = args[0];
		String outputFile = args[1];

        //loop over files in resources path (moved a sample of processed speeches here)
        File[] files = new File(inputFile).listFiles();
        for (File file : files) {
            System.out.println("Directory: " + file.getName());
			
			// ROB: addition to delete existing file
			String outf = outputFile + file.getName();
			File file2del = new File(outf);
			if(file2del.delete())
			{
				System.out.println("File deleted successfully");
			}
			else
			{
				System.out.println("File not deleted");
			}
			
            // create Scanner inFile1
            Scanner inFile1 = new Scanner(new File(String.valueOf(file))).useDelimiter("(\\n)");

            List<String> temps = new ArrayList<String>();

            // while loop
            while (inFile1.hasNext()) {
                // find next line
                token1 = inFile1.next();
                temps.add(token1);
            }
            inFile1.close();

            String[] tempsArray = temps.toArray(new String[0]);

            //create a file (using same naming system) to send the results to, in append mode
            FileWriter myWriter = new FileWriter(outputFile + file.getName(), true);
            //Create a variable for filewriter to make part of linking variable for python
            String write_name_str = String.valueOf(file.getName()).substring(0, 12);
            //create a header row to match python
            myWriter.write("Sent_ID" + " <TIMEX3 "+ "TIMEX");
            myWriter.write("\n");

            //Run SUTime on loaded speech
            // set up pipeline properties
            Properties props = new Properties();
            // general properties
            props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner");
            //props.setProperty("ner.docdate.usePresent", "true");

            //update the reference data iteratively by extracting the date from the filename
            //String name_str = new String("\""+String.valueOf(file.getName()).substring(4,14)+"\"");
            //String new_name_str = name_str.replace("_", "-");
            String name_str = String.valueOf(file.getName()).substring(0, 10);
            String new_name_str = name_str.replace("_", "-");
            System.out.println(new_name_str);
            /*
            String new_name_str = "2020-02-06";
            System.out.println(new_name_str);
            */
            props.setProperty("ner.docdate.useFixedDate", new_name_str); // ENTER THE REFERENCE DATE HERE
            props.setProperty("sutime.includeRange", "true");
            props.setProperty("sutime.markTimeRanges", "true");
            props.setProperty("teRelHeurLevel", "MORE"); // NONE (default), BASIC, MORE
            //props.setProperty("sutime.rules", "C:\\Users\\Dave\\Documents\\Communications\\stanford-corenlp-4.0.0\\sutime\\defs2.sutime.txt,C:\\Users\\Dave\\Documents\\Communications\\stanford-corenlp-4.0.0\\sutime\\english2.sutime.txt");
            props.setProperty("sutime.rules", ".\\sutime\\defs2.sutime.txt,.\\sutime\\english2.sutime.txt");

            //props.setProperty("ner.rulesOnly", "true");
            // build pipeline
            StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
            int counter = 0;
            String str = String.valueOf(counter);

            //Run SUTime over every sentence in speech
            for (String s : tempsArray) {
                System.out.println("----------------------------------------");
                System.out.println("String Input: Number " + str);
                System.out.println("----------------------------------------");
                counter++;
                str = String.valueOf(counter);
                CoreDocument document = new CoreDocument(s);
                pipeline.annotate(document);
                for (CoreEntityMention cem : document.entityMentions()) {
                    //System.out.println("temporal expression: " + cem.text());
                    String temp_val = String.valueOf(cem.coreMap().get(TimeAnnotations.TimexAnnotation.class));
                    if (temp_val.equals("null")) {
                        assert true;
                    } else {
                        System.out.println("temporal expression: " + cem.text());
                        System.out.println("temporal value: " +
                                cem.coreMap().get(TimeAnnotations.TimexAnnotation.class));
                        myWriter.write(write_name_str + "_S" + str + " " +
                                cem.coreMap().get(TimeAnnotations.TimexAnnotation.class));
                        myWriter.write("\n");
                    }

                }
            }

            myWriter.close();
        }
    }
}

