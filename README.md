# Question Answering via Sentence Composition (QASC)

QASC is a question-answering dataset with a focus on sentence composition. It consists of 9,980 8-way multiple-choice questions about grade school science (8,134 train, 926 dev, 920 test), and comes with a corpus of 17M sentences. This repository shows how to download the QASC dataset and corpora. It also provides two sample baselines that can be used to produce the predictions needed by the [QASC leaderboard](https://leaderboard.allenai.org/qasc)

* **Key Links**
	* **QASC Dataset**: [http://data.allenai.org/downloads/qasc/qasc_dataset.tar.gz](http://data.allenai.org/downloads/qasc/qasc_dataset.tar.gz)
	* **QASC Corpus**:  [http://data.allenai.org/downloads/qasc/qasc_corpus.tar.gz](http://data.allenai.org/downloads/qasc/qasc_corpus.tar.gz)
	* **Leaderboard**:  [https://leaderboard.allenai.org/qasc](https://leaderboard.allenai.org/qasc)
	* **Arxiv Paper**: [TBD](TBD)


Table of Contents
===============

* [Downloading Data](#downloading-data)
    * [Dataset](#dataset)
    * [Corpus](#Corpus)
    * [Models](#models)
* [Setup Environment](#setup-environment)
* [Evaluating Models](#evaluating-models)
* [Training Models](#training-models)


## Downloading Data

### Dataset
Download and unzip the dataset in `data/QASC_Dataset` folder
```
mkdir -p data
wget -o http://data.allenai.org/downloads/qasc/qasc_dataset.tar.gz
tar xvfz qasc_dataset.tar.gz  -C data/
rm qasc_dataset.tar.gz
```
### Corpus
Download and unzip the text corpus (17M sentences) in `data/QASC_Corpus` folder
```
mkdir -p data
wget -o http://data.allenai.org/downloads/qasc/qasc_corpus.tar.gz
tar xvfz qasc_corpus.tar.gz  -C data/
rm qasc_corpus.tar.gz
```


### Models
Download and unzip the baseline models in `data/QASC_Models` folder
```
mkdir -p data
wget -o http://data.allenai.org/downloads/qasc/qasc_models.tar.gz
tar xvfz qasc_models.tar.gz  -C data/
rm qasc_models.tar.gz
```


## Setup Environment
We currently use a [fork](https://github.com/OyvindTafjord/allennlp/tree/bert_exp1) of [AllenNLP](https://github.com/allenai/allennlp) by [Oyvind Tafjord](https://github.com/oyvindTafjord/) to train and evaluate our models. To use this repository, setup a __Python 3.6__ environment in venv or conda (to ensure a clean setup) and then run 

```
pip install -r requirements.txt
```

We intend to release models and scripts that directly use [AllenNLP](https://github.com/allenai/allennlp)/[Transformers library by HuggingFace](https://github.com/huggingface/transformers) in the near future. 

## Evaluating Models
We release two sample models that predict answer choices based on (1) no knowledge and (2) single-step retrieval knowledge. 

### No Knowledge Baseline
This model can be run directly against the test set to produce predictions using AllenNLP's predict command. 
```
python -m allennlp.run predict \
     --include-package qasc \
     --predictor multiple-choice-qa-json \
     --output-file data/nokb_predictions.jsonl \
     data/QASC_Models/bertlc_nokb/model.tar.gz  \
     data/QASC_Dataset/test.jsonl
```

To convert the predictions into the CSV format expected by the leaderboard, use [jq](https://stedolan.github.io/jq/), a command-line tool to parse JSON files. 
```
jq -r "[.id,.answer]|@csv" data/nokb_predictions.jsonl > data/nokb_predictions.csv
```

### Single Step Baseline
To run the single-step retrieval baseline, we provide the train, dev and test files with the retrieved context [here](http://data.allenai.org/downloads/qasc/qasc_dataset_1step.tar.gz). 

To download the data:
```
wget -o http://data.allenai.org/downloads/qasc/qasc_dataset_1step.tar.gz
tar xvfz qasc_dataset_1step.tar.gz  -C data/
rm qasc_dataset_1step.tar.gz
```

To produce predictions:
```
python -m allennlp.run predict \
     --include-package qasc \
     --predictor multiple-choice-qa-json \
     --output-file data/1step_predictions.jsonl \
     data/QASC_Models/bertlc_1step/model.tar.gz  \
     data/QASC_Dataset_1Step/test.jsonl

jq -r "[.id,.answer]|@csv" data/1step_predictions.jsonl > data/1step_predictions.csv
```



