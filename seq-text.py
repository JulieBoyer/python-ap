import sys
import re
import argparse

    #Function for command line arguments 
def read_args():
    #Create arguments
    parser = argparse.ArgumentParser(description = 'Implementation of the snake game')
    #parser.add_argument('--help','-h', help ='usage: align.py [-h] [-m MATCH_SCORE] [-x MISMATCH_SCORE] [-i INDEL_SCORE] [--log-file LOG_FILE] [-v]')
    parser.add_argument('--match-score','-m',help='The score for a match of two bases', default = 1, type = int)
    parser.add_argument('--mismatch-score','-x',help='The score for a mismatch of two bases', default = -1, type = int)
    parser.add_argument('--indel-score','-i',help='The score for an insertion or a deletrion of two bases', default = -2 , type = int)
    parser.add_argument('--log-file', help='Path to a log file', default = None)
    parser.add_argument('--verbose', '-v', help = 'Verbose level', default = 0)
    return(parser.parse_args())


def Needleman_Wunsch_algo(seq,varseq, match_score, mismatch_score, index_score):
    # Creation of matrix
    n=len(seq)+1
    m=len(varseq)+1
    matrix = [[0 for k in range (m)] for j in range(n)]
    chemin = [[(0,0) for k in range (m)] for j in range(n)]
    operation = [[0 for k in range (m)] for j in range(n)]

    #Initialize matrix
    for j in range (m):
        matrix[0][j]=j*index_score
    for i in range (n):
        matrix[i][0]=i*index_score

    #Fill the matrix
    for i in range (1,n):
        for j in range(1,m):
            if seq[i-1]==seq[j-1]: 
                val_diag = matrix[i-1][j-1]+match_score
            else :
                val_diag = matrix[i-1][j-1]+mismatch_score
            val_haut = matrix[i-1][j]+index_score
            val_gauche = matrix[i][j-1]+index_score
            maxi = max (val_diag ,(max (val_gauche, val_haut)))
            if maxi == val_diag :
                matrix[i][j]=val_diag
                chemin[i][j]=(i-1,j-1)
                operation[i][j]=1
            elif maxi == val_haut :
                matrix[i][j]=val_haut
                chemin[i][j]=(i-1,j)
                operation[i][j]=2
            else :
                matrix[i][j]=val_gauche
                chemin[i][j]=(i,j-1)
                operation[i][j]=3
    return (matrix,chemin,operation)

def read_chemin(chemin,operation):
    indice =(0,0)
    list_op = []
    while indice[0]>0 and indice[1]>0:
        a,b=indice
        i,j=chemin[a,b]
        list_op.append(operation[a,b])
        indice = (i,j)
    return (operation)

def read_list(seq,varseq,operation):
    operation = operation[::-1]
    seq_new=''
    id_seq = 0
    varseq_new=''
    id_varseq = 0
    for x in liste :
        if x==1:
            seq_new=seq_new+seq[id_seq]
            id_seq=id_seq+1
            varseq_new=varseq_new+varseq[id_seq]
            id_varseq=id_varseq+1
        if x==2:
            seq_new=seq_new+seq[id_seq]
            id_seq=id_seq+1
            varseq_new=varseq_new+'_'
        else : 
            seq_new=seq_new+'_'
            varseq_new=varseq_new+varseq[id_seq]
            id_varseq=id_varseq+1


id_seq=''
id_var=''
seq=''
varseq=''
i=0
y=0
liste=[]
for line in sys.stdin :
    y=y+1
    line =line.rstrip()
    if not line.startswith(';'):
        if line.startswith('>'):
            if id_seq=='':
                id_seq=line[1:]
            elif id_var=='' :
                id_var=line[1:]
            else :
                #print(seq,varseq,i,y) #change with a function
                if i==0: 
                    liste.append(seq)
                    liste.append(varseq)
                seq=''
                varseq=''
                id_seq=line[1:]
                id_var=''
                i=i+1
        elif re.match('[GTCA]*$',line):
            if id_var=='':
                seq=seq+line
            else :
                varseq=varseq+line
        else :
            raise Exception("Wrong line '%s' at '%d'"%(line,y))
    #print(f'Processing Message from sys.stdin ****{line}*****')
#print(seq,varseq,i,y) 
print(liste)
args=read_args()
print(Needleman_Wunsch_algo(liste[0],liste[1],args.match_score,args.mismatch_score,args.indel_score))


