## Quickstart

      python amrreader/main.py [-h] [-g GRAPH] [-n] [-p] [-e] [-v VISUALIZATION] indir outdir
      e.g., python amrreader/main.py amrreader/test/test_amr_doc/ output/ -v=n


      positional arguments:
        indir                 directory to AMR input files
        outdir                output directory

      optional arguments:
        -g GRAPH, --graph GRAPH
                              generate AMR graphs -g=n: standard graphs
                                                  -g=s: simplified graphs
        -n, --node            generate AMR nodes
        -p, --path            generate AMR paths
        -e, --entity          generate named entities
        -v VISUALIZATION, --visualization VISUALIZATION
                              generate html visualization -v=n: standard graphs
                                                          -v=s: simplified graphs

- Ptyhon3
- Your input should be raw AMR format (see amr-reader/tests/test_amr_doc/test).
- If you would like to use AMR visualization functionality, please install [PyGraphviz](https://pygraphviz.github.io/) first.<br>

## Example
      # ::snt I am cautiously anticipating the GOP nominee in 2012 not to be Mitt Romney.

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
[AMR based Entity Linker](http://panx27.github.io/amr)

## API
[AMR based Entity Linker](http://panx27.github.io/amr_api)
