# Wikiformer
**Source code of AAAI 2024 long paper:** 

**Wikiformer: Pre-training with Structured Information of Wikipedia for Ad-hoc Retrieval**

[Paper Link](https://arxiv.org/pdf/2312.10661.pdf)

![](https://github.com/oneal2000/Wikiformer/blob/main/pics/logo.png)



```
@misc{su2023wikiformer,
      title={Wikiformer: Pre-training with Structured Information of Wikipedia for Ad-hoc Retrieval}, 
      author={Weihang Su and Qingyao Ai and Xiangsheng Li and Jia Chen and Yiqun Liu and Xiaolong Wu and Shengluan Hou},
      year={2023},
      eprint={2312.10661},
      archivePrefix={arXiv},
      primaryClass={cs.IR}
}
```



## Introduction

### Overview
Imagine a scenario: we need to design a retrieval system for an entirely new **Corpus**. This Corpus contains structured information, such as multi-level titles, topics, abstracts, and references between documents.

In the design process, we will face the following challenges:
- Inability to predict user queries
- Lack of Query-Passage relevance annotations
- Difficulty in training a retrieval model specific to this Corpus without queries



### Our Solution
Our proposed method Wikiformer aims to customize a retrieval model for any corpus with structured information, without the need for manual supervision. Our advantages include:
- No need for existing queries or manual annotations
- Achieves SOTA performance
- Broad applicability for many formats, including academic paper Corpus, Web Corpus, and Markdown.md, XML, etc.
- Intuitive and simple method, easy to get started with, low-cost



Our methodology is effective for any Corpus that shares a structural resemblance with Wikipedia. 



![](https://github.com/oneal2000/Wikiformer/blob/main/pics/structure2.png)



Including:

Academic Paper Corpus (LaTeX Format)

```latex
\documentclass{article}
\usepackage{hyperref}

\title{Example Academic Paper}
\author{Author Name}

\begin{document}
\maketitle

\section{Introduction}
Introduction text goes here. Referencing Section \ref{sec:methodology}.

\section{Methodology}
\label{sec:methodology}
Detailed methodology description. As discussed in \cite{relatedwork}.

\subsection{Subsection of Methodology}
Further details about the methodology.

\bibliographystyle{plain}
\bibliography{references}
\end{document}
```

Web Corpus (HTML Format)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Example Web Page</title>
</head>
<body>
    <h1>Main Title</h1>
    <p>Welcome to our web corpus example.</p>
    
    <h2>Section 1</h2>
    <p>Details about section 1.</p>
    
    <h2 id="section2">Section 2</h2>
    <p>Details about section 2. .</p>
</body>
</html>
```

Markdown Format

```markdown
# Main Title
Welcome to our Markdown example.

## Section 1
Details about section 1. 

## Section 2
Details about section 2. 
```

XML Format

```xml
<document>
    <title>Main Document Title</title>
    <section id="sec1">
        <title>Section 1</title>
        <content>Content of Section 1. See also <reference target="sec2"/></content>
    </section>
    <section id="sec2">
        <title>Section 2</title>
        <content>Content of Section 2. Referring back to <reference target="sec1"/></content>
    </section>
</document>
```



## Citation

If you find our work useful, please cite our paper :)



```
@misc{su2023wikiformer,
      title={Wikiformer: Pre-training with Structured Information of Wikipedia for Ad-hoc Retrieval}, 
      author={Weihang Su and Qingyao Ai and Xiangsheng Li and Jia Chen and Yiqun Liu and Xiaolong Wu and Shengluan Hou},
      year={2023},
      eprint={2312.10661},
      archivePrefix={arXiv},
      primaryClass={cs.IR}
}
```



## Links to Related Works

**PROP\_MS**  adopts the Representative Words Prediction (ROP) task to learn relevance matching from the pseudo-query-document pairs. It is pre-trained on MS MARCO. [Link to Code](https://github.com/Albert-Ma/PROP)

**PROP\_WIKI** adopts the same pre-training task as PROP\_MS. The only difference is that PROP\_WIKI is pre-trained on Wikipedia. [Link to Code](https://github.com/Albert-Ma/PROP)

**HARP** utilizes hyperlinks and anchor texts to generate pseudo-query-document pairs and achieves state-of-the-art performance on ad-hoc retrieval. [Link to Code](https://github.com/zhengyima/anchors)

**ARES** is a pre-trained language model with Axiomatic Regularization for ad hoc Search. [Link to Code](https://github.com/xuanyuan14/ARES)

**Webformer** is a pre-trained language model based on large-scale web pages and their DOM (Document Object Model) tree structures. [Link to Code](https://github.com/xrr233/Webformer)



## Methodology

### SRR Task

The SRR task is inspired by an important IR problem: document re-ranking. In general, the goal of the document re-ranking task is to sort a series of documents that are highly related to the query, and then select the ones that are most related to the query. According to the characteristics of this task, we aim to design a self-supervised learning task to select the most relevant document from a series of documents with similar contents. In the SRR task, we make full use of the hierarchical heading (multi-level title) structure of Wikipedia to achieve the above objective. Every article on Wikipedia is organized by the hierarchical heading (multi-level title) structure, the subtitle corresponding to a certain section tends to be the representative words or summarization of the text. Besides, different subsections of the same section share similar semantics. As a result, through this structure, we can obtain a series of texts that are highly similar but slightly different in content and generate the query through the multi-level titles as shown in the following Figure.



To be specific, we modeled each Wikipedia article into a tree structure namely Wiki Structure Tree (WST)  based on the hierarchical heading structure. It can be defined as: 



WST = <D, R>, where $D$ is a finite set containing $n$ nodes and $R$ is the root node of $ WST$. Each node in $D$ consists of two parts: the subtitle and its corresponding content. The root node $R$ contains the main title and the abstract of this article. Starting from the root node $R$, recursively take all the corresponding lower-level sections as its child nodes until every section in this article is added to the $WST$. 



After building $WST$, we use a contrastive sampling strategy to construct pseudo query-document pairs based on the tree. For a non-leaf node $F$ in the $WST$, we add all its child nodes to the set $S$. A node $d_i$ is randomly selected from $S$. Traversing from the root node to node $d_i$, all the titles on the path are put together to form a query $q$. This process is shown in Figure \ref{fig:sep_query}. The content of the node $d_i$ is defined as $d^+$, and the content of the other nodes in $S$ is defined as $d^-$. 



![](https://github.com/oneal2000/Wikiformer/blob/main/pics/SRR.png)



We use a Transformer based PLM to compute the relevance score of a pseudo query-document pair:

$$Input = [CLS] query [SEP] document [SEP] $$

$$score(query,document) = MLP(Transformer(Input) ) $$

where $Transformer(Input)$ is the vector representation of the "[CLS]" token. $MLP(\cdot)$ is a multi-layer perceptron that projects the [CLS] vector to a relevance score. For the loss function, we use the Softmax Cross Entropy Loss to optimize the Transformer model, which is defined as:




   $$\mathcal{L}_{SRR} = -\log_{}{    \frac{exp(score(q,d^+))}{exp(score(q,d^+))+\sum_{d\in S} exp(score(q,d))}}$$



where $q$, and $d^+$ are defined above and $S$ is the set of all negative passages generated from $WST$.



### RWI Task

![](https://github.com/oneal2000/Wikiformer/blob/main/pics/RWI.png)

### ATI Task



### LTM Task

![](https://github.com/oneal2000/Wikiformer/blob/main/pics/SAG.png)











