# EasyDesign
## Table of contents

- [Introduction](#Introduction)
- [Design online](#design-online)
- [Installation](#Installation)
  - [Dependencies](#Dependencies)
  - [Setting up a conda environment](#setting-up-a-conda-environment)
  - [Install and run](#install-and-run)
- [Getting Started](#getting-started)
- [Data clean](#data-clean)
- [Citation](#Citation)

## Introduction 

Enhanced crRNA design system with Deep learning for Cas12a-mediated Diagnostics, termed EasyDesign. EasyDesign predicts sgRNAs based on deep learning techniques and its design scheme support recombinase polymerase amplification (RPA).

## Design online

You can perform online design through our [website](https://crispr.zhejianglab.com/), eliminating the need for 
installation steps. Additionally, for the website operation video, you can click [here](https://crispr.zhejianglab.com/help).

## Installation

### Dependencies

- Python == 3.8
- Fastapi >= 0.78.0
- Uvicorn >= 0.18.1
- Pandas >= 1.0.0
- Protobuf <= 3.20.3
- Python-multipart >= 0.0.6
- NumPy >= 1.16.0, < 1.19.0
- SciPy == 1.4.1
- TensorFlow == 2.3.0

For alignment features, EasyDesign also requires a path to an executable of [MAFFT](https://mafft.cbrc.jp/alignment/software/).

### Setting up a conda environment

_Note: This section is optional, but it can be helpful for Python beginners to effectively resolve dependency issues across different projects._

[conda](https://conda.io/en/latest/) and [Miniconda](https://conda.io/en/latest/miniconda.html) are popular solutions for managing dependencies. Here, we will focus on demonstrating the usage of Miniconda on Linux. 

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Once you have conda, you can [create](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) an environment for EasyDesign with Python 3.8:

```bash
conda create -n easyDesign python=3.8
```

Then, you can activate the `EasyDesign` environment:

```bash
conda activate easyDesign
```

After the environment is created and activated, you can install EasyDesign as described below. You will need to activate the environment each time you use EasyDesign.

### Install and run
- Download the source code.
```bash
git clone https://github.com/scRNA-Compt/EasyDesign.git
cd EasyDesign
```
- When use conda as package management(choose conda or pip).
```bash
conda env create -f environment.yml
```
- When use pip that you can do this.
```shell
pip install -e .
```
- Start the service.
```bash
python ./web/server.py
```

## Getting Started

For quick start of EasyDesign, we provide an example dataset provided the examples/ folder, which includes one DNA sequence. Additionally, we recommend providing a URL that allows downloading the FASTA file as input.

You can use tools like curl, request, or similar ones for making the API call. Now open another terminal session  and the demonstration of using curl is as follows.

_Note: If the fasta_url download link is not available, you can customize the fasta_url as long as it can be downloaded, or set the fasta_url to empty and provide the absolute path for example.fasta in source folder for fasta_file parameter._

```
curl -X POST -H "Content-Type: application/json" -d '{
    "fasta_url": "https://drive.usercontent.google.com/download?id=19gtOYesjCd2x2LyYTPIveOT41dzzkmXZ",  
    "fasta_file": "", 
    "ai_model": "cas12a",
    "gl":21, 
    "amplification_mode": "RPA",
    "bestntargets": 5,
    "job_id": "UGEqrihrEl",
    "upload_result_addr": "http://localhost:8001",
    "reversed": 0
}' http://127.0.0.1:8001/postadapt
```

Explanation of parameters:

- fasta_url: url that can use to download a FASTA file, choose fasta_url or fasta_file as input
- fasta_file: fasta_file path, choose fasta_url or fasta_file as input
- ai_model, gl, amplification_mode: default parameters, no need for modification, convenient for future expansion
- bestntargets: number of results displayed at the end
- job_id: distinguish different tasks
- upload_result_addr: the url for further processing the generated results
- reversed: 1 reversed, 0 no

The output is:

- Location: /data/easyDesign/output/{job_id}/result/result.0.tsv
- The main output information includes: guide-expected-activities, guide-target-sequences, guide-target-sequence-positions...

Once finished, you can stop the server with `Ctrl-C` at any time

# Data clean

- For output data part
  - The default output directory is `/data/easyDesign`, you can clean data using a data cleaning script `rm -rf /data/easyDesign/output/{job_id}`. You can also delete all the output by removing the default folder.
- For source folder
  - `rm -rf /your_source_folder/EasyDesign`

## Citation

We now have a paper you can cite our paper as: