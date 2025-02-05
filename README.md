# conser-vision

## Introduction

Conser-vision is a project aimed at leveraging machine learning and computer vision to aid conservation efforts. By using camera trap images, we can automate the identification of animal species, allowing conservationists to focus more on protecting wildlife and less on data processing.

## Project Overview

This project is based on the [Conservision Practice Area](https://www.drivendata.org/competitions/87/competition-image-classification-wildlife-conservation/) challenge on DrivenData. The goal is to identify animal species in a real-world dataset of wildlife images from [Tai National Park](https://en.wikipedia.org/wiki/Ta%C3%AF_National_Park) in Côte d'Ivoire.

## Steps to Train the Model

We will go through the following steps to train a PyTorch model that can identify the species of animals in given images:

1. Set up your environment
2. Download the data
3. Explore the data
4. Split into train and evaluation sets
5. Build the model
6. Training
7. Evaluation
8. Create submission

## Dataset

The dataset includes images collected from Tai National Park in Africa. It contains labeled images of various animal species, as well as some images labeled as "blank" where no animal was detected.

## Getting Started

### Prerequisites

- Basic familiarity with Python
- Basic understanding of deep learning concepts

### Setting Up the Environment

We recommend using conda to manage environments. Once you have [conda installed](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html), you can create a new environment with:

```sh
conda create -n conserviz python=3.8
conda activate conserviz
pip install pandas matplotlib Pillow tqdm scikit-learn torch torchvision
```

### Downloading the Data

Download the competition data from the [Data Download](https://www.drivendata.org/competitions/87/competition-image-classification-wildlife-conservation/data/) page. Unzip the archive into a location of your choice.

## Literature Survey

We have included a literature survey to provide background information and context for the project.
