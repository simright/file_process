*INCLUDE
includes/nodes.k
*ELEMENT_SHELL
$    eid     pid      n1      n2      n3      n4
      11       1     101     102     103     104
*INCLUDE
includes/elements.k
*MAT_ELASTIC
$      mid        ro         e        pr        da        db         k
         1           2000000.0       0.3
*SECTION_SHELL
$    secid    elform      shrf       nip     propt   qr/irid     icomp
      1001
$       t1       t2        t3        t4      nloc     marea      idof    edgset
      0.05      0.05      0.05      0.05
