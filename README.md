## Quickstart

      python amr_reader/main.py <directory of AMR files> <directory of output files> [-h] [-g GRAPH] [-n] [-p] [-e] [-q] [-v VISUALIZATION]
      e.g., python amr_reader/main.py amr-reader/test/test_amr_doc/ output/ -v=n


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
      I am cautiously anticipating the GOP nominee in 2012 not to be Mitt Romney.

      (a / anticipate-01
      :ARG0 (i / i)
      :ARG1 (n / nominate-01 :polarity -
            :ARG0 (p2 / political-party 
                        :wiki "Republican_Party_(United_States)" 
                        :name (n3 / name :op1 "GOP"))
            :ARG1 (p / person
                  :wiki "Mitt_Romney" 
                  :name (n2 / name :op1 "Mitt" :op2 "Romney"))
            :time (d / date-entity :year 2012)))

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
