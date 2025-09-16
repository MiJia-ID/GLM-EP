import numpy as np

train_path = '/home/mijia/EGPDI/data/DNA-573_Train_Extracted.fasta'
one_hot_path = '/home/mijia/EGPDI/data/one-hot/'

def one_hot_encode(sequence):
    # create one-hot
    amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
    aa_to_int = {aa: i for i, aa in enumerate(amino_acids)}
    encoded_sequence = np.zeros((len(sequence), len(amino_acids)), dtype=np.float32)
    for i, aa in enumerate(sequence):
        encoded_sequence[i, aa_to_int[aa]] = 1
    return encoded_sequence

ID_list = []
seq_list = []
with open(train_path, "r") as f:
    lines = f.readlines()
for line in lines:
    line = line.strip()  # 移除行末尾的换行符和空白字符
    if line and line[0] == ">":  # 检查行是否非空且是否为ID行
        ID_list.append(line[1:])  # 去除ID行的大于号
    elif line:  # 检查行是否非空
        seq_list.append("".join(list(line)))  # 将非空行的序列加入序列列表中
        encoded_proteins = [one_hot_encode(sequence) for sequence in seq_list]

for i, encoded in enumerate(encoded_proteins):
    filename = f"{ID_list[i]}.npy"  # 使用序列ID作为文件名
    np.save(filename, encoded)
    print(f"Saved {filename}")