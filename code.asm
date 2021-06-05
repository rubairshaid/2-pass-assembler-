COPY       START     1000 
FIRST      STL       RETADR                   
CLOOP      JSUB      RDREC
           LDA       LENGTH              
           COMP      ZERO
           JEQ       ENDFIL
           JSUB      RDREC
           J         CLOOP
ENDFIL     LDA       =C'EOF'
           LDA       =X'F1'        
           STA       BUFFER
           LDA       THREE
           STA       LENGTH
           JSUB      RDREC
           LDL       RETADR
           RSUB   
           LTORG   
.        LITERAL POOL
EOF        BYTE      C'EOF'
THREE      WORD      3
ZERO       WORD      0
RETADR     RESW      1
LENGTH     RESW      1
BUFFER     RESB      4096
.      SUBROUTINE TO READ RECORD INTO BUFFER
RDREC      LDX       ZERO
           LDA       ZERO
           LDA       =X'F2'          
RLOOP      TD        INPUT
           JEQ       RLOOP
           RD        INPUT
           COMP      ZERO
           JEQ       EXIT
           STCH      BUFFER,X
           TIX       LENGTH
           JLT       RLOOP
EXIT       STX       LENGTH
INPUT      BYTE      X'F1'
           RSUB  
           RSUB  
           END       FIRST