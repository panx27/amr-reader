# amr_reader
Input: raw AMR<br>
Output: AMR graphs, AMR paths

## Example
PROXY_APW_ENG_20080515_0931.31<br>
   The Yuri dolgoruky is the first in a series of new nuclear submarines to be commissioned this year but the bulava nuclear-armed missile developed to equip the submarine has failed tests and the deployment prospects are uncertain.<br>

    (c3 / contrast-01
      :ARG1 (c / commission-01
            :ARG1 (p / product :wiki "Russian_submarine_Yury_Dolgorukiy_(K-535)"
                  :name (n / name :op1 "Yuri" :op2 "Dolgoruky")
                  :mod (f2 / first
                        :ARG1-of (i / include-91
                              :ARG2 (s / series
                                    :mod (s2 / submarine
                                          :mod (n2 / nucleus)
                                          :mod (n3 / new))))))
            :time (y / year
                  :mod (t / this))))

Paths:<br>
root to entity:<br>

      contrast-01 --> (:ARG1) commission-01 --> (:ARG1) product	Yuri Dolgoruky
entity to leaf:<br> 

      product	Yuri Dolgoruky --> (:mod) first --> (:ARG1-of) include-91 --> (:ARG2) series --> (:mod) submarine --> (:mod) nucleus
      product	Yuri Dolgoruky --> (:mod) first --> (:ARG1-of) include-91 --> (:ARG2) series --> (:mod) submarine --> (:mod) new

Graph:<br>

      Green Ellispe: concept
      Orange Ellispe: concept with sense
      Blue Rectangle: named entity
![alt tag](https://github.com/panx27/amr-reader/blob/master/example.png)

## Citation
If you would like to cite this work, please cite the following publication: <br>
Unsupervised Entity Linking with Abstract Meaning Representation.
