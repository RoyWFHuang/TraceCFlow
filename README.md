How to execute and test
```
$ source add_line.sh; gcc test.c test2.c;./out
```

the result will be:
```
main (12)
main (13)
main (14)
testprint (5)
test2.c - testprint(5) in printf 
testprint (6)
main (15)
main_test (6)
main_test (7)
test.c - main_test(7) in printf (3)
main_test (8)
main (16)
test.c - main(16) in printf 
main (17)
main (18)
```
