This folder contains the following list of files:
- utilities.py
- reaction.py
- reaction_system.py
- interactive_process.py
- simRS.py
- example7.txt
- interactive_process_binary.py
- simRSbinaryN4.py
- binaryCounterN4.txt
- ReactionSystemFramework.pdf

The PDF file is a small presentation of the problem and a quick overview of the approch used to implement the framework.
All the work is based on the paper: "A tour of reaction systems", R. Brijder, A. Ehrenfeucht, M. Main and G. Rozenberg.

The file 'utilities.py' contains some useful functions used in the other python scripts.

The three files 'reaction.py', 'reaction_system.py' and 'interactive_process.py' contains the implementation of the class described in the presentation.

The 'simRS.py' is the main program that makes use of the other scripts.

The two files 'interactive_process_binary.py' and 'simRSbinaryN4.py' are small variations of the 'interactive_process.py' and 'simRS.py' files rispectively. They have been created just to implement
the binary counter example as explained in the paper. Essentially they map the state sequence into the correspondent binary number (4 bits).

So the file 'example7.txt' is the definition of the reaction system used in the example 7 of the paper, and it has to be used with the 'simRS.py' script, whereas the file 'binaryCounterN4.txt' is the
definition of reaction system necessary to implement a binary counter with this framework, then ita has to be used with 'simRSbinaryN4.py' script.

USAGE:
This demo is been tested on a Linux system (Ubuntu 18.04 LTS), inside the project folder open a terminal and run the following bash command:
 ./simRS.py example7.txt            // to make an interactive process over the reaction system of the example 7
 ./simRS.py binaryCounterN4.txt     // to make an interactive process over the reaction system of the binary counter example
