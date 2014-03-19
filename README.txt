To run the spatial role labelling project you need to have jython in your system
To install jython:

Jython 2.2.1 is distributed as an executable jar file installer. The installer file is included in the project directory. To run the file either double click the jython_installer-2.2.1.jar or run java with the -jar option

>java -jar jython_installer-2.2.1.jar

This will start the regular GUI installer on most systems, or a consoler installer on headless systems. To force the installer to work in headless mode invoke the installer with a console switch

java -jar jython_installer-2.2.1.jar --console

The installer will then walk through a similar set of steps in graphical or console mode: showing the license, selecting an install directory and JVM and actually copying Jython to the filesystem. After this completes, Jython is installed in the directory you selected.

*******Input to be given through the file named input.txt
*******Each line should contain one sentence only 

*******The spatial indicator, trajector and landmark are printed for each such set in a differnet line in the file output.txt

After installing you need to make the script file run_nlp.sh executable
chmod +x run_nlp.sh
and then run the script from the terminal
> ./run_nlp.sh
