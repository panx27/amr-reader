## Usage

      python main.py [-h] [-g] [-n] [-e] [-q] [directory of AMR files]

optional arguments:

      -g, --graph   output AMR graphs '../output/graphs/'
      -n, --node    output AMR nodes '../output/amr_nodes'
      -e, --entity  output named entities '../output/nes'
      -q, --query   output named entity queries '../output/queries'

If you would like to use AMR visualization functionality, please install [PyGraphviz](https://pygraphviz.github.io/) first.
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
      Orange Ellispe: concept with sense
      Blue Rectangle: named entity
![alt tag](https://github.com/panx27/amr-reader/blob/master/example.png)

## Citation
If you would like to cite this work, please cite the following publication: <br>
[Unsupervised Entity Linking with Abstract Meaning Representation](http://nlp.cs.rpi.edu/paper/amrel.pdf).
