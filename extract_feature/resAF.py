from pymol import cmd
import numpy as np
import os

# 加载PDB文件的路径
pdb_path = "/home/mijia/EGPDI/data/pdb_dir"
resAF_saved_path = "/home/mijia/EGPDI/data/resAF/"

def to_ascii(string):
    num = 0
    for char in string:
        num += ord(char)
    num = num / len(string)
    return num

# 提取氨基酸特征的函数
def extract_residue_features():
    # 获取所有残基的信息
    residues = cmd.get_model("all")

    # 创建一个字典来存储特征，以氨基酸编号为键
    residue_features = {}

    # 遍历所有原子，并按氨基酸编号分组
    for atom in residues.atom:
        resi_id = atom.chain + "_" + atom.resi  # 组合链和氨基酸编号作为唯一标识符
        if resi_id not in residue_features:
            residue_features[resi_id] = {
                "coords": [],
                "b_factors": [],
                "atom_names": [],
                "symbols": [],
                "residue_name": atom.resn
            }

        residue_features[resi_id]["coords"].append(atom.coord)
        residue_features[resi_id]["b_factors"].append(atom.b)
        residue_features[resi_id]["atom_names"].append(atom.name)
        residue_features[resi_id]["symbols"].append(atom.symbol)

    # 将原子级别的特征汇总为氨基酸级别的特征
    features = []
    for resi_id, data in residue_features.items():
        coords = np.mean(data["coords"], axis=0)  # 计算原子坐标的平均值
        avg_b_factor = np.mean(data["b_factors"])  # 计算平均B因子
        avg_atom_name = to_ascii("".join(data["atom_names"]))  # 所有原子名的ASCII平均值
        avg_symbol = to_ascii("".join(data["symbols"]))  # 所有原子符号的ASCII平均值

        # 创建氨基酸级别的特征向量
        residue_feature = [
            avg_atom_name,
            avg_symbol,
            coords[0],
            coords[1],
            coords[2],
            avg_b_factor,
            to_ascii(data["residue_name"])
        ]
        features.append(residue_feature)

    return np.array(features)

def main():
    pdb_files = [f for f in os.listdir(pdb_path) if f.endswith(".pdb")]

    for filename in pdb_files:
        full_path = os.path.join(pdb_path, filename)
        cmd.load(full_path)

        # 调用函数提取氨基酸特征
        residue_features = extract_residue_features()

        # 保存特征矩阵为 .npy 文件
        save_path = os.path.join(resAF_saved_path, f"{os.path.splitext(filename)[0]}_resAF.npy")
        np.save(save_path, residue_features)

        # 输出特征矩阵形状
        print(f"Features for {filename}:")
        print(residue_features.shape)

        # 删除当前加载的结构
        cmd.delete("all")

if __name__ == "__main__":
    main()
