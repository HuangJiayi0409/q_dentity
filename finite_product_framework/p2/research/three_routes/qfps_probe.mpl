restart:
interface(prettyprint=0):
read "vendor/qFPS.mpl":
with(qFPS):
writeto("qfps_probe.log"):
printf("P2_QFPS_LOADED\n"):
printf("VERSION %a\n",kernelopts(version)):
# Supported built-in sanity test, not a train identity proof.
try
  sanity := timelimit(20,qHolonomicRE(LittleqJacobi(n,a,b,t,q),F(t),var=q)):
  printf("SANITY_RE %a\n",sanity):
catch:
  printf("SANITY_ERROR %a\n",[lastexception]):
end try:
# Transcription of the 9.Ex5ii RHS. Generic qPhi requires a terminating-series
# bridge before it may be identified with the frozen finite Lean definition.
gfInput := qphihypergeom([q^(x-N),b*q^(x+1)],[q^(-N)/c],t*q^(-x),q)
       *qpochhammer(b*c*q*t,q,x):
printf("GF_INPUT %a\n",gfInput):
try
  phiRE := timelimit(30,qHolonomicRE(op(1,gfInput),F(t),var=q)):
  printf("GF_PART1_RE %a\n",phiRE):
  pochRE := timelimit(30,qHolonomicRE(op(2,gfInput),F(t),var=q)):
  printf("GF_PART2_RE %a\n",pochRE):
  gfRE := timelimit(45,qProductRE(phiRE,pochRE,F(t),var=q)):
  printf("GF_FUNCTION_RE %a\n",gfRE):
  coeffRE := timelimit(30,qREtoRE(gfRE,F(t),A(j),var=q)):
  printf("GF_COEFFICIENT_RE %a\n",coeffRE):
  sol := timelimit(30,qHypergeomSolveRE(coeffRE,A(j),var=q,output=basis)):
  printf("GF_COEFFICIENT_SOLUTIONS %a\n",sol):
catch:
  printf("GF_ERROR %a\n",[lastexception]):
end try:
# Algebraic placeholder normalization: the parameters here are independent of t.
# This is a separate adapter experiment, not an assertion that the original
# finite truncation has already been proved equivalent.
try
  kernelopts(opaquemodules=false):
  genericRE := timelimit(25,qFPS:-qphihypergeomRE([U,V],[W],t,q,F(t),var=q)):
  printf("GENERIC_PHI_RE %a\n",genericRE):
  scaledRE := subs(U=q^(x-N),V=b*q^(x+1),W=q^(-N)/c,t=q^(-x)*t,genericRE):
  # Reset all shifted F arguments after substituting the independent variable.
  scaledRE := subs(F(q^(-x)*t)=F(t),scaledRE):
  printf("SCALED_PHI_RE %a\n",scaledRE):
  productRE := timelimit(35,qProductRE(genericRE,
      (1-H*t)*Sq[t](F(t))-(1-H*Q*t)*F(t)=0,F(t),var=q)):
  printf("GENERIC_PRODUCT_RE %a\n",productRE):
  genericCoeffRE := timelimit(20,qREtoRE(productRE,F(t),A(j),var=q)):
  printf("GENERIC_COEFFICIENT_RE %a\n",genericCoeffRE):
catch:
  printf("GENERIC_ERROR %a\n",[lastexception]):
end try:
# Raw AW representation probe only. The specialized divided-difference/basis
# preprocessing in the AW paper is NOT implemented by this call.
aw := qphihypergeom([q^(-n),a*b*c*d*q^(n-1),a*z,a/z],[a*b,a*c,a*d],q,q):
try
  awRE := timelimit(30,qHolonomicRE(aw,G(z),var=q)):
  printf("AW_RAW_RE %a\n",awRE):
catch:
  printf("AW_RAW_ERROR %a\n",[lastexception]):
end try:
printf("P2_QFPS_FINISHED\n"):
writeto(terminal):
quit:
