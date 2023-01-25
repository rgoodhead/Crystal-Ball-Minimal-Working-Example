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
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class run_sutime_on_NewFed {

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
            String write_name_str = String.valueOf(file.getName()).substring(0, file.getName().length()-4);
			System.out.println("filename written to file: " + write_name_str);
			
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
            String name_str1 = String.valueOf(file.getName());
	    System.out.println(name_str1);
			
	    Matcher m = Pattern.compile("\\d{4}\\d{2}\\d{2}").matcher(name_str1);
			
	    String name_str = "";
	    if (m.find()==true) {
	       name_str = m.group(0);
	    } else {
	       name_str = "Break!";
	       System.out.println("ERROR: unable to extract date from file name");
	       System.exit(0);
	    }
			
            String new_name_str = name_str.substring(0,4) + "-" + name_str.substring(4,6) + "-" + name_str.substring(6,8);
            System.out.println("reference date: " + new_name_str);

            props.setProperty("ner.docdate.useFixedDate", new_name_str); // ENTER THE REFERENCE DATE HERE
            props.setProperty("sutime.includeRange", "true");
            props.setProperty("sutime.markTimeRanges", "true");
            props.setProperty("teRelHeurLevel", "MORE"); // NONE (default), BASIC, MORE

            props.setProperty("sutime.rules", ".//sutime//defs2.sutime.txt,.//sutime//english2.sutime.txt");

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
				try {
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
				} catch(Exception e) {

                    System.out.println("SUTime failure");
                    System.out.println("failed to parse the following sentence: ");
                    System.out.println(s);
                    System.out.println("NOTE: if the above line is empty this error is innocuous");
                }
            }

            myWriter.close();
        }
    }
}
