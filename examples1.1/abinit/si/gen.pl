@names=split(' ',`echo *.sys | sed s/.sys//g`);

foreach $n (@names) { 
open(OUT, ">$n.hf");
print OUT "
method { VMC nconfig 10 nstep 10 nblock 10 timestep 1.0 } 
include $n.sys
trialfunc { include $n.slater } 
";
close(OUT);
}
