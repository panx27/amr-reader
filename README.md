## Quickstart

      bin/amr_reader <directory of AMR files> <directory of output files> [-h] [-g GRAPH] [-n] [-p] [-e] [-q] [-v]



optional arguments:

      -h, --help              show this help message and exit
      -g GRAPH, --graph GRAPH
                              output AMR graphs
                              GRAPH=n: normal graphs
                              GRAPH=s: simple graphs (without :instance label)
      -n, --node              output AMR nodes
      -p, --path              output AMR paths
      -e, --entity            output named entities
      -q, --query             output named entity queries
      -v VISUALIZATION, --visualization VISUALIZATION
                              output html format visualization
                              VISUALIZATION=n: normal graphs
                              VISUALIZATION=s: simple graphs

- Your input should be raw AMR format (see ./amr/tests/test_amr_doc/test).
- If you would like to use AMR visualization functionality, please install [PyGraphviz](https://pygraphviz.github.io/) first.<br>
- If you would like to modify the output format, please modify ./amr/src/output.py file.

## Example
   First, what is the biggest puzzle between China and the US?<br>

      (p / puzzle-01
         :ARG0 (a / amr-unknown)
         :ARG1 (b2 / between
               :op1 (c / country :wiki "China"
                     :name (n / name :op1 "China"))
               :op2 (c2 / country :wiki "United_States"
                     :name (n2 / name :op1 "US")))
         :mod (b / big
               :degree (m / most))
         :li (x / 1))

Graph:<br>

      Green Ellispe: concept
      Orange Ellispe: predict with sense
      Black Ellispe: constant
      Blue Rectangle: named entity
![alt tag](https://github.com/panx27/amr-reader/blob/master/docs/example.png)

## Citation
If you would like to cite this work, please cite the following publication: <br>
[Unsupervised Entity Linking with Abstract Meaning Representation](http://nlp.cs.rpi.edu/paper/amrel.pdf).
