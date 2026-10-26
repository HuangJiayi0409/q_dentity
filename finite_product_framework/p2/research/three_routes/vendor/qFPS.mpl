## Maple-Package qFPS 
## 
## Dr. Torsten Sprenger
## Work Group Computational Mathematics
## Institute of Mathematics
## University of Kassel
##
## Phone:    +49 561 804 4192
## Fax:      +49 561 804 4646
## E-Mail:   sprenger@mathematik.uni-kassel.de
## Homepage: http://www.mathematik.uni-kassel.de/~sprenger
##
## December 2011
      
unprotect('qFPS'):
qFPS:=module()
   option package;
   export
      # q-functions
      qbrackets,                                                  # q-brackets
      qfactorial,                                                 # q-factorial
      qbinomial,                                                  # q-binomial
      qpower1,`qdiff/qpower1`,`qshift/qpower1`,                   # q-power
      qpower2,`qdiff/qpower2`,`qshift/qpower2`,                      
      qpower,`qdiff/qpower`,`qshift/qpower`,                      
      qpochhammer,`qdiff/qpochhammer`,`qshift/qpochhammer`,       # q-pochhammer symbol
      qphihypergeom,`qdiff/qphihypergeom`,`qshift/qphihypergeom`, # generalized q-hypergeometric function 
      qexp,`qdiff/qexp`,`qshift/qexp`,                            # small q-exponential function
      qExp,`qdiff/qExp`,`qshift/qExp`,                            # big q-exponential function
      expq,`qdiff/expq`,`qshift/expq`,                            # small q-exponential function (Kac/Cheung)
      Expq,`qdiff/Expq`,`qshift/Expq`,                            # big q-exponential function (Kac/Cheung)
      logq,`qdiff/logq`,`qshift/logq`,                            # q-logarithm function
      qsin,`qdiff/qsin`,`qshift/qsin`,                            # small q-sine function
      qSin,`qdiff/qSin`,`qshift/qSin`,                            # big q-sine function
      sinq,`qdiff/sinq`,`qshift/sinq`,                            # small q-sine function (Kac/Cheung)
      Sinq,`qdiff/Sinq`,`qshift/Sinq`,                            # big q-sine function (Kac/Cheung)
      qcos,`qdiff/qcos`,`qshift/qcos`,                            # small q-cosine function
      qCos,`qdiff/qCos`,`qshift/qCos`,                            # big q-cosine function
      cosq,`qdiff/cosq`,`qshift/cosq`,                            # small q-cosine function (Kac/Cheung)
      Cosq,`qdiff/Cosq`,`qshift/Cosq`,                            # big q-cosine function (Kac/Cheung)
      qLaguerre,`qdiff/qLaguerre`,`qshift/qLaguerre`,             # q-Laguerre polynomial
      BigqLaguerre,`qdiff/BigqLaguerre`,`qshift/BigqLaguerre`,    # big q-Laguerre polynomial
      LittleqLaguerre,`qdiff/LittleqLaguerre`,`qshift/LittleqLaguerre`,                # little q-Laguerre polynomial
      LittleqJacobi,`qdiff/LittleqJacobi`,`qshift/LittleqJacobi`,                      # little q-Jacobi polynomial
      LittleqLegendre,`qdiff/LittleqLegendre`,`qshift/LittleqLegendre`,                # little q-Legendre polynomial
      BigqJacobi,`qdiff/BigqJacobi`,`qshift/BigqJacobi`,                               # big q-Jacobi polynomial
      BigqLegendre,`qdiff/BigqLegendre`,`qshift/BigqLegendre`,                         # big q-Legendre polynomial
      qMeixner,`qdiff/qMeixner`,`qshift/qMeixner`,                                     # q-Meixner polynomial
      QuantumqKrawtchouk,`qdiff/QuantumqKrawtchouk`,`qshift/QuantumqKrawtchouk`,       # Quantum-q-Krawtchouk polynomial
      qKrawtchouk,`qdiff/qKrawtchouk`,`qshift/qKrawtchouk`,                            # q-Krawtchouk polynomial
      AffineqKrawtchouk,`qdiff/AffineqKrawtchouk`,`qshift/AffineqKrawtchouk`,          # affine q-Krawtchouk polynomial
      DiscreteqHermiteI,`qdiff/DiscreteqHermiteI`,`qshift/DiscreteqHermiteI`,          # discrete q-Hermite I polynomial
      DiscreteqHermiteII,`qdiff/DiscreteqHermiteII`,`qshift/DiscreteqHermiteII`,       # discrete q-Hermite II polynomial
      AlSalamCarlitzI,`qdiff/AlSalamCarlitzI`,`qshift/AlSalamCarlitzI`,                # q-Al-Salam-Carlitz I polynomial
      AlSalamCarlitzII,`qdiff/AlSalamCarlitzII`,`qshift/AlSalamCarlitzII`,             # q-Al-Salam-Carlitz II polynomial
      qCharlier,`qdiff/qCharlier`,`qshift/qCharlier`,                                  # q-Charlier polynomial
      AlternativeqCharlier,`qdiff/AlternativeqCharlier`,`qshift/AlternativeqCharlier`, # alternative q-Charlier polynomial
      qHahn,`qdiff/qHahn`,`qshift/qHahn`,                                              # q-Hahn polynomial
      StieltjesWigert,`qdiff/StieltjesWigert`,`qshift/StieltjesWigert`,                # q-Stieltjes-Wigert polynomial
      qBernstein,`qdiff/qBernstein`,`qshift/qBernstein`,                               # q-Bernstein polynomials

      # q-routines
      
      # routines for q-differentiation and q-shifting
      qdiff,                  # routine for q-differentiation
      qshift,                 # routine for computing q-shifts
            
      # routines of q-holonomic algebra
      qHolonomicDE,           # routine for computing q-holonomic differential equations
      qHolonomicRE,           # routine for computing q-holonomic recurrence equations
      qSumDE,                 # routine for computing the sum of two q-holonomic differential equations
      qSumRE,                 # routine for computing the sum of two q-holonomic recurrence equations
      qProductDE,             # routine for computing the product of two q-holonomic differential equations
      qProductRE,             # routine for computing the product of two q-holonomic recurrence equations
      qCompositionDE,         # routine for computing the composition of a q-holonomic differential equation and g(x)=a*x^b
      qCompositionRE,         # routine for computing the composition of a q-holonomic recurrence equation and g(x)=a*x^b
      qDivideRE,              # routine for left or right dividing a q-recurrence operator by another q-recurrence operator
      qMultiplyRE,            # routine for left or right multiplying a q-recurrence operator with another q-recurrence operator
      qGCD,                   # routine for computing the greatest common right divisor of two q-recurrence operators
      qLCM,                   # routine for computing the least common left multiple of two q-recurrence operators
      qAdjoint,               # routine for computing the q-adjoint of a q-recurrence operator
      
      # routines for conversion between q-recurrences
      DqtoSq,                 # routine for expressing a higher q-derivative in Dq-operator form as linear combination of q-shifts in Sq-operator form
      SqtoDq,                 # routine for expressing a q-shift in Sq-operator form as linear combination of q-derivatives in Dq-operator form 
      Dqtoqdiff,              # routine for computing the explicit q-derivative out of an q-derivative in Dq-operator form
      Sqtoqshift,             # routine for computing the explicit q-shift out of an q-shift in Sq-operator form
      qDEtoqRE,               # routine for converting a q-holonomic differential equation into a q-holonomic recurrence equation
      qREtoqDE,               # routine for converting a q-holonomic recurrence equation into a q-holonomic differential equation  
      qREtoqRE,               # routine for converting between the different notations of q-holonomic recurrence equations
      qDEtoRE,                # routine for converting a q-holonomic differential equation of an expression f into a recurrence equation for the coefficients of the power series of f             
      qREtoRE,                # routine for converting a q-holonomic recurrence equation of an expression f into a recurrence equation for the coefficients of the power series of f             
      REtoqDE,                # routine for converting a recurrence equation for the coefficients of the power series of an expression f into a q-holonomic differential equation of f              
      REtoqRE,                # routine for converting a recurrence equation for the coefficients of the power series of an expression f into a q-holonomic recurrence equation of f              
      qREtohomqRE,            # routine for converting an inhomogoneous q-recurrence equation into a q-holonomic recurrence equation              
      qDEtohomqDE,            # routine for converting an inhomogoneous q-differential equation into a q-holonomic differential equation              

      # routines for solving q-recurrence equations
      qPolUpperBound,         # routine for determing the upper degreebound of all polynomial solutions of a q-holonomic recurrence equation 
      qUniversalDenominator,  # routine for determing the universal denominator of all rational solutions of a q-holonomic recurrence equation 
      qPolynomialSolveRE,     # routine for getting all polynomial solutions of a q-recurrence equation
      qRationalSolveRE,       # routine for getting all rational solutions of a q-recurrence equation
      qHypergeomTypeSolveRE,  # routine for solving a q-recurrence equation of q-hypergeometric type
      qHypergeomSolveRE,      # routine for solving a linear q-recurrence equation 
      
      # miscellaneous q-routines  
      qsimpcomb,qsimplify,    # routine for simplification of/to q-hypergeometric terms
      qShiftRE,               # routine for shifting a recurrence equation to positive or negative q-shifts
      qOrder,                 # routine for computing the order of a q-holonomic recurrence/differential equation 
      qContent,               # routine for determing the content of a q-holonomic recurrence/differential equation
      qNormal,                # routine for determing the normal form of a q-holonomic recurrence/differential equation
      qCertificate,           # routine for determing the q-certificate of a q-hypergeometric term
      qShiftRelation,         # routine for computing the q-shift relation for a generalized q-hypergeometric function
      qContiguityRelation,    # routine for computing the q-contiguity relation for a generalized q-hypergeometric function 
      qRelation,              # routine for computing the q-shift/q-contiguity relation for a generalized q-hypergeometric function
      
      # routines for q-Van-Hoeij algorithm
      qPlotNewtonPolygon,     # routine for plotting the newton polygon of a q-recurrence equation
      qNewtonPolygon,         # routine for determing the newton polygon of a q-recurrence equation
      qDispersion,            # routine for determing the q-dispersion or q-dispersion set of two polynomials
      qShiftEquivalent,       # routine for checking whether two q-expressions are q-shift equivalent or not
      qFactors,               # routine for determing the factors of a polynomial (in q-shift equivalence classes)
      qFactorsOperator,       # routine for determing the factors of two polynomials (in q-shift equivalence classes)
      qLocalTypes,            # routine for determing the local type of a q-hypergeometric term
      qLocalTypesCandidates,  # routine for determing the candidates of the local types 
      
      # auxiliary procedures
      qCompare,               # routine for checking identities of q-hypergeometric terms and sums
      
      # routines for expansion of package
      addqdiff,addqshift,addqrec;   # routines for adding q-derivative rules, q-shift rules or q-recurrence equations
      
   local 
      qfunctions,qdiffs,qshifts,qrecs, # tables of q-functions,q-derivatives and q-shifts    
      qSimplifyRE,            # routine for reducing a recurrence equation (help function for qHolonomicRE)
      qFPSnormal,             # routine for representing formal power series simplified
      orderRE,                # routine for determing the order of a recurrence equation
      contentRE,              # routine for determing the content of a recurrence equation
      shiftRE,                # routine for shifting a recurrence equation, so that only positive shifts appear
      qEQtoPol,               # routine for converting a q-recurrence equation or a q-differential equation into a polynomial
      qPoltoRE,               # routine for converting a polynomial into a q-recurrence equation 
      qcontentPol,            # routine for determing the content of a polynomial    
      qreduceRE,              # routine for reducing an expression of Sq-operators by a given q-recurrence equation 
      qreduceDE,              # routine for reducing an expression of Dq-operators by a given q-differential equation 
      qgetoperator,           # routine for extracting several information out of a q-shifted function in Sq-operator form or a q-derivative in Dq-operator form
      qsetoperator,           # routine for setting the operator form 
      qtoqpochhammer,         # routine for determing the q-pochhammer symbol out of one factor of the q-ratio of a q-hypergeometric term
      qgetargs,               # routine for getting the a[i]'s and n[i]'s, so that u[i]=a[i]*q^n[i] for all elements of list u (help routine of procedures involving qphihypergeom)
      qgetfactors,            # routine for getting every factor out of an expression (help routine of qPetkovsek) 
      qgetcoeffs,             # routine for getting the coefficients of a q-holonomic recurrence or differential equation 
      qphihypergeomDE,        # routine for determing the q-differential equation of a generalized q-hypergeometric function
      qphihypergeomRE,        # routine for determing the q-recurrence equation of a generalized q-hypergeometric function
      qFPSHypergeomTypeSolveRE,  # routine for determing the summand(s) of a formal power series out of a q-recurrence equation of q-hypergeometric type
      qFPSHypergeomSolveRE;      # routine for determing the summand(s) of a formal power series out of a general q-recurrence equation via q-Petkovsek algorithm
   
   global 
      `convert/qFPS`,         # routine for computing the formal power series for a q-holonomic function 
      `convert/qphihypergeom`,# routine for computing the q-hypergeometric representation of a q-holonomic function/q-hypergeometric series 
      `convert/qfactorial`,   # routine for converting q-pochhammer symbols into q-factorials 
      `convert/qbinomial`,    # routine for converting q-pochhammer symbols into q-binomials 
      `convert/qpochhammer`,  # routine for converting q-factorials and q-binomials into q-pochhammer symbols 
      `simplify/qpochhammer`, # routine for combining several q-pochhammer symbols to one q-pochhammer symbol
      `simplify/power2`,      # routine for simplifying terms like 1/(-1)^k
      `simplify/qFPS`,        # routine for simplifying q-formal power series
      `combine/qFPS`,         # routine for combining q-formal power series into a single q-formal power series
      Dq,Sq;                  # operators
   

qsimpcomb := proc(expr::algebraic,{QDE::boolean:=false})
local f,expterms,i,term,result;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
f:=expr;
if QDE then
   f:=applyrule(qpower(a::anything,b::anything,c::anything,d::anything)=a^d*qpochhammer(b/a,c,d),f);
   f:=subs(qpochhammer=QDifferenceEquations['QPochhammer'],qbinomial=QDifferenceEquations['QBinomial'],
           qfactorial=QDifferenceEquations['QFactorial'],qGAMMA=QDifferenceEquations['QGAMMA'],f);
   f:=QDifferenceEquations['QSimpComb'](f);
   f:=subs(QDifferenceEquations['QPochhammer']=qpochhammer,QDifferenceEquations['QBinomial']=qbinomial,
           QDifferenceEquations['QFactorial']=qfactorial,QDifferenceEquations['QGAMMA']=qGAMMA,f);
else
   f:=QDifferenceEquations['QSimpComb'](f): 
end if;

# due to error in QDifferenceEquations['QSimpComb']!?!
expterms:=indets(f,specfunc(anything,exp));
if not expterms={} and nops(expterms)=1 then
   term:=op([1,1],expterms)/Pi*2;
   if type(term,'`*`') and nops(term)=2 then
      if not convert(op(1,term),string)="Imagin" then
         result:=subs(k=op(1,term),I^k)
      else 
         result:=subs(k=op(2,term),I^k)
      end if;
      return applyrule(exp(y::anything)=result,f)
   elif type(term,symbol) and convert(term,string)="Imagin" then
      return applyrule(exp(y::anything)=I,f)
   end if;
end if;
f
end proc:


qsimplify := proc(expr::algebraic,{QDE::boolean:=false})
local f,expterms,i,term,result;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
f:=expr;
if QDE then
   f:=applyrule(qpower(a::anything,b::anything,c::anything,d::anything)=a^d*qpochhammer(b/a,c,d),f);
   f:=subs(qpochhammer=QDifferenceEquations['QPochhammer'],qbinomial=QDifferenceEquations['QBinomial'],
           qfactorial=QDifferenceEquations['QFactorial'],qGAMMA=QDifferenceEquations['QGAMMA'],expr);
   f:=QDifferenceEquations['QSimplify'](f);
   f:=subs(QDifferenceEquations['QPochhammer']=qpochhammer,QDifferenceEquations['QBinomial']=qbinomial,
           QDifferenceEquations['QFactorial']=qfactorial,QDifferenceEquations['QGAMMA']=qGAMMA,f);
else
   f:=QDifferenceEquations['QSimplify'](f): 
end if;

# due to error in QDifferenceEquations['QSimplify']!?!
expterms:=indets(f,specfunc(anything,exp));
if not expterms={} and nops(expterms)=1 then
   term:=op([1,1],expterms)/Pi*2;
   if type(term,'`*`') and nops(term)=2 then
      if not convert(op(1,term),string)="Imagin" then
         result:=subs(k=op(1,term),I^k)
      else 
         result:=subs(k=op(2,term),I^k)
      end if;
      return applyrule(exp(y::anything)=result,f)
   elif type(term,symbol) and convert(term,string)="Imagin" then
      return applyrule(exp(y::anything)=I,f)
   end if;
end if;
f
end proc:
      
Dq:=Dq:
Sq:=Sq:  


# LOCAL PROCEDURES


qEQtoPol := proc(expr::Or(algebraic,equation),Fx::function,y::name,q::algebraic)
local F,x,n,i,rules,pol;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
n:=qOrder(expr,F(x),var=q);
if has(expr,Sq) then 
   rules:=seq(qshift(F(x),[x$(n-i)],q)=y^(n-i),i=0..n)
else
   rules:=seq(qdiff(F(x),[x$(n-i)],q)=y^(n-i),i=0..n)
end if;
pol:=subs(rules,expr);
if type(pol,equation) then
   lhs(pol)-rhs(pol)
else
   pol
end if;
end proc:


qPoltoRE := proc(expr::algebraic,y::name,Fx::function,q::algebraic)
local F,x,n,i,rules;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
n:=degree(expr,y);
rules:=seq(y^(n-i)=qshift(F(x),[x$(n-i)],q),i=0..n-1);
collect(subs({rules},expr)-coeff(expr,y,0)+coeff(expr,y,0)*F(x),Sq,factor@qsimpcomb)
end proc:


