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



### Our methodology is effective for any Corpus that shares a structural resemblance with Wikipedia. 



![](https://github.com/oneal2000/Wikiformer/blob/main/pics/structure2.png)



### Including:


#### Academic Paper Corpus (LaTeX Format)

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

#### Web Corpus (HTML Format)

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

#### Markdown Format

```markdown
# Main Title
Welcome to our Markdown example.

## Section 1
Details about section 1. 

## Section 2
Details about section 2. 
```

#### XML Format

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

![](https://github.com/oneal2000/Wikiformer/blob/main/pics/srr.png)

### RWI Task

![](https://github.com/oneal2000/Wikiformer/blob/main/pics/RWI_f.png)

### ATI Task



### LTM Task

![](https://github.com/oneal2000/Wikiformer/blob/main/pics/SAG.png)











