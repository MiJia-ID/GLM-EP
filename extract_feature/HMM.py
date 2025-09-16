import os
import numpy as np
from Bio import SeqIO


def save_hmm_features(fasta_file, domtblout_lines, output_dir, n_features=30):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 解析FASTA文件，获取序列ID和长度
    for record in SeqIO.parse(fasta_file, "fasta"):
        seq_id = record.id  # 获取序列ID
        sequence_length = len(record.seq)  # 获取序列长度
        print(seq_id)
        print(sequence_length)
        # 初始化特征矩阵
        features = np.zeros((sequence_length, n_features))

        # 解析 HMM 比对输出并填充特征矩阵
        features = parse_domtblout_to_features(domtblout_lines, sequence_length, n_features)

        # 保存特征矩阵到文件，文件名为序列ID
        output_file = os.path.join(output_dir, f"{seq_id}.npy")
        np.save(output_file, features)

        print(f"Saved: {output_file} with shape {features.shape}")


def parse_domtblout_to_features(domtblout_file, sequence_length, n_features=30):
    features = np.zeros((sequence_length, n_features))  # 初始化 L x N 特征矩阵

    with open(domtblout_file) as f:
        for line in f:
            if line.startswith("#"):  # 跳过注释行
                continue
            fields = line.strip().split()
            start_pos = int(fields[17]) - 1  # 比对开始位置（转换为0基索引）
            end_pos = int(fields[18])  # 比对结束位置

            # 确保 end_pos 不超出 sequence_length
            end_pos = min(end_pos, sequence_length)

            score = float(fields[15])  # 比对得分
            c_e_value = float(fields[13])  # E值
            i_e_value = float(fields[14])
            bias = float(fields[16])
            coverage = float(fields[21])  # 假设这是比对覆盖率
            tlen = float(fields[2])
            qlen = float(fields[6])
            e_value = float(fields[7])

            emission_prob = np.random.rand(20)  # 这里假设发射概率是20维的向量
            insert_prob = np.random.rand()  # 假设插入概率
            delete_prob = np.random.rand()  # 假设删除概率

            for i in range(start_pos, end_pos):
                features[i, 0] = score  # 比对得分
                features[i, 1] = c_e_value  # E值
                features[i, 2] = coverage  # 比对覆盖率
                features[i, 3:23] = emission_prob  # 发射概率（20维）
                features[i, 23] = insert_prob  # 插入概率
                features[i, 24] = delete_prob  # 删除概率
                features[i, 25] = i_e_value
                features[i, 26] = bias
                features[i, 27] = tlen
                features[i, 28] = qlen
                features[i, 29] = e_value

    return features


# 示例输入数据
fasta_file = "/home/mijia/EGPDI/data/DNA-573_Train_Extracted.fasta"  # 替换为你的FASTA文件路径
domtblout_file = "/home/mijia/app/hmmer/databases/output.domtblout"
output_dir = "/home/mijia/EGPDI/data/hmm"  # 替换为你希望保存输出文件的目录

save_hmm_features(fasta_file, domtblout_file, output_dir)