qsetoperator := proc(operator::symbol,x::Or(list,name),f::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if type(x,'list') then 
   operator[op(x)](f)
else                 
   operator[x](f)
end if; 
end proc:


qgetoperator := proc(f::algebraic,{Op::boolean:=false,Arg::boolean:=false,X::boolean:=false,N::boolean:=false,Xlist::boolean:=false})
local g,n,x,xlist,operator,arg;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
arg:=NULL;
if has(f,Sq) or has(f,Dq) then
   if type(op(0,f),'indexed') then 
      g:=op(0,f);
      arg:=op(f);
   else 
      g:=f
   end if;
   if op(0,g)=Dq or op(0,g)=Sq then
     operator:=op(0,g);
     xlist:=[op(g)];
     n:=nops(xlist);
     x:=op(1,xlist);
     if Op then 
        return operator                # returns operator      
     end if;
     if Arg then                        
        return arg                     # returns operand
     end if;
     if X then                         
        return x                       # returns the first element of the list of the q-shifted/q-derived variables 
     end if;
     if N then                         
        return n                       # returns the n of the n-th q-shift/q-derivative
     end if;
     if Xlist then                     
        return xlist                   # returns list of all q-shifted/q-derived variables
     end if;
     return [operator,xlist,x,n,arg]
   end if;
else 
   if Op then 
      return NULL                      # returns operator      
   end if;
   if Arg then                          
      return f                         # returns operand
   end if;
   if X then                        
      return NULL                      # returns the first element of the list of the q-shifted/q-derived variables 
   end if;
   if N then                        
      return 0                         # returns the n of the n-th q-shift/q-derivative
   end if;
   if Xlist then                    
      return NULL                      # returns list of all q-shifted/q-derived variables
   end if;
   f
end if;
end proc:


qgetcoeffs := proc(EQ::Or(algebraic,equation),Fx::function,q::algebraic)
local F,x,y,n,i,Eq,Pol,RE,arg;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
arg:=map(op,select(has,indets(EQ,function),F)); # arguments
if type(EQ,equation) then
   Eq:=lhs(EQ)-rhs(EQ)
else
   Eq:=EQ
end if;
if has(Eq,Dq) or has(Eq,Sq) then
   Eq:=collect(Eq,{Sq,Dq});
   Pol:=qEQtoPol(Eq,F(x),y,q);
   n:=degree(Pol,y);
   return [seq(coeff(Pol,y,i),i=0..n)]
elif has(arg,q) then 
   n:=qOrder(Eq,F(x),var=q);
   return [seq(coeff(Eq,F(q^i*x)),i=0..n)]
else
   n:=qOrder(Eq,F(x),var=q);
   return [seq(coeff(Eq,F(x+i)),i=0..n)]
end if;
end proc:


qreduceDE := proc(expr::algebraic,Fx::function,DE::Or(algebraic,equation),q::algebraic)
local redexpr,n,m,subsDE,F,x;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
n:=qOrder(DE,F(x),var=q);
m:=qOrder(expr,F(x),var=q);
subsDE:=solve(DE,qdiff(F(x),[x$n],q));  
if m>=n then 
   redexpr:=subs(qdiff(F(x),[x$m],q)=qdiff(subsDE,[x$m-n],q),expr); # substitution rule given by q-holonomic differential equation DE
   qreduceDE(redexpr,F(x),DE,q) # apply qreduceDE recursively
else 
   collect(expr,{Dq,F(x)})
end if;
end proc:


qreduceRE := proc(expr::algebraic,Fx::function,RE::Or(algebraic,equation),q::algebraic)
local redexpr,n,m,subsRE,F,x;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
n:=qOrder(RE,F(x),var=q);
m:=qOrder(expr,F(x),var=q);
subsRE:=solve(RE,qshift(F(x),[x$n],q));  
if m>=n then 
   redexpr:=subs(qshift(F(x),[x$m],q)=qshift(subsRE,[x$m-n],q),expr); # substitution rule given by q-holonomic recurrence equation RE
   qreduceRE(redexpr,F(x),RE,q) # apply qreduceRE recursively
else 
   collect(expr,{Sq,F(x)})
end if;
end proc:


qcontentPol := proc(pol::algebraic,x::algebraic,{eq::boolean:=false})
local p,i,cont;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
p:=factor(qsimpcomb(pol));

cont:=1;
if type(p,'`*`') then
   for i from 1 to nops(p) do
      if not has(op(i,p),x) then
         cont:=cont*op(i,p)
      end if;
   end do;
end if;

if eq then 
   collect(normal(p/cont),x,factor@qsimpcomb)
else
   cont
end if;  
end proc:


qtoqpochhammer := proc(f::algebraic,q::algebraic,k::name,{delta::posint:=1,rho::nonnegint:=0,initial::algebraic:=0,output::identical(qpochhammer,parameter):='qpochhammer'})
local expr,x,a,b,lambda;                                                                         
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;                
# requires application of qsimpcomb/qsimplify to work
expr:=subs(q^k=x,f);

if has(expr,x) then
   lambda:=degree(expr,x);
   a:=coeff(expr,x,lambda);
   b:=coeff(expr,x,0);
   if b=0 then
      if output=qpochhammer then
         (a*q^(rho*lambda))^(k-initial)*q^(delta*lambda*(binomial(k,2)-binomial(initial,2)))
      else 
         [(a*q^(rho*lambda))^(-initial)*q^(delta*lambda*(binomial(k,2)-binomial(initial,2))),(a*q^(rho*lambda))] # 1: constant, 2: base
      end if;
   else
      if output=qpochhammer then
         b^(k-initial)*qpochhammer(-a/b*q^(lambda*(delta*initial+rho)),q^(lambda*delta),k-initial)
      else
         [b^(-initial),-a/b*q^(lambda*(delta*initial+rho)),lambda*delta,k-initial,b] # 1: constant, 2: parameter, 3: q-argument, 4: argument, 5: base
      end if;
   end if;
else
   if output=qpochhammer then
      expr^(k-initial)
   else 
      [expr^(-initial),expr]
   end if;
end if;
end proc:


qSimplifyRE := proc(RElist::list,x::symbol,q::algebraic)
local Flist1,Flist2,newRElist,REFlist,L,F,Nargs,Args,a,X,n,rec,i,j,k,l,rat,coe;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
newRElist:=RElist;
Flist1:=indets(newRElist,'function');
Flist2:=map(t->[op(0,t),nops(t)],Flist1); # function name and nargs
for a in Flist2 do
   if assigned(qrecs[op(a)]) then
      F:=op(1,a); 
      Nargs:=op(2,a);
      REFlist:=select((t,f,n)->op(0,t)=f and nops(t)=n,Flist1,F,Nargs); # select those functions
      Args:=map((t,N)->[op(2..N,t)],REFlist,Nargs); # separate in different arguments, e.g. L(n,X) and L(n,Y)
      for X in Args do
         L:=map2(op,1,select((t,X,n)->[op(2..n,t)]=X,REFlist,X,Nargs));
         while nops(L)>2 do
            n:=max(op(L)); 
            if type(n,'function') then 
               n:=op(1,n) 
            end if:
            if member(n-1,L) and member(n-2,L) then
               rec:=qrecs[F,Nargs](n,op(X));
               for i from 1 to nops(newRElist) do
                  if has(newRElist[i],F(n,op(X))) then
                     for j from 1 to nops(newRElist[i]) do 
                        coe:=newRElist[i][j]/F(n,op(X));
                        for k from 1 to nops(rec) do
                           for l from 1 to nops(newRElist) do
                              rat:=qsimpcomb(coe*op(k,rec)/newRElist[l][1]);
                              if type(rat,ratpoly(ratpoly(anything,x),q^anything)) then 
                                 newRElist[l]:={qsimpcomb(coe*op(k,rec))} union newRElist[l];
                                 break;
                              end if; # add the substituted part of recurrence to the corresponding equivalence class
                           end do;
                        end do;
                     end do;
                     newRElist:=remove((t,m)->t=m,newRElist,newRElist[i]); # delete the right side of recurrence in equivalence class
                     break;    
                  end if;
               end do;
            end if:
            L:=L minus {n}
         end do
      end do
   end if
end do:
newRElist
end proc:


orderRE  := proc(RE::equation,Ak::function,{minimum::boolean:=false})
local A,k,Alist,klist;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
A:=op(0,Ak);
k:=op(1,Ak);
Alist:=indets(RE,specfunc(anything,A));       
klist:=subs(k=0,map(op,Alist));        
        
if minimum then
   min(op(klist))
else
   max(op(klist))-min(op(klist))
end if;
end proc:


shiftRE := proc(RE::equation,Ak::function)
local A,k,n;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
A:=op(0,Ak);
k:=op(1,Ak);
n:=orderRE(RE,Ak,'minimum');

contentRE(subs(k=k-n,RE),Ak,'eq')
end proc:


contentRE := proc(RE::equation,Ak::function,{eq::boolean:=false})
local A,k,rec,content,i,Alist;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
A:=op(0,Ak);
k:=op(1,Ak);
Alist:=indets(RE,specfunc(anything,A));     
rec:=factor(qsimpcomb(lhs(RE)-rhs(RE)));

content:=1;
if type(rec,'`*`') then
   for i from 1 to nops(rec) do
      if not has(op(i,rec),Alist) then
         content:=content*op(i,rec)
      end if;
   end do;
end if;

if eq then 
   collect(normal(rec/content),Alist,factor@qsimpcomb)=0
else
   content
end if;
end proc:


qgetargs := proc(u::list,q::algebraic)
local i,r,a,n,facq,fac;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
r:=nops(u);

# get a[i]'s and n[i]'s, so that u[i]=a[i]*q^n[i] 
for i from 1 to r do
   if has(u[i],q) then
      if type(u[i],'`*`') then
         facq:=simplify(select(has,u[i],q),power,symbolic);
         fac:=simplify(u[i]/facq,power,symbolic);
         if type(facq,'`^`') then
            if op(1,facq)=q then
               a[i]:=fac;
               n[i]:=op(2,facq)
            end if;
         elif facq=q then
            a[i]:=fac;
            n[i]:=1
         end if;
      elif type(u[i],'`^`') then
         if op(1,u[i])=q then
            a[i]:=1;
            n[i]:=op(2,u[i])
         end if;
      elif u[i]=q then
         a[i]:=1;
         n[i]:=1
      end if;
   else
      a[i]:=u[i];
      n[i]:=0
   end if;
end do;

[[seq(a[i],i=1..r)],[seq(n[i],i=1..r)]]
end proc:


qgetfactors := proc(expr::algebraic,x::symbol,{var::algebraic:='q',roots::set:={}})
local f,S,i,j,indexset;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if roots<>{} then
   try 
      f:=factor(expr,roots)
   catch:
      f:=factor(expr)
   end try;
else
   f:=factor(expr)
end if;
f:=convert(f,multiset); # factors in multiset
S:=[];
indexset:=[];
j:=1;
for i from 1 to nops(f) do 
   if has(op([i,1],f),x) then 
      S:=[op(S),op([i,1],f)];
      indexset:=[op(indexset),j $ op([i,2],f)];
      j:=j+1;
   end if;
end do;
S:=map(y->y/lcoeff(y,x),S);

[S,map(y->degree(y,x),S),map(y->ldegree(y,x),S),map(y->tcoeff(y,x),S),indexset] 
end proc:


qphihypergeomRE := proc(u::list,v::list,xarg::algebraic,qexpr::algebraic,Fx::function,{var::algebraic:='q',explicit::boolean:=false})
local F,x,i,SQ,qRE,r,s,d,n,m,a,b,j,coelist,explist,x1,x2,q1,q2,k,term,A,newterm,ratio,xterm,exppt,RE,coe,qvar,opt;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
r:=nops(u);
s:=nops(v);
# preprocessing
if not has(u,x) and not has(v,x) and not has(xarg,x) then 
   return qshift(F(x),x,var)-F(x)=0
end if;
if type(var,'`^`') and qexpr=1/var then
   qvar:=1/var;
elif type(qexpr,'`^`') and qexpr=var then 
   qvar:=1/var;
   qRE:=qphihypergeomRE(u,v,xarg,1/qexpr,Fx,subs(var=qvar,_options[-1]));
   n:=qOrder(qRE,F(x),subs(var=qvar,_options[-1]));
   coe:=qgetcoeffs(qRE,F(x),qvar);
   qRE:=qNormal(add(subs(qvar=1/qvar,coe[i])*qshift(F(x),[x$i-1],var),i=1..n+1)=0,F(x),subs(var=qvar,_options[-1]));
elif qexpr=1/var then
   qvar:=var;
   qRE:=qphihypergeomRE(u,v,xarg,1/qexpr,Fx,subs(var=1/qvar,_options[-1]));
   n:=qOrder(qRE,F(x),subs(var=1/qvar,_options[-1]));
   coe:=qgetcoeffs(qRE,F(x),qvar);
   qRE:=qNormal(add(subs(qvar=1/qvar,coe[i])*qshift(F(x),[x$i-1],var),i=1..n+1)=0,F(x),subs(var=qvar,_options[-1]));
elif qexpr=var then
   qvar:=var;
else 
   error "wrong arguments"
end if;
opt:=subs(var=qvar,_options);
a,n:=op(qgetargs(u,qvar));
b,m:=op(qgetargs(v,qvar));
x1,x2:=op(qgetargs([xarg],x));

term:=((-1)^k*qvar^binomial(k,2))^(1+s-r);
for i from 1 to r do
   term:=term*qpochhammer(u[i],qvar,k)
end do;
for j from 1 to s do
   term:=term/qpochhammer(v[j],qvar,k)
end do;
term:=term*xarg^k/qpochhammer(qvar,qvar,k);

# power x^k
newterm:=term/x^k;
ratio:=normal(qsimpcomb(subs(k=k+1,newterm)/newterm,QDE));
if not has(ratio,x) and not assigned(qRE) then
   RE:=numer(ratio)*A(k)-denom(ratio)*A(k+1)=0;
   userinfo(4,'qHolonomicRE',`q-holonomic recurrence equation for coefficients`,print(RE));
   userinfo(4,'qHolonomicRE',`base=qpower with expansionpt`,print(0));
   qRE:=REtoqRE(RE,A(k),F(x),base=qpower,expansionpt=0,opt);
end if;   

# q-pochhammer
xterm:=select(has,u,x);
if nops(xterm)=1 and not assigned(qRE) then
   xterm:=xterm[1];
   exppt:=normal(x/xterm);
   newterm:=term/qpochhammer(xterm,qvar,k)/exppt^k;
   ratio:=normal(qsimpcomb(subs(k=k+1,newterm)/newterm,QDE));
   if not has(ratio,x) and not has(exppt,x) and type(xterm,polynom(anything,x)) then
      RE:=numer(ratio)*A(k)-denom(ratio)*A(k+1)=0;
      userinfo(4,'qHolonomicRE',`q-holonomic recurrence equation for coefficients`,print(RE));
      userinfo(4,'qHolonomicRE',`base=qpochhammer with expansionpt`,print(exppt));
      qRE:=REtoqRE(RE,A(k),F(x),base=qpochhammer,expansionpt=exppt,opt);
   end if
end if;

# q-power
xterm:=select(has,u,x);
if nops(xterm)=1 and not assigned(qRE) then
   xterm:=xterm[1];
   exppt:=normal(x*xterm);
   newterm:=term/qpochhammer(xterm,qvar,k)/x^k;
   ratio:=normal(qsimpcomb(subs(k=k+1,newterm)/newterm,QDE));
   if not has(ratio,x) and not has(exppt,x) and type(1/xterm,polynom(anything,x)) then
      RE:=numer(ratio)*A(k)-denom(ratio)*A(k+1)=0;
      userinfo(4,'qHolonomicRE',`q-holonomic recurrence equation for coefficients`,print(RE));
      userinfo(4,'qHolonomicRE',`base=qpower with expansionpt`,print(exppt));
      qRE:=REtoqRE(RE,A(k),F(x),base=qpower,expansionpt=exppt,opt);
   end if
end if;

if assigned(qRE) then
   if type(var,'`^`') and qexpr=1/var then
      qRE:=qShiftRE(qRE,F(x),_options);
   end if;
   if explicit then
      n:=qOrder(qRE,F(x),_options);
      qRE:=subs(seq(qshift(F(x),[x$n-i],var)=F(var^(n-i)*x),i=0..n),qRE);
      return qRE;
   else
      return qRE;      
   end if;
else
   error "no q-holonomic recurrence equation could be found"
end if;
# end if;
end proc:


qphihypergeomDE := proc(u::list,v::list,xarg::algebraic,qexpr::algebraic,Fx::function,{var::algebraic:='q'})
local F,x,qRE;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
qRE:=qphihypergeomRE(args,_options);
qREtoqDE(qRE,F(x))
end proc:


qPolUpperBound := proc(RE::equation,Fx::function,{var::algebraic:='q'})
local F,x,a,m,n,p,k,i,z,s,t,alpha;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
n:=qOrder(RE,F(x));
a:=qgetcoeffs(RE,F(x),var);
m:=max(op(map(degree,a,x))); # maximum of the degrees of the coefficient polynomials
alpha:=map(coeff,a,x,m);
alpha:=map('`*`',alpha,lcm(op(map(denom,alpha)))); # make polynomial
p:=add(alpha[k+1]*x^k,k=0..n);
s:=ldegree(p,x);
z:=alpha[s+1];
t:=ldegree(z,var);

for i from t by -1 to 0 do 
   if expand(subs(x=var^i,p))=0 then
      return i
   end if; 
end do;
-1
end proc:


qUniversalDenominator := proc(RE::equation,Fx::function,{var::algebraic:='q'})
local F,x,n,coepol,g,p,r,i,j,k,DS,d,ud,ltzero,ltinf,ltz,lti,a,m,maxexp,am;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
n:=qOrder(RE,F(x));
coepol:=qgetcoeffs(RE,F(x),var);
g:=coepol[1];
for i from 2 to nops(coepol) do
  g:=gcdex(g,qshift(coepol[i],[x$(i-1)],1/var),x)
end do;
g:=qcontentPol(g,x,'eq');
p:=normal(qshift(coepol[-1],[x$n],1/var)/g);
r:=normal(coepol[1]/g);
DS:=sort([op(qDispersion(p,r,x,_options,'set'))],`>`);
for i in DS do
  d[i+1]:=gcdex(p,qshift(r,[x$i],var),x);
  p:=normal(p/d[i+1]);
  r:=normal(r/qshift(d[i+1],[x$i],1/var));
end do;

ud:=factor(qsimpcomb(g*mul(mul(qshift(d[k+1],[x$j],1/var),j=0..k),k in DS)));

# powers of x
maxexp:=0;
ltzero:=qLocalTypesCandidates(RE,F(x),var,ltype=0);
for ltz in ltzero do
   if ltz[2]=0 then 
      if patmatch(ltz[1],a::anything*var^m::negint,'am') then
         maxexp:=max(maxexp,subs(am,-m))
      end if;
   end if;
end do;

ud*x^maxexp
end proc:


qFPSHypergeomTypeSolveRE := proc(RE::equation,Ak::function,f::algebraic,Fx::function,{var::algebraic:='q',expansionpt::algebraic:=0,base::identical(qpower,qpochhammer):='qpower',initialcheck::boolean:=true})
local i,j,A,k,F,x,sol,m,n,p,index,inival,finished,posmin,allzero;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
A:=op(0,Ak);
k:=op(1,Ak);  
F:=op(0,Fx);
x:=op(1,Fx);

# order of recurrence equation is 0
if orderRE(RE,A(k))=0 then
   return [eval(f,x=0)]
end if;                            

# order of recurrence equation is greater than 0
sol:=qHypergeomTypeSolveRE(RE,A(k),_options[-1],qsimplified=false);                                      userinfo(5,'qFPS',`q-hypergeometric solution`,print(sol));  
n:=nops(sol);  
index:=map(op@op@indets,sol,specfunc(integer,A)); # extract index (s of s=n*t+u) of unknown initial value
index:=(index-[m $ m=0..n-1])/n; # extract index (t of s=n*t+u) of unknown initial value 
member(min(op(index)),index,'posmin'); # determine the position of the minimal index of the unknown initial values      
m:=i->(posmin+i-2 mod n)+1; # function to iterate correctly (ascending w.r.t. index) in determination of initial values 
sol:=applyrule(A(k::anything)=1,sol); # delete the unknown initial values

if initialcheck then # determine initial values
   j:=0;
   finished:=false;
   while not finished and j<3 do
      for i from 1 to n do
         if base=qpower then
            try
               inival[m(i)]:=qsimpcomb(eval(qdiff(f,[x$(n*index[m(i)]+m(i)-1)],var,explicit),x=expansionpt)/qfactorial(n*index[m(i)]+m(i)-1,var)); # try to determine initial value
               if j<>0 then
                  inival[m(i)]:=inival[m(i)]/eval(sol[m(i)],k=index[m(i)])
               end if;
            catch:    
            end try;
         elif base=qpochhammer then
            try
               inival[m(i)]:=qsimpcomb((-1)^(n*index[m(i)]+m(i)-1)*eval(qdiff(f,[x$(n*index[m(i)]+m(i)-1)],1/var,explicit),x=expansionpt)/qfactorial(n*index[m(i)]+m(i)-1,var)); # try to determine initial value
               if j<>0 then
                  inival[m(i)]:=inival[m(i)]/eval(sol[m(i)],k=index[m(i)])
               end if;
            catch:    
            end try;
         end if;
         index[m(i)]:=index[m(i)]+1;
   
         allzero:=false;
         if convert({seq(assigned(inival[p]),p=1..n)},`and`) then  # test, if all initial values are computed and not zero 
            if {seq(inival[p],p=1..n)}={0} then
               allzero:=true 
            else
               finished:=true;
               break
            end if;
         end if; 
      end do;                      
      j:=j+1
   end do;

   if not finished then
      if allzero then
         return [0 $ n] # if no other values than zeros are computed, then return zeros 
      else  
         error "initial values could not be computed" 
      end if;
   end if;
end if;

for i from 1 to n do
   if initialcheck then
      sol[i]:=sol[i]*inival[i]; # multiply with computed initial values  
   end if;
   if base=qpower then
      if expansionpt=0 then
         sol[i]:=sol[i]*x^(n*k+i-1); # multiply with correct power            
      else
         sol[i]:=sol[i]*qpower(x,expansionpt,var,(n*k+i-1)); # multiply with correct power            
      end if;
   elif base=qpochhammer then 
      if expansionpt=1 then
         sol[i]:=sol[i]*qpochhammer(x,var,(n*k+i-1));             
      else
         sol[i]:=sol[i]*qpower(expansionpt,x,var,(n*k+i-1)); # multiply with correct power            
      end if;
   end if;
   if initialcheck then
      sol[i]:=subs(k=k+index[i]-1,sol[i]);
   else
      sol[i]:=`tools/genglobal`('C')*sol[i];
   end if;
   sol[i]:=`simplify/qpochhammer`(sol[i]) assuming k::integer # shift the solution                        
end do;

sol
end proc:


qFPSHypergeomSolveRE := proc(RE::equation,Ak::function,f::algebraic,Fx::function,{var::algebraic:='q',expansionpt::algebraic:=0,base::identical(qpower,qpochhammer):='qpower',initialcheck::boolean:=true})
local A,k,F,x,sol,n,eqs,rec,m,p,i,j,ini,l,s,err,lh,rh,inisol,inicheck,ak,a,maxloop,lini,rini,ivc;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
A:=op(0,Ak);
k:=op(1,Ak);  
F:=op(0,Fx);
x:=op(1,Fx);

rec:=RE;
rec:=shiftRE(rec,A(k));
m:=orderRE(rec,A(k));

# tries to compute a q-hypergeometric solution of q-recurrence equation with q-Petkovsek algorithm 
sol:=qHypergeomSolveRE(rec,A(k),_options[-1],qsimplified=false,output='basis');         
# sol:=qHypergeomSolveRE(rec,A(k),_options[-1],output='basis');         
n:=nops(sol);

userinfo(5,'qFPS',`q-hypergeometric solution`,print(sol));   

if n>0 then
   sol:=applyrule(A(k::anything)=1,sol);
   eqs:={};
   ini:={solve(subs(var^k=x,qsimpcomb(coeff(lhs(rec),A(k+m)))),x)};
   ini:=select(patmatch,ini,var^p::nonnegint);
   ini:=map2(op,2,ini);
   if nops(ini)>0 then
      ini:=max(op(ini))+2
   else
      ini:=1
   end if;
   j:=1;   
   l:=ini;
   ivc:=1;
   maxloop:=max(m,n)+ini+2;
   while j<=n and l<maxloop do
      err:=false;
      try
         if base=qpower then
            lh:=qsimplify(normal(limit(qdiff(f,[x$(l-1)],var,explicit),x=expansionpt)/qfactorial(l-1,var)));
         elif base=qpochhammer then
            lh:=qsimplify(normal((-1)^(l-1)*limit(qdiff(f,[x$(l-1)],1/var,explicit),x=expansionpt)/qfactorial(l-1,var)));
         end if;
      catch:
         err:=true:
      end try:
      try
         rh:=qsimplify(normal(eval(add(a[i]*sol[i],i=1..n),k=l-1)));
      catch:
         err:=true:
      end try:
      if err=false then # initial value could be computed
         if j=n then 
            inisol:=solve({op(eqs),lh=rh},{seq(a[i],i=1..n)}); # tries to determine all initial values
            if not(subs(inisol,{seq(a[i],i=1..n)}={0})) then # checking if at least one initial value is not zero
               inicheck:=true;
               while j<=max(m,n) and initialcheck do
                  lini:=normal(eval(add(subs(inisol,a[i])*sol[i],i=1..n),k=l));
                  lini:=subs(seq(a[i]=0,i=1..n),lini);
                  if base=qpower then
                     rini:=normal(eval(qdiff(f,[x$l],var,explicit),x=expansionpt)/qfactorial(l,var));
                     if not simplify(qsimpcomb(lini-rini,QDE),power,symbolic)=0 then # checking more initial values
                        inicheck:=false
                     end if;
                  elif base=qpochhammer then
                     rini:=normal((-1)^l*eval(qdiff(f,[x$l],1/var,explicit),x=expansionpt)/qfactorial(l,var));
                     if not simplify(qsimpcomb(lini-rini,QDE),power,symbolic)=0 then # checking more initial values
                        inicheck:=false
                     end if;
                  end if;
                  userinfo(6,'qFPS',`initial value`,ivc,print([simplify(qsimpcomb(lini,QDE),power,symbolic),simplify(qsimpcomb(rini,QDE),power,symbolic)]));   
                  ivc:=ivc+1;
                  j:=j+1;
                  l:=l+1;
               end do;
               if inicheck=true or not initialcheck then 
                  ak:=add(subs(inisol,a[i])*sol[i],i=1..n);
               else
                  error "initial values could not be computed"
               end if;
               ak:=subs(seq(a[i]=0,i=1..n),ak);
               ak:=qsimpcomb(subs(k=k+ini-1,ak),QDE);
               # ak:=`convert/qfactorial`(ak);
               # ak:=`simplify/qpochhammer`(ak) assuming k::integer;
               # ak:=subs(exp(1/2*k*Pi*I)=I^k,ak);
               # ak:=qsimplify(ak);
               if base=qpower then
                  if expansionpt=0 then
                     return [ak*x^(k+ini-1)]            
                  else
                     return [ak*qpower(x,expansionpt,var,(k+ini-1))]            
                  end if;
               elif base=qpochhammer then
                  if expansionpt=1 then
                     return [ak*qpochhammer(x,var,(k+ini-1))]            
                  else
                     return [ak*qpower(expansionpt,x,var,(k+ini-1))]            
                  end if;
               end if;
            else
               if l=maxloop-1 then
                  return [0]
               else
                  j:=j-1; # try again to compute the last initial value, if all values are zero
               end if;
            end if;
         else
            userinfo(6,'qFPS',`initial value`,ivc,print([lh,rh]));   
            ivc:=ivc+1;
            eqs:={op(eqs),lh=rh}; # add equation in set eqs
         end if;
         j:=j+1;
      end if;
      l:=l+1;
   end do;
end if;
error "there exists no q-hypergeometric solution of recurrence equation"
end proc:


# DEFINITION OF Q-FUNCTIONS 


# definition of q-brackets
qbrackets := (k,q) -> (q^k-1)/(q-1):

# definition of q-factorial
qfactorial := proc(n::algebraic,q::algebraic)
local j;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if type(n,'numeric') then
   return product(qbrackets(j,q),j=1..n)
end if;
'procname'(args)   
end proc:

# definition of q-binomial
qbinomial := proc(n::algebraic,k::algebraic,q::algebraic)
local j;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if type(n,'numeric') and type(k,'numeric') then 
   return qfactorial(n,q)/qfactorial(k,q)/qfactorial(n-k,q)
elif type(k,'numeric') then   
   return mul(1-q^(n-j+1),j=1..k)/qpochhammer(q,q,k)
end if;
'procname'(args)   
end proc:

# definition of q-powers (note: qpower1(n,m,q,k)=qpower2(m,n,q,k))
qpower1 := proc(n::algebraic,m::algebraic,q::algebraic,k::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if type(k,'numeric') and n<>0 then
   return n^k*qpochhammer(m/n,q,k)
elif m=0 and n=1 then 
   return 1
elif k<>infinity then  
   if n=0 then
      return (-1)^k*q^binomial(k,2)*m^k 
   elif n=1 then
      return qpochhammer(m,q,k)
   elif m=0 then
      return n^k
   end if;
end if;
'procname'(args)   
end proc:

qpower2 := proc(n::algebraic,m::algebraic,q::algebraic,k::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if type(k,'numeric') and m<>0 then
   return m^k*qpochhammer(n/m,q,k)
elif m=1 and n=0 then 
   return 1
elif k<>infinity then 
   if n=0 then
      return m^k 
   end if;
end if;
'procname'(args)   
end proc:

qpower := proc(n::algebraic,m::algebraic,q::algebraic,k::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if type(k,'numeric') and n<>0 then
   return n^k*qpochhammer(m/n,q,k)
elif m=0 and n=1 then 
   return 1
elif k<>infinity then    
   if n=0 then
      return (-1)^k*q^binomial(k,2)*m^k 
   elif n=1 then
      return qpochhammer(m,q,k)
   elif m=0 then
      return n^k
   end if;
end if;
'procname'(args)
end proc:

`qdiff/qpower1` := proc(x::algebraic,a::algebraic,q::algebraic,k::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q and type(a,'freeof(x)') and k<>infinity then
   return qbrackets(k,q)/(x-q^(k-1)*a)*qpower1(x,a,q,k)
elif y=x and p=1/q and type(a,'freeof(x)') and k<>infinity then
   return qbrackets(k,q)/(x-a)/q^(k-1)*qpower1(x,a,q,k)
end if;
end proc:

`qdiff/qpower2` := proc(x::algebraic,a::algebraic,q::algebraic,k::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q and type(a,'freeof(x)') and x<>a then
   if k=infinity then
      return (x-a+1)/(x-a)/(1-q)/x*qpower2(x,a,q,k)
   else
      return -qbrackets(k,q)/(a-x)*qpower2(x,a,q,k)
   end if;
elif y=x and p=1/q and type(a,'freeof(x)') and x<>a then
   if k=infinity then
      return (x+q*(1-a))/(q-1)/x*qpower2(x,a,q,k)
   else
      return -qbrackets(k,q)/(a-q^(k-1)*x)*qpower2(x,a,q,k) 
   end if;
end if;
end proc:

`qdiff/qpower` := proc(x::algebraic,a::algebraic,q::algebraic,k::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q and type(a,'freeof(x)') and k<>infinity then
   return qbrackets(k,q)/(x-q^(k-1)*a)*qpower(x,a,q,k)   
elif y=x and p=1/q and type(a,'freeof(x)') and k<>infinity then
   return qbrackets(k,q)/(x-a)/q^(k-1)*qpower(x,a,q,k)   
elif y=a and p=q and type(x,'freeof(a)') and x<>a then
   if k=infinity then
      return (a-x+1)/(a-x)/(1-q)/a*qpower(x,a,q,k)   
   else
      return -qbrackets(k,q)/(x-a)*qpower(x,a,q,k)      
   end if;
elif y=a and p=1/q and type(x,'freeof(a)') and x<>a then
   if k=infinity then
      return (a+q*(1-x))/(q-1)/a*qpower(x,a,q,k)
   else
      return -qbrackets(k,q)/(x-q^(k-1)*a)*qpower(x,a,q,k)   
   end if;
end if;
end proc:

`qshift/qpower1` := proc(x::algebraic,a::algebraic,q::algebraic,k::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q and type(a,'freeof(x)') and k<>infinity then
   return q^(k-1)*(q*x-a)/(x-q^(k-1)*a)*qpower1(x,a,q,k)
elif y=x and p=1/q and type(a,'freeof(x)') and k<>infinity then
   return (x-a*q^k)/q^k/(x-a)*qpower1(x,a,q,k)
end if;
end proc:

`qshift/qpower2` := proc(x::algebraic,a::algebraic,q::algebraic,k::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q and type(a,'freeof(x)') and x<>a then
   if k=infinity then
      return 1/(a-x)*qpower2(x,a,q,k) 
   else   
      return (a-q^k*x)/(a-x)*qpower2(x,a,q,k)
   end if;
elif y=x and p=1/q and type(a,'freeof(x)') and x<>a then
   if k=infinity then
      return (q*a-x)/q*qpower2(x,a,q,k)
   else   
      return (x-a*q)/q/(q^(k-1)*x-a)*qpower2(x,a,q,k)
   end if;
end if;
end proc:

`qshift/qpower` := proc(x::algebraic,a::algebraic,q::algebraic,k::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q and type(a,'freeof(x)') and k<>infinity then
   return q^(k-1)*(q*x-a)/(x-q^(k-1)*a)*qpower(x,a,q,k)
elif y=x and p=1/q and type(a,'freeof(x)') and k<>infinity then
   return (x-a*q^k)/q^k/(x-a)*qpower(x,a,q,k)
elif y=a and p=q and type(x,'freeof(a)') and x<>a then
   if k=infinity then
      return 1/(x-a)*qpower(x,a,q,k)      
   else
      return (x-q^k*a)/(x-a)*qpower(x,a,q,k)
   end if;
elif y=a and p=1/q and type(x,'freeof(a)') and x<>a then
   if k=infinity then
      return (x*q-a)/q*qpower(x,a,q,k)
   else
      return (a-x*q)/q/(q^(k-1)*a-x)*qpower(x,a,q,k)
   end if;
end if;
end proc:

# definition of q-pochhammer symbol
# qpochhammer := (n,q,k) -> QDifferenceEquations['QPochhammer'](n,q,k):  
qpochhammer := proc(n::algebraic,q::algebraic,k::algebraic)
local i;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if type(k,'numeric') then
   if k=0 then
      return 1
   elif type(k,'posint') then
      return mul(1-n*q^i,i=0..k-1)   
   elif type(k,'negint') then
      return 1/mul(1-n*q^(-i),i=1..-k)
   end if;
else     
   if n=0 then
      return 1 
   elif n=1 then
      return 0
   end if;
end if;
'procname'(args)        
end proc:  

`qdiff/qpochhammer` := proc(x::algebraic,q::algebraic,k::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   if k=infinity then 
      return 1/(q-1)/(1-x)*qpochhammer(x,q,infinity)
   else 
      return -qbrackets(k,q)/(1-x)*qpochhammer(x,q,k)
   end if;
end if;
if y=x and p=1/q then
   if k=infinity then 
      return -p/(p-1)*qpochhammer(x,q,infinity)
   else 
      return qbrackets(k,p)/(x-p^(k-1))*qpochhammer(x,q,k)
   end if;
end if;
end proc:

`qshift/qpochhammer` := proc(x::algebraic,q::algebraic,k::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   if k=infinity then 
      return 1/(1-x)*qpochhammer(x,q,infinity)
   else 
      return (1-x*q^k)/(1-x)*qpochhammer(x,q,k)
   end if;
end if;
if y=x and p=1/q then
   if k=infinity then 
      return (1-x*p)*qpochhammer(x,q,infinity)
   else 
      return (1-x*p)/(1-x*p^(1-k))*qpochhammer(x,q,k)
   end if;
end if;
end proc:

# definition of generalized q-hypergeometric function
qphihypergeom := proc(a::list,b::list,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=0 then
   return 1
elif member(1,a) and not member(1,b) then
   return 1
end if;
'procname'(args)        
end proc:  

`qdiff/qphihypergeom` := proc(a::list,b::list,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
local c,m,j,f;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then        
   f:=qphihypergeom(a,b,x,q);
   # iterate through list of upper parameters
   if nops(a)>0 then
      m:=nops(a);
      j:=1;
      while j<=m do
         c:=a[j];
         if c<>0 then
            return (c-1)/c/x/(q-1)*subsop([1,j]=simplify(q*c,power),f)-(c-1)/c/x/(q-1)*f
         end if;
         j:=j+1
      end do;
   end if;
   # iterate through list of lower parameters
   if nops(b)>0 then
      m:=nops(b);
      j:=1;
      while j<=m do
         c:=simplify(b[j]/q,power);
         if c<>0 then
            return (c-1)/c/x/(q-1)*subsop([2,j]=c,f)-(c-1)/c/x/(q-1)*f
         end if;
         j:=j+1
      end do;
   end if;
end if;
end proc:

`qshift/qphihypergeom` := proc(a::list,b::list,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
local c,m,j,f;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then        
   f:=qphihypergeom(a,b,x,q);
   # iterate through list of upper parameters
   if nops(a)>0 then
      m:=nops(a);
      j:=1;
      while j<=m do
         c:=a[j];
         if c<>0 then
            return (c-1)/c*subsop([1,j]=simplify(q*c,power),f)+1/c*f
         end if;
         j:=j+1
      end do;
   end if;
   # iterate through list of lower parameters
   if nops(b)>0 then
      m:=nops(b);
      j:=1;
      while j<=m do
         c:=simplify(b[j]/q,power);
         if c<>0 then
            return (c-1)/c*subsop([2,j]=c,f)+1/c*f
         end if;
         j:=j+1
      end do;
   end if;
end if;
end proc:

# definition of small q-exponential function
# qexp:=(x,q)->sum(1/qpochhammer(q,q,k)*x^k,k=0..infinity):
qexp := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 1
end if;
'procname'(args)        
end proc:

`qdiff/qexp` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return -1/(q-1)*qexp(x,q)    
elif y=x and p=1/q then 
   return p/(p-1)/(1-x*p)*qexp(x,q)
end if;        
end proc:

`qshift/qexp` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (1-x)*qexp(x,q)    
elif y=x and p=1/q then 
   return 1/(1-x*p)*qexp(x,q)
end if;        
end proc:

# definition of big q-exponential function
# qExp:=(x,q)->sum(q^binomial(k,2)/qpochhammer(q,q,k)*x^k,k=0..infinity):
qExp := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 1
#elif numer(q)=1 then
#     return (1+x)*qexp(-x,1/q) 
end if;
'procname'(args)        
end proc:

`qdiff/qExp` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return -1/(q-1)/(1+x)*qExp(x,q)    
elif y=x and p=1/q then 
   return p/(p-1)*qExp(x,q)
end if;        
end proc:

`qshift/qExp` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return 1/(x+1)*qExp(x,q)    
elif y=x and p=1/q then 
   return (1+x*p)*qExp(x,q)
end if;        
end proc:

# definition of small q-exponential function (Kac/Cheung)
# expq:=(x,q)->sum(1/qfactorial(k,q)*x^k,k=0..infinity):
expq := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 1
end if;
'procname'(args)        
end proc:

`qdiff/expq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return expq(x,q)    
elif y=x and p=1/q then 
   return 1/((1-p)*x+1)*expq(x,q)
end if;        
end proc:

`qshift/expq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return ((q-1)*x+1)*expq(x,q)    
elif y=x and p=1/q then 
   return 1/((1-p)*x+1)*expq(x,q)
end if;        
end proc:   

# definition of big q-exponential function (Kac/Cheung)
# Expq:=(x,q)->sum(q^(k*(k-1)/2)/qfactorial(k,q)*x^k,k=0..infinity):
Expq := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 1
end if;
'procname'(args)        
end proc:

`qdiff/Expq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return 1/((1-q)*x+1)*Expq(x,q)    
elif y=x and p=1/q then 
   return Expq(x,q)
end if;        
end proc:

`qshift/Expq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return 1/((1-q)*x+1)*Expq(x,q)       
elif y=x and p=1/q then 
   return ((p-1)*x+1)*Expq(x,q)
end if;        
end proc:   

# definition of q-logarithmic function
# logq:=(x,q)->sum((-1)^k/(q^k-1)*(x-1)^k,k=0..infinity):
logq := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=1 then
   return 0
end if;
'procname'(args)        
end proc:

`qdiff/logq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x+1 and p=q then
   return 1/(q-1)/(x+1)
elif y=x+1 and p=1/q then 
   return NULL
end if;        
end proc:

`qshift/logq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x+1 and p=q then
   return logq(x+1,q)+x/(x+1)
elif y=x+1 and p=1/q then 
   return NULL
end if;        
end proc:

# definition of small q-sine function
# qsin:=(x,q)->(qexp(I*x,q)-qexp(-I*x,q))/(2*I):
qsin := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 0
end if;
'procname'(args)        
end proc:

`qdiff/qsin` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return -1/(q-1)*qcos(x,q)
elif y=x and p=1/q then 
   return p/((p-1)*(1+x^2*p^2))*(qcos(x,q)-p*x*qsin(x,q))
end if;        
end proc:

`qshift/qsin` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return qsin(x,q)-x*qcos(x,q)
elif y=x and p=1/q then 
   return 1/(1+x^2*p^2)*(qsin(x,q)+p*x*qcos(x,q))
end if;        
end proc:

# definition of big q-sine function
# qSin:=(x,q)->(qExp(I*x,q)-qExp(-I*x,q))/(2*I):
qSin := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 0
end if;
'procname'(args)        
end proc:

`qdiff/qSin` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return -1/(q-1)/(x^2+1)*(qCos(x,q)+x*qSin(x,q))
elif y=x and p=1/q then 
   return p/(p-1)*qCos(x,q)
end if;        
end proc:

`qshift/qSin` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return 1/(x^2+1)*(qSin(x,q)-x*qCos(x,q))
elif y=x and p=1/q then 
   return qSin(x,q)+p*x*qCos(x,q)
end if;        
end proc:

# definition of small q-sine function (Kac/Cheung)
# sinq:=(x,q)->(expq(I*x,q)-expq(-I*x,q))/(2*I):
sinq := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 0
end if;
'procname'(args)        
end proc:

`qdiff/sinq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return cosq(x,q)
elif y=x and p=1/q then 
   return 1/((p-1)^2*x^2+1)*cosq(x,q)-(p-1)*x/((p-1)^2*x^2+1)*sinq(x,q)
end if;        
end proc:

`qshift/sinq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (q-1)*x*cosq(x,q)+sinq(x,q)
elif y=x and p=1/q then 
   return (p-1)*x/((p-1)^2*x^2+1)*cosq(x,q)+1/((p-1)^2*x^2+1)*sinq(x,q)
end if;        
end proc:

# definition of big q-sine function (Kac/Cheung)
# Sinq:=(x,q)->(Expq(I*x,q)-Expq(-I*x,q))/(2*I):
Sinq := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 0
end if;
'procname'(args)        
end proc:

`qdiff/Sinq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return 1/((q-1)^2*x^2+1)*Cosq(x,q)-(q-1)*x/((q-1)^2*x^2+1)*Sinq(x,q)
elif y=x and p=1/q then 
   return Cosq(x,q)
end if;        
end proc:

`qshift/Sinq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (q-1)*x/((q-1)^2*x^2+1)*Cosq(x,q)+1/((q-1)^2*x^2+1)*Sinq(x,q)
elif y=x and p=1/q then 
   return (p-1)*x*Cosq(x,q)+Sinq(x,q)
end if;        
end proc:

# definition of small q-cosine function
# qcos:=(x,q)->(qexp(I*x,q)+qexp(-I*x,q))/2:
qcos := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 1
end if;
'procname'(args)        
end proc:

`qdiff/qcos` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return 1/(q-1)*qsin(x,q)
elif y=x and p=1/q then 
   return -p/((p-1)*(1+x^2*p^2))*(qsin(x,q)+p*x*qcos(x,q))
end if;        
end proc:

`qshift/qcos` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return qcos(x,q)+x*qsin(x,q)
elif y=x and p=1/q then 
   return 1/(1+x^2*p^2)*(qcos(x,q)-p*x*qsin(x,q))
end if;        
end proc:

# definition of big q-cosine function
# qCos:=(x,q)->(qExp(I*x,q)+qExp(-I*x,q))/2:
qCos := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 1 
end if;
'procname'(args)        
end proc:

`qdiff/qCos` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return 1/(q-1)/(x^2+1)*(qSin(x,q)-x*qCos(x,q)) 
elif y=x and p=1/q then 
   return -p/(p-1)*(qSin(x,q))
end if;        
end proc:

`qshift/qCos` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return 1/(x^2+1)*(qCos(x,q)+x*qSin(x,q))
elif y=x and p=1/q then 
   return qCos(x,q)-p*x*qSin(x,q)
end if;        
end proc:

# definition of small q-cosine function (Kac/Cheung)
# cosq:=(x,q)->(expq(I*x,q)+expq(-I*x,q))/2:
cosq := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 1
end if;
'procname'(args)        
end proc:

`qdiff/cosq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return -sinq(x,q)
elif y=x and p=1/q then 
   return (1-p)*x/((p-1)^2*x^2+1)*cosq(x,q)-1/((p-1)^2*x^2+1)*sinq(x,q)
end if;        
end proc:

`qshift/cosq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (1-q)*x*sinq(x,q)+cosq(x,q)
elif y=x and p=1/q then 
   return 1/((p-1)^2*x^2+1)*cosq(x,q)-(p-1)*x/((p-1)^2*x^2+1)*sinq(x,q)
end if;        
end proc:

# definition of big q-cosine function (Kac/Cheung)
# Cosq:=(x,q)->(Expq(I*x,q)+Expq(-I*x,q))/2:
Cosq := proc(x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if x=0 then
   return 1 
end if;
'procname'(args)        
end proc:

`qdiff/Cosq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (1-q)*x/((q-1)^2*x^2+1)*Cosq(x,q)-1/((q-1)^2*x^2+1)*Sinq(x,q)
elif y=x and p=1/q then 
   return -Sinq(x,q)
end if;        
end proc:

`qshift/Cosq` := proc(x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return 1/((q-1)^2*x^2+1)*Cosq(x,q)-(q-1)*x/((q-1)^2*x^2+1)*Sinq(x,q)
elif y=x and p=1/q then 
   return Cosq(x,q)-(p-1)*x*Sinq(x,q)
end if;        
end proc:

# definition of q-Bernstein polynomials (Phillips)       
qBernstein := proc(n::algebraic,i::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if type(n,numeric) and type(i,numeric) then
   return qbinomial(n,i,q)*x^i*qpochhammer(x,q,n-i)
end if;
'procname'(args)
end proc:

`qdiff/qBernstein` := proc(n::algebraic,i::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (x+q^i-1-q^n*x)/(1-q)/(x-1)/x*qBernstein(n,i,x,q)
elif y=x and p=1/q then
   return q*(-q^n*x+q^i*q-q+x)/(q-1)/(-q^n*x+q^i*q)/x*qBernstein(n,i,x,q)
end if;        
end proc:

`qshift/qBernstein` := proc(n::algebraic,i::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (q^n*x-q^i)/(x-1)*qBernstein(n,i,x,q)
elif y=x and p=1/q then
   return -(q-x)/(q^n*x-q^i*q)*qBernstein(n,i,x,q)
end if;        
end proc:
            
# definition of q-Laguerre polynomial
qLaguerre := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=0 then
   return qpochhammer(q^(a+1),q,n)/qpochhammer(q,q,n) 
elif x=-1 then
   return 1/qpochhammer(q,q,n) 
end if;
'procname'(args)
# qpochhammer(q^(a+1),q,n)/qpochhammer(q,q,n)*qphihypergeom([q^(-n)],[q^(a+1)],-q^(n+a+1)*x,q)
# 1/qpochhammer(q,q,n)*qphihypergeom([q^(-n),-x],[0],q^(n+a+1),q)
end proc:

`qdiff/qLaguerre` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*(x*q^n*q^a+1)*qLaguerre(n,a,x,q)/(q^n*q^a*(x+1)*(-1+q)*x)-(q^n*q^a-1)*qLaguerre(n-1,a,x,q)/(q^n*q^a*(x+1)*(-1+q)*x)
elif y=x and p=1/q then
   return (-1+q^n)*q*qLaguerre(n,a,x,q)/(q^n*x*(-1+q))-(q^n*q^a-1)*qLaguerre(n-1,a,x,q)*q/(q^n*x*(-1+q))
end if;        
end proc:

`qshift/qLaguerre` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return -(q^a*q^n-1)*qLaguerre(n-1,a,x,q)/(q^n*q^a*(x+1))+(-1+q^n+q^a*q^n+q^a*x*(q^n)^2)*qLaguerre(n,a,x,q)/(q^n*q^a*(x+1))
elif y=x and p=1/q then
   return (q^a*q^n-1)*qLaguerre(n-1,a,x,q)/q^n+qLaguerre(n,a,x,q)/q^n
end if;        
end proc:

# definition of little q-Laguerre polynomial
LittleqLaguerre := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=0 then
   return 1
elif x=1 then
   return (-a)^n*q^(n*(n+1)/2)/qpochhammer(a,q,n+1) 
end if;
'procname'(args)
# qphihypergeom([q^(-n),0],[a*q],q*x,q)
end proc:

`qdiff/LittleqLaguerre` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*LittleqLaguerre(n,a,x,q)/((q-1)*x)-(-1+q^n)*LittleqLaguerre(n-1,a,x,q)/((q-1)*x)
elif y=x and p=1/q then
   return (-1+q^n)*(-a*q^n+x)*q*LittleqLaguerre(n,a,x,q)/((x-1)*q^n*(q-1)*x)+a*(-1+q^n)*LittleqLaguerre(n-1,a,x,q)*q/((x-1)*(q-1)*x)
end if;        
end proc:

`qshift/LittleqLaguerre` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return LittleqLaguerre(n,a,x,q)*q^n+(1-q^n)*LittleqLaguerre(n-1,a,x,q)
elif y=x and p=1/q then
   return ((q^n)^2*a-q^n-a*q^n+x)*LittleqLaguerre(n,a,x,q)/((x-1)*q^n)-a*(-1+q^n)*LittleqLaguerre(n-1,a,x,q)/(x-1)
end if;        
end proc:

# definition of big q-Laguerre polynomial
BigqLaguerre := proc(n::algebraic,a::algebraic,b::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1 then
   return 1
elif x=a*q then
   return 1/qpochhammer(q^(-n)/b,q,n)
end if;
'procname'(args)
#1/qpochhammer(1/b/q^n,q,n)*qphihypergeom([q^(-n),a*q/x],[a*q],x/b,q)
#qphihypergeom([q^(-n),0,x],[a*q,b*q],q,q)
end proc:

`qdiff/BigqLaguerre` := proc(n::algebraic,a::algebraic,b::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*BigqLaguerre(n,a,b,x,q)/((x-1)*(q-1))-(-1+q^n)*BigqLaguerre(n-1,a,b,x,q)/((x-1)*(q-1))
elif y=x and p=1/q then
   return (-1+q^n)*(-q*q^n*a*b+x)*q*BigqLaguerre(n,a,b,x,q)/(q^n*(x-a*q)*(-b*q+x)*(q-1))+(-1+q^n)*q^2*a*b*BigqLaguerre(n-1,a,b,x,q)/((x-a*q)*(-b*q+x)*(q-1))
end if;        
end proc:

`qshift/BigqLaguerre` := proc(n::algebraic,a::algebraic,b::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+x*q^n)*BigqLaguerre(n,a,b,x,q)/(x-1)-x*(-1+q^n)*BigqLaguerre(n-1,a,b,x,q)/(x-1)
elif y=x and p=1/q then 
   return (q^2*q^n*a*b+x*q*(q^n)^2*a*b+x^2-x*q*q^n*b-x*q*q^n*a*b-x*q*q^n*a)*BigqLaguerre(n,a,b,x,q)/(q^n*(x-a*q)*(-b*q+x))-(-1+q^n)*x*q*a*b*BigqLaguerre(n-1,a,b,x,q)/((x-a*q)*(-b*q+x))
end if;        
end proc:

# definition of little q-Jacobi polynomial
LittleqJacobi := proc(n::algebraic,a::algebraic,b::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=0 then
   return 1 
end if;
'procname'(args)
#qphihypergeom([q^(-n),a*b*q^(n+1)],[a*q],q*x,q)
end proc:

`qdiff/LittleqJacobi` := proc(n::algebraic,a::algebraic,b::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*(-1+q^n*b)*LittleqJacobi(n-1,a,b,x,q)/((b*x*q-1)*(-1+(q^n)^2*a*b)*(q-1)*x)+(-1+q^n)*(x*q*(q^n)^2*a*b^2-q^n*b+1-b*x*q)*LittleqJacobi(n,a,b,x,q)/((b*x*q-1)*(-1+(q^n)^2*a*b)*(q-1)*x)
elif y=x and p=1/q then 
   return a*(-1+q^n)*(-1+q^n*b)*q*LittleqJacobi(n-1,a,b,x,q)/((x-1)*(-1+(q^n)^2*a*b)*(q-1)*x)+(-1+q^n)*((q^n)^2*a*b*x-(q^n)^2*a*b+q^n*a-x)*q*LittleqJacobi(n,a,b,x,q)/((x-1)*(-1+(q^n)^2*a*b)*q^n*(q-1)*x)
end if;        
end proc:

`qshift/LittleqJacobi` := proc(n::algebraic,a::algebraic,b::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*(-1+q^n*b)*LittleqJacobi(n-1,a,b,x,q)/((b*x*q-1)*(-1+(q^n)^2*a*b))+q^n*(x*q*(q^n)^2*a*b^2-b*x*q-b*a*q^n+b-q^n*b+1)*LittleqJacobi(n,a,b,x,q)/((b*x*q-1)*(-1+(q^n)^2*a*b))
elif y=x and p=1/q then 
   return -a*(-1+q^n)*(-1+q^n*b)*LittleqJacobi(n-1,a,b,x,q)/((x-1)*(-1+(q^n)^2*a*b))+((q^n)^2*a*b*x-(q^n)^2*a*b+q^n*a-(q^n)^2*a+q^n-x)*LittleqJacobi(n,a,b,x,q)/((x-1)*(-1+(q^n)^2*a*b)*q^n)
end if;        
end proc:

# definition of little q-Legendre polynomial
LittleqLegendre := proc(n::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=0 then
   return 1 
end if;
'procname'(args)
end proc:

`qdiff/LittleqLegendre` := proc(n::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*LittleqLegendre(n-1,x,q)/((x*q-1)*(q^n+1)*(q-1)*x)+(-1+q^n)*(x*q*q^n+x*q-1)*LittleqLegendre(n,x,q)/((x*q-1)*(q^n+1)*(q-1)*x)
elif y=x and p=1/q then 
   return (-1+q^n)*q*LittleqLegendre(n-1,x,q)/((x-1)*(q^n+1)*(q-1)*x)+(-1+q^n)*(x*q^n-q^n+x)*q*LittleqLegendre(n,x,q)/((x-1)*q^n*(q^n+1)*(q-1)*x)
end if;        
end proc:

`qshift/LittleqLegendre` := proc(n::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*LittleqLegendre(n-1,x,q)/((x*q-1)*(q^n+1))+q^n*(x*q*q^n+x*q-2)*LittleqLegendre(n,x,q)/((x*q-1)*(q^n+1))
elif y=x and p=1/q then 
   return -(-1+q^n)*LittleqLegendre(n-1,x,q)/((x-1)*(q^n+1))+(-2*q^n+x+x*q^n)*LittleqLegendre(n,x,q)/((x-1)*q^n*(q^n+1))
end if;        
end proc:

# definition of big q-Jacobi polynomial
BigqJacobi := proc(n::algebraic,a::algebraic,b::algebraic,c::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1 then
   return 1
end if;
'procname'(args)
end proc:

`qdiff/BigqJacobi` := proc(n::algebraic,a::algebraic,b::algebraic,c::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*((q^n)^2*a*x*b^2-q^n*a*b-q^n*b*c-b*x+c+b)*BigqJacobi(n,a,b,c,x,q)/((q-1)*(b*x-c)*(x-1)*(-1+(q^n)^2*a*b))-(-1+q^n)*(-1+q^n*b)*(q^n*a*b-c)*BigqJacobi(n-1,a,b,c,x,q)/((b*x-c)*(x-1)*(-1+(q^n)^2*a*b)*(q-1))
elif y=x and p=1/q then 
   return (-1+q^n)*(x*(q^n)^2*a*b-(q^n)^2*c*a*b*q-(q^n)^2*a^2*q*b+q*q^n*a*b+q*q^n*a*c-x)*q*BigqJacobi(n,a,b,c,x,q)/((q-1)*q^n*(x-q*a)*(x-c*q)*(-1+(q^n)^2*a*b))-(-1+q^n)*a*q^2*(-1+q^n*b)*(q^n*a*b-c)*BigqJacobi(n-1,a,b,c,x,q)/((x-q*a)*(x-c*q)*(-1+(q^n)^2*a*b)*(q-1))
end if;        
end proc:

`qshift/BigqJacobi` := proc(n::algebraic,a::algebraic,b::algebraic,c::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
    return(x^2*(q^n)^3*a*b^2-(q^n)^2*a*x*b^2+(q^n)^2*a*c*b-(q^n)^2*b*a*x-x*(q^n)^2*c*a*b+x*q^n*a*b-x*(q^n)^2*b*c-x^2*q^n*b+x*q^n*b*c+x*q^n*b+x*c*q^n-c)*BigqJacobi(n,a,b,c,x,q)/((b*x-c)*(x-1)*(-1+(q^n)^2*a*b))-(-1+q^n)*x*(-1+q^n*b)*(q^n*b*a-c)*BigqJacobi(n-1,a,b,c,x,q)/((b*x-c)*(x-1)*(-1+(q^n)^2*a*b))
elif y=x and p=1/q then 
   return (q^2*(q^n)^3*a^2*c*b-q^2*q^n*a*c-q*x*a^2*(q^n)^2*b-x*q*(q^n)^2*a*b-q*x*c*(q^n)^2*a*b+q*x*q^n*a*b-q*x*(q^n)^2*a*c+q*x*q^n*a*c+a*q^n*x*q+q*x*c*q^n+x^2*(q^n)^2*a*b-x^2)*BigqJacobi(n,a,b,c,x,q)/(q^n*(x-q*a)*(x-c*q)*(-1+(q^n)^2*a*b))+x*(-1+q^n)*a*q*(-1+q^n*b)*(q^n*a*b-c)*BigqJacobi(n-1,a,b,c,x,q)/((x-q*a)*(x-c*q)*(-1+(q^n)^2*a*b))
end if;        
end proc:

# definition of big q-Legendre polynomial
BigqLegendre := proc(n::algebraic,c::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1 then
   return 1
end if;
'procname'(args)
end proc:

`qdiff/BigqLegendre` := proc(n::algebraic,c::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*((q^n)^2*x-q^n-q^n*c-x+c+1)*BigqLegendre(n,c,x,q)/((q-1)*(x-c)*(x-1)*(-1+(q^n)^2))-(-1+q^n)*(-1+q^n)*(q^n-c)*BigqLegendre(n-1,c,x,q)/((b*x-c)*(x-1)*(-1+(q^n)^2)*(q-1))
elif y=x and p=1/q then 
   return (-1+q^n)*(x*(q^n)^2-(q^n)^2*c*q-(q^n)^2*q+q*q^n+q*q^n*c-x)*q*BigqLegendre(n,c,x,q)/((q-1)*q^n*(x-q)*(x-c*q)*(-1+(q^n)^2))-(-1+q^n)*q^2*(-1+q^n)*(q^n-c)*BigqLegendre(n-1,c,x,q)/((x-q)*(x-c*q)*(-1+(q^n)^2)*(q-1))
end if;        
end proc:

`qshift/BigqLegendre` := proc(n::algebraic,c::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
    return(x^2*(q^n)^3-(q^n)^2*x+(q^n)^2*c-(q^n)^2*x-x*(q^n)^2*c+x*q^n-x*(q^n)^2*c-x^2*q^n+x*q^n*c+x*q^n+x*c*q^n-c)*BigqLegendre(n,c,x,q)/((x-c)*(x-1)*(-1+(q^n)^2))-(-1+q^n)*x*(-1+q^n)*(q^n-c)*BigqLegendre(n-1,c,x,q)/((x-c)*(x-1)*(-1+(q^n)^2))
elif y=x and p=1/q then 
   return (q^2*(q^n)^3*c-q^2*q^n*c-q*x*(q^n)^2-x*q*(q^n)^2-q*x*c*(q^n)^2+q*x*q^n-q*x*(q^n)^2*c+q*x*q^n*c+q^n*x*q+q*x*c*q^n+x^2*(q^n)^2-x^2)*BigqLegendre(n,c,x,q)/(q^n*(x-q)*(x-c*q)*(-1+(q^n)^2))+x*(-1+q^n)*q*(-1+q^n)*(q^n-c)*BigqLegendre(n-1,c,x,q)/((x-q)*(x-c*q)*(-1+(q^n)^2))
end if;        
end proc:

# definition of q-Meixner polynomial
qMeixner := proc(n::algebraic,a::algebraic,b::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1 then
   return 1
end if;
'procname'(args)
end proc:

`qdiff/qMeixner` := proc(n::algebraic,a::algebraic,b::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*(x*q^n+b)*qMeixner(n,a,b,x,q)/((-1+q)*q^n*(x-1)*(x+a*b))-(-1+q^n)*(q^n+b)*qMeixner(n-1,a,b,x,q)/(q^n*(x-1)*(x+a*b)*(-1+q))
elif y=x and p=1/q then 
   return q*(-1+q^n)*qMeixner(n,a,b,x,q)/((x-q*a)*q^n*(-1+q))-(-1+q^n)*(q^n+b)*qMeixner(n-1,a,b,x,q)*q/(q^n*(x-q*a)*b*(-1+q))
end if;        
end proc:

`qshift/qMeixner` := proc(n::algebraic,a::algebraic,b::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (x*b*q^n-q^n*b*a-x*q^n+q^n*x*b*a+x^2*(q^n)^2-x*b)*qMeixner(n,a,b,x,q)/(q^n*(-1+x)*(x+b*a))-x*(q^n-1)*(b+q^n)*qMeixner(n-1,a,b,x,q)/(q^n*(-1+x)*(x+b*a))
elif y=x and p=1/q then 
   return (x-q^n*q*a)*qMeixner(n,a,b,x,q)/((x-a*q)*q^n)+(q^n-1)*(b+q^n)*x*qMeixner(n-1,a,b,x,q)/(q^n*b*(x-a*q))
end if;        
end proc:

# definition of Quantum-q-Krawtchouk polynomial
QuantumqKrawtchouk := proc(n::algebraic,p::algebraic,N::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1 then
   return 1
end if;
'procname'(args)
end proc:

`qdiff/QuantumqKrawtchouk` := proc(n::algebraic,p::algebraic,N::algebraic,x::algebraic,q::algebraic,y::algebraic,pp::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and pp=q then
   return q^N*q*(-1+q^n)*(x*p*q^n-1)*QuantumqKrawtchouk(n,p,N,x,q)/((q-1)*q^n*(x-1)*(p*q^N*q*x-1))-q*(-1+q^n)*(-1+p*q^n)*q^N*QuantumqKrawtchouk(n-1,p,N,x,q)/(q^n*(x-1)*(p*q^N*q*x-1)*(q-1))
elif y=x and pp=1/q then 
   return q^N*(-1+q^n)*q*QuantumqKrawtchouk(n,p,N,x,q)/(q^n*(q^N*x-1)*(q-1))+(-1+q^n)*(-1+p*q^n)*q^N*QuantumqKrawtchouk(n-1,p,N,x,q)*q/(q^n*(q^N*x-1)*(q-1))
end if;        
end proc:

`qshift/QuantumqKrawtchouk` := proc(n::algebraic,p::algebraic,N::algebraic,x::algebraic,q::algebraic,y::algebraic,pp::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and pp=q then
   return (-x*q^N*q^n*q*p+q^N*x^2*p*q*(q^n)^2-q^N*x*q*q^n-x*q^n+q^n+q^N*x*q)*QuantumqKrawtchouk(n,p,N,x,q)/(q^n*(x-1)*(p*q^N*q*x-1))-q*(-1+q^n)*(-1+p*q^n)*q^N*x*QuantumqKrawtchouk(n-1,p,N,x,q)/(q^n*(x-1)*(p*q^N*q*x-1))
elif y=x and pp=1/q then 
   return (q^N*x-q^n)*QuantumqKrawtchouk(n,p,N,x,q)/(q^n*(q^N*x-1))-(-1+q^n)*(-1+p*q^n)*q^N*x*QuantumqKrawtchouk(n-1,p,N,x,q)/(q^n*(q^N*x-1))
end if;        
end proc:

# definition of q-Krawtchouk polynomial
qKrawtchouk := proc(n::algebraic,p::algebraic,N::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1 then
   return 1
end if;
'procname'(args)
end proc:

`qdiff/qKrawtchouk` := proc(n::algebraic,p::algebraic,N::algebraic,x::algebraic,q::algebraic,y::algebraic,pp::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and pp=q then
   return (-1+q^n)*(q^N*p*(q^n)^2*x+q^n+q^N*x*q-q^N*q)*qKrawtchouk(n,p,N,x,q)/(q^N*(x-1)*(q+(q^n)^2*p)*(-1+q)*x)-q^n*(-1+q^n)*(q^N*q^n*p+1)*qKrawtchouk(n-1,p,N,x,q)/(q^N*(x-1)*(q+(q^n)^2*p)*(-1+q)*x)
elif y=x and pp=1/q then 
   return (-1+q^n)*(-(q^n)^2*p+q^N*p*(q^n)^2*x+q^n*p*q*q^N+q^N*x*q)*q*qKrawtchouk(n,p,N,x,q)/((q+(q^n)^2*p)*q^n*(q^N*x-1)*(-1+q)*x)+p*q^n*(-1+q^n)*(q^N*q^n*p+1)*qKrawtchouk(n-1,p,N,x,q)*q/((q+(q^n)^2*p)*(q^N*x-1)*(-1+q)*x)
end if;        
end proc:

`qshift/qKrawtchouk` := proc(n::algebraic,p::algebraic,N::algebraic,x::algebraic,q::algebraic,y::algebraic,pp::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and pp=q then
   return q^n*(q^n-q^N*q^n*p+q^N*p*(q^n)^2*x+q^N*x*q-q^N*q-1)*qKrawtchouk(n,p,N,x,q)/(q^N*(x-1)*(q+(q^n)^2*p))-q^n*(-1+q^n)*(q^N*q^n*p+1)*qKrawtchouk(n-1,p,N,x,q)/(q^N*(x-1)*(q+(q^n)^2*p))
elif y=x and pp=1/q then 
   return -((q^n)^2*p*q^N*q-q^N*p*(q^n)^2*x-q^n*p*q*q^N-q^N*x*q+(q^n)^2*p+q^n*q)*qKrawtchouk(n,p,N,x,q)/((q+(q^n)^2*p)*q^n*(q^N*x-1))-p*q^n*(-1+q^n)*(q^N*q^n*p+1)*qKrawtchouk(n-1,p,N,x,q)/((q+(q^n)^2*p)*(q^N*x-1))
end if;        
end proc:

# definition of affine q-Krawtchouk polynomial
AffineqKrawtchouk := proc(n::algebraic,p::algebraic,N::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1 then
   return 1
elif x=q^(-N) or x=1/q^N then
   return (-p*q)^n*q^(n*(n-1)/2)/qpochhammer(p*q,q,n)
end if;
'procname'(args)
end proc:

`qdiff/AffineqKrawtchouk` := proc(n::algebraic,p::algebraic,N::algebraic,x::algebraic,q::algebraic,y::algebraic,pp::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and pp=q then
   return (-1+q^n)*AffineqKrawtchouk(n,p,N,x,q)/((x-1)*(q-1))-(-1+q^n)*AffineqKrawtchouk(n-1,p,N,x,q)/((x-1)*(q-1))
elif y=x and pp=1/q then 
   return (-1+q^n)*(p*q^n-q^N*x)*q*AffineqKrawtchouk(n,p,N,x,q)/((q-1)*(-x+p*q)*(q^N*x-1)*q^n)-(-1+q^n)*p*AffineqKrawtchouk(n-1,p,N,x,q)*q/((q^N*x-1)*(-x+p*q)*(q-1))
end if;        
end proc:

`qshift/AffineqKrawtchouk` := proc(n::algebraic,p::algebraic,N::algebraic,x::algebraic,q::algebraic,y::algebraic,pp::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and pp=q then
   return (-1+x*q^n)*AffineqKrawtchouk(n,p,N,x,q)/(x-1)-x*(-1+q^n)*AffineqKrawtchouk(n-1,p,N,x,q)/(x-1)
elif y=x and pp=1/q then 
   return -(x*p*(q^n)^2-q^N*x*q*p*q^n+p*q^n*q-x*p*q^n-x*q^n+q^N*x^2)*AffineqKrawtchouk(n,p,N,x,q)/(q^n*(q^N*x-1)*(-x+p*q))+(-1+q^n)*x*p*AffineqKrawtchouk(n-1,p,N,x,q)/((q^N*x-1)*(-x+p*q))
end if;        
end proc:

# definition of discrete q-Hermite I polynomial
DiscreteqHermiteI := proc(n::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1 then
   return q^binomial(n,2)
end if;
'procname'(args)
end proc:

`qdiff/DiscreteqHermiteI` := proc(n::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*DiscreteqHermiteI(n-1,x,q)/(q-1)
elif y=x and p=1/q then 
   return -(-1+q^n)*DiscreteqHermiteI(n-1,x,q)/((x-1)*(x+1)*(q-1))+x*q*(-1+q^n)*DiscreteqHermiteI(n,x,q)/(q^n*(x-1)*(x+1)*(q-1))
end if;        
end proc:

`qshift/DiscreteqHermiteI` := proc(n::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return x*(-1+q^n)*DiscreteqHermiteI(n-1,x,q)+DiscreteqHermiteI(n,x,q)
elif y=x and p=1/q then 
   return x*(-1+q^n)*DiscreteqHermiteI(n-1,x,q)/(q*(x-1)*(x+1))+(-q^n+x^2)*DiscreteqHermiteI(n,x,q)/(q^n*(x-1)*(x+1))
end if;        
end proc:

# definition of discrete q-Hermite II polynomial
DiscreteqHermiteII := proc(n::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1/I then
   return (-1)^n*I^n*q^(-binomial(n,2))
end if;
'procname'(args)
end proc:

`qdiff/DiscreteqHermiteII` := proc(n::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return x*(-1+q^n)*DiscreteqHermiteII(n,x,q)/((x^2+1)*(-1+q))+q*(-1+q^n)*DiscreteqHermiteII(n-1,x,q)/(q^n*(x^2+1)*(-1+q))
elif y=x and p=1/q then 
   return (-1+q^n)*DiscreteqHermiteII(n-1,x,q)*q/(q^n*(-1+q))
end if;        
end proc:

`qshift/DiscreteqHermiteII` := proc(n::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (x^2*q^n+1)*DiscreteqHermiteII(n,x,q)/(x^2+1)+x*q*(q^n-1)*DiscreteqHermiteII(n-1,x,q)/(q^n*(x^2+1))
elif y=x and p=1/q then 
   return DiscreteqHermiteII(n,x,q)-(q^n-1)*x*DiscreteqHermiteII(n-1,x,q)/q^n
end if;        
end proc:

# definition of Al-Salam-Carlitz I polynomial
AlSalamCarlitzI := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1 then
   return (-a)^n*q^binomial(n,2)
end if;
'procname'(args)
end proc:

`qdiff/AlSalamCarlitzI` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*AlSalamCarlitzI(n-1,a,x,q)/(q-1)
elif y=x and p=1/q then 
   return x*(-1+q^n)*q*AlSalamCarlitzI(n,a,x,q)/(q^n*(x-1)*(x-a)*(q-1))+(-1+q^n)*a*AlSalamCarlitzI(n-1,a,x,q)/((x-1)*(x-a)*(q-1))
end if;        
end proc:

`qshift/AlSalamCarlitzI` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return AlSalamCarlitzI(n,a,x,q)+x*(-1+q^n)*AlSalamCarlitzI(n-1,a,x,q)
elif y=x and p=1/q then 
   return (-x*q^n-x*a*q^n+x^2+a*q^n)*AlSalamCarlitzI(n,a,x,q)/(q^n*(x-1)*(x-a))-x*(-1+q^n)*a*AlSalamCarlitzI(n-1,a,x,q)/(q*(x-1)*(x-a))
end if;        
end proc:

# definition of Al-Salam-Carlitz II polynomial
AlSalamCarlitzII := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1 then
   return (-a)^n*q^(-binomial(n,2))
end if;
'procname'(args)
end proc:

`qdiff/AlSalamCarlitzII` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return x*(-1+q^n)*AlSalamCarlitzII(n,a,x,q)/((x-1)*(x-a)*(-1+q))+a*q*(-1+q^n)*AlSalamCarlitzII(n-1,a,x,q)/(q^n*(x-1)*(x-a)*(-1+q))
elif y=x and p=1/q then 
   return (-1+q^n)*AlSalamCarlitzII(n-1,a,x,q)*q/(q^n*(-1+q))
end if;        
end proc:

`qshift/AlSalamCarlitzII` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return a*q*x*(q^n-1)*AlSalamCarlitzII(n-1,a,x,q)/(q^n*(-1+x)*(x-a))+(-x*a+a+x^2*q^n-x)*AlSalamCarlitzII(n,a,x,q)/((-1+x)*(x-a))
elif y=x and p=1/q then 
   return -(q^n-1)*x*AlSalamCarlitzII(n-1,a,x,q)/q^n+AlSalamCarlitzII(n,a,x,q)
end if;        
end proc:

# definition of q-Charlier polynomial
qCharlier := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=0 then
   return qpochhammer(-q/a,q,n)
elif x=1 then
   return 1 
end if;
'procname'(args)
end proc:

`qdiff/qCharlier` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*(x*q^n+a)*qCharlier(n,a,x,q)/(q^n*(x-1)*(-1+q)*x)-(-1+q^n)*(a+q^n)*qCharlier(n-1,a,x,q)/(q^n*(x-1)*(-1+q)*x)
elif y=x and p=1/q then 
   return (-1+q^n)*q*qCharlier(n,a,x,q)/(q^n*x*(-1+q))-(-1+q^n)*(a+q^n)*qCharlier(n-1,a,x,q)*q/(q^n*a*x*(-1+q))
end if;        
end proc:

`qshift/qCharlier` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (a*q^n-q^n+(q^n)^2*x-a)*qCharlier(n,a,x,q)/(q^n*(x-1))-(q^n-1)*(a+q^n)*qCharlier(n-1,a,x,q)/(q^n*(x-1))
elif y=x and p=1/q then 
   return qCharlier(n,a,x,q)/q^n+(q^n-1)*(a+q^n)*qCharlier(n-1,a,x,q)/(a*q^n)
end if;        
end proc:

# definition of alternative q-Charlier polynomial
AlternativeqCharlier := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=0 then
   return 1
elif x=1 then
   return (-a)^n*q^n*(q^binomial(n,2))^2
end if;
'procname'(args)
end proc:

`qdiff/AlternativeqCharlier` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (-1+q^n)*(x*(q^n)^2*a+q^n+x*q)*AlternativeqCharlier(n,a,x,q)/(x^2*(q+(q^n)^2*a)*(q-1))-q^n*(-1+q^n)*AlternativeqCharlier(n-1,a,x,q)/(x^2*(q+(q^n)^2*a)*(q-1))
elif y=x and p=1/q then 
   return (-1+q^n)*(x*(q^n)^2*a-(q^n)^2*a+x*q)*q*AlternativeqCharlier(n,a,x,q)/((x-1)*(q+(q^n)^2*a)*q^n*(q-1)*x)+a*q^n*(-1+q^n)*AlternativeqCharlier(n-1,a,x,q)*q/((x-1)*(q+(q^n)^2*a)*(q-1)*x)
end if;        
end proc:

`qshift/AlternativeqCharlier` := proc(n::algebraic,a::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return (x*q+x*(q^n)^2*a-1+q^n)*q^n*AlternativeqCharlier(n,a,x,q)/(x*(q+(q^n)^2*a))-q^n*(-1+q^n)*AlternativeqCharlier(n-1,a,x,q)/(x*(q+(q^n)^2*a))
elif y=x and p=1/q then 
   return (x*q-q^n*q+x*(q^n)^2*a-(q^n)^2*a)*AlternativeqCharlier(n,a,x,q)/((x-1)*(q+(q^n)^2*a)*q^n)-a*q^n*(-1+q^n)*AlternativeqCharlier(n-1,a,x,q)/((x-1)*(q+(q^n)^2*a))
end if;        
end proc:

# definition of q-Hahn polynomial
qHahn := proc(n::algebraic,a::algebraic,b::algebraic,N::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=1 then
   return 1
end if;
'procname'(args)
end proc:

`qdiff/qHahn` := proc(n::algebraic,a::algebraic,b::algebraic,N::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return -(q*q^n*a*b*q^N-1)*(-1+q^n*b)*(-1+q^n)*qHahn(n-1,a,b,N,x,q)/((x*b*q*q^N-1)*(x-1)*(-1+(q^n)^2*a*b)*(q-1))+(-1+q^n)*(q^N*(q^n)^2*a*x*b^2*q-q*q^n*a*b*q^N-q^n*b+b*q*q^N-x*b*q*q^N+1)*qHahn(n,a,b,N,x,q)/((x*b*q*q^N-1)*(x-1)*(-1+(q^n)^2*a*b)*(q-1))
elif y=x and p=1/q then 
   return -(q*q^n*a*b*q^N-1)*(-1+q^n*b)*a*(-1+q^n)*q*qHahn(n-1,a,b,N,x,q)/((x-q*a)*(x*q^N-1)*(-1+(q^n)^2*a*b)*(q-1))+(-1+q^n)*(x*(q^n)^2*a*q^N*b-(q^n)^2*a*b-q*a^2*(q^n)^2*b*q^N+q*q^n*a*b*q^N+a*q^n-x*q^N)*q*qHahn(n,a,b,N,x,q)/((q-1)*q^n*(x-q*a)*(x*q^N-1)*(-1+(q^n)^2*a*b))
end if;        
end proc:

`qshift/qHahn` := proc(n::algebraic,a::algebraic,b::algebraic,N::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
   return -(q*q^n*a*b*q^N-1)*(-1+q^n*b)*x*(-1+q^n)*qHahn(n-1,a,b,N,x,q)/((x*b*q*q^N-1)*(x-1)*(-1+(q^n)^2*a*b))+(x^2*q^N*(q^n)^3*q*a*b^2-q^N*(q^n)^2*a*x*b^2*q-x*(q^n)^2*q*a*b*q^N+x*q^n*q*a*b*q^N-x^2*q^N*q^n*q*b+x*q^n*q*b*q^N-x*(q^n)^2*a*b+(q^n)^2*a*b-x*(q^n)^2*b+x*q^n*b+x*q^n-1)*qHahn(n,a,b,N,x,q)/((x*b*q*q^N-1)*(x-1)*(-1+(q^n)^2*a*b))
elif y=x and p=1/q then 
   return (q*q^n*a*b*q^N-1)*(-1+q^n*b)*a*x*(-1+q^n)*qHahn(n-1,a,b,N,x,q)/((x-q*a)*(x*q^N-1)*(-1+(q^n)^2*a*b))+((q^n)^3*a^2*q*b-x*a^2*q*q^N*(q^n)^2*b-x*(q^n)^2*q*a*b*q^N+x*q^n*q*a*b*q^N+x*a*q*q^N*q^n-q*a*q^n-x*(q^n)^2*a*b+x^2*q^N*(q^n)^2*a*b-x*(q^n)^2*a+x*q^n*a+x*q^n-x^2*q^N)*qHahn(n,a,b,N,x,q)/(q^n*(x-q*a)*(x*q^N-1)*(-1+(q^n)^2*a*b))
end if;        
end proc:

# definition of q-Stieltjes-Wigert polynomial
StieltjesWigert := proc(n::algebraic,x::algebraic,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if x=0 then
   return 1/qpochhammer(q,q,n)
end if;
'procname'(args)
end proc:

`qdiff/StieltjesWigert` := proc(n::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
      return (-1+q^n)*(1+x*q^n)*StieltjesWigert(n,x,q)/(x^2*q^n*(-1+q))+StieltjesWigert(n-1,x,q)/(x^2*q^n*(-1+q))
elif y=x and p=1/q then 
   return (-1+q^n)*q*StieltjesWigert(n,x,q)/(q^n*x*(-1+q))+StieltjesWigert(n-1,x,q)*q/(q^n*x*(-1+q))
end if;        
end proc:

`qshift/StieltjesWigert` := proc(n::algebraic,x::algebraic,q::algebraic,y::algebraic,p::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
if y=x and p=q then
      return (q^n-1+x*(q^n)^2)*StieltjesWigert(n,x,q)/(x*q^n)+StieltjesWigert(n-1,x,q)/(x*q^n)
elif y=x and p=1/q then 
   return StieltjesWigert(n,x,q)/q^n-StieltjesWigert(n-1,x,q)/q^n
end if;        
end proc:


# GLOBAL PROCEDURES


`convert/qFPS` := proc(f::algebraic,{var::algebraic:='q',expansionpt::algebraic:=0,base::identical(qpower,qpochhammer):='qpower',termwise::boolean:=false,MAXREORDER::posint:=4,initialcheck::boolean:=true})
local modifiedf,indet,F,x,A,k,qRE,RE,sol,i,j,m,n,fps,pn,cr,ak,rat,radius1,radius2,cand,multiplicator,functions,power,exponent,qpowers,rule,expo,prefactor,
newfps,bk,ck,opt,coe;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
                           
# parameter processing
indet:=indets(f,'name') minus {constants,var,1/var};
F:=`tools/genglobal`('F',indet);
A:=`tools/genglobal`('A',indet);

if _nrest=0 then
   if nops(indet)=1 then
      x:=op(1,indet);
      k:=`tools/genglobal`('k',indet) 
   elif nops(indet)>1 then
      error "input contains more than one variable" 
   else
      return f
   end if;
elif _nrest=1 then
   if has(_rest[1],indet) then
      x:=_rest[1];
      k:=`tools/genglobal`('k',indet)
   else
      if nops(indet)=1 then
         if op(1,indet)=_rest[1] then
            x:=op(1,indet);
            k:=_rest[1]
         else
            return f
         end if;
      elif nops(indet)>1 then
         error "input contains more than one variable" 
      else
         return f
      end if;
   end if;     
elif _nrest=2 then
   if has(_rest[1],indet) then
      x:=_rest[1];
      k:=_rest[2]
   else
      x:=_rest[2];
      k:=_rest[1]
   end if;
else
   error "wrong number of arguments"
end if;        
# end of parameter processing

# special case of polynomials or constants or powers
if type(f,polynom(anything,x)) or not has(f,x) or (patmatch(f,x^n::anything) and expansionpt=0) then
   return f
end if;

# preprocessing
if type(f,specfunc(anything,Sum)) then
   modifiedf:=`convert/qphihypergeom`(f,_options[-1]);
else
   modifiedf:=expand(f);
end if;

multiplicator:=1;
if type(modifiedf,'`+`') and termwise then
   return `combine/qFPS`(`convert/qFPS`(op(1,modifiedf),args[2..-1]) + `convert/qFPS`(subsop(1=0,modifiedf),args[2..-1]),x,var,k)
elif type(modifiedf,'`^`') and termwise then
   return `convert/qFPS`(op(1,modifiedf),args[2..-1]) * `convert/qFPS`(op(1,modifiedf)^(op(2,modifiedf)-1),args[2..-1])
elif type(modifiedf,'`*`') and termwise then
   return `convert/qFPS`(op(1,modifiedf),args[2..-1]) * `convert/qFPS`(subsop(1=1,modifiedf),args[2..-1])
elif type(modifiedf,'`*`') and hastype(modifiedf,function) then
   for i from 1 to nops(modifiedf) do 
      if not type(op(i,modifiedf),function) and not type(1/op(i,modifiedf),function) then
         if (has(op(i,modifiedf),x) and nops(indets(op(i,modifiedf)))=1) or not has(op(i,modifiedf),x) then
            multiplicator:=multiplicator*op(i,modifiedf)
         end if;
      end if;
   end do;
   modifiedf:=normal(modifiedf/multiplicator);
end if;
if multiplicator<>1 then
   userinfo(4,'qFPS',`divide by`,multiplicator,print(modifiedf));   
end if;

functions:=map(op,indets(modifiedf,'function'));
power:=[op(select(patmatch,functions,a::anything*x^m::posint))];
prefactor,exponent:=op(qgetargs(power,x));

if nops(power)>1 then
   expo:=exponent[1];
   for i from 2 to nops(exponent) do 
      expo:=gcd(expo,exponent[i])
   end do
elif nops(power)>0 then
   expo:=exponent[1]
else 
   expo:=1
end if;

if expo<>1 then
   modifiedf:=subs(x=x^(1/expo),(x^(1/expo))^expo=x,modifiedf);
   userinfo(4,'qFPS',`substitute`,x=x^(1/expo),print(modifiedf));
end if;

opt:=_options;
# var=1/q is handled
if type(var,'`^`') then 
   modifiedf:=subs(1/var=var,modifiedf);
   userinfo(4,'qFPS',`substitute`,1/var=var,print(modifiedf));
   opt:=subs(var=1/var,_options[-1]); # substitute of var=1/q to var=q
   opt:=_options[1..-2],opt;
end if;
# end of preprocessing

qRE:=qHolonomicRE(modifiedf,F(x),opt);             userinfo(4,'qFPS',`q-holonomic recurrence equation of order`,qOrder(qRE,F(x)),print(qRE));   

RE:=qREtoRE(qRE,F(x),A(k),opt);                    userinfo(4,'qFPS',`q-holonomic recurrence equation for series coefficients w.r.t.`,base,`of order`,orderRE(RE,A(k)),print(RE));

try
   # solve q-recurrence equation, if it is of q-hypergeometric type
   sol:=qFPSHypergeomTypeSolveRE(RE,A(k),modifiedf,F(x),opt);   
catch "the recurrence equation is not of q-hypergeometric type":
   userinfo(4,'qFPS',`recurrence equation for coefficients w.r.t.`,base,`is not of q-hypergeometric type`);
   try
      # try to solve general q-recurrence equation with q-Petkovsek algorithm
      sol:=qFPSHypergeomSolveRE(RE,A(k),modifiedf,F(x),opt);   
   catch "initial values could not be computed":  
      userinfo(4,'qFPS',`recurrence equation for coefficients w.r.t.`,base,`has a q-hypergeometric solution, but initial values could not be computed`);
   catch "there exists no q-hypergeometric solution of recurrence equation":   
      userinfo(4,'qFPS',`recurrence equation for coefficients w.r.t.`,base,`has no q-hypergeometric solutions`);
   end try
catch "initial values could not be computed":  
   userinfo(4,'qFPS',`recurrence equation for coefficients w.r.t.`,base,`is of q-hypergeometric type, but initial values could not be computed`);
   try
      # try to solve general q-recurrence equation with q-Petkovsek algorithm
      sol:=qFPSHypergeomSolveRE(RE,A(k),modifiedf,F(x),opt);   
   catch "initial values could not be computed":  
      userinfo(4,'qFPS',`recurrence equation for coefficients w.r.t.`,base,`has a q-hypergeometric solution, but initial values could not be computed`);
   catch "there exists no q-hypergeometric solution of recurrence equation":   
      userinfo(4,'qFPS',`recurrence equation for coefficients w.r.t.`,base,`has no q-hypergeometric solutions`);
   end try
end try;

# if q-hypergeometric solution is found, then return q-formal power series
if assigned(sol) then
   userinfo(4,'qFPS',`solution of recurrence equation for coefficients w.r.t.`,base,print(sol));
   n:=nops(sol);
   fps:=0;
   cr:=[];
   for i from 1 to n do 
      if sol[i]<>0 then
         if has(sol[i],k) then
            fps:=fps+Sum(sol[i],k=0..infinity);
         else
            fps:=fps+sol[i]
         end if;
      end if;
   end do;
   # var=1/q is handled
   if type(var,'`^`') then
      fps:=subs(1/var=var,fps);
      userinfo(4,'qFPS',`substitute`,var=1/var,print(fps));
   end if;
   if expo<>1 then
      fps:=subs(x=x^expo,fps);
      userinfo(4,'qFPS',`resubstitute`,x=x^expo,print(fps));
   end if;
   if multiplicator<>1 then
      fps:=multiplicator*fps;
      userinfo(4,'qFPS',`multiply by`,multiplicator,print(fps));   
   end if;
   if has(fps,I) then
      ak:=op(1,fps);
      bk:=simplify(ak) assuming k::even;
      bk:=subs(exp(1/2*k*Pi*I)=I^k,bk);
      bk:=subs(k=2*k,bk);
      bk:=simplify(bk) assuming k::integer;
      bk:=qsimplify(bk);
      bk:=applyrule((x^k::anything)^l::anything=x^(l*k),bk);
      ck:=simplify(ak) assuming k::odd;
      ck:=subs(exp(1/2*k*Pi*I)=I^k,ck);
      ck:=subs(k=2*k+1,ck);
      ck:=simplify(ck) assuming k::integer;
      ck:=qsimplify(ck);
      ck:=applyrule((x^k::anything)^l::anything=x^(l*k),ck);
      newfps:=0;
      if bk<>0 then
         if has(bk,k) then
            newfps:=newfps+Sum(bk,k=0..infinity);
         else
            newfps:=newfps+bk
         end if;
      end if;
      if ck<>0 then
         if has(ck,k) then
            newfps:=newfps+Sum(ck,k=0..infinity);
         else
            newfps:=newfps+ck
         end if;
      end if;
      if not has(newfps,I) or (ck=0 or bk=0) then
         fps:=newfps
      end if;
   end if;
   return `combine/qFPS`(fps,x,var,k);
end if;

f
end proc:


`convert/qphihypergeom` := proc(f::algebraic,{var::algebraic:='q'})
local i,j,k,K,x,y,cert,num,den,start,solnum,solden,sol,expo,qpowers,invqpowers,const,base,upper,lower,powerterm,newpowerterm,
ratio,r,s,ff,qvar,m,c0,v0;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;

if type(f,specfunc(anything,Sum)) then
   k:=op([2,1],f); # summation index
   if type(var,'`^`') then
      qvar:=1/var;
      return subs(qvar=1/qvar,`convert/qphihypergeom`(subs(qvar=1/qvar,f),subs(var=qvar,_options)));
   else
      qvar:=var
   end if;
   cert:=subs(k=k+1,op(1,f))/op(1,f);
   cert:=`convert/qpochhammer`(cert);
   cert:=qsimpcomb(qsimpcomb(cert,QDE));
   if type(cert,ratpoly(ratpoly(anything,x),qvar^anything)) then
      # factor terms like ((q^k)^m-1)  
      cert:=subs(var^k=K,cert);
      m:=max(degree(numer(cert),K),degree(denom(cert),K));
      for i from m by -1 to 2 do
         cert:=subs(var=var^(1/i),factor(subs(var=var^i,cert)));
      end do;
      v0:=ldegree(numer(cert),K)-ldegree(denom(cert),K);
      c0:=tcoeff(numer(cert),K)/tcoeff(denom(cert),K);
      cert:=subs(K=var^k,cert);
      
      qpowers:=select(patmatch,select(has,indets(cert,'`^`'),qvar),qvar^z::anything);
      qpowers:=map(y->`tools/genglobal`('Q')=y,qpowers);
      invqpowers:=map(y->rhs(y)=lhs(y),qpowers);
      try
         num:=subs(qpowers,convert(PolynomialTools[Split](subs(invqpowers,qsimpcomb(numer(cert))),x),radical));
         den:=subs(qpowers,convert(PolynomialTools[Split](subs(invqpowers,qsimpcomb(denom(cert))),x),radical));                                       
      catch:
         error("polynomials of q-certificate could not be splitted in linear factors");
      end try;
      start:=max(op(select(type,{solve(num*den,k)},'nonnegint')));                        # determine the nonnegative zeros of the numerator and denominator
      if type(start,'integer') then                                                       # determine index of valid initial value
         start:=start+1
      else 
         start:=0
      end if;
       
      solnum:=[];
      solden:=[];      
      if type(num,'`*`') then                                                             # determine the upper q-pochhammer symbols
         for j from 1 to nops(num) do
            if type(op(j,num),'`^`') and type(op([j,2],num),posint) then
               for expo from 1 to op([j,2],num) do
                  solnum:=[op(solnum),qtoqpochhammer(op([j,1],num),qvar,k,'delta'=1,'rho'=0,'initial'=start,output=parameter)]
               end do;
            else
               solnum:=[op(solnum),qtoqpochhammer(op(j,num),qvar,k,'delta'=1,'rho'=0,'initial'=start,output=parameter)]
            end if;
         end do;
      elif type(num,'`^`') and type(op(2,num),posint) then
         for expo from 1 to op(2,num) do
            solnum:=[op(solnum),qtoqpochhammer(op(1,num),qvar,k,'delta'=1,'rho'=0,'initial'=start,output=parameter)]
         end do;
      else 
         solnum:=[op(solnum),qtoqpochhammer(num,qvar,k,'delta'=1,'rho'=0,'initial'=start,output=parameter)]                          
      end if;  
      if type(den,'`*`') then                                                             # determine the lower q-pochhammer symbols
         for j from 1 to nops(den) do
            if type(op(j,den),'`^`') and type(op([j,2],den),posint) then
               for expo from 1 to op([j,2],den) do
                  solden:=[op(solden),qtoqpochhammer(op([j,1],den),qvar,k,'delta'=1,'rho'=0,'initial'=start,output=parameter)]
               end do;
            else
               solden:=[op(solden),qtoqpochhammer(op(j,den),qvar,k,'delta'=1,'rho'=0,'initial'=start,output=parameter)]
            end if;
         end do;
      elif type(den,'`^`') and type(op(2,den),posint) then
         for expo from 1 to op(2,den) do
            solden:=[op(solden),qtoqpochhammer(op(1,den),qvar,k,'delta'=1,'rho'=0,'initial'=start,output=parameter)]
         end do;
      else 
         solden:=[op(solden),qtoqpochhammer(den,qvar,k,'delta'=1,'rho'=0,'initial'=start,output=parameter)]
      end if; 
       
      sol:=[A(start),solnum,solden]   
   else
      error "no q-hypergeometric representation exists"
   end if;
   
   const:=1;
   ff:=expand(op(1,f));
   if type(ff,'`*`') then
      ff:=convert(ff,list)
   else
      ff:=[ff]
   end if;
   for i from 1 to nops(ff) do
      if not has(ff[i],k) then
         const:=const*ff[i]
      end if;
   end do;
   const:=simplify(const,power,symbolic);
   base:=1;
   upper:=[];
   lower:=[];

   # upper parameters
   for i from 1 to nops(solnum) do
      if nops(solnum[i])=2 then
         base:=base*solnum[i,2];
      elif solnum[i,3]=1 and solnum[i,4]=k then
         upper:=[op(upper),solnum[i,2]];
         base:=base*solnum[i,5];         
      else 
         error "no q-hypergeometric representation could be found"
      end if;
   end do;
   
   # lower parameters
   for i from 1 to nops(solden) do
      if nops(solden[i])=2 then
         base:=base/solden[i,2];
      elif solden[i,3]=1 and solden[i,4]=k then
         lower:=[op(lower),solden[i,2]];
         base:=base/solden[i,5];         
      else 
         error "no q-hypergeometric representation could be found"
      end if;
   end do;
   
   if member(qvar,lower,'pos') then
      lower:=subsop(pos=NULL,lower)
   else
      upper:=[op(upper),qvar];
   end if;

   r:=nops(upper);
   s:=nops(lower);
   if v0<1+s-r then
      upper:=[op(upper),seq(0,j=1..1+s-r-v0)];
      r:=r+1+s-r-v0;
   elif v0>1+s-r then
      lower:=[op(lower),seq(0,j=1..v0-s+r-1)];
      s:=s+v0-s+r-1;
   end if;
   return factor(simplify(qsimpcomb(eval(op(1,f),k=0),QDE),power,symbolic))*qphihypergeom(upper,lower,factor(expand(c0/(-1)^(1+s-r))),qvar);
end if;                        
error "no q-hypergeometric representation could be found"
end proc:


`convert/qfactorial` := proc(f::algebraic)
local q,rules,indet;                                                                                                   
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;      
indet:=indets(f,'name') minus {constants}; 
rules:=[];
for q in indet do
   rules:=[op(rules),qpochhammer(q,q,k::anything)/(1-q)^k::anything=qfactorial(k,q),
      qpochhammer(q,q,k::anything)/(q-1)^k::anything=(-1)^k*qfactorial(k,q),
      (1-q)^k::anything/qpochhammer(q,q,k::anything)=1/qfactorial(k,q),
      (q-1)^k::anything/qpochhammer(q,q,k::anything)=1/(-1)^k/qfactorial(k,q)]
end do;
if nops(rules)>0 then
   applyrule(rules,f)
else
   f
end if;
end proc:


`convert/qbinomial` := proc(f::algebraic)
local q,rules,indet;                                                                                                         
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;      
indet:=indets(f,'name') minus {constants};
rules:=[];
for q in indet do
   rules:=[op(rules),qpochhammer(q^(-m::anything),q,k::anything)/qpochhammer(q,q,k::anything)=(-1)^k*qbinomial(m,k,q)/q^(m*k-expand(binomial(k,2))),
   qpochhammer(1/q^m::anything,q,k::anything)/qpochhammer(q,q,k::anything)=(-1)^k*qbinomial(m,k,q)/q^(m*k-expand(binomial(k,2)))]
end do;
if nops(rules)>0 then
   simplify(applyrule(rules,f),power,symbolic)
else
   f
end if;
end proc:


`convert/qpochhammer` := proc(f::algebraic)
local q,rules,indet;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;      
indet:=indets(f,'name') minus {constants};
rules:=[];
for q in indet do
   rules:=[op(rules),qfactorial(k::anything,q)=qpochhammer(q,q,k)/(1-q)^k,
      1/qfactorial(k::anything,q)=(1-q)^k/qpochhammer(q,q,k),
      qbinomial(m::anything,k::anything,q)=(-1)^k*q^(m*k-expand(binomial(k,2)))*qpochhammer(q^(-m),q,k)/qpochhammer(q,q,k)]
end do;
if nops(rules)>0 then
   applyrule(rules,f)
else
   f
end if;
end proc:


`simplify/qpochhammer` := proc(f::algebraic,{var::algebraic:='q'})
local a,b,expr,qpochlist,arg1,arg2,arg3,i,j,m,n,l,num,den,k,newexpr;                                                                                                         
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;                                                                                                         
if denom(f)=1 then                                                                                                                                                      
   expr:=factor(f);                                                                                                                                                     
   qpochlist:=indets(expr,specfunc(anything,qpochhammer)); # all q-pochhammer symbols of expression                                                                                                               
   if nops(qpochlist)<>0 then                                                                                                                                           
      arg1:=map2(op,1,qpochlist); # list of first arguments of q-pochhammer symbols                                                                                                                            
      arg2:=map2(op,2,qpochlist); # list of second arguments of q-pochhammer symbols
      arg2:=select(y->degree(y,var)<=nops(qpochlist),arg2);                                                                                                                                        
      arg3:=map2(op,3,qpochlist); # list of third arguments of q-pochhammer symbols                                                                                                                                     
      for i from 1 to nops(arg1) do                                                                                                                                     
         for j from 1 to nops(arg2) do                                                                                                                                  
            for m from 1 to nops(arg3) do                                                                                                                               
               # apply simplification rule (a*q^b;q^n)_k * (a*q^(b+1);q^n)_k * ... * (a*q^(b+n-1);q^n)_k -> (a*q^b;q)_(n*k) = (a*q;q)_(n*k+b-1)/(a*q;q)_(b-1)           
               try 
                  b:=degree(arg1[i],var);                                                                                                                                     
                  n:=degree(arg2[j],var);                                                                                                                                     
                  a:=coeff(arg1[i],var,b);                                                                                                                                    
                  k:=arg3[m];                                                                                                                                              
                  if n>1 and mul(qpochhammer(a*var^(b+l),var^n,k),l=0..n-1)<>0 then                                                                
                     #expr:=algsubs(mul(qpochhammer(a*var^(b+l),var^n,k),l=0..n-1)=qpochhammer(a*var^b,var,n*k),expr)
                     expr:=algsubs(mul(qpochhammer(a*var^(b+l),var^n,k),l=0..n-1)=qpochhammer(a*var,var,n*k+b-1)/qpochhammer(a*var,var,b-1),expr)
                  end if;
               catch: 
               end try;
            end do;                                                                                                                                                     
         end do;                                                                                                                                                        
      end do;                                                                                                                                                              
   end if;
   expr                                                                                                                                                              
else
   expr:=f;   
   num:=`simplify/qpochhammer`(numer(expr),_options);                                                                                                                                     
   den:=`simplify/qpochhammer`(denom(expr),_options);
   expr:=num/den;
   simplify(qsimplify(`simplify/power2`(expr)),power,symbolic)   
end if;                                                                                                                                                                 
end proc:                                                                                                                                                               


`simplify/power2` := proc(f::algebraic)
local pow,num,den,k;                                                                                                       
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;                                                                                                         
num:=numer(f);
den:=denom(f);       
pow:=indets(den,'`^`');                                              # extract powers of denominator of f                                                            
pow:=select(patmatch,pow,(-1)^k::anything);                          # extract (-1)^k of denominator of f                                                            
if nops(pow)=1 then                                                                                                                                                  
   if type(op(1,pow),'`^`') then                                                                                                                                     
      k:=op([1,2],pow);
      den:=subs((-1)^k=1/(-1)^k,den)                                 # substitute (-1)^k to 1/(-1)^k                                                              
   end if;                                                                                                                                                            
end if;                                                                                                                                                               
normal(num/den)                                                                                                                                                                                                                                                                                 
end proc:


`simplify/qFPS` := proc(f::algebraic)
local expandedf,result,prod,i,s,onesum;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
# multiplies power factor to the summand of formal power series
if type(f,specfunc(anything,Sum)) then
   return f
end if;
expandedf:=f;                                                                                                         
# expandedf:=expand(f);                                                                                                         
if type(expandedf,'`+`') then
  result:=0;
  for i from 1 to nops(expandedf) do
    result:=result+`simplify/qFPS`(op(i,expandedf))  
  end do;
  return result;
elif type(expandedf,'`*`') then
  onesum:=0;
  for i from 1 to nops(expandedf) do
    if has(op(i,expandedf),Sum) then   
      s:=op(i,expandedf);
      prod:=subsop(i=1,expandedf);
      onesum:=onesum+1;
    end if; 
  end do;
  if onesum=1 then    
    return subsop(1=`simplify/power`(prod*op(1,s)),s)
  end if;
end if;
f
end proc:


`qFPSnormal` := proc(f::algebraic,x::symbol,k::symbol,q::algebraic)
local fps,Q,v0,kk;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
fps:=factor(f);
fps:=subs(q^k=Q,fps);
fps:=subs(exp(1/2*k*Pi*I)=I^k,fps);
fps:=applyrule((x^k::anything)^l::anything=x^(l*k),fps);
fps:=[selectremove(has,fps,Q)];
v0:=ldegree(numer(fps[1]),Q)-ldegree(denom(fps[1]),Q);
fps:=factor(simplify(subs(Q=q^k,normal(fps[1]/Q^v0)),power,symbolic))*factor(simplify(fps[2]*(q^k)^v0,power,symbolic));
fps:=`convert/qfactorial`(fps);
fps
end proc:


`combine/qFPS` := proc(f::algebraic,x::symbol,q::algebraic,k::symbol)
local a,b,simplifiedf,summand,summand2,result,i,j,s,t,sumfps,success,r,quot,maxquo,el;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`; 
# combines two or more formal power series
simplifiedf:=f;
simplifiedf:=`simplify/qFPS`(simplifiedf);
summand:=table();
result:=0;

if type(simplifiedf,'`+`') then
   simplifiedf:=convert(simplifiedf,list)
elif type(simplifiedf,specfunc(anything,Sum)) then
   simplifiedf:=[simplifiedf]
end if;

if type(simplifiedf,list) then
  for i from 1 to nops(simplifiedf) do
    success:=false;
    if type(op(i,simplifiedf),specfunc(anything,Sum)) then
      if patmatch(collect(simplify(expand(op(1,op(i,simplifiedf))),power,symbolic),x,factor),a::freeof(x)*x^b::anything,'s') then
        if assigned(summand[subs(s,b)]) then
          summand[subs(s,b)]:=[op(summand[subs(s,b)]),op(1,op(i,simplifiedf))];
        else 
          summand[subs(s,b)]:=[op(1,op(i,simplifiedf))];
        end if;
        success:=true;
      end if;
    end if;
    if not success then
      if type(op(i,simplifiedf),specfunc(anything,Sum)) then
         result:=result+Sum(qFPSnormal(op(1,op(i,simplifiedf)),x,k,q),k=0..infinity)
      else
         result:=result+op(i,simplifiedf)
      end if;
    end if;
  end do;
else 
  return simplifiedf
end if;

maxquo:=table();
summand2:=table();

for s in indices(summand) do
   for i from 1 to nops(summand[op(s)]) do 
      if patmatch(op(s),a::anything*k+b::anything,'t') then
         r:=modp(subs(t,b),subs(t,a)); 
         quot:=(subs(t,b)-r)/subs(t,a); 
         if assigned(maxquo[subs(t,a)*k+r]) then
            maxquo[subs(t,a)*k+r]:=max(quot,maxquo[subs(t,a)*k+r]);
         else
            maxquo[subs(t,a)*k+r]:=quot;
         end if;
      end if
   end do;
end do;

for s in indices(summand) do
   for i from 1 to nops(summand[op(s)]) do 
      if patmatch(op(s),a::anything*k+b::anything,'t') then
         r:=modp(subs(t,b),subs(t,a));
         quot:=(subs(t,b)-r)/subs(t,a)-maxquo[subs(t,a)*k+r]; 
         r:=r+subs(t,a)*maxquo[subs(t,a)*k+r];
         el:=subs(k=k-quot,summand[op(s)][i]);
         if assigned(summand2[subs(t,a)*k+r]) then
            summand2[subs(t,a)*k+r]:=qsimpcomb(summand2[subs(t,a)*k+r]+el,QDE);
         else 
            summand2[subs(t,a)*k+r]:=el;
         end if;
         try
            if quot>0 then 
               result:=result-add(eval(el,k=j),j=0..quot-1);
            elif quot<0 then
               result:=result+add(eval(el,k=j),j=quot..-1);
            end if;
         catch:
         end try;
      end if
   end do;
end do;

for s in indices(summand2) do
  sumfps:=normal(summand2[op(s)]/x^op(s));
  if has(sumfps,k) then 
    result:=result+Sum(qFPSnormal(sumfps*x^op(s),x,k,indets(q)[1]),k=0..infinity)
  else
    result:=result+sumfps
  end if;
end do;
result
end proc:


# MAIN PROCEDURES


# routines for q-shifting and q-differentiating


qdiff := proc(f::algebraic,x::Or(list,name),q::algebraic,{explicit::boolean:=false})
local i,o,a,b,s,g,u,v,d,du,dv,m,j;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;

o:=_options;

if type(x,'list') then  
   for i from 1 to nops(x) do
      if not has(f,x[i]) then
         return 0                                                                   # if f is independent of all variables in list x then return 0 
      end if;
   end do;
   if nops(x)=0 then 
      return f
      elif not type(f,'function') or (qgetoperator(f,'Op')<>Dq and explicit) then
         return qdiff(qdiff(f,x[1],q,o),x[2..-1],q,o)                               # higher q-derivatives / apply qdiff recursively      
      elif op(0,f) in qfunctions then
         return qdiff(qdiff(f,x[1],q,o),x[2..-1],q,o)                               # higher q-derivatives / apply qdiff recursively
      elif qgetoperator(f,'Op')=Dq then
         if not type(qgetoperator(f,'Arg'),'function') or explicit then
            return qdiff(qdiff(qgetoperator(f,'Arg'),qgetoperator(f,'X'),q,o),
                         [op(2..-1,qgetoperator(f,'Xlist')),op(x)],q,o)             # operator applied to operator / apply qdiff recursively
         else 
            if nops(remove(has,[op(qgetoperator(f,'Xlist')),op(x)],indets(f,name)))>0 then
               return 0
            else 
               return qsetoperator(Dq,[op(qgetoperator(f,'Xlist')),op(x)],
                                   qgetoperator(f,'Arg'),q)                         # operator applied to operator in operator form 
            end if;
         end if;
      else   
         if nops(remove(has,x,indets(f,name)))>0 then
            return 0
         else
            return qsetoperator(Dq,x,f,q)                                           # returns operator form 
         end if;  
      end if;
end if;     

# q-functions
if not has(f,x) then
   return 0                                                                         # constants                                                                
   
elif f=x then                                                                       
   return 1                                                                         # x
   
elif typematch(f,identical(x)^freeof({x,op(indets(q))})) then 
   return qbrackets(op(2,f),q)*op(1,f)^(op(2,f)-1)                                  # x^n

elif op(0,f) in qfunctions then
   d:=qdiffs[op(0,f)](op(f),x,q)                                                    # special q-functions
end if;

# composition    
if type(f,'function') then
   if type(f,specfunc(anything,qpochhammer)) or type(f,specfunc(anything,qpower1)) or type(f,specfunc(anything,qpower2)) then
      if patmatch(op(1,f),a::freeof(x)*x^b::freeof({x,op(indets(q))}),'s') and 
         op(1,f)<>x then                                                            # chain rule for f(g(x)), where g(x)=a*x^b and f=qpochhammer or f=qpower
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b and f=qpochhammer or f=qpower
            g:=op(1,f);
            d:=subs(x=g,(qshift(subsop(1=x,f),[x$subs(s,b)],q,o)-subsop(1=x,f))/((q^subs(s,b)-1)*x))*
               qdiff(g,x,q,o);
         elif type(subs(s,b),'negint') then   
            g:=op(1,f);
            d:=subs(x=g,(qshift(subsop(1=x,f),[x$(-subs(s,b))],q^(-1),o)-subsop(1=x,f))/((q^subs(s,b)-1)*x))*
               qdiff(g,x,q,o);
         end if;
      end if;
   elif type(f,specfunc(anything,qpower)) then
      if patmatch(op(1,f),a::freeof(x)*x^b::freeof({x,op(indets(q))}),'s') and 
         op(1,f)<>x and not has(op(2,f),x) then        # chain rule for f(g(x)), where g(x)=a*x^b and f=qpower and first argument g(x)
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b and f=qpochhammer or f=qpower
            g:=op(1,f);
            d:=subs(x=g,(qshift(subsop(1=x,f),[x$subs(s,b)],q,o)-subsop(1=x,f))/((q^subs(s,b)-1)*x))*
               qdiff(g,x,q,o);
         elif type(subs(s,b),'negint') then   
            g:=op(1,f);
            d:=subs(x=g,(qshift(subsop(1=x,f),[x$(-subs(s,b))],q^(-1),o)-subsop(1=x,f))/((q^subs(s,b)-1)*x))*
            qdiff(g,x,q,o);
         end if;
      elif patmatch(op(2,f),a::freeof(x)*x^b::freeof({x,op(indets(q))}),'s') and 
         op(2,f)<>x and not has(op(1,f),x) then        # chain rule for f(g(x)), where g(x)=a*x^b and f=qpower and second argument g(x)
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b and f=qpochhammer or f=qpower
            g:=op(2,f);
            d:=subs(x=g,(qshift(subsop(2=x,f),[x$subs(s,b)],q,o)-subsop(2=x,f))/((q^subs(s,b)-1)*x))*
               qdiff(g,x,q,o); 
         elif type(subs(s,b),'negint') then   
            g:=op(2,f);
            d:=subs(x=g,(qshift(subsop(2=x,f),[x$(-subs(s,b))],q^(-1),o)-subsop(2=x,f))/((q^subs(s,b)-1)*x))*
               qdiff(g,x,q,o); 
         end if;
      end if;
   else
      if patmatch(op(-2,f),a::freeof(x)*x^b::freeof({x,op(indets(q))}),'s') and 
         op(-2,f)<>x then                                              # chain rule for f(g(x)), where g(x)=a*x^b
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b and f=qpochhammer or f=qpower
            g:=op(-2,f);
            d:=subs(x=g,(qshift(subsop(-2=x,f),[x$subs(s,b)],q,o)-subsop(-2=x,f))/((q^subs(s,b)-1)*x))*
               qdiff(g,x,q,o); 
         elif type(subs(s,b),'negint') then   
            g:=op(-2,f);
            d:=subs(x=g,(qshift(subsop(-2=x,f),[x$(-subs(s,b))],q^(-1),o)-subsop(-2=x,f))/((q^subs(s,b)-1)*x))*
               qdiff(g,x,q,o); 
         end if;
      end if;
   end if;
        
# sum 
elif type(f,'`+`') then                                                             # q-derivative of sums
   d:=map(procname,f,x,q,o) 

# product
elif type(f,'`*`') then                                                 
   if has(denom(f),x) then 
      u:=numer(f);
      v:=denom(f);
      du:=qdiff(u,x,q,o);
      dv:=qdiff(v,x,q,o);
      #d:=(v*du-u*dv)/(v*subs(x=q*x,v));                                            # standard quotient rule 
      d:=(v*du-u*dv)/(v*(v+(q-1)*x*dv))                                             # quotient rule
   else 
      u:=op(1,f);v:=subsop(1=1,f);
      du:=qdiff(u,x,q,o);dv:=qdiff(v,x,q,o);
      #d:=subs(x=q*x,u)*dv+v*du;                                                    # standard product rule 
      d:=u*dv+v*du+(q-1)*x*du*dv                                                    # product rule
   end if;

# power    
elif type(f,'`^`') then                                                 
   if type(op(2,f),'negint') then 
      u:=numer(f);
      v:=denom(f);
      du:=qdiff(u,x,q,o);
      dv:=qdiff(v,x,q,o);
      #d:=(v*du-u*dv)/(v*subs(x=q*x,v));                                            # reciprocal / standard quotient rule 
      d:=(v*du-u*dv)/(v*(v+(q-1)*x*dv))                                             # reciprocal / quotient rule
   end if;
   if type(op(2,f),'posint') then  
      u:=op(1,f);v:=op(1,f)^(op(2,f)-1);
      du:=qdiff(u,x,q,o);dv:=qdiff(v,x,q,o);
      #d:=subs(x=q*x,u)*dv+v*du;                                                    # standard product rule 
      d:=u*dv+v*du+(q-1)*x*du*dv                                                    # product rule    
   end if;                                     
   if type(op(2,f),'name') then 
      u:=simplify(f,power,symbolic);
      if patmatch(u,a::freeof(x)*x^b::freeof({x,op(indets(q))})) then 
         return qdiff(u,x,q,o)                                                      # chainrule for powers
      end if;
   end if;       
end if;

if assigned(d) and d<>NULL then
  return collect(d,indets(d,function),distributed,qsimpcomb)
end if;

if qgetoperator(f,'Op')<>Dq and explicit then 
   qsimpcomb((subs(x=q*x,f)-f)/((q-1)*x))                                           # definition of first q-derivative
elif qgetoperator(f,'Op')=Dq then
   if not type(qgetoperator(f,'Arg'),'function') or explicit then
      return qdiff(qdiff(qgetoperator(f,'Arg'),qgetoperator(f,'X'),q,o),
                    [op(2..-1,qgetoperator(f,'Xlist')),x],q,o)                      # operator applied to operator / apply qdiff recursively
   else 
      if nops(remove(has,[op(qgetoperator(f,'Xlist')),x],indets(f,name)))>0 then
         return 0
      else
         return qsetoperator(Dq,[op(qgetoperator(f,'Xlist')),x],
                             qgetoperator(f,'Arg'),q)                               # operator applied to operator in operator form
      end if;
   end if;
else
   qsetoperator(Dq,x,f,q)                                                           # operator form
end if;

end proc:


qshift := proc(f::algebraic,x::Or(list,name),q::algebraic,{explicit::boolean:=false})
local i,o,k,n,s,a,b,d,xlist,m,j;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;

o:=_options;

if type(q,'`^`') then                                                               # apply qshift recursively in case of q=q^k with integer k>1 or k<-1 
   if nops(x)=1 then 
      if type(op(2,q),'posint') then
         return qshift(f,[op(indets(x))$op(2,q)],op(1,q))
      elif type(op(2,q)+1,'negint') then
         return qshift(f,[op(indets(x))$(-op(2,q))],1/op(1,q))
      end if;
   end if;
end if;
      
if type(x,'list') then
   if nops(x)=0 then 
      return f
   elif (not hastype(f,'function') or (hastype(f,'function') and not has(f,qfunctions) and qgetoperator(f,'Op')<>Sq and explicit)) and nops({op(x)})=1 then
      return subs(x[1]=q^nops(x)*x[1],f)                                            # higher q-shifts (w.r.t. one variable)
   elif not type(f,'function') or (qgetoperator(f,'Op')<>Sq and explicit) then
      return qshift(qshift(f,x[1],q,o),x[2..-1],q,o)                                # higher q-shifts / apply qshift recursively    
   elif op(0,f) in qfunctions then
      return qshift(qshift(f,x[1],q,o),x[2..-1],q,o)                                # higher q-shifts / apply qshift recursively
   elif qgetoperator(f,'Op')=Sq then
      if not type(qgetoperator(f,'Arg'),'function') or explicit then
         return qshift(qshift(qgetoperator(f,'Arg'),qgetoperator(f,'X'),q,o),
                       [op(2..-1,qgetoperator(f,'Xlist')),op(x)],q,o)               # operator applied to operator / apply qshift recursively
      else                                       
         xlist:=select(has,[op(qgetoperator(f,'Xlist')),op(x)],indets(f,name));
         if nops(xlist)=0 then
            return qgetoperator(f,'Arg')
         else
            return qsetoperator(Sq,xlist,qgetoperator(f,'Arg'),q)                   # operator applied to operator in operator form   
         end if;
      end if;
   else  
      xlist:=select(has,x,indets(f,name));
      if nops(xlist)=0 then
         return f
      else
         return qsetoperator(Sq,xlist,f,q)                                          # returns operator form
      end if;
   end if;
end if;

# q-functions
if not has(f,x) then
   return f                                                                         # constants

elif type(f,'freeof(x)') or f=x or
     typematch(f,identical(x)^freeof({x,op(indets(q))})) then                       # a*x^n 
   return subs(x=q*x,f)                                                                         
   
elif op(0,f) in qfunctions then
   d:=qshifts[op(0,f)](op(f),x,q)                                                   # special q-functions
end if;

# composition    
if type(f,'function') then                                                 
   if type(f,specfunc(anything,qpochhammer)) or type(f,specfunc(anything,qpower1)) or type(f,specfunc(anything,qpower2)) then
      if patmatch(op(1,f),a::freeof(x)*x^b::freeof({x,op(indets(q))}),'s') and 
         op(1,f)<>x then
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b and f=qpochhammer or f=qpower
            d:=subs(x=op(1,f),qshift(subsop(1=x,f),[x$subs(s,b)],q,o))
         elif type(subs(s,b),'negint') then   
            d:=subs(x=op(1,f),qshift(subsop(1=x,f),[x$(-subs(s,b))],q^(-1),o))
         end if;
      end if;
   elif type(f,specfunc(anything,qpower)) then
      if patmatch(op(1,f),a::freeof(x)*x^b::freeof({x,op(indets(q))}),'s') and 
         op(1,f)<>x and not has(op(2,f),x) then
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b and f=qpower and first argument g(x)
            d:=subs(x=op(1,f),qshift(subsop(1=x,f),[x$subs(s,b)],q,o))
         elif type(subs(s,b),'negint') then   
            d:=subs(x=op(1,f),qshift(subsop(1=x,f),[x$(-subs(s,b))],q^(-1),o))
         end if;
      elif patmatch(op(2,f),a::freeof(x)*x^b::freeof({x,op(indets(q))}),'s') and 
         op(2,f)<>x and not has(op(1,f),x) then
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b and f=qpower and second argument g(x)
            d:=subs(x=op(2,f),qshift(subsop(2=x,f),[x$subs(s,b)],q,o))
         elif type(subs(s,b),'negint') then   
            d:=subs(x=op(2,f),qshift(subsop(2=x,f),[x$(-subs(s,b))],q^(-1),o))
         end if;
      end if;
   else
      if patmatch(op(-2,f),a::freeof(x)*x^b::freeof({x,op(indets(q))}),'s') and 
         op(-2,f)<>x then
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b, is considered
            d:=subs(x=op(-2,f),qshift(subsop(-2=x,f),[x$subs(s,b)],q,o))
         elif type(subs(s,b),'negint') then   
            d:=subs(x=op(-2,f),qshift(subsop(-2=x,f),[x$(-subs(s,b))],q^(-1),o))
         end if;
      end if;
   end if;
        
# sum 
elif type(f,'`+`') then                                                             # q-shift of sums
   d:=map(procname,f,x,q,o) 

# product
elif type(f,'`*`') then                                                             # q-shift of products                                             
   d:=map(procname,f,x,q,o)
   
# power    
elif type(f,'`^`') then                                                             # q-shift of powers                                               
   d:=map(procname,f,x,q,o)        
end if;

if assigned(d) and d<>NULL then
  return collect(d,indets(d,function),distributed,qsimpcomb)
end if;

if qgetoperator(f,'Op')<>Sq and explicit then 
   subs(x=q*x,f)                                                                    # definition of first q-shift
elif qgetoperator(f,'Op')=Sq then
   if not type(qgetoperator(f,'Arg'),'function') or explicit then
      return qshift(qshift(qgetoperator(f,'Arg'),qgetoperator(f,'X'),q,o),
                    [op(2..-1,qgetoperator(f,'Xlist')),x],q,o)                      # operator applied to operator / apply qshift recursively
   else               
      xlist:=select(has,[op(qgetoperator(f,'Xlist')),x],indets(f,name));
      return qsetoperator(Sq,xlist,qgetoperator(f,'Arg'),q)                         # operator applied to operator in operator form
   end if;
else
   qsetoperator(Sq,x,f,q)                                                           # operator form
end if;  
    
end proc:


# routines of q-holonomic algebra


qHolonomicDE := proc(expr::algebraic,Fx::Or(function,name),{var::algebraic:='q',MAXDEORDER::posint:=4,minsol::boolean:=true})
local f,F,x,rat,a,n,i,j,k,DElist,filled,d,eq,sol,der,DE,DEset;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if type(Fx,'function') then 
   F:=op(0,Fx);
   x:=op(1,Fx)
else 
   F:=`tools/genglobal`('F',indets(expr,'name'));
   x:=Fx
end if;

try  
   DE:=qHolonomicRE(expr,F(x),_options[-2..-1],MAXREORDER=MAXDEORDER);
   if type(DE,list) then
      DE:=map(qREtoqDE,DE,F(x),_options[-1])
   else
      DE:=qREtoqDE(DE,F(x),_options[-1])
   end if;
   return DE;
catch:
   error cat("there exists no q-differential equation with order less or equal than MAXDEORDER=",MAXDEORDER)
end try;
end proc:


qHolonomicRE := proc(expr::algebraic,Fx::Or(function,name),{var::algebraic:='q',MAXREORDER::posint:=4,explicit::boolean:=false,minsol::boolean:=true})
local f,F,x,rat,a,n,i,j,k,RElist,filled,s,eq,sol,shi,RE,_redoptions,REset,coe,qorthpol;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if type(Fx,'function') then
   F:=op(0,Fx);
   x:=op(1,Fx)
else
   F:=`tools/genglobal`('F',indets(expr,'name')); 
   x:=Fx
end if;

_redoptions:=_options[1],_options[4]; # reduced options

REset:=[];

f:=expand(expr);
qorthpol:=['qLaguerre','LittleqLaguerre','BigqLaguerre','LittleqJacobi','BigqJacobi','LittleqLegendre','qMeixner','QuantumqKrawtchouk','qKrawtchouk','AffineqKrawtchouk','DiscreteqHermiteI','DiscreteqHermiteII',
'AlSalamCarlitzI','AlSalamCarlitzII','qCharlier','AlternativeqCharlier','qHahn','StieltjesWigert'];
if type(f,'`*`') and has(f,qorthpol) and nops(select(has,indets(f),qorthpol))>1 then # special case of q-orthogonal polynomials
   return qProductRE(qHolonomicRE(op(1,f),F(x),_redoptions),qHolonomicRE(subsop(1=1,f),F(x),_redoptions),F(x),_options) # product algorithm
elif has(f,qphihypergeom) then # special case of generalized q-hypergeometric function
   if type(f,'`+`') then
      return qSumRE(qHolonomicRE(op(1,f),F(x),_redoptions),qHolonomicRE(subsop(1=0,f),F(x),_redoptions),F(x),_options) # sum algorithm
   elif type(f,'`*`') then
      return qProductRE(qHolonomicRE(op(1,f),F(x),_redoptions),qHolonomicRE(subsop(1=1,f),F(x),_redoptions),F(x),_options) # product algorithm
   elif type(f,'`^`') then
      if type(op(2,f),posint) then
         return qProductRE(qHolonomicRE(op(1,f)^(op(2,f)-1),F(x),_redoptions),qHolonomicRE(op(1,f),F(x),_redoptions),F(x),_options) # product algorithm      
      else
         error "no q-recurrence equation could be found" 
      end if;
   elif type(f,specfunc(anything,qphihypergeom)) then
      try
         if patmatch(op(-2,f),a::freeof(x)*x^b::freeof({x,op(indets(var))}),'s') and 
            op(-2,f)<>x then
            if type(subs(s,b),'posint') and subs(s,b)<>1 then                   # f(g(x)), where g(x)=a*x^b, is considered
            return qCompositionRE(qHolonomicRE(subsop(-2=x,f),Fx,_options),Fx,subs(s,a*x^b),_options)
            end if;
         end if;
      catch:
      end try;
      try
         return qphihypergeomRE(op(f),F(x),_options)
      catch: 
      end try;
      try
         RE:=qphihypergeomRE(op(subs(x=1/x,f)),F(x),_options);
         n:=qOrder(RE,F(x),_options);
         coe:=qgetcoeffs(RE,F(x),var);
         coe:=subs(x=1/x,x=var^n*x,coe);
         RE:=add(coe[n-i+1]*qshift(F(x),[x$i],var),i=0..n);
         RE:=qNormal(RE,F(x),_options);
         return RE 
      catch: 
      end try;
      error "no q-recurrence equation could be found" 
   else 
      error "no q-recurrence equation could be found" 
   end if;
elif type(f,'function') and minsol then # composition (recursive invocation)                                                      
   if type(f,specfunc(anything,qpochhammer)) or type(f,specfunc(anything,qpower1)) or type(f,specfunc(anything,qpower2)) then
      if patmatch(op(1,f),a::freeof(x)*x^b::freeof({x,op(indets(var))}),'s') and 
         op(1,f)<>x then
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b and f=qpochhammer or f=qpower
            return qCompositionRE(qHolonomicRE(subsop(1=x,f),Fx,_options),Fx,subs(s,a*x^b),_options)
         end if;
      end if;
   elif type(f,specfunc(anything,qpower)) then
      if patmatch(op(1,f),a::freeof(x)*x^b::freeof({x,op(indets(var))}),'s') and 
         op(1,f)<>x and not has(op(2,f),x) then
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b and f=qpower and first argument g(x)
            return qCompositionRE(qHolonomicRE(subsop(1=x,f),Fx,_options),Fx,subs(s,a*x^b),_options)
         end if;
      elif patmatch(op(2,f),a::freeof(x)*x^b::freeof({x,op(indets(var))}),'s') and 
         op(2,f)<>x and not has(op(1,f),x) then
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b and f=qpower and second argument g(x)
            return qCompositionRE(qHolonomicRE(subsop(2=x,f),Fx,_options),Fx,subs(s,a*x^b),_options)
         end if;
      end if;
   else
      if patmatch(op(-2,f),a::freeof(x)*x^b::freeof({x,op(indets(var))}),'s') and 
         op(-2,f)<>x then
         if type(subs(s,b),'posint') then                                           # f(g(x)), where g(x)=a*x^b, is considered
         return qCompositionRE(qHolonomicRE(subsop(-2=x,f),Fx,_options),Fx,subs(s,a*x^b),_options)
         end if;
      end if;
   end if;
end if;

# all the other cases
n:=0;
if type(f,'`+`') then
   RElist:=[{a[0]*op(1,f)}] # initialize RElist with first summand of f
  else 
   RElist:=[{a[0]*f}]
end if;
shi:=f;

while n<=MAXREORDER do
   s:=shi;
   if not(type(s,'`+`')) then
      s:={s} 
   end if;
   for k from 1 to nops(s) do # check l.d. for every summand of the q-shifted function f(q^n*x)  
      filled:=false;
      for i from 1 to nops(RElist) do
         rat:=expand(op(k,s)/RElist[i][1]);
         rat:=qsimpcomb(rat);
         if type(rat,ratpoly(ratpoly(anything,x),var^anything)) then
            RElist[i]:={op(RElist[i]),a[n]*op(k,s)};
            filled:=true
         end if;    
      end do;
      if not(filled) then 
         RElist:=[op(RElist),{a[n]*op(k,s)}] # construct a new equivalence class if no summand of the q-shifted function f(q^n*x) is l.d. 
      end if;
   end do;
   RElist:=qSimplifyRE(RElist,x,var); # try to use existing recurrence equation to put some equivalence classes together
   userinfo(4,'qHolonomicRE',`equivalence classes for order`,n,print(RElist));

   eq:=subs(a[n]=1,map(y->add(i,i=y),RElist)); # add terms in equivalence classes
   sol:=SolveTools[Linear](eq,{a[j] $ j=0..n-1});
   if sol <> NULL and sol <> {0} then 
      RE:=subs(sol,add(a[j]*qshift(F(x),[x$j],var,_options),j=0..n));
      RE:=numer(normal(RE));
      RE:=subs(seq(a[j]=1,j=0..n),RE); # substitute all variables to 1 
      RE:=qContent(RE,F(x),'eq')=0;
      if minsol then
         return RE
      else
         REset:=[op(REset),RE]
      end if;
   else
      n:=n+1;
      shi:=qshift(f,[x$n],var)
   end if;
   
   # old (missing minimal RE for qcos(x,q) + I*qsin(x,q))
   
   # if nops(RElist)<=n then
   #    eq:=subs(a[n]=1,map(y->add(i,i=y),RElist)); # add terms in equivalence classes
   #    sol:=SolveTools[Linear](eq,{a[j] $ j=0..n-1});
   #    RE:=subs(sol,add(a[j]*qshift(F(x),[x$j],var,_options),j=0..n));
   #    RE:=numer(normal(RE));
   #    RE:=subs(seq(a[j]=1,j=0..n),RE); # substitute all variables to 1 
   #    RE:=qContent(RE,F(x),'eq')=0;
   #    if minsol then
   #       return RE
   #    else
   #       REset:=[op(REset),RE]
   #    end if;
   # end if;
   # n:=n+1;
   # shi:=qshift(f,[x$n],var)
end do;

if nops(REset)<>0 then 
   REset
else
   error cat("there exists no q-recurrence equation with order less or equal than MAXREORDER=",MAXREORDER)
end if;
end proc:


qSumDE := proc(DE1::equation,DE2::equation,Fx::function,{var::algebraic:='q'})
local DE,De1,De2,F,a,x,i,j,n,m,k,f,g,vars,approach,dfg,eq,sol;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);

n:=qOrder(DE1,F(x));
m:=qOrder(DE2,F(x));
j:=min(n,m);
De1:=subs(F(x)=f(x),lhs(DE1)-rhs(DE1));
De2:=subs(F(x)=g(x),lhs(DE2)-rhs(DE2));
vars:=[seq(qdiff(f(x),[x$k],var),k=0..n-1),seq(qdiff(g(x),[x$k],var),k=0..m-1)];

approach:=0;
for k from 0 to j-1 do
   dfg:=qreduceDE(qdiff(f(x),[x$k],var),f(x),De1,var)+
        qreduceDE(qdiff(g(x),[x$k],var),g(x),De2,var);
   approach:=approach+a[k]*dfg;
end do;

for k from j to n+m do
   dfg:=qreduceDE(qdiff(f(x),[x$k],var),f(x),De1,var)+
        qreduceDE(qdiff(g(x),[x$k],var),g(x),De2,var);
   approach:=approach+a[k]*dfg;
   eq:=collect(approach,vars);
   userinfo(4,'qSumDE',`equation for order`,k,print(eq));
   eq:={coeffs(eq,vars)};
   sol:=SolveTools[Linear](eq,[a[i] $ i=0..k]);
   if subs(op(sol),{a[i] $ i=0..k})={0} then 
   else DE:=subs(op(sol),add(a[i]*qdiff(F(x),[x$i],var),i=0..k));
        DE:=subs(seq(a[i]=1,i=0..k),DE); # substitute all variables to 1
        DE:=numer(normal(DE));
        DE:=qContent(DE,F(x),'eq')=0;
        return DE 
   end if;
end do;
end proc:


qProductDE := proc(DE1::equation,DE2::equation,Fx::function,{var::algebraic:='q'})
local DE,De1,De2,dfg,F,a,x,i,j,n,m,k,l,f,g,vars,approach,subsdfg,eq,sol,rules;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);

n:=qOrder(DE1,F(x));
m:=qOrder(DE2,F(x));
j:=min(n,m);
De1:=subs(F(x)=f(x),lhs(DE1)-rhs(DE1));
De2:=subs(F(x)=g(x),lhs(DE2)-rhs(DE2));
rules:=[seq(seq(qdiff(f(x),[x$n-i],var)*qdiff(g(x),[x$m-k],var)=vars[n*(k-1)+i],i=1..n),k=1..m)];

approach:=0;
dfg:=f(x)*g(x);
for k from 0 to j-1 do
   dfg:=qreduceDE(dfg,f(x),De1,var);
   dfg:=qreduceDE(dfg,g(x),De2,var);
   subsdfg:=dfg;
   for l from 1 to n*m do
      subsdfg:=collect(subsdfg,indets(dfg,'function'),distributed);
      subsdfg:=algsubs(op(l,rules),subsdfg)
   end do;
   approach:=approach+a[k]*subsdfg;
   dfg:=qdiff(dfg,x,var);
end do;

for k from j to n*m do
   dfg:=qreduceDE(dfg,f(x),De1,var);
   dfg:=qreduceDE(dfg,g(x),De2,var);
   subsdfg:=dfg;
   for l from 1 to n*m do
      subsdfg:=collect(subsdfg,indets(dfg,'function'),distributed);
      subsdfg:=algsubs(op(l,rules),subsdfg)
   end do;
   approach:=approach+a[k]*subsdfg;
   
   eq:=collect(approach,{vars[i] $ i=1..n*m});
   userinfo(4,'qProductRE',`equation for order`,k,print(eq));
   eq:={coeffs(eq,{vars[i] $ i=1..n*m})};
   sol:=SolveTools[Linear](eq,[a[i] $ i=0..k]);
   if subs(op(sol),{a[i] $ i=0..k})={0} then 
   else DE:=subs(op(sol),add(a[i]*qdiff(F(x),[x$i],var),i=0..k));
        DE:=subs(seq(a[i]=1,i=0..k),DE); # substitute all variables to 1
        DE:=numer(normal(DE));
        DE:=qContent(DE,F(x),'eq')=0;
        return DE 
   end if;
   dfg:=qdiff(dfg,x,var);
end do;
end proc:


qSumRE := proc(RE1::equation,RE2::equation,Fx::function,{var::algebraic:='q',explicit::boolean:=false})
local RE,Re1,Re2,F,a,x,i,j,n,m,k,f,g,vars,approach,sfg,eq,sol;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);

n:=qOrder(RE1,F(x));
m:=qOrder(RE2,F(x));
j:=min(n,m);
Re1:=subs(F(x)=f(x),lhs(RE1)-rhs(RE1));
Re2:=subs(F(x)=g(x),lhs(RE2)-rhs(RE2));
vars:=[seq(qshift(f(x),[x$k],var),k=0..n-1),seq(qshift(g(x),[x$k],var),k=0..m-1)];

approach:=0;
for k from 0 to j-1 do
   sfg:=qDivideRE(qshift(f(x),[x$k],var),Re1,f(x),_options[-1])+
        qDivideRE(qshift(g(x),[x$k],var),Re2,g(x),_options[-1]);
   approach:=approach+a[k]*sfg;
end do;

for k from j to n+m do
   sfg:=qDivideRE(qshift(f(x),[x$k],var),Re1,f(x),_options[-1])+
        qDivideRE(qshift(g(x),[x$k],var),Re2,g(x),_options[-1]);
   approach:=approach+a[k]*sfg;
   eq:=collect(approach,vars);
   userinfo(4,'qSumRE',`equation for order`,k,print(eq));
   eq:={coeffs(eq,vars)};
   sol:=SolveTools[Linear](eq,[a[i] $ i=0..k]);
   if subs(op(sol),{a[i] $ i=0..k})={0} then 
   else RE:=subs(op(sol),add(a[i]*qshift(F(x),[x$i],var,_options),i=0..k));
        RE:=subs(seq(a[i]=1,i=0..k),RE); # substitute all variables to 1
        RE:=numer(normal(RE));
        RE:=qContent(RE,F(x),'eq')=0;
        return RE 
   end if;
end do;
end proc:


qProductRE := proc(RE1::equation,RE2::equation,Fx::function,{var::algebraic:='q',explicit::boolean:=false})
local RE,Re1,Re2,F,a,x,i,j,n,m,k,l,f,g,vars,approach,coesfg,sfg,t,eq,sol,X,Y,monom;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
n:=qOrder(RE1,F(x));
m:=qOrder(RE2,F(x));
j:=min(n,m);
Re1:=subs(F(x)=f(x),lhs(RE1)-rhs(RE1));
Re2:=subs(F(x)=g(x),lhs(RE2)-rhs(RE2));

approach:=0;
for k from 0 to j-1 do
   sfg:=qEQtoPol(qDivideRE(qshift(f(x),[x$k],var),Re1,f(x),_options[-1]),f(x),X,var)*
        qEQtoPol(qDivideRE(qshift(g(x),[x$k],var),Re2,g(x),_options[-1]),g(x),Y,var);
   coesfg:=[coeffs(collect(sfg,{X,Y},distributed,qsimplify),{X,Y},'t')];
   monom:=[t];
   approach:=approach+a[k]*add(coesfg[i]*vars[n*degree(monom[i],Y)+degree(monom[i],X)+1],i=1..nops(coesfg));
end do;

for k from j to n*m do
   sfg:=qEQtoPol(qDivideRE(qshift(f(x),[x$k],var),Re1,f(x),_options[-1]),f(x),X,var)*
        qEQtoPol(qDivideRE(qshift(g(x),[x$k],var),Re2,g(x),_options[-1]),g(x),Y,var);
   coesfg:=[coeffs(collect(sfg,{X,Y},distributed,qsimplify),{X,Y},'t')];
   monom:=[t];
   approach:=approach+a[k]*add(coesfg[i]*vars[n*degree(monom[i],Y)+degree(monom[i],X)+1],i=1..nops(coesfg));
   eq:=collect(approach,{vars[i] $ i=1..n*m});
   eq:={coeffs(eq,{vars[i] $ i=1..n*m})};
   sol:=SolveTools[Linear](eq,[a[i] $ i=0..k]);
   if subs(op(sol),{a[i] $ i=0..k})={0} then 
   else RE:=subs(op(sol),add(a[i]*qshift(F(x),[x$i],var,_options),i=0..k));
        RE:=subs(seq(a[i]=1,i=0..k),RE); # substitute all variables to 1
        RE:=numer(normal(RE));
        RE:=qContent(RE,F(x),'eq')=0;
        return RE 
   end if;
end do;
end proc:


qCompositionDE := proc(DE::equation,Fx::function,xarg::algebraic,{var::algebraic:='q'})
local RE;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
RE:=qDEtoqRE(DE,Fx,_options);
RE:=qCompositionRE(RE,Fx,xarg,_options);
qREtoqDE(RE,Fx,_options)
end proc:


qCompositionRE := proc(RE::equation,Fx::function,xarg::algebraic,{var::algebraic:='q',explicit::boolean:=false})
local F,x,n,Re,qshifts,a,m,X,approach,eq,sol,qRE;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
n:=qOrder(RE,F(x));
Re:=lhs(RE)-rhs(RE);
m:=degree(xarg,x);

qshifts:=[seq(qEQtoPol(qDivideRE(qshift(F(x),[x$i*m],var),Re,F(x),_options[-1]),F(x),X,var),i=0..n)]; # list of qshifts for the composition (as polynomial)   
approach:=add(a[i]*qshifts[i+1],i=0..n);
eq:={coeffs(collect(approach,X),X)};
sol:=SolveTools[Linear](eq,[a[i] $ i=0..n]);
sol:=subs(x=xarg,sol);
qRE:=subs(op(sol),add(a[i]*qshift(F(x),[x$i],var,_options),i=0..n));
qRE:=subs(seq(a[i]=1,i=0..n),qRE); # substitute all variables to 1
qRE:=numer(normal(qRE));
qContent(qRE,F(x),'eq')=0
end proc:


qDivideRE := proc(expr1::Or(algebraic,equation),expr2::Or(algebraic,equation),Fx::function,{var::algebraic:='q',direction::identical(left,right):=right,polynomial::identical(quo,rem,all):=rem})
local F,x,n,m,i,pol1,pol2,quot,quotcoe,coe,sol,y;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
pol1:=qEQtoPol(expr1,F(x),y,var);
pol2:=qEQtoPol(expr2,F(x),y,var);
n:=degree(pol1,y);
m:=degree(pol2,y);
if n<m then 
   if polynomial=quo then
      return 0
   else
      return expr1 
   end if;
end if;
coe:=[seq(coeff(pol2,y,i),i=0..m)];

quot:=0;
while n>=m do
   if direction=right then
      quotcoe:=qsimplify(lcoeff(pol1,y)/qshift(lcoeff(pol2,y),[x$(n-m)],var));
      pol1:=collect(expand(pol1-add(quotcoe*qshift(coe[i+1],[x$(n-m)],var)*y^(n-m+i),i=0..m)),y,qsimplify)
   else 
      quotcoe:=qsimplify(qshift(lcoeff(pol1,y)/lcoeff(pol2,y),[x$m],1/var));     
      pol1:=collect(expand(pol1-add(qshift(quotcoe,[x$i],var)*coe[i+1]*y^(n-m+i),i=0..m)),y,qsimplify)
   end if;
   quot:=quotcoe*y^(n-m)+quot;
   n:=degree(pol1,y);
end do;
quot:=qPoltoRE(collect(quot,y,factor@qsimpcomb),y,F(x),var);
pol1:=qPoltoRE(collect(pol1,y,factor@qsimpcomb),y,F(x),var);

if polynomial=quo then 
   return quot
elif polynomial=rem then 
   return pol1
else 
   return [quot,pol1]
end if;
end proc:


qMultiplyRE := proc(expr1::Or(algebraic,equation),expr2::Or(algebraic,equation),Fx::function,{var::algebraic:='q',direction::identical(left,right):=right})
local F,x,n,m,i,j,pol1,pol2,coe0,coe1,coe2,sol,y;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
pol1:=qEQtoPol(expr1,F(x),y,var);
pol2:=qEQtoPol(expr2,F(x),y,var);
n:=degree(pol1,y);
m:=degree(pol2,y);
coe1:=[seq(coeff(pol1,y,i),i=0..n)];
coe2:=[seq(coeff(pol2,y,j),j=0..m)];

if direction=right then 
   sol:=add(add(coe1[i+1]*qshift(coe2[j+1],[x$i],var)*y^(i+j),j=0..m),i=0..n)
else 
   sol:=add(add(coe2[j+1]*qshift(coe1[i+1],[x$j],var)*y^(i+j),j=0..m),i=0..n)
end if;
qPoltoRE(collect(sol,y,factor@qsimpcomb),y,F(x),var)
end proc:


qGCD := proc(expr1::Or(algebraic,equation),expr2::Or(algebraic,equation),Fx::function,{var::algebraic:='q',direction::identical(left,right):=right})
local F,x,pol1,pol2,temp,lcoe;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
if type(expr1,equation) and type(expr2,equation) then 
   pol1:=lhs(expr1)-rhs(expr1);
   pol2:=lhs(expr2)-rhs(expr2);
else
   pol1:=expr1;
   pol2:=expr2;
end if;

if direction=left then
   pol1:=qAdjoint(pol1,F(x),_options);
   pol2:=qAdjoint(pol2,F(x),_options);
end if;

while pol2<>0 do
   temp:=pol2;
   pol2:=qDivideRE(pol1,pol2,F(x),_options[-1]);
   pol1:=temp;   
end do;

if direction=left then
   pol1:=qAdjoint(pol1,F(x),_options);
end if;

if has(pol1,Sq) then
   pol1
else
   Fx
end if;
end proc:


qLCM := proc(expr1::Or(algebraic,equation),expr2::Or(algebraic,equation),Fx::function,{var::algebraic:='q',direction::identical(left,right):=left})
local F,x,pol,pol1,pol2,d,sol,n,r1,r2;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
if direction=left then
   pol1:=expr1;
   pol2:=expr2;
else
   pol1:=qAdjoint(expr1,F(x),_options);
   pol2:=qAdjoint(expr2,F(x),_options);
end if;

n:=qOrder(expr1,F(x),_options)+qOrder(expr2,F(x),_options);
d:=1;

while d<>0 do
   pol:=qshift(F(x),[x$n],var)+add(c[i]*qshift(F(x),[x$i],var),i=0..n-1);
   r1:=qDivideRE(pol,pol1,F(x),'polynomial'='rem',_options[-1]);
   r2:=qDivideRE(pol,pol2,F(x),'polynomial'='rem',_options[-1]);
   sol:=solve({op(qgetcoeffs(r1=0,F(x),var)),op(qgetcoeffs(r2=0,F(x),var))},{seq(c[i],i=0..n-1)});
   pol:=subs(sol,pol);
   d:=nops(select(has,indets(pol,indexed),c));
   n:=n-d;
end do;
if direction=left then
   pol
else
   qAdjoint(pol,F(x),_options);
end;
end proc:


qAdjoint := proc(expr::Or(algebraic,equation),Fx::function,{var::algebraic:='q'})
local F,x,coe;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
coe:=qgetcoeffs(expr,F(x),var);
add(normal(qshift(subs(x=1/x,coe[i]),[x$(i-1)],var))*qshift(F(x),[x$(i-1)],var),i=1..nops(coe));
end proc:


# routines for conversion between q-recurrences


Sqtoqshift := proc(Sqf,q::algebraic)
local xlist,f;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if type(Sqf,'`+`') then
   return map(procname,Sqf,q)
elif type(Sqf,'`*`') then
   return map(procname,Sqf,q)
elif type(Sqf,'function') then
   if qgetoperator(Sqf,'Op')=Sq then
      f:=qgetoperator(Sqf,'Arg');
      xlist:=qgetoperator(Sqf,'Xlist');
      return qshift(f,xlist,q,'explicit')
   end if;
end if; 
Sqf
end proc:


Dqtoqdiff := proc(Dqf,q::algebraic)
local xlist,f;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if type(Dqf,'`+`') then
   return map(procname,Dqf,q)
elif type(Dqf,'`*`') then
   return map(procname,Dqf,q)
elif type(Dqf,'function') then
   if qgetoperator(Dqf,'Op')=Dq then 
      f:=qgetoperator(Dqf,'Arg');
      xlist:=qgetoperator(Dqf,'Xlist');
      return qdiff(f,xlist,q,'explicit')
   end if;
end if; 
Dqf
end proc:


SqtoDq := proc(Sqf,q::algebraic)
local f,x,k,n;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if type(Sqf,'`+`') then
   return collect(map(procname,Sqf,q),Dq,factor)
elif type(Sqf,'`*`') then
   return map(procname,Sqf,q)
elif type(Sqf,'function') then
   if qgetoperator(Sqf,'Op')=Sq then
      f:=qgetoperator(Sqf,'Arg');
      x:=qgetoperator(Sqf,'X');
      n:=qgetoperator(Sqf,'N');
      return add(qsimpcomb((q-1)^k*qbinomial(n,k,q)*q^binomial(k,2)*x^k*qdiff(f,[x$k],q)),k=0..n)
   end if;
end if;
Sqf      
end proc:


DqtoSq := proc(Dqf,q::algebraic)
local f,x,k,n;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if type(Dqf,'`+`') then
   return collect(map(procname,Dqf,q),Sq,factor)
elif type(Dqf,'`*`') then
   return map(procname,Dqf,q)
elif type(Dqf,'function') then
   if qgetoperator(Dqf,'Op')=Dq then 
      f:=qgetoperator(Dqf,'Arg');
      x:=qgetoperator(Dqf,'X');
      n:=qgetoperator(Dqf,'N');
      return add(qsimpcomb((-1)^n/(q-1)^n/x^n*(-1)^k*qbinomial(n,k,q)*q^(binomial(k,2)-(n-1)*k)*qshift(f,[x$k],q)),k=0..n)
   end if;
end if;
Dqf      
end proc:


qREtoqDE := proc(RE::equation,Fx::function,{var::algebraic:='q'})
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
qContent(SqtoDq(lhs(RE)-rhs(RE),var),Fx,'eq')=0
end proc:


qDEtoqRE := proc(DE::equation,Fx::function,{var::algebraic:='q'})
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
qContent(DqtoSq(lhs(DE)-rhs(DE),var),Fx,'eq')=0
end proc:  


qREtoRE := proc(RE::equation,Fx::function,Ak::function,{var::algebraic:='q',expansionpt::algebraic:=0,base::identical(qpochhammer,qpower):='qpower'})
local i,j,F,x,A,B,k,m,n,rec,rules,indet,G,reclist,Gargs,coe,Q;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);  
A:=op(0,Ak);
k:=op(1,Ak);
n:=qOrder(RE,F(x));
rec:=expand(lhs(RE));       
rules:=[];

indet:=indets(RE,'name') minus {constants,var};
G:=`tools/genglobal`('G',indet);
if base=qpower then 
   for i from 0 to n do
      rules:=[x^m::nonnegint*qshift(F(x),[x$n-i],var)=A(k)*G(n-i,m),
              qshift(F(x),[x$n-i],var)=A(k)*G(n-i,0),op(rules)]  
   end do;
elif base=qpochhammer then
   for i from 0 to n do
      rules:=[x^m::nonnegint*qshift(F(x),[x$n-i],var)=(var^(-n))^m*A(k)*G(i,m),  # factor (q^(-n))^m occurs because of shifting to inverse q-shifts 
              qshift(F(x),[x$n-i],var)=A(k)*G(i,0),op(rules)]                    # q-shifted recurrence with negative q-shifts only!!!
   end do;
end if;
unassign('i');
rec:=collect(applyrule(rules,rec),G);
if type(rec,'`+`') then
   reclist:=convert(rec,list);
else
   reclist:=[rec];
end if;

for i from 1 to nops(reclist) do
   Gargs:=[op(op(indets(reclist[i],specfunc(anything,G))))];
   if Gargs[1]>0 then
      coe:=coeff(reclist[i],G(op(Gargs)));
      for j from 1 to Gargs[1] do # eliminating q-shifts
         if base=qpower then
            coe:=collect(subs(B=A,applyrule(A(k::algebraic)=var^k*B(k)+expansionpt*(var^k-1)*var^(k-1)*B(k-1),coe)),A,factor@qsimpcomb)
         elif base=qpochhammer then
            coe:=collect(subs(B=A,applyrule(A(k::algebraic)=var^(-k)*B(k)+expansionpt*var^(-k)*(var^k-1)*B(k-1),coe)),A,factor@qsimpcomb)
         end if;
      end do;
      reclist[i]:=coe*G(0,Gargs[2]);
   end if;
   if Gargs[2]>0 then
      coe:=coeff(reclist[i],G(0,Gargs[2]));
      for j from 1 to Gargs[2] do # eliminating powers of x
         if base=qpower then
            coe:=collect(subs(B=A,applyrule(A(k::algebraic)=B(k+1)+expansionpt*var^k*B(k),coe)),A,factor@qsimpcomb)
         elif base=qpochhammer then
            coe:=collect(subs(B=A,applyrule(A(k::algebraic)=-var^(-k)*B(k+1)+expansionpt*var^(-k)*B(k),coe)),A,factor@qsimpcomb)
         end if;
      end do;
      reclist[i]:=coe;
   end if;
end do;

reclist:=subs(G(0,0)=1,reclist);
rec:=collect(convert(reclist,'`+`'),A,factor@qsimpcomb);
if type(rec,'`+`') then
   reclist:=convert(rec,list);
else
   reclist:=[rec];
end if;
reclist:=subs(var^k=Q,reclist);
for i from 1 to nops(reclist) do # substitution of powers of q^k 
   j:=op(op(indets(reclist[i],specfunc(anything,A))))-k;
   reclist[i]:=subs(Q=Q/var^j,coeff(reclist[i],A(k+j))*A(k-j));
end do;
rec:=collect(subs(Q=var^k,convert(reclist,'`+`')),A,factor@qsimpcomb);
rec:=numer(normal(rec))=0;
shiftRE(rec,Ak)
end proc:


qDEtoRE := proc(DE::equation,Fx::function,Ak::function,{var::algebraic:='q',expansionpt::algebraic:=0,base::identical(qpochhammer,qpower):='qpower'})
local qRE;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
qRE:=qDEtoqRE(DE,Fx);
qREtoRE(qRE,Fx,Ak,_options)
end proc:


REtoqRE := proc(RE::equation,Ak::function,Fx::function,{var::algebraic:='q',expansionpt::algebraic:=0,base::identical(qpochhammer,qpower):='qpower'})
local i,j,F,x,A,B,k,M,N,m,n,rec,rules,indet,G,reclist,Gargs,coe,Q,arg,shift;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
A:=op(0,Ak);
k:=op(1,Ak);
F:=op(0,Fx);
x:=op(1,Fx);   
 
n:=orderRE(RE,A(k));
rules:=[];
indet:=indets(RE,'name') minus {constants,var};
G:=`tools/genglobal`('G',indet);

if base=qpochhammer then
   rec:=subs(var^k=Q,qsimpcomb(lhs(RE)));
   rec:=expand(rec);

   for i from 0 to n do
      rules:=[Q^M::nonnegint*A(k+n-i)=F(x)*G(n-i,M),  
              A(k+n-i)=F(x)*G(n-i,0),op(rules)]                 
   end do;
   unassign('i');
   rec:=collect(applyrule(rules,rec),G);
   if type(rec,'`+`') then
      reclist:=convert(rec,list);
   else
      reclist:=[rec];
   end if;

   for i from 1 to nops(reclist) do
      Gargs:=[op(op(indets(reclist[i],specfunc(anything,G))))];
      if Gargs[1]>0 then
         coe:=coeff(reclist[i],G(op(Gargs)));
         for j from 1 to Gargs[1] do # eliminating shifts
            coe:=var/(var*expansionpt-x)*qshift(coe,x,1/var,explicit)
         end do;
         reclist[i]:=coe*G(0,Gargs[2]);
      end if;
      if Gargs[2]>0 then
         coe:=coeff(reclist[i],G(0,Gargs[2]));
         for j from 1 to Gargs[2] do # eliminating powers of q^k
            coe:=(x-expansionpt)/x*qshift(coe,x,var,explicit)+expansionpt/x*coe
         end do;
         reclist[i]:=coe;
      end if;
   end do;
else
   coe:=qgetcoeffs(RE,A(k),var);
   shift:=min(seq(i-1-degree(subs(var^k=Q,coe[i]),Q),i=1..nops(coe)));
   rec:=RE;
   if shift<0 then
      rec:=subs(k=k-shift,RE);
   end if;
   n:=n-shift;
   rec:=subs(var^k=Q,map(qsimpcomb,expand(lhs(rec))));

   for i from 0 to n do
      rules:=[Q^M::nonnegint*A(k+n-i)=F(x)*G(n-i,M),  
              A(k+n-i)=F(x)*G(n-i,0),op(rules)]                 
   end do;
   unassign('i');
   rec:=collect(applyrule(rules,rec),G);
   if type(rec,'`+`') then
      reclist:=convert(rec,list);
   else
      reclist:=[rec];
   end if;

   for i from 1 to nops(reclist) do
      Gargs:=[op(op(indets(reclist[i],specfunc(anything,G))))];
      if Gargs[2]>0 then
         coe:=coeff(reclist[i],G(op(Gargs)));
         for j from 1 to Gargs[2] do # eliminating powers of q^k
            if expansionpt=0 then
               coe:=1/var^Gargs[1]*qshift(coe,x,var,explicit)
            else 
               coe:=1/(var*x-expansionpt)/var^(j-1)*qshift(coe,x,var)               
            end if;
         end do;
         if expansionpt=0 then
            reclist[i]:=coe*G(Gargs[1],0)
         else
            reclist[i]:=coe*G(Gargs[1]-Gargs[2],0)
         end if;
      end if;
      Gargs:=[op(op(indets(reclist[i],specfunc(anything,G))))];
      if Gargs[1]>0 then
         coe:=coeff(reclist[i],G(Gargs[1],0));
         for j from 1 to Gargs[1] do # eliminating shifts
            if expansionpt=0 then
               coe:=1/x*coe
            else 
               coe:=qMultiplyRE(coe,expansionpt/(var*x-expansionpt)/x*qshift(F(x),x,var)+1/x*F(x),F(x))
            end if;
         end do;
         reclist[i]:=coe;
      end if;
   end do;
end if;

reclist:=subs(G(0,0)=1,reclist);
rec:=convert(reclist,'`+`');
arg:=indets(rec,specfunc(anything,F));
shift:=min(op(applyrule(var^m::integer=m,map('`/`',map(op,arg),x))));
if has(arg,F(x)) then # special case q^0
   shift:=min(0,shift);
end if;
rec:=subs(x=var^(-shift)*x,rec);
rec:=applyrule(F(var^m::anything*x)=qshift(F(x),[x$m],var),rec);
qNormal(rec,F(x),_options[-1]);   
end proc:


REtoqDE := proc(RE::equation,Ak::function,Fx::function,{var::algebraic:='q',expansionpt::algebraic:=0,base::identical(qpochhammer,qpower):='qpower'})
local qRE;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
qRE:=REtoqRE(RE,Ak,Fx,_options);
qREtoqDE(qRE,Fx)
end proc:


qREtoqRE := proc(RE::equation,Fx::function,Ak::function,{var::algebraic:='q',explicit::boolean:=false,conversion::identical(operator,nonoperator,default):='default'})
local F,x,y,A,k,n,newRE,qRE,arg;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
A:=op(0,Ak);
k:=op(1,Ak);
arg:=map(op,select(has,indets(RE,function),F)); # arguments
n:=qOrder(RE,F(x),var);
# WARNING: special case n=0 is not handled
qRE:=qContent(lhs(RE),F(x),'eq')=0;
newRE:=subs(F=A,x=k,qRE);  
if has(qRE,Sq) and conversion<>operator then # q-recurrence in operator form to q-recurrence in nonoperator form
   newRE:=subs(seq(qshift(F(x),[x$(n-i)],var)=A(y+n-i),i=0..n),x=var^k,y=k,qRE)
elif has(qRE,Sq) and conversion=operator then # q-recurrence in operator form to q-recurrence explicitly
   if explicit then 
      newRE:=subs(seq(qshift(F(x),[x$(n-i)],var)=qshift(A(y),[y$(n-i)],var,_options[2]),i=0..n),x=k,y=k,qRE)
   end if;
elif has(arg,var) and conversion<>operator then # q-recurrence explicitly to q-recurrence in nonoperator form
   newRE:=subs(seq(F(var^i*x)=A(y+i),i=0..n),x=var^k,y=k,qRE)
elif has(arg,var) and conversion=operator then # q-recurrence explicitly to q-recurrence in operator form
   newRE:=subs(seq(F(var^i*x)=qshift(A(y),[y$i],var),i=0..n),x=k,y=k,qRE)
elif conversion<>nonoperator then # q-recurrence in nonoperator form to q-recurrence explicitly or operator form
   newRE:=subs(seq(F(x+i)=qshift(A(y),[y$i],var,_options[2]),i=0..n),var^x=k,y=k,qRE)
end if;
newRE
end proc:


qREtohomqRE := proc(RE::equation,Fx::function,{var::algebraic:='q'})
local F,x,qRE,shiftedqRE,inhomo,ratio;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
qRE:=qContent(lhs(RE),F(x),'eq');  # homogeneous part
inhomo:=rhs(RE);
if inhomo<>0 then
   ratio:=normal(qsimpcomb(qshift(inhomo,x,var)/inhomo,QDE));
   if type(ratio,ratpoly(ratpoly(anything,x),var^anything)) then
      shiftedqRE:=qshift(qRE,x,var);
      return qNormal(denom(ratio)*shiftedqRE-numer(ratio)*qRE=0,F(x),_options);
   end if;
end if;
error "the right hand side is not q-hypergeometric"
end proc:


qDEtohomqDE := proc(DE::equation,Fx::function,{var::algebraic:='q'})
local F,x,qDE,derivatedqDE,inhomo,ratio;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
qDE:=qContent(lhs(DE),F(x),'eq');  # homogeneous part
inhomo:=rhs(DE);
if inhomo<>0 then
   ratio:=normal(qsimpcomb(qdiff(inhomo,x,var)/inhomo,QDE));
   if type(ratio,ratpoly(ratpoly(anything,x),var^anything)) then
      derivatedqDE:=qdiff(qDE,x,var);
      return qNormal(denom(ratio)*derivatedqDE-numer(ratio)*qDE=0,F(x),_options);
   end if;
end if;
error "the right hand side is not q-hypergeometric"
end proc:


# routines for solving q-recurrence equations


qPolynomialSolveRE := proc(RE::equation,Fx::function,{var::algebraic:='q',output::identical(gensol,onesol,basis):=gensol,genvar::symbol:=`tools/genglobal`('A')})
local F,x,a,i,j,n,N,pol,coepol,eq,sol;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
n:=qOrder(RE,F(x));
N:=qPolUpperBound(RE,F(x),_options[-1]);
if N<0 then 
   error "there exists no polynomial solution"
end if;
pol:=add(a[i]*x^i,i=0..N);
coepol:=qgetcoeffs(RE,F(x),var);
eq:=[coeffs(collect(add(coepol[i+1]*qshift(pol,[x$i],var,explicit),i=0..n),x),x)];
sol:=SolveTools[Linear](eq,{seq(a[j],j=0..N)});

if sol<>NULL then
   sol:=subs(sol,pol);
   if output=onesol then
      sol:=subs(seq(a[i]=1,i=0..N),sol) # substitute all variables to 1 
   else
      sol:=subs(seq(a[i]=genvar[i],i=0..N),sol)
   end if;
   return sol
end if;
error "there exists no polynomial solution"
end proc:


qRationalSolveRE := proc(RE::equation,Fx::function,{var::algebraic:='q',output::identical(gensol,onesol,basis):=gensol,genvar::symbol:=`tools/genglobal`('A')})
local F,x,n,v,coepol,qRE,sol;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
n:=qOrder(RE,F(x),_options[-1]);
v:=qUniversalDenominator(RE,F(x),_options[-1]);
coepol:=qgetcoeffs(RE,F(x),var);

qRE:=add(coepol[j+1]/qshift(v,[x$j],var)*qshift(F(x),[x$j],var),j=0..n);
qRE:=qContent(qRE,F(x),_options[-1],'eq')=0;

try
   sol:=qPolynomialSolveRE(qRE,F(x),_options);
catch:
   error "there exists no rational solution"
end try;
normal(sol/v)
end proc:  


qHypergeomTypeSolveRE := proc(RE::equation,Fx::function,{var::algebraic:='q',certificate::boolean:=false,qsimplified::boolean:=true})
local F,x,y,A,k,n,rec,REtype,start,rat,num,den,solnum,solden,i,j,lambda,a,b,hypsol,sol,varx,qpowers,expo,Q;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);

rec:=RE;
if nops(select(has,indets(rec,function),F(x)))>1 then # RE is of type F(x)
   rec:=qREtoqRE(rec,F(x),A(k),_options[-1]);
   REtype:=true
else                                                  # RE is of type A(k)
   A:=F;
   k:=x;
   REtype:=false
end if;

n:=orderRE(rec,A(k));
rec:=shiftRE(rec,A(k));
rec:=lhs(rec)-rhs(rec);
rec:=subs(var^k=varx,qsimpcomb(rec));
qpowers:=map(x->x=`tools/genglobal`('Q'),select((x,y)->op(1,x)=y and type(op(2,x),symbol),indets(rec,'`^`'),var)); # rules for substitution of powers of q
rec:=subs(qpowers,rec);
rec:=subs(varx=var^k,rec);
rec:=collect(rec,A);
sol:=[];
       
if n>0 and nops(rec)=2 then                                                               # recurrence is of q-hypergeometric type
   rat:=normal(solve(rec,A(k+n))/A(k));
   num:=factor(subs(var^k=varx,qsimpcomb(numer(rat))),I);
   den:=factor(subs(var^k=varx,qsimpcomb(denom(rat))),I);  
   num:=subs(varx=var^k,num);
   den:=subs(varx=var^k,den);
   for i from 0 to n-1 do                                                                 # determine the n solutions A(n*k),A(n*k+1),...,A(n*k+(n-1))                                                      
      if certificate or REtype then
         sol:=[op(sol),num/den];
      else
         start[i]:=max(op(select(type,{solve(subs(k=n*k+i,den),k)},'nonnegint')));        # determine the nonnegative zeros of the denominator
         if type(start[i],'integer') then                                                 # determine index of valid initial value
            start[i]:=start[i]+1
         else 
            start[i]:=0
         end if;
                    
         solnum:=1;
         solden:=1;
         if not REtype then
            if type(num,'`*`') then                                                       # determine the upper q-pochhammer symbols
               for j from 1 to nops(num) do
                  if type(op(j,num),'`^`') and type(op([j,2],num),posint) then
                     for expo from 1 to op([j,2],num) do
                        solnum:=solnum*qtoqpochhammer(op([j,1],num),var,k,'delta'=n,'rho'=i,'initial'=start[i])
                     end do;
                  else
                     solnum:=solnum*qtoqpochhammer(op(j,num),var,k,'delta'=n,'rho'=i,'initial'=start[i])
                  end if;
               end do;
            elif type(num,'`^`') and type(op(2,num),posint) then
               for expo from 1 to op(2,num) do
                  solnum:=solnum*qtoqpochhammer(op(1,num),var,k,'delta'=n,'rho'=i,'initial'=start[i])
               end do;
            else 
               solnum:=solnum*qtoqpochhammer(num,var,k,'delta'=n,'rho'=i,'initial'=start[i])                          
            end if;  
            if type(den,'`*`') then                                                             # determine the lower q-pochhammer symbols
               for j from 1 to nops(den) do
                  if type(op(j,den),'`^`') and type(op([j,2],den),posint) then
                     for expo from 1 to op([j,2],den) do
                        solden:=solden*qtoqpochhammer(op([j,1],den),var,k,'delta'=n,'rho'=i,'initial'=start[i])
                     end do;
                  else
                     solden:=solden*qtoqpochhammer(op(j,den),var,k,'delta'=n,'rho'=i,'initial'=start[i])
                  end if;
               end do;
            elif type(den,'`^`') and type(op(2,den),posint) then
               for expo from 1 to op(2,den) do
                  solden:=solden*qtoqpochhammer(op(1,den),var,k,'delta'=n,'rho'=i,'initial'=start[i])
               end do;
            else 
               solden:=solden*qtoqpochhammer(den,var,k,'delta'=n,'rho'=i,'initial'=start[i])
            end if;
         end if;
         hypsol:=`simplify/qpochhammer`(solnum/solden,_options)*A(n*start[i]+i);
         sol:=[op(sol),hypsol]
      end if;
   end do;
   sol:=subs(map(x->rhs(x)=lhs(x),qpowers),sol); # resubstitution of powers of q
   if qsimplified then
      sol:=map(qsimpcomb,sol,QDE);
      sol:=map(qsimpcomb@normal,sol);
      sol:=subs(var^k=Q,sol);
      sol:=map(simplify,sol,power,symbolic);
      sol:=subs(Q=var^k,sol);
   end if;
   # sol:=map(`convert/qbinomial`,sol);
   sol:=map(`convert/qfactorial`,sol);
   if REtype then 
      sol:=subs(var^k=x,sol)
   end if;
   if certificate or REtype then
      sol[1]
   else 
      sol
   end if;
else   
   error "the recurrence equation is not of q-hypergeometric type"
end if;
end proc:   


qHypergeomSolveRE := proc(RE::equation,Fx::function,{var::algebraic:='q',certificate::boolean:=false,output::identical(gensol,onesol,basis):=gensol,genvar::symbol:=`tools/genglobal`('A'),qsimplified::boolean:=true,method::identical(qPetkovsek,modqPetkovsek,qVanHoeij):='modqPetkovsek',mhypersol::nonnegint:=1})
local rec,F,x,A,k,FF,ff,xx,coe,a,b,aa,bb,c,i,ii,j,jj,l,r,p,polsol,polrec,m,n,f,u,zsol,sols,ratsols,cert,REtype,ltypeinfinity,ltypes,ltypezero,ltypepointcheck,
ltypepoints,counter,vinf,v0,exponent,exponenta,exponentb,firstfuchs,secondfuchs,s,c0,pola,disp1,disp2,shifts,ss,polb,varq,shift,relfulfilled,cinf,cinfcandidates,
c0candidates,faca,facb,realltypes,realltypepoints,zeros,inform,cp,lt,prodRE,ltpoints,ratsol,qpowers,indet,gensolvars,newsol,h,qhypterm,eqn,K,cartprodnops,dd,
tcff,II,JJ,mult,ltypezerovs,ltypeinfinityvs,sumu,SS,len,kk,sol,REnew,certificates,y,certif,nopssols;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);

rec:=RE;
if nops(select(has,indets(rec,function),F(x)))>1 then    # RE is of type F(x)
   REtype:=true;
else                                                     # RE is of type A(k)
   rec:=qREtoqRE(rec,F(x),FF(xx),_options[-1]);
   A:=F;
   k:=x;
   F:=FF;
   x:=xx;
   REtype:=false;
end if;

if mhypersol=0 then  # determine all m-q-hypergeometric solutions
   SS:={};
   len:={op(map2(op,1,qNewtonPolygon(rec,F(x),var,'length',v=((aaa,xxx)->-degree(aaa,xxx)))))} union {op(map2(op,1,qNewtonPolygon(rec,F(x),var,'length',v=((aaa,xxx)->ldegree(aaa,xxx)))))};
   for kk from 1 to nops(len) do
      SS:=SS union numtheory[divisors](len[kk]) 
   end do;
   sols:={};

   for kk in SS do
      sol:=qHypergeomSolveRE(RE,Fx,op(subs(0=kk,[_options])));
      if sol<>[] then
         sols:=sols union {[kk,sol]};
      end if;
   end do;
   return sols;
end if;

qpowers:=map(x->x=`tools/genglobal`('Q'),select((x,y)->op(1,x)=y and type(op(2,x),symbol),indets(rec,'`^`'),var)); # rules for substitution of powers of q
rec:=subs(qpowers,rec);

# candidates
ltypes:=qLocalTypesCandidates(rec,F(x),var,_options[4]);
ltypeinfinity:=ltypes[1];
ltypezero:=ltypes[2];
ltypepoints:=[];
cartprodnops:=[];
for ii from 1 to nops(ltypes[3]) do
   ff:=ltypes[3][ii][1];
   II:=ltypes[3][ii][2,1];
   JJ:=ltypes[3][ii][2,2];
   tcff:=tcoeff(ff,x);
   ltpoints:=[];
   for mult from II to JJ do
      ltpoints:=[op(ltpoints),[[ff,tcff^mult],mult]] # 1: factor, 2: tcoeff
   end do;
   cartprodnops:=[op(cartprodnops),[seq(jj,jj=1..(JJ-II+1))]];
   ltypepoints:=[op(ltypepoints),ltpoints];   
end do;
# zeros:=select(type,select(type,`union`(map2(op,1,ltypes[1]),map2(op,1,ltypes[2])),'`^`'),radext);
zeros:={I};
counter:=0;
inform:=table(["first q-fuchs relation"=0,"second q-fuchs relation"=0]);

if method='qVanHoeij' then
   cp:=combinat[cartprod]([[seq(ii,ii=1..nops(ltypeinfinity))],[seq(ii,ii=1..nops(ltypezero))],op(cartprodnops)]);  # ((c_infty,v_infty),(c_0,v_0),(p,v_p),...) only indices
   sols:={};

   while not cp[finished] do 
      lt:=cp[nextvalue]();
      vinf:=ltypeinfinity[lt[1]][2];
      v0:=ltypezero[lt[2]][2];
      if vinf+v0+add(ltypepoints[k-2][lt[k]][2],k=3..nops(lt))=0 then                                                   # first q-fuchs relation
         c0:=ltypezero[lt[2]][1];
         cinf:=ltypeinfinity[lt[1]][1];
         if qShiftEquivalent(c0,cinf*mul(ltypepoints[k-2][lt[k]][1,2],k=3..nops(lt)),var,_options[4]) then              # second q-fuchs relation
            cert:=cinf*x^v0*mul(ltypepoints[k-2][lt[k]][1,1]^ltypepoints[k-2][lt[k]][2],k=3..nops(lt));                 # certificate of q-hypergeometric term with same type as a solution   
            prodRE:=qProductRE(rec,qNormal(numer(cert)*qshift(F(x),[x$mhypersol],var)-denom(cert)*F(x)=0,F(x),_options[-1]),F(x),_options[-1]);
            userinfo(5,'qHypergeomSolveRE',`candidates for local types and certificate`,print([[cinf,vinf],[c0,v0],seq([ltypepoints[k-2][lt[k]][1,1],ltypepoints[k-2][lt[k]][2]],k=3..nops(lt))],cert));
            try 
               counter:=counter+1;
               ratsol:=qRationalSolveRE(prodRE,F(x),_options[-1],_options[2],output='gensol');
               if ratsol<>0 then
                  sols:=sols union {normal(qsimpcomb(normal(qshift(ratsol,[x$mhypersol],var)/ratsol*cert)))}; 
               end if;
            catch:
            end try;
         else
            inform["second q-fuchs relation"]:=inform["second q-fuchs relation"]+1;
         end if;
      else
         inform["first q-fuchs relation"]:=inform["first q-fuchs relation"]+1;
      end if;
   end do;
else # method='qPetkovsek' or method='modqPetkovsek'
   n:=qOrder(rec,F(x));
   coe:=qgetcoeffs(rec,F(x),var);
   a:=coe[1];
   b:=qshift(coe[n+1],[x$n-mhypersol],1/var);
   aa:=qgetfactors(a,x,_options,roots=zeros);        # 1: factors, 2: degree, 3: ldegree, 4: tcoeff, 5: indexset
   bb:=qgetfactors(b,x,_options,roots=zeros);
   
   a:=combinat[powerset](aa[-1]);
   b:=combinat[powerset](bb[-1]);

   sols:={};
   ltypeinfinityvs:=map2(op,2,ltypeinfinity);
   ltypezerovs:=map2(op,2,ltypezero);
   
   if mhypersol > 1 then
      SS:={};
      len:=qNewtonPolygon(rec,F(x),var,'length',v=((aaa,xxx)->-degree(aaa,xxx)),_options[4]); # determine the right j such that (i*m+j,v(a_{i*m+j})) is on edge of NP
      for kk from 1 to nops(len) do
         if irem(len[kk][1],mhypersol)=0 then
            SS:=SS union {len[kk][2]}
         end if;
      end do;
   else
      SS:={0}
   end if;
   
   for i from 1 to nops(a) do
      for j from 1 to nops(b) do
         if method='modqPetkovsek' then   
            # vinf:=degree(b[j],x)-degree(a[i],x);                            # (both inefficient, because of handling with polynomials) 
            # v0:=ldegree(a[i],x)-ldegree(b[j],x);
         
            vinf:=add(bb[2][jj],jj in b[j])-add(aa[2][ii],ii in a[i]);
            v0:=add(aa[3][ii],ii in a[i])-add(bb[3][jj],jj in b[j]);
         
            # test of v0 and vinf
            if (not vinf in ltypeinfinityvs) or (not v0 in ltypezerovs) then # test of local types in 0 and at infinity
               inform["first q-fuchs relation"]:=inform["first q-fuchs relation"]+1;
               next
            end if;

            # test of c0 and cinf               
            cinfcandidates:=select(y->op(2,y)=vinf,ltypeinfinity);
            c0candidates:=select(y->op(2,y)=v0,ltypezero);

            # cinf:=normal(lcoeff(a[i],x)/lcoeff(b[j],x));                    # (both inefficient, because of handling with polynomials)
            # c0:=normal(tcoeff(a[i],x)/tcoeff(b[j],x));                      
            c0:=mul(aa[4][ii],ii in a[i])/mul(bb[4][jj],jj in b[j]);

            zsol:={};         
            relfulfilled:=false;
            for r from 1 to nops(cinfcandidates) do 
               for s from 1 to nops(c0candidates) do
                  if qShiftEquivalent(c0candidates[s][1],cinfcandidates[r][1]*c0,var) then
                     zsol:=zsol union {z=normal(c0candidates[s][1]/c0)};
                     relfulfilled:=true;
                     # break
                  end if;
               end do;
            end do;
            
            if not relfulfilled then
               inform["second q-fuchs relation"]:=inform["second q-fuchs relation"]+1;
               next
            end if;
         end if;

         pola:=mul(aa[1][ii],ii in a[i]);  
         polb:=mul(bb[1][jj],jj in b[j]);

         for jj in SS do
            dd[jj]:=floor((n-jj)/mhypersol);
         
            f:=[seq(coe[l*mhypersol+jj+1]*mul(qshift(pola,[x$m*mhypersol+jj],var),m=0..l-1)*mul(qshift(polb,[x$m*mhypersol+jj],var),m=l..n-1),l=0..dd[jj])]; # coefficient polynomials for recurrence of polynomial c(x)
      
            if method='qPetkovsek' then
               r:=min(op(map(ldegree,f,x)));
               if r>0 then 
                  f:=normal(map('`/`',f,x^r)); # dividing by powers of x to ensure that one u[l] ist not zero
               end if;
               u:=[seq(coeff(f[l+1],x,0),l=0..dd[jj])];
               sumu:=add(u[m+1]*z^m,m=0..dd[jj]);
               if has(sumu,z) then
                  zsol:=solve(add(u[m+1]*z^m,m=0..dd[jj]),{z})
               else
                  zsol:={}
               end if;
            end if;
      
            counter:=counter+1;
      
            for p in zsol do
               polrec:=add(subs(p,z^l)*f[l+1]*qshift(c(x),[x$l*mhypersol+jj],var),l=0..dd[jj])=0; # q-recurrence equation of polynomial c(x) 
               try
                  polsol:=qPolynomialSolveRE(polrec,c(x),_options[-1],_options[2],output='gensol'); # solve q-recurrence equation (polynomial solution)  
               catch: 
                  polsol:=0:
               end try;
               if has(polsol,x) or polsol<>0 then
                  certif:=qsimpcomb(normal(subs(p,z)*pola/polb*qshift(polsol,[x$mhypersol],var)/polsol)); # create normal form z*a(x)/b(x)*c(q*x)/c(x)
                  if mhypersol>1 then
                     if qDivideRE(rec,denom(certif)*qshift(F(x),[x$mhypersol],var)-numer(certif)*F(x)=0,F(x),_options[-1])=0 then
                        sols:=sols union {certif};
                     end if;
                  else 
                     sols:=sols union {certif};
                  end if;
               end if; 
            end do;
         end do;
      end do;
   end do;
end if;   
   
userinfo(6,'qHypergeomSolveRE',`number of combinations`,print(counter));

if method='modqPetkovsek' or method='qVanHoeij' then
   userinfo(6,'qHypergeomSolveRE',`filtered`,print(op(inform)))
end if;

ratsols:=sols; # q-certificates 
ratsols:=subs(map(x->rhs(x)=lhs(x),qpowers),ratsols); # resubstitution of powers of q

gensolvars:=select(has,indets(ratsols,indexed),genvar);
newsol:={};
for i from 1 to nops(ratsols) do
   if has(ratsols[i],gensolvars) then 
      for j from 1 to nops(gensolvars) do
         try 
            newsol:=newsol union {subs(gensolvars[j]=1,seq(gensolvars[h]=0,h=1..nops(gensolvars)),ratsols[i])}
         catch:
         end try;
      end do;
   else 
      newsol:=newsol union {ratsols[i]}
   end if;
end do;
ratsols:=newsol;

if not REtype and certificate then
   return [op(subs(xx=var^k,ratsols))]
elif REtype then
   return [op(ratsols)]
end if;

if ratsols={} then
   return []
end if;

sols:={};
for i from 1 to nops(ratsols) do
   sols:=sols union {qHypergeomTypeSolveRE(qREtoqRE(denom(ratsols[i])*qshift(F(x),[x$mhypersol],var)-numer(ratsols[i])*F(x)=0,F(x),A(k),_options[-1]),A(k),_options[-1],_options[-2])}
end do;
if mhypersol > 1 then
   nopssols:=nops(sols);
   sols:=[seq(map2(op,kk,[op(sols)]),kk=1..mhypersol)];
   sols:=map2(applyrule,A(K::anything)=1,sols);
   if output='gensol' then
      if nopssols>1 then
         sols:=[seq(add(genvar[j,i]*sols[j][i],i=1..nopssols),j=1..mhypersol)]
      else
         sols:=[seq(genvar[j]*sols[j][1],j=1..mhypersol)]
      end if;
   elif output='onesol' then
      sols:=[seq(sols[j][1],j=1..mhypersol)];
   end if;
   subs(exp(1/2*k*Pi*I)=I^k,sols)
else
   sols:=map(op,sols);
   sols:=[op(sols)];
   sols:=applyrule(A(K::anything)=1,sols);
   if output='gensol' then
      sols:=add(genvar[i]*sols[i],i=1..nops(sols));
   elif output='onesol' then
      sols:=sols[1];
   end if;
   subs(exp(1/2*k*Pi*I)=I^k,sols)
end if;
end proc:


# miscellaneous q-routines 


qShiftRE := proc(RE::equation,Fx::function,{var::algebraic:='q'})
local F,x,opt,n,coe,qRE;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);                                          
x:=op(1,Fx);
if type(var,'`^`') then 
   opt:=subs(var=1/var,_options);
   n:=qOrder(RE,F(x),opt);
   coe:=qgetcoeffs(RE,F(x),1/var);
   qRE:=qNormal(add(subs(x=var^n*x,coe[i])*qshift(F(x),[x$n+1-i],var),i=1..n+1)=0,F(x),opt);
else
   opt:=_options;
   n:=qOrder(RE,F(x),opt);
   coe:=qgetcoeffs(RE,F(x),var);
   qRE:=qNormal(add(subs(x=var^n*x,coe[i])*qshift(F(x),[x$n+1-i],1/var),i=1..n+1)=0,F(x),opt);
end if;
qRE
end proc:


qOrder := proc(EQ::Or(algebraic,equation),Fx::function,{var::algebraic:='q'})
local F,x,Oplist,Flist;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);                                          
x:=op(1,Fx);
if has(EQ,Sq) or has(EQ,Dq) then                      # q-recurrence equation in operator form
   Oplist:=indets(EQ,function);                       # list of operators
   Oplist:=select(has,Oplist,F(x));
   return max(op(map(qgetoperator,Oplist,'N')),0)
else                                                  # q-recurrence equation explicitly or ordinary recurrence equation 
   Flist:=indets(EQ,function); 
   Flist:=select(has,Flist,F); 
   if has(Flist,var) then                             # q-shifts occur
      Flist:=map(degree,subs(x=1,map(op,Flist)),var); # get the exponent of every q-shift 
   else                                               # ordinary shifts occur
      Flist:=subs(x=0,map(op,Flist))                  # get the index of every shift 
   end if;
   return max(op(Flist),0)
end if;
end proc:


qContent := proc(EQ::Or(algebraic,equation),Fx::function,{var::algebraic:='q',eq::boolean:=false})
local F,x,Eq,i,content,Oplist;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
if type(EQ,equation) then
   Eq:=lhs(EQ)-rhs(EQ);
else 
   Eq:=EQ;
end if;
Eq:=factor(qsimpcomb(Eq));
Oplist:=indets(Eq,function); 
Oplist:=select(has,Oplist,F); # list of operators 

content:=1;
if type(Eq,'`*`') then
   for i from 1 to nops(Eq) do
      if not has(op(i,Eq),Oplist) then
         content:=content*op(i,Eq)
      end if;
   end do;
end if;

if eq then 
   Eq:=collect(normal(Eq/content),Oplist,factor@qsimpcomb)=0;
   #Eq:=collect(normal(Eq/content),Oplist,coe->collect(coe,x,factor))=0;
   if type(EQ,equation) then
      return Eq
   else 
      return lhs(Eq)
   end if
end if;
content
end proc:


qNormal := proc(EQ::Or(algebraic,equation),Fx::function,{var::algebraic:='q'})
local F,x,equation,pol,y,shift,n,i,G,M;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);                                          
x:=op(1,Fx);
equation:=EQ;
if has(EQ,Sq) then
   pol:=qEQtoPol(equation,F(x),y,var);
   shift:=ldegree(pol,y);
   pol:=subs(x=1/var^shift*x,normal(pol/y^shift));
   equation:=qPoltoRE(pol,y,F(x),var);
   equation:=equation=0;
end if;
qContent(equation,F(x),'eq',_options);
end proc:


qCertificate := proc(f::algebraic,x::symbol,q::algebraic)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
normal(qsimpcomb(qshift(f,x,q)/f))
end proc:


qShiftRelation := proc(f::algebraic,Fx::function,{var::algebraic:='q',qoperator::identical(Dq,Sq):='Sq'})
local u,v,r,s,a,n,b,m,F,x,xarg,i,shiftrel,p;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if type(f,specfunc(anything,qphihypergeom)) then
   u:=op(1,f);
   v:=op(2,f);
   xarg:=op(3,f);
   r:=nops(u);
   s:=nops(v);
   a,n:=op(qgetargs(u,var));
   b,m:=op(qgetargs(v,var));
   F:=op(0,Fx);
   x:=op(1,Fx);
   
   # determine shift relation
   if member(x,u,'i') and not member(x,v) then
      p:=a[i]*var^n[i];
      if qoperator=Dq then
         shiftrel:=p/(1-p)*(1-var)*xarg*qsetoperator(qoperator,xarg,f,var)+f-subs(p=var*p,f)
      else
         shiftrel:=p/(1-p)*(f-qsetoperator(qoperator,xarg,f,var))+f-subs(p=var*p,f)
      end if;
   elif member(x,v,'i') and not member(x,u) then
      p:=b[i]*var^(m[i]-1);
      if qoperator=Dq then
         shiftrel:=p/(1-p)*(1-var)*xarg*qsetoperator(qoperator,xarg,f,var)+f-subs(simplify(p*var)=p,f)
      else
         shiftrel:=p/(1-p)*(f-qsetoperator(qoperator,xarg,f,var))+f-subs(simplify(p*var)=p,f)
      end if;
   else 
      error cat(x," is no member of list of upper or list of lower parameters, or occurs in both lists")
   end if;

   shiftrel:=numer(normal(shiftrel));
   shiftrel:=qContent(shiftrel,F(x),'eq')=0;
   shiftrel:=qsetoperator(qoperator,xarg,f,var)=solve(shiftrel,qsetoperator(qoperator,xarg,f,var));
   map(collect,shiftrel,indets(shiftrel,function),factor@qsimpcomb)
else
   error "wrong type of input"
end if;
end proc:


qContiguityRelation := proc(f::algebraic,Fx::function,{var::algebraic:='q',explicit::boolean:=false})
local u,v,r,s,d,a,n,b,m,F,x,xarg,p,i,j,qRE,A,contigrel,coelist,explist;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if type(f,specfunc(anything,qphihypergeom)) then
   u:=op(1,f);
   v:=op(2,f);
   xarg:=op(3,f);
   r:=nops(u);
   s:=nops(v);
   a,n:=op(qgetargs(u,var));
   b,m:=op(qgetargs(v,var));
   F:=op(0,Fx);
   x:=op(1,Fx);

   # determine q-recurrence equation in operator form
   d:=min(r,s+1);
   qRE:=(-1)^(s+1)*var^(r-d)*xarg*SQ^(s+1-d)*mul(1-a[j]*var^n[j]*SQ,j=1..r)+(-1)^r*(SQ-1)*SQ^(r-d)*mul(1-b[j]*var^(m[j]-1)*SQ,j=1..s);
   qRE:=numer(normal(qRE));
   qRE:=collect(qRE,SQ);

   # determine contiguity relation
   if has(u,x) and not has(v,x) then
      for j from 1 to r do
         if has(u[j],x) then
            i:=j;
            break
         end if;
      end do;
      p:=a[i]*var^n[i];
      contigrel:=subs(SQ=(p-1)/p*A+1/p,qRE) # convert into a polynomial in A
   elif has(v,x) and not has(u,x) then
      for j from 1 to s do
         if has(v[j],x) then
            i:=j;
            break
         end if;
      end do;
      p:=b[i]*var^(m[i]-1);
      contigrel:=subs(SQ=(p-1)/p*A+1/p,qRE); # convert into a polynomial in A
      p:=simplify(p*var,power,symbolic);
   else 
      error cat(x," is no member of list of upper or list of lower parameters or occurs in both lists")
   end if;
   
   contigrel:=numer(normal(contigrel));
   contigrel:=collect(contigrel,A);
   coelist:=[coeffs(contigrel,A,'explist')];
   explist:=map(degree,[explist],A);
   contigrel:=add(coelist[j]*qshift(F(p),[p$explist[j]],var,_options),j=1..nops(coelist));
   contigrel:=qContent(contigrel,F(p),_options[-1],'eq')=0;
   if p<>x then
      subs(p=x,contigrel)
   else
      contigrel
   end if;
else
   error "wrong type of input"
end if;
end proc:


qRelation := proc(f::algebraic,Fx::function,shiftvar::algebraic,{var::algebraic:='q',explicit::boolean:=false,direction::identical(up,down):=up})
local u,v,r,s,d,a,n,b,m,F,x,xarg,p,i,j,qRE,A,contigrel,coelist,explist,qvar,qexpr,x1,x2,q1,q2;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if type(f,specfunc(anything,qphihypergeom)) then
   F:=op(0,Fx);
   x:=op(1,Fx);
   u:=op(1,f);
   v:=op(2,f);
   xarg:=op(3,f);
   qexpr:=op(4,f);
   r:=nops(u);
   s:=nops(v);
   a,n:=op(qgetargs(u,var));
   b,m:=op(qgetargs(v,var));
   x1,x2:=op(qgetargs([xarg],x));
   q1,q2:=op(qgetargs([qexpr],var));

   # determine contiguity relation
   if has(u,shiftvar) and not has(v,shiftvar) then
      for j from 1 to r do
         if has(u[j],shiftvar) then
            i:=j;
            break
         end if;
      end do;
      p:=a[i]*var^n[i];
      if direction=up then 
         return normal((1-p*qshift(F(x),[x$op(q2)],var,_options))/(1-p)) 
      else
         qvar:=var;
         qRE:=qEQtoPol(lhs(qphihypergeomRE(u,v,xarg,qexpr,F(x),_options)),F(x),SQ,var);
         contigrel:=subs(SQ=(p-1)/p*A+1/p,qRE) # convert into a polynomial in A
      end if;
   elif has(v,shiftvar) and not has(u,shiftvar) then
      for j from 1 to s do
         if has(v[j],shiftvar) then
            i:=j;
            break
         end if;
      end do;
      p:=b[i]*var^(m[i]-1);
      if direction=down then 
         return normal((1-p*qshift(F(x),[x$op(q2)],var,_options))/(1-p)) 
      else
         qvar:=1/var;
         qRE:=qEQtoPol(lhs(qphihypergeomRE(u,v,xarg,qexpr,F(x),_options)),F(x),SQ,var);
         contigrel:=subs(SQ=(p-1)/p*A+1/p,qRE); # convert into a polynomial in A
         p:=simplify(p*var,power,symbolic)
      end if;
   else 
      error cat(shiftvar," is no member of list of upper or list of lower parameters or occurs in both lists")
   end if;

   contigrel:=numer(normal(contigrel));
   contigrel:=-normal((contigrel-coeff(contigrel,A,0))/A/coeff(contigrel,A,0));
   contigrel:=collect(contigrel,A);
   coelist:=[coeffs(contigrel,A,'explist')];
   explist:=map(degree,[explist],A);
   contigrel:=add(coelist[j]*qshift(F(p),[p$explist[j]],qvar,_options),j=1..nops(coelist));
   #contigrel:=qContent(contigrel,F(p),'eq')=0;
   #contigrel:=lhs(contigrel);
   if p<>shiftvar then
      subs(p=shiftvar,contigrel)
   else
      contigrel
   end if;
else
   error "wrong type of input"
end if;
end proc:


# routines for q-Van-Hoeij algorithm


qPlotNewtonPolygon := proc(RE::equation,Fx::function,{var::algebraic:='q',v::procedure:=((a,x)->-degree(a,x))})
local np,p1,p2;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
np:=qNewtonPolygon(RE,Fx,var,_options);
p1:=plots[listplot](np);
p2:=plots[pointplot](np,symbol=circle,symbolsize=20);
plots[display](p1,p2,scaling=constrained)
end proc:


qNewtonPolygon := proc(RE::equation,Fx::function,q::algebraic,{v::procedure:=((a,x)->-degree(a,x)),slopes::boolean:=false,eq::boolean:=false,eqvar::algebraic:='T',mhypersol::posint:=1,length::boolean:=false})
local F,x,n,coepol,i,j,NP,slope,charpols,vi,vj,s,charpol,k,J,JJ,ii,jj,lengths;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
F:=op(0,Fx);
x:=op(1,Fx);
n:=qOrder(RE,F(x),var=q);
coepol:=qgetcoeffs(RE,F(x),q);
i:=0;
NP:=[];
charpols:=[];
lengths:=[];
while i<>n do
   if coepol[i+1]=0 then next end if;
   vi:=v(coepol[i+1],x);
   NP:=[op(NP),[i,vi]];
   slope:=infinity;
   for j from i+1 to n do 
      if coepol[j+1]=0 then next end if;
      vj:=v(coepol[j+1],x);
      s:=(vj-vi)/(j-i);
      if s<slope then 
         slope:=s;
         if mhypersol > 1 then
            ii:=iquo(i,mhypersol);
            jj:=irem(i,mhypersol);
            charpol:=q^((1/2*ii*(ii-1)*mhypersol^2+ii*jj*mhypersol)*s*(-v(x,x)))*coeff(coepol[i+1],x,v(x,x)*vi);
         else
            charpol:=q^(-1/2*i*(i-1)*s*v(x,x))*coeff(coepol[i+1],x,v(x,x)*vi);
         end if;
      end if;
      if s=slope then
         if mhypersol > 1 then
            if irem(j-i,mhypersol) = 0 then
               ii:=iquo(j,mhypersol);
               jj:=irem(j,mhypersol);
               charpol:=charpol+q^((1/2*ii*(ii-1)*mhypersol^2+ii*jj*mhypersol)*s*(-v(x,x)))*coeff(coepol[j+1],x,v(x,x)*vj)*eqvar^(iquo(j-i,mhypersol));
            end if;
         else 
            charpol:=charpol+q^(-1/2*j*(j-1)*s*v(x,x))*coeff(coepol[j+1],x,v(x,x)*vj)*eqvar^(j-i);
         end if;
         k:=j;
      end if;
   end do;
   if has(charpol,eqvar) then
      charpols:=[op(charpols),[slope,charpol]];
      if mhypersol=1 then
         jj:=0
      end if;
      lengths:=[op(lengths),[mhypersol*degree(charpol,eqvar),jj]];
   end if;
   i:=k;
end do;
NP:=[op(NP),[n,v(coepol[n+1],x)]];

if length then
   return lengths
end if;

if slopes then
   map2(op,1,charpols)
elif eq then
   charpols
else
   NP
end if;
end proc:


qDispersion:=proc(p::algebraic,r::algebraic,x::algebraic,{var::algebraic:='q',set::boolean:=false})
local i,j,candidate,deg,pf,rf,pol,ratio,rule,dispset,a,b,c,d,m;
pf:=p;
rf:=r;
while type(normal(pf/x),polynom(anything,x)) do
  pf:=normal(pf/x);
end do;
while type(normal(rf/x),polynom(anything,x)) do
  rf:=normal(rf/x);
end do;
pf:=map2(op,1,op(2,factors(pf)));
rf:=map2(op,1,op(2,factors(rf)));
dispset:={};
for i from 1 to nops(pf) do
  for j from 1 to nops(rf) do
    deg:=degree(op(i,pf),x);
    if deg=degree(op(j,rf),x) and deg>0 then 
      a:=coeff(op(i,pf),x,deg);
      b:=coeff(op(i,pf),x,0);
      c:=coeff(op(j,rf),x,deg);
      d:=coeff(op(j,rf),x,0);
      ratio:=normal(a*d/b/c);
      if patmatch(ratio,m::anything*var^k::nonnegint,'rule') then
        candidate:=subs(rule,k)/deg;
        if type(candidate,nonnegint) then
          pol:=expand(subs(x=var^candidate*x,op(j,rf)));
          if not has(normal(pol/expand(op(i,pf))),x) then
            dispset:=dispset union {candidate}
          end if;
        end if;
      end if;
      if not has(ratio,x) then
        if not has(normal(op(j,rf)/op(i,pf)),x) then
          dispset:=dispset union {0}
        end if;
      end if;
    end if; 
  end do;
end do;
if not set then 
  max(op(dispset))  
else
  dispset
end if;
end proc:


qShiftEquivalent := proc(expr1::algebraic,expr2::algebraic,q::algebraic,{mhypersol::posint:=1})
local rat,n,nn;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if expr1=0 and expr2=0 then # both are equal zero
   return true
end if;
if expr1<>0 and expr2<>0 then  # both are not equal zero
   rat:=qsimpcomb(expr1/expr2);
   if rat=1 then
      return true
   end if;
   if patmatch(rat,q^n::integer,'nn') then 
      if mhypersol > 1 then
         if irem(subs(nn,n),mhypersol)=0 then
            return true
         else 
            return false
         end if;
      else 
         return true
      end if;
   end if;
end if;
false
end proc:


qFactors := proc(term::algebraic,x::algebraic,q::algebraic,{mhypersol::posint:=1})
local fact,eqcl,f,i,qDis1,qDis2;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
fact:=factors(term)[2];
if nops(fact)=0 then
   return []
end if;
eqcl:=[fact[1]];
fact:=fact[2..-1];
for f in fact do
   for i from 1 to nops(eqcl) do
      qDis1:=qDispersion(f[1],eqcl[i,1],x,'var'=q);
      qDis2:=qDispersion(eqcl[i,1],f[1],x,'var'=q);
      if type(qDis1,numeric) or type(qDis2,numeric) then # they are qshift equivalent
         if mhypersol>1 then 
            if irem(qDis1,mhypersol)=0 or irem(qDis2,mhypersol)=0 then # they are m-q-shift equivalent
               eqcl[i,2]:=eqcl[i,2]+f[2]; 
               break;
            end if;
         else
            eqcl[i,2]:=eqcl[i,2]+f[2]; 
            break;
         end if;
      end if;
      if i=nops(eqcl) then
         eqcl:=[op(eqcl),f] # build a new qshift equivalence class
      end if;      
   end do;
end do;

eqcl
end proc:


qFactorsOperator := proc(term1::algebraic,term2::algebraic,x::algebraic,q::algebraic)
local fact,eqcl,f,i,plusdisp,minusdisp;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
fact:=[op(factors(term1)[2]),op(map(x->[op(1,x),-op(2,x)],factors(term2)[2]))];
if nops(fact)=0 then
   return []
end if;

eqcl:=[fact[1]];
if fact[1,2]<0 then
   eqcl:=map(x->[op(x),[[],[[0,fact[1,2]]]]],eqcl)
else
   eqcl:=map(x->[op(x),[[[0,fact[1,2]]],[]]],eqcl)
end if;
fact:=fact[2..-1];
for f in fact do
   for i from 1 to nops(eqcl) do
      minusdisp:=qDispersion(f[1],eqcl[i,1],x,'var'=q);
      plusdisp:=qDispersion(eqcl[i,1],f[1],x,'var'=q);
      if type(minusdisp,numeric) then 
         eqcl[i,2]:=eqcl[i,2]+f[2]; # they are qshift equivalent
         if f[2]<0 then
            eqcl[i,3,2]:=[op(eqcl[i,3,2]),[-minusdisp,f[2]]];
         else
            eqcl[i,3,1]:=[op(eqcl[i,3,1]),[-minusdisp,f[2]]];            
         end if;
         break;
      elif type(plusdisp,numeric)  then
         eqcl[i,2]:=eqcl[i,2]+f[2]; # they are qshift equivalent
         if f[2]<0 then
            eqcl[i,3,2]:=[op(eqcl[i,3,2]),[plusdisp,f[2]]];
         else
            eqcl[i,3,1]:=[op(eqcl[i,3,1]),[plusdisp,f[2]]];            
         end if;
         break;
      end if;
      if i=nops(eqcl) then
         if f[2]<0 then
            eqcl:=[op(eqcl),[op(f),[[],[[0,f[2]]]]]] # build a new qshift equivalence class
         else
            eqcl:=[op(eqcl),[op(f),[[[0,f[2]]],[]]]] # build a new qshift equivalence class
         end if;
      end if;      
   end do;
end do;
eqcl
end proc:


qLocalTypes := proc(term::algebraic,x::algebraic,q::algebraic,{certificate::boolean:=false,ltype::identical(0,infinity,points,all):='all'})
local num,den,qterm,nzeroes,dzeroes,dz,nz,ltp,ltinf,ltzero,a,b;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
if certificate then
   qterm:=normal(term);
else
   qterm:=qCertificate(term,x,q);
end if;
num:=collect(numer(qterm),x);
den:=collect(denom(qterm),x);

# local type at infinity
if ltype='all' or ltype=infinity then
   ltinf:=[lcoeff(num,x)/lcoeff(den,x),-(degree(num,x)-degree(den,x))];
   if ltype=infinity then
      return ltinf
   end if;
end if;

# local type at zero
if ltype='all' or ltype=0 then
   ltzero:=[tcoeff(num,x)/tcoeff(den,x),ldegree(num,x)-ldegree(den,x)];   
   if ltype=0 then
      return ltzero
   end if;
end if;

# local type in point
if ltype='all' or ltype='points' then
   nzeroes:=remove(not has,remove(patmatch,qFactors(num,x,q),[a::anything*x,b::anything]),x);
   dzeroes:=remove(not has,remove(patmatch,qFactors(den,x,q),[a::anything*x,b::anything]),x);
   ltp:={};
   for nz in nzeroes do
      for dz in dzeroes do
         if type(qDispersion(nz[1],dz[1],x,'var'=q),numeric) or type(qDispersion(dz[1],nz[1],x,'var'=q),numeric) then # they are q-shift equivalent
            ltp:=ltp union {[nz[1],nz[2]-dz[2]]};  
            nzeroes:=remove(y->y=nz,nzeroes);
            dzeroes:=remove(y->y=dz,dzeroes);
            break;
         end if;
      end do;
   end do;
   for nz in nzeroes do
      ltp:=ltp union {[nz[1]/lcoeff(nz[1],x),nz[2]]};
   end do;
   for dz in dzeroes do
      ltp:=ltp union {[dz[1]/lcoeff(dz[1],x),-dz[2]]};
   end do;
   if ltype='points' then
      return ltp
   end if;
end if;

[ltinf,ltzero,ltp]
end proc:


qLocalTypesCandidates := proc(RE::equation,Fx::function,q::algebraic,{ltype::identical(0,infinity,points,all):='all',mhypersol::posint:=1,output::identical(all,relevant):='relevant'})
local a,F,x,T,np,n,lt,i,j,sol,coe,lcoe,tcoe,lzeroes,tzeroes,lz,tz,allzeroes,p,lsingul,tsingul,rightstart,leftstart,pl,pr,Bleft,
Bright,uu,vv,rightRE,leftRE,num,den,epsilon,l,qDis1,qDis2;
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
n:=qOrder(RE,Fx,var=q);
F:=op(0,Fx);
x:=op(1,Fx);
coe:=qgetcoeffs(RE,F(x),q);
tcoe:=coe[1];
lcoe:=coe[-1];

lt:=[{},{},{}];

# local type at infinity
if ltype=infinity or ltype='all' then
   np:=qNewtonPolygon(RE,F(x),q,'eq','eqvar'=T,'v'=((a,x)->-degree(a,x)),_options[-2]);
   userinfo(5,'qHypergeomSolveRE',`polynomials of the q-newton polygon (at infinity)`,print(np));
   for i from 1 to nops(np) do 
      if (output='relevant' and type(np[i][1]*mhypersol,integer)) or output='all' then
         sol:=[solve(np[i][2],T)];
         for j from 1 to nops(sol) do
            lt[1]:=lt[1] union {[sol[j],-np[i][1]*mhypersol]}  
         end do;
      end if;
   end do;
   if ltype=infinity then 
      return lt[1]
   end if;
end if;

# local type at zero
if ltype=0 or ltype='all' then
   np:=qNewtonPolygon(RE,F(x),q,'eq','eqvar'=T,'v'=((a,x)->ldegree(a,x)),_options[-2]);
   userinfo(4,'qHypergeomSolveRE',`polynomials of the q-newton polygon (at 0)`,print(np));
   for i from 1 to nops(np) do
      if (output='relevant' and type(np[i][1]*mhypersol,integer)) or output='all' then
         sol:=[solve(np[i][2],T)];
         for j from 1 to nops(sol) do
            lt[2]:=lt[2] union {[sol[j],-np[i][1]*mhypersol]}
         end do;
      end if;
   end do;
   if ltype=0 then 
      return lt[2]
   end if;
end if;

# local type in point 
if ltype='points' or ltype='all' then
   lzeroes:=remove(not has,remove(patmatch,qFactors(qshift(lcoe,[x$(n-mhypersol)],1/q),x,q,_options),[a::anything*x,b::anything]),x);
   tzeroes:=remove(not has,remove(patmatch,qFactors(tcoe,x,q,_options),[a::anything*x,b::anything]),x);

   for lz in lzeroes do
      for tz in tzeroes do
         qDis1:=qDispersion(lz[1],tz[1],x,'var'=q);
         qDis2:=qDispersion(tz[1],lz[1],x,'var'=q);
         if type(qDis1,numeric) or type(qDis2,numeric) then # they are q-shift equivalent
            if mhypersol>1 then
               if irem(qDis1,mhypersol)=0 or irem(qDis2,mhypersol)=0 then # they are m-q-shift equivalent
                  lt[3]:=lt[3] union {[lz[1]/lcoeff(lz[1],x),[-lz[2],tz[2]]]};  
                  lzeroes:=remove(y->y=lz,lzeroes);
                  tzeroes:=remove(y->y=tz,tzeroes);
                  break;
               end if;
            else
               lt[3]:=lt[3] union {[lz[1]/lcoeff(lz[1],x),[-lz[2],tz[2]]]};  
               lzeroes:=remove(y->y=lz,lzeroes);
               tzeroes:=remove(y->y=tz,tzeroes);
               break;
            end if;
         end if;
      end do;
   end do;
   for lz in lzeroes do
      lt[3]:=lt[3] union {[lz[1]/lcoeff(lz[1],x),[-lz[2],0]]};
   end do;
   for tz in tzeroes do
      lt[3]:=lt[3] union {[tz[1]/lcoeff(tz[1],x),[0,tz[2]]]};
   end do;
   if ltype='points' then
      return lt[3]
   end if;
end if;

lt
end proc:


# AUXILIARY PROCEDURES


qCompare:=proc(term1,term2,{var::symbol:='q',limit::posint:=3,info::boolean:=false,params::set:={}})
local n,vars,cp,values,terms,check;
vars:=(indets(term1,symbol) union indets(term2,symbol)) minus {var,op(params)};
vars:=[op(vars)];
n:=nops(vars);
cp:=combinat[cartprod]([seq([seq(k,k=0..limit)],j=1..n)]);
check:=true;
while not cp[finished] do
  values:=cp[nextvalue]();
  terms:=subs(sum=add,seq(vars[j]=op(j,values),j=1..n),[term1,term2,term1-term2]);
  terms:=map(qsimpcomb@eval@expand,terms);
  if op(-1,terms)<>0 then
    check:=false;
  end if; 
  if info then
    print([seq(vars[j]=op(j,values),j=1..n)],terms);
  end if;
end do;
check
end proc:


# INITIALIZATION OF TABLES OF Q-FUNCTIONS, Q-DERIVATIVES AND Q-SHIFTS


addqdiff := proc(f::symbol,impl::procedure)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
qdiffs[f]:=impl;
qfunctions:=qfunctions union {f};
userinfo(1,'qFPS',`q-derivative rule for`,f,`has been added`)
end proc:


addqshift := proc(f::symbol,impl::procedure)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
qshifts[f]:=impl;
qfunctions:=qfunctions union {f};
userinfo(1,'qFPS',`q-shift rule for`,f,`has been added`)
end proc:


addqrec := proc(f::symbol,n::posint,impl::procedure)
option `Copyright 2006-2011 Torsten Sprenger, University of Kassel`;
qrecs[f,n]:=impl;
userinfo(1,'qFPS',`q-recurrence equation for`,f,`has been added`)
end proc:

qfunctions := {}:

qdiffs:=table();
addqdiff('qpower1',`qdiff/qpower1`):
addqdiff('qpower2',`qdiff/qpower2`):
addqdiff('qpower',`qdiff/qpower`):
addqdiff('qpochhammer',`qdiff/qpochhammer`):
addqdiff('qphihypergeom',`qdiff/qphihypergeom`):
addqdiff('qexp',`qdiff/qexp`):
addqdiff('qExp',`qdiff/qExp`):
addqdiff('expq',`qdiff/expq`):
addqdiff('Expq',`qdiff/Expq`):
addqdiff('logq',`qdiff/logq`):
addqdiff('qsin',`qdiff/qsin`):
addqdiff('qSin',`qdiff/qSin`):
addqdiff('sinq',`qdiff/sinq`):
addqdiff('Sinq',`qdiff/Sinq`):
addqdiff('qcos',`qdiff/qcos`):
addqdiff('qCos',`qdiff/qCos`):
addqdiff('cosq',`qdiff/cosq`):
addqdiff('Cosq',`qdiff/Cosq`):
addqdiff('qBernstein',`qdiff/qBernstein`):
addqdiff('qLaguerre',`qdiff/qLaguerre`):
addqdiff('LittleqLaguerre',`qdiff/LittleqLaguerre`):
addqdiff('BigqLaguerre',`qdiff/BigqLaguerre`):
addqdiff('LittleqJacobi',`qdiff/LittleqJacobi`):
addqdiff('LittleqLegendre',`qdiff/LittleqLegendre`):
addqdiff('BigqJacobi',`qdiff/BigqJacobi`):
addqdiff('BigqLegendre',`qdiff/BigqLegendre`):
addqdiff('qMeixner',`qdiff/qMeixner`):
addqdiff('QuantumqKrawtchouk',`qdiff/QuantumqKrawtchouk`):
addqdiff('qKrawtchouk',`qdiff/qKrawtchouk`):
addqdiff('AffineqKrawtchouk',`qdiff/AffineqKrawtchouk`):
addqdiff('DiscreteqHermiteI',`qdiff/DiscreteqHermiteI`):
addqdiff('DiscreteqHermiteII',`qdiff/DiscreteqHermiteII`):
addqdiff('AlSalamCarlitzI',`qdiff/AlSalamCarlitzI`):
addqdiff('AlSalamCarlitzII',`qdiff/AlSalamCarlitzII`):
addqdiff('qCharlier',`qdiff/qCharlier`):
addqdiff('AlternativeqCharlier',`qdiff/AlternativeqCharlier`):
addqdiff('qHahn',`qdiff/qHahn`):
addqdiff('StieltjesWigert',`qdiff/StieltjesWigert`):

qshifts:=table();
addqshift('qpower1',`qshift/qpower1`):
addqshift('qpower2',`qshift/qpower2`):
addqshift('qpower',`qshift/qpower`):
addqshift('qpochhammer',`qshift/qpochhammer`):
addqshift('qphihypergeom',`qshift/qphihypergeom`):
addqshift('qexp',`qshift/qexp`):
addqshift('qExp',`qshift/qExp`):
addqshift('expq',`qshift/expq`):
addqshift('Expq',`qshift/Expq`):
addqshift('logq',`qshift/logq`):
addqshift('qsin',`qshift/qsin`):
addqshift('qSin',`qshift/qSin`):
addqshift('sinq',`qshift/sinq`):
addqshift('Sinq',`qshift/Sinq`):
addqshift('qcos',`qshift/qcos`):
addqshift('qCos',`qshift/qCos`):
addqshift('cosq',`qshift/cosq`):
addqshift('Cosq',`qshift/Cosq`):
addqshift('qBernstein',`qshift/qBernstein`):
addqshift('qLaguerre',`qshift/qLaguerre`):
addqshift('LittleqLaguerre',`qshift/LittleqLaguerre`):
addqshift('BigqLaguerre',`qshift/BigqLaguerre`):
addqshift('LittleqJacobi',`qshift/LittleqJacobi`):
addqshift('LittleqLegendre',`qshift/LittleqLegendre`):
addqshift('BigqJacobi',`qshift/BigqJacobi`):
addqshift('BigqLegendre',`qshift/BigqLegendre`):
addqshift('qMeixner',`qshift/qMeixner`):
addqshift('QuantumqKrawtchouk',`qshift/QuantumqKrawtchouk`):
addqshift('qKrawtchouk',`qshift/qKrawtchouk`):
addqshift('AffineqKrawtchouk',`qshift/AffineqKrawtchouk`):
addqshift('DiscreteqHermiteI',`qshift/DiscreteqHermiteI`):
addqshift('DiscreteqHermiteII',`qshift/DiscreteqHermiteII`):
addqshift('AlSalamCarlitzI',`qshift/AlSalamCarlitzI`):
addqshift('AlSalamCarlitzII',`qshift/AlSalamCarlitzII`):
addqshift('qCharlier',`qshift/qCharlier`):
addqshift('AlternativeqCharlier',`qshift/AlternativeqCharlier`):
addqshift('qHahn',`qshift/qHahn`):
addqshift('StieltjesWigert',`qshift/StieltjesWigert`):

qrecs:=table();
addqrec('qLaguerre',4,(n,a,x,q)->(q-q^n*q^a)/(q^n-1)*qLaguerre(n-2,a,x,q)+(q^(n-1)*(q^(a+1)*(1+q^(n-1)*x)+q)-1-q)/(q^n-1)*qLaguerre(n-1,a,x,q)):
addqrec('LittleqLaguerre',4,(n,a,x,q)->(q^(n-1)*(1-a*q^n)+a*q^(n-1)*(1-q^(n-1))-x)/q^(n-1)/(1-a*q^n)*LittleqLaguerre(n-1,a,x,q)-a*(1-q^(n-1))/(1-a*q^n)*LittleqLaguerre(n-2,a,x,q));
addqrec('BigqLaguerre',5,(n,a,b,x,q)->(q*x-b*q^n*q-a*b*q^n*q+a*(q^n)^2*b-a*q^n*q+a*(q^n)^2*b*q)*BigqLaguerre(n-1,a,b,x,q)/(q*(-1+b*q^n)*(a*q^n-1))+a*b*q^n*(q-q^n)*BigqLaguerre(n-2,a,b,x,q)/(q*(-1+b*q^n)*(a*q^n-1)));
addqrec('LittleqJacobi',5,(n,a,b,x,q)->(q-(q^n)^2*a*b)*(-q^2*x+x*(q^n)^2*q^2*a*b-(q^n)^2*q*a*b-(q^n)^2*a*q+q*q^n+q^n*a*q-(q^n)^2*a-(q^n)^2*a*b-x*a^2*b^2*(q^n)^4+x*(q^n)^2*a*b+(q^n)^3*a*b+(q^n)^3*a^2*b)*LittleqJacobi(n-1,a,b,x,q)/(q^n*(-1+q^n*a)*(a*b*q^n-1)*(-(q^n)^2*a*b+q^2))+a*(q-q^n)*(q-q^n*b)*(-1+(q^n)^2*a*b)*LittleqJacobi(n-2,a,b,x,q)/((-1+q^n*a)*(a*b*q^n-1)*(-(q^n)^2*a*b+q^2)));
addqrec('LittleqLegendre',3,(n,x,q)->(q^n+1)*(-q^n+q)*LittleqLegendre(n-2,x,q)/((q^n-1)*(q^n+q))+(q-(q^n)^2)*(q*q^n*x+q*x-2*q^n+q^n*x+x*(q^n)^2)*LittleqLegendre(n-1,x,q)/((q^n-1)*(q^n+q)*q^n));
addqrec('BigqJacobi',6,(n,a,b,c,x,q)->(q-(q^n)^2*b*a)*(-(q^n)^2*c*b*a*q^2+(q^n)^2*b*a*x*q^2+q^n*b*a*q^2-(q^n)^2*c*a*q^2+q^2*q^n*a*c-q^2*(q^n)^2*b*a-(q^n)^2*a^2*b*q^2+q^n*a*q^2+q^n*c*q^2-x*q^2-q*(q^n)^2*b*a*c-q*(q^n)^2*b*a-q*(q^n)^2*a^2*b-q*(q^n)^2*a*c+(q^n)^3*a^2*b^2*q+q*(q^n)^3*a^2*b*c+(q^n)^3*a^2*q*b+(q^n)^3*a*b*c*q+(q^n)^2*b*a*x-(q^n)^4*b^2*a^2*x)*BigqJacobi(n-1,a,b,c,x,q)/(q*(q^n*a-1)*(-1+q^n*b*a)*(-(q^n)^2*b*a+q^2)*(q^n*c-1))+q^n*a*(-q^n+q)*(q-q^n*b)*((q^n)^2*b*a-1)*(c*q-q^n*b*a)*BigqJacobi(n-2,a,b,c,x,q)/(q*(q^n*a-1)*(-1+q^n*b*a)*(-(q^n)^2*b*a+q^2)*(q^n*c-1)));
addqrec('BigqLegendre',4,(n,c,x,q)->(q-(q^n)^2)*(-(q^n)^2*c*q^2+(q^n)^2*x*q^2+q^n*q^2-(q^n)^2*c*q^2+q^2*q^n*c-q^2*(q^n)^2-(q^n)^2*q^2+q^n*q^2+q^n*c*q^2-x*q^2-q*(q^n)^2*c-q*(q^n)^2-q*(q^n)^2-q*(q^n)^2*c+(q^n)^3*q+q*(q^n)^3*c+(q^n)^3*q+(q^n)^3*c*q+(q^n)^2*x-(q^n)^4*x)*BigqLegendre(n-1,c,x,q)/(q*(q^n-1)*(-1+q^n)*(-(q^n)^2+q^2)*(q^n*c-1))+q^n*(-q^n+q)*(q-q^n)*((q^n)^2-1)*(c*q-q^n)*BigqLegendre(n-2,c,x,q)/(q*(q^n-1)*(-1+q^n)*(-(q^n)^2+q^2)*(q^n*c-1)));
addqrec('qMeixner',5,(n,a,b,x,q)->(q-q^n)*(q*b+q^n)*qMeixner(n-2,a,b,x,q)/(q*b*(-1+a*q^n))+((q^n)^2*x-q*b+b*a*q^n*q-q^2*b-q^n*q+b*q^n*q)*qMeixner(n-1,a,b,x,q)/(q*b*(-1+a*q^n))):
addqrec('QuantumqKrawtchouk',5,(n,p,N,x,q)->-q^N*(q^n-q)*(p*q^n-q)*QuantumqKrawtchouk(n-2,p,N,x,q)/(q^N*q-q^n)+(q^N*p*(q^n)^2*x+q^N*q-q^N*q*q^n+q^2*q^N-q^n-q^n*p*q*q^N)*QuantumqKrawtchouk(n-1,p,N,x,q)/(q^N*q-q^n)):
addqrec('qKrawtchouk',5,(n,p,N,x,q)->-(q^n)^2*p*(q^n-q)*(q+(q^n)^2*p)*(q^N*q^n*p+q)*qKrawtchouk(n-2,p,N,x,q)/(q*((q^n)^2*p+q^3)*(p*q^n+q)*(q^N*q-q^n))+(q^2+(q^n)^2*p)*(q^N*x*(q^n)^4*p^2-(q^n)^3*p^2*q^N*q+q*(q^n)^3*p-(q^n)^2*p*q^N*q^2-q^N*p*(q^n)^2*q^3-q*(q^n)^2*p+p*(q^n)^2*q*q^N*x-q^2*(q^n)^2*p+q^N*p*(q^n)^2*x*q^3+q^n*p*q^N*q^3-q^n*q^3+q^N*x*q^4)*qKrawtchouk(n-1,p,N,x,q)/(q*((q^n)^2*p+q^3)*(p*q^n+q)*(q^N*q-q^n))):
addqrec('AffineqKrawtchouk',5,(n,p,N,x,q)->p*q^n*(q^n-q)*AffineqKrawtchouk(n-2,p,N,x,q)/(q*(-1+p*q^n)*(q^N*q-q^n))+(-q*(q^n)^2*p+q^n*q^2*p*q^N+q^n*p*q-q^N*x*q^2+q^n*q-(q^n)^2*p)*AffineqKrawtchouk(n-1,p,N,x,q)/(q*(-1+p*q^n)*(q^N*q-q^n))):
addqrec('DiscreteqHermiteI',3,(n,x,q)->-q^n*(-q^n+q)*DiscreteqHermiteI(n-2,x,q)/q^3+x*DiscreteqHermiteI(n-1,x,q));
addqrec('DiscreteqHermiteII',3,(n,x,q)->x*DiscreteqHermiteII(n-1,x,q)-q^2*(q-q^n)*DiscreteqHermiteII(n-2,x,q)/(q^n)^2);
addqrec('AlSalamCarlitzI',4,(n,a,x,q)->(-q^n-q^n*a+x*q)*AlSalamCarlitzI(n-1,a,x,q)/q+a*q^n*(q-q^n)*AlSalamCarlitzI(n-2,a,x,q)/q^3);
addqrec('AlSalamCarlitzII',4,(n,a,x,q)->(-q-a*q+x*q^n)*AlSalamCarlitzII(n-1,a,x,q)/q^n-a*q^2*(q-q^n)*AlSalamCarlitzII(n-2,a,x,q)/(q^n)^2);
addqrec('qCharlier',4,(n,a,x,q)->-((q^n)^2*x-a*q-a*q^2-q^n*q+q^n*a*q)*qCharlier(n-1,a,x,q)/(a*q)-(q-q^n)*(a*q+q^n)*qCharlier(n-2,a,x,q)/(a*q));
addqrec('AlternativeqCharlier',4,(n,a,x,q)->-((q^n)^2*a+q^2)*(x*q^4+x*a*(q^n)^2*q^3-q^n*q^3-(q^n)^2*a*q^2+x*(q^n)^2*a*q-(q^n)^2*a*q+q*(q^n)^3*a+x*(q^n)^4*a^2)*AlternativeqCharlier(n-1,a,x,q)/(q*q^n*(a*q^n+q)*((q^n)^2*a+q^3))-q^n*a*(q-q^n)*(q+(q^n)^2*a)*AlternativeqCharlier(n-2,a,x,q)/((a*q^n+q)*((q^n)^2*a+q^3)));
addqrec('qHahn',6,(n,a,b,N,x,q)->a*q^n*(q-q^n)*(q-b*q^n)*(-1+a*(q^n)^2*b)*(a*q^n*b*q^N-1)*qHahn(n-2,a,b,N,x,q)/((-1+a*q^n)*(-1+a*b*q^n)*(-a*(q^n)^2*b+q^2)*(q*q^N-q^n))-(q-a*(q^n)^2*b)*(x*a*b*(q^n)^2*q^2*q^N+q^2*a*q^n*q^N+a*q^n*b*q^2*q^N-a^2*(q^n)^2*b*q^2*q^N-q^2*x*q^N-a*(q^n)^2*b*q^2*q^N-a*(q^n)^2*b*q+a*q^n*q-(q^n)^2*a*b*q*q^N+q*q^n-q*a^2*(q^n)^2*b*q^N-a*(q^n)^2*q+(q^n)^3*a^2*b*q*q^N+a^2*b^2*(q^n)^3*q*q^N-a*(q^n)^2-x*a^2*b^2*(q^n)^4*q^N-a*(q^n)^2*b+x*a*b*(q^n)^2*q^N+(q^n)^3*a^2*b+(q^n)^3*a*b)*qHahn(n-1,a,b,N,x,q)/((-1+a*q^n)*(-1+a*b*q^n)*(-a*(q^n)^2*b+q^2)*(q*q^N-q^n)));
addqrec('StieltjesWigert',3,(n,x,q)->(-q-q^2+q^n*q+(q^n)^2*x)*StieltjesWigert(n-1,x,q)/(q*(q^n-1))+q*StieltjesWigert(n-2,x,q)/(q^n-1));
end module:

infolevel[qFPS]:=1:

protect('qFPS','q'):

try
   if parse(convert(kernelopts(version),string)[7..8])<11 then
      WARNING("qFPS requires Maple version 11 or higher");
   end if;
catch:
end try:
