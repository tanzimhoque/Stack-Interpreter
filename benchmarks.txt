Fibonacci of 10,000,000 (LARGE)

Interpreter 1 JIT
-8398834052292539589
===> multitime results
1: ./interpreterjit-c fibonacci
            Mean        Std.Dev.    Min         Median      Max
real        0.144       0.003       0.140       0.146       0.148       
user        0.138       0.003       0.132       0.136       0.144       
sys         0.004       0.003       0.000       0.004       0.008  


Interpreter 1 No JIT
-8398834052292539589
===> multitime results
1: ./interpreternojit-c fibonacci
            Mean        Std.Dev.    Min         Median      Max
real        0.465       0.003       0.460       0.464       0.469       
user        0.460       0.003       0.456       0.460       0.468       
sys         0.001       0.002       0.000       0.000       0.004   


Interpreter 2 JIT
-8398834052292539589
===> multitime results
1: ./interpreterjit-c fibonacci
            Mean        Std.Dev.    Min         Median      Max
real        0.127       0.004       0.123       0.128       0.135       
user        0.120       0.005       0.116       0.118       0.132       
sys         0.004       0.003       0.000       0.004       0.008   


Intepreter 2 No JIT
-8398834052292539589
===> multitime results
1: ./interpreternojit-c fibonacci
            Mean        Std.Dev.    Min         Median      Max
real        0.450       0.003       0.444       0.450       0.454       
user        0.446       0.003       0.440       0.448       0.452       
sys         0.002       0.002       0.000       0.000       0.004 
