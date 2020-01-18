def get_fasta(input, output):
    with open(output, 'w') as op:
        with open(input, 'r') as fp:
            for (i, line) in enumerate(fp):
                if i > 0:
                    now = line.split(',')
                    now_str = ">" + now[1] + "\n" + now[2] + "\n"
                    op.write(now_str)


# get_fasta('./data/Malonylation/Human/HM_encoded.csv', './data/Malonylation/Human/HM.fasta')
# get_fasta('./data/Malonylation/Mice/MM_encoded.csv', './data/Malonylation/Mice/MM.fasta')