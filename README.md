# amr_reader
Input: raw AMR

Output: AMR graph, AMR paths

PROXY_APW_ENG_20080515_0931.31
The Yuri dolgoruky is the first in a series of new nuclear submarines to be commissioned this year but the bulava nuclear-armed missile developed to equip the submarine has failed tests and the deployment prospects are uncertain.

(c3 / contrast-01
      :ARG1 (c / commission-01
            :ARG1 (p / product :wiki "Russian_submarine_Yury_Dolgorukiy_K-535"
                  :name (n / name :op1 "Yuri" :op2 "Dolgoruky")
                  :mod (f2 / first
                        :ARG1-of (i / include-91
                              :ARG2 (s / series
                                    :mod (s2 / submarine
                                          :mod (n2 / nucleus)
                                          :mod (n3 / new))))))
            :time (y / year
                  :mod (t / this))))

![alt tag](https://github.com/panx27/amr-reader/blob/master/example.png)
