# Table of Contents
1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Run Instructions](README.md#run-instructions)
4. [Test Instructions](README.md#test-instructions)


# Problem

Reddit generates ~2 million comments / day. 480,000 of those comments are banned / flagged as inapropriate. The rules for banning / flagging comments are rule or regex based. They are inefficient.

Social Media companies take platform abuse seriously.

This project aims to automate the process of collecting the necessary data to run in depth analysis on reddit comments. Latent Diriclecht Allocation is used to extract topics from a corpus of reddit comments. A neural network is trained on these topics of intent. A data pipeline ingests reddit data to classify reddit comments by intent in real-time.

# Approach
```
      ├── README.md 
      ├── run.sh
      ├── src
      │   └──h1b_counting.py
      │   └──dataProcessor.py
      │   └──test_dataProcessor.py
      │   └──parser.py
      │   └──test_parser.py
      │   └──utils.py
      ├── input
      │   └──h1b_input.csv
      ├── output
      |   └── top_10_occupations.txt
      |   └── top_10_states.txt
      ├── insight_testsuite
          └── run_tests.sh
          └── tests
              └── test_1
              |   ├── input
              |   │   └── h1b_input.csv
              |   |__ output
              |   |   └── top_10_occupations.txt
              |   |   └── top_10_states.txt
              ├── your-own-test_1
                  ├── input
                  │   └── h1b_input.csv
                  |── output
                  |   |   └── top_10_occupations.txt
                  |   |   └── top_10_states.txt
```
h1b_counting.py is the entry-point of the program. A DataProcessor object is initialized and aggregates statstics from input files line-by-line. After all files have been processed write the statistics to a txt file.
DataProcessor draws inspiration from a pandas DataFrame.
 

# Run-Instructions

```
    cd /directory/containing/run.sh
    sudo chmod +x ./run.sh
    ./run.sh
```

# Test-Instructions

```
    cd /directory/containing/run.sh
    cd src
    python test_parser.py
    python test_dataProcessor.py

    cd ..
    cd insight_testsuite
    ./run_tests.sh
```

