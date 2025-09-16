# GLM-EP: An Equivariant Graph Neural Network and Protein Language Model Integrated Framework for Predicting Essential Proteins in Bacteriophages


## Abstract
Accurately identifying essential proteins in bacteriophages is crucial for understanding their mechanisms of replication and survival, as well as for advancing phage therapy and other antimicrobial strategies. However, current methods still fall short in modeling the synergistic features between protein sequences and structural information. To address this gap, we propose an integrated prediction framework named GLM-EP, which combines protein language models with equivariant graph neural networks. By integrating semantic features derived from protein sequences and structure-aware graph representations, GLM-EP enables comprehensive characterization of phage proteins and significantly improves the identification of essential proteins. Extensive experiments on multiple benchmark phage datasets demonstrate that GLM-EP substantially outperforms traditional sequence-based approaches and standalone deep learning models in metrics such as F1-score and AUROC. Ablation studies further validate the complementary roles and importance of the GCNII, EGNN, and gated multi-head attention modules in modeling complex protein features. Overall, GLM-EP serves as a powerful computational tool that not only facilitates functional genomics studies of bacteriophages but also provides novel methodological support for identifying therapeutic targets in the context of antibiotic resistance. The source code can be found at: https://github.com/MiJia-ID/GLM-EP.

<div align=center>
<img src="fig.1.jpg" width=75%>
</div>


## Preparation
### Environment Setup
```python 
   git clone https://github.com/MiJia-ID/GLM-EP.git
   conda env create -f uspdb_environment.yml
```
You also need to install the relative packages to run ESM2, ProtTrans and ESM3 protein language model. 

## Experimental Procedure
### Create Dataset
**Firstly**, you need to use AF3 to obtain the PDB files of proteins in the tran and test datasets. 

Then, run the script below to create node features (PSSM, SS, AF, One-hot encoding). The file is located in the scripts folder.
```python 
python3 data_io.py 
```

**Secondly** , run the script below to create node features(ESM2 embeddings and ProtTrans embeddings). The file can be found in feature folder.</br>

```python 
python3 ESM2_5120.py 
```
```python 
python3 ProtTrans.py 
```
We choose the esm2_t48_15B_UR50D() pre-trained model of ESM-2 which has the most parameters. More details about it can be found at: https://huggingface.co/facebook/esm2_t48_15B_UR50D   </br>
We also choose the prot_t5_xl_uniref50 pre-trained model of ProtTrans, which uses a masked language modeling(MLM). More details about it can be found at: https://huggingface.co/Rostlab/prot_t5_xl_uniref50    </br>

**Thirdly**, run the script below to create edge features. The file can be found in feature folder.
```python 
python3 create_edge.py 
```

### Model Training
Run the following script to train the model.
```python
python3 train_val_bestAUPR_predicted.py 
```

### Inference on Pretrained Model
Run the following script to test the model. Both test datasets, DNA_129_Test and DNA_181_Test , were included in the testing of the model.
```python
python3 test_129_final.py 
```
```python
python3 test_181_final.py 
```

