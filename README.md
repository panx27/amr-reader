## Quickstart

      bin/amr_reader <directory of AMR files> <directory of output files> [-h] [-g GRAPH] [-n] [-p] [-e] [-q] [-v VISUALIZATION]
      e.g., bin/amr_reader amr-reader/test/test_amr_doc/ output/ -v=n


optional arguments:

      -h, --help              show this help message and exit
      -g GRAPH, --graph GRAPH
                              output AMR graphs
                              GRAPH=n: normal graphs
                              GRAPH=s: simplified graphs (without :instance label)
      -n, --node              output AMR nodes
      -p, --path              output AMR paths
      -e, --entity            output named entities
      -q, --query             output named entity queries
      -v VISUALIZATION, --visualization VISUALIZATION
                              output html format visualization
                              VISUALIZATION=n: normal graphs
                              VISUALIZATION=s: simplified graphs

- Your input should be raw AMR format (see amr-reader/tests/test_amr_doc/test).
- If you would like to use AMR visualization functionality, please install [PyGraphviz](https://pygraphviz.github.io/) first.<br>
- If you would like to modify the output format, you could modify amr-reader/src/output.py file.

## Example
   Sentence: First, what is the biggest puzzle between China and the US?<br>
   AMR:<br>

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

  Visualization:<br>

      Green Ellispe: concept
      Orange Ellispe: predict with sense
      Black Ellispe: constant
      Blue Rectangle: named entity
![alt tag](https://github.com/panx27/amr-reader/blob/master/docs/example.png)

## Citation
If you would like to cite this work, please cite the following publication: <br>
[Unsupervised Entity Linking with Abstract Meaning Representation](http://nlp.cs.rpi.edu/paper/amrel.pdf).

## Demo
[AMR based Entity Linker](https://blender04.cs.rpi.edu/~panx2/amr/)
