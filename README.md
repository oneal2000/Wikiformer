# Wikiformer

**Source code of AAAI 2024 long paper:** 

**Wikiformer: Pre-training with Structured Information of Wikipedia for Ad-hoc Retrieval**

[Paper Link](https://arxiv.org/pdf/2312.10661.pdf)

[GitHub Link](https://github.com/oneal2000/Wikiformer)





<p align="center">
  <img src="https://github.com/oneal2000/Wikiformer/blob/main/pics/logo.png" width="50%" height="auto" />
</p>




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

Our proposed method Wikiformer aims to customize a retrieval model for any corpus with structured information without manual supervision. Our advantages include:

- There is no need for existing queries or manual annotations
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





## Methodology

**This section briefly introduces our method; for more details, please refer to our paper.** [Paper Link](https://arxiv.org/pdf/2312.10661.pdf)

### SRR Task

The SRR task is inspired by an important IR problem: document re-ranking. In general, the goal of the document re-ranking task is to sort a series of documents that are highly related to the query, and then select the ones that are most related to the query. According to the characteristics of this task, we aim to design a self-supervised learning task to select the most relevant document from a series of documents with similar contents. In the SRR task, we make full use of the hierarchical heading (multi-level title) structure of Wikipedia to achieve the above objective. Every article on Wikipedia is organized by the hierarchical heading (multi-level title) structure, the subtitle corresponding to a certain section tends to be the representative words or summarization of the text. Besides, different subsections of the same section share similar semantics. As a result, through this structure, we can obtain a series of texts that are highly similar but slightly different in content and generate the query through the multi-level titles as shown in the following Figure:



![](https://github.com/oneal2000/Wikiformer/blob/main/pics/SRR.png)



To be specific, we modeled each Wikipedia article into a tree structure namely Wiki Structure Tree (WST)  based on the hierarchical heading structure. It can be defined as: 



WST = <D, R>, where $D$ is a finite set containing $n$ nodes and $R$ is the root node of $ WST$. Each node in $D$ consists of two parts: the subtitle and its corresponding content. The root node $R$ contains the main title and the abstract of this article. Starting from the root node $R$, recursively take all the corresponding lower-level sections as its child nodes until every section in this article is added to the $WST$. 



After building $WST$, we use a contrastive sampling strategy to construct pseudo-query-document pairs based on the tree. For a non-leaf node $F$ in the $WST$, we add all its child nodes to the set $S$. A node $d_i$ is randomly selected from $S$. Traversing from the root node to node $d_i$, all the titles on the path are put together to form a query $q$. This process is shown in Figure \ref{fig:sep_query}. The content of the node $d_i$ is defined as $d^+$, and the content of the other nodes in $S$ is defined as $d^-$. After this contrastive sampling, we use contrastive learning to train the model based on the above data



### RWI Task

RWI task is inspired by an IR axiom which assumes that the user’s query is the representative words extracted from the relevant documents. According to the Wikipedia structure, we regard the subtitle of each section as representative words, and then we sample pseudo-query-document pair via a simple strategy based on the hierarchical heading (multi-level title) structure, as shown in the following figure.



Specifically, pseudo-query-document pairs are organized as follows: for each Wikipedia article, we first model it as the $WST$ structure. Then we add all nodes of $WST$ except the root node to the set $S$. A node $d_i$ is randomly selected from $S$, and we define the depth of this node in $WST$ as $n$. Traversing from the root node to node $d_i$, all the titles on the path are put together to form a query $q^+$. The content of the node $d_i$ is defined as $D$. For the negative queries, we randomly select $n-1$ nodes from $S$, and concatenate the main title and subtitles of the selected nodes to define it as $q^-$. After this contrastive sampling, we use contrastive learning to train the model based on the above data

![](https://github.com/oneal2000/Wikiformer/blob/main/pics/RWI.png)

### ATI Task

In the ATI task, we utilize the abstract and the inner structure of Wikipedia. The abstract (the first section) of Wikipedia is regarded as the summarization of the whole article. Compared with other sections of the same article, the abstract is more likely to meet the user’s information needs when the query is the title. Therefore, we extract the title from the Wikipedia article as the query (denoted as $q$). Then the abstract of the same article is regarded as a positive document (denoted as $d^+$). For the negative ones, we use the other sections of the same article (denoted as $d^-$). After this contrastive sampling, we use contrastive learning to train the model based on the above data

### LTM Task

After pre-training with RWI, ATI, and SRR tasks, Wikiformer acquires the ability to measure the relevance between a short text (query) and a long text. This can help the model better handle the vast majority of ad-hoc retrieval tasks. However, there are also scenarios involving "long queries", such as legal case retrieval and document-to-document search. In these scenarios, the model is required to match the relevance between two long texts. Fortunately, with the structured information of Wikipedia, especially hyperlinks, we can build a series of informative pseudo-long query-document pairs. To be specific, we utilize the See Also section of Wikipedia which consists of hyperlinks that link to the other articles related to or comparable to this article. The See Also section is mainly written manually, based on the judgment and common sense of the authors and editors. Thus, we can obtain a series of reliable web pages that are highly related to the content of this page.

To this end, we designed the Long Texts Matching (LTM) task to encourage the Wikiformer to learn the relevance matching ability between two long documents. Initially, we transformed the complete Wikipedia corpus into a graph structure by leveraging the interconnections provided by the 'See Also' links. This graph is designated as the See Also Graph (SAG). Each hyperlink in the See Also section can be formally represented as $(v_i, v_j)$, which means that $v_j$ appears in the See Also section of $v_i$. Consequently, $SAG$ can be defined as a \textit{directed graph}: $SAG = (V, E)$, where $E$ is the above-mentioned set of ordered pairs $(v_i, v_j)$ and $V$ is a set of Wikipedia articles. The order of an edge indicates the direction of hyperlinks. After building $SAG$, we use a contrastive sampling strategy based on the graph. For each node in $SAG$, we define its content as query $D$ and define all its adjacent nodes as positive documents $d^+$. We randomly select other documents as $d^-$. After this contrastive sampling, we use contrastive learning to train the model based on the above data

![](https://github.com/oneal2000/Wikiformer/blob/main/pics/SAG.png)



## Experiment Results

| Model Type         | Model Name | MS MARCO MRR@10 (Zero-shot) | MS MARCO MRR@100 (Zero-shot) | TREC DL 2019 N@10 (Zero-shot) | TREC DL 2019 N@100 (Zero-shot) | MS MARCO MRR@10 (Fine-tuned) | MS MARCO MRR@100 (Fine-tuned) | TREC DL 2019 N@10 (Fine-tuned) | TREC DL 2019 N@100 (Fine-tuned) |
| ------------------ | ---------- | --------------------------- | ---------------------------- | ----------------------------- | ------------------------------ | ---------------------------- | ----------------------------- | ------------------------------ | :-----------------------------: |
| Traditional Models | BM25       | 0.2656                      | 0.2767                       | 0.5315                        | 0.4996                         | 0.2656                       | 0.2767                        | 0.5315                         |             0.4996              |
|                    | QL         | 0.2143                      | 0.2268                       | 0.5234                        | 0.4983                         | 0.2143                       | 0.2268                        | 0.5234                         |             0.4983              |
| Neural IR Models   | KNRM       | NA                          | NA                           | NA                            | NA                             | 0.1526                       | 0.1685                        | 0.3071                         |             0.4591              |
|                    | Conv-KNRM  | NA                          | NA                           | NA                            | NA                             | 0.1554                       | 0.1792                        | 0.3112                         |             0.4762              |
| Pre-trained Models | BERT       | 0.1684                      | 0.1811                       | 0.3407                        | 0.4316                         | 0.3826                       | 0.3881                        | 0.6540                         |             0.5325              |
|                    | PROP_WIKI  | 0.2205                      | 0.2321                       | 0.4712                        | 0.4709                         | 0.3866                       | 0.3922                        | 0.6399                         |             0.5311              |
|                    | PROP_MS    | 0.2585                      | 0.2696                       | 0.5203                        | 0.4810                         | 0.3930                       | 0.3980                        | 0.6425                         |             0.5318              |
|                    | Webformer  | 0.1664                      | 0.1756                       | 0.3758                        | 0.4550                         | 0.3984                       | 0.4036                        | 0.6479                         |             0.5335              |
|                    | HARP       | 0.2372                      | 0.2465                       | 0.5244                        | 0.4721                         | 0.3961                       | 0.4012                        | 0.6562                         |             0.5337              |
|                    | ARES       | 0.2736                      | 0.2851                       | 0.5736                        | 0.4752                         | 0.3995                       | 0.4041                        | 0.6505                         |             0.5353              |
| Our Approach       | Wikiformer | **0.2844**                  | **0.2911**                   | **0.5907**                    | **0.5143**                     | **0.4085**                   | **0.4136**                    | **0.6587**                     |           **0.5392**            |



## Usage

### Requirements

```
python>=3.9
torch>=1.6.0
transformers>=4.0.0
datasets>=1.1.3
tqdm>=4.65.0 
```



### Pre-training Data

For **Wikipedia**, download [the Wikidump](https://dumps.wikimedia.org/enwiki/) and reformat the text with [`WikiExtractor.py`](https://github.com/attardi/wikiextractor)

Demo data is included in this repository at `wikiformer/data/demo_data`



### Source Code for Each Task

#### SRR Task

`wikiformer/code/SRR`



##### Step1: Run `gen_data.sh` to reformat the Wikipedia articles:

```
python ./gen_data.py \
--input_folder ../../data/demo_data \
--output_path ./output.json \
--log_path ./log.txt
```



Output format: json

Example of a line:

```json
{
	"title": "Foreign relations of Azerbaijan",
	"docid": "1087",
	"section_list": [{
		"subtitle": "Diplomatic relations.",
		"level": 2,
		"merged_title": ["Foreign relations of Azerbaijan", "Diplomatic relations."],
		"text": "As of 2019, Azerbaijan maintains diplomatic relations with 182 United Nations member states, the State of Palestine and the Holy See. Azerbaijan does not have diplomatic relations with the following countries: Azerbaijan also maintains good relations with the European Union, in the framework of its Eastern European Neighbourhood Policy (\"See Azerbaijan and the European Union\")."
	}, {
		"subtitle": "International organizations.",
		"level": 2,
		"merged_title": ["Foreign relations of Azerbaijan", "International organizations."],
		"text": "AsDB BSEC CE CIS EAPC EBRD ECE ECO ESCAP FAO GUAM IAEA IBRD ICAO ICRM IDA IDB IFAD IFC IFRCS ILO IMF IMO Interpol IOC, IOM ISO (correspondent) ITU ITUC OAS (observer) OIC OPCW OSCE PFP United Nations UNCTAD UNESCO UNIDO UPU WCO WFTU WHO WIPO WMO WToO WTrO(observer)"
	}, {
		"subtitle": "Disputes.",
		"level": 2,
		"merged_title": ["Foreign relations of Azerbaijan", "Disputes."],
		"text": ""
	}, {
		"subtitle": "Nagorno-Karabakh/Azerbaijan.",
		"level": 3,
		"merged_title": ["Foreign relations of Azerbaijan", "Disputes.", "Nagorno-Karabakh/Azerbaijan."],
		"text": "The frozen conflict over currently largely Armenian-populated region of Nagorno-Karabakh within the Republic of Azerbaijan began when in 1988 the Armenian majority of Nagorno-Karabakh demanded autonomy with demonstrations and persecutions against ethnic Azeris following in Armenia. This led to anti-Armenian rioting in Azerbaijan, with Azerbaijani militias beginning their effort to expel Armenians from the enclave. In 1992 a war broke out and pogroms of Armenians and Azeris forced both groups to flee their homes. In 1994, a Russian-brokered ceasefire ended the war but more than 1 million ethnic Armenians and Azeris are still not able to return home. The conflict over Nagorno-Karabakh remains unresolved despite negotiations, that are ongoing since 1992 under the aegis of the Minsk Group of the OSCE, to resolve the conflict peacefully."
	}, {
		"subtitle": "Caviar diplomacy.",
		"level": 3,
		"merged_title": ["Foreign relations of Azerbaijan", "Disputes.", "Caviar diplomacy."],
		"text": "The European Stability Initiative (ESI) has revealed in a report from 2012 with the title \"Caviar diplomacy: How Azerbaijan silenced the Council of Europe\", that since Azerbaijan's entry into the Council of Europe, each year 30 to 40 deputies are invited to Azerbaijan and generously paid with expensive gifts, including caviar (worth up to 1.400 euro), silk carpets, gold, silver and large amounts of money. In return they become lobbyists for Azerbaijan. This practice has been widely referred to as \"Caviar diplomacy\". ESI also published a report on 2013 Presidential elections in Azerbaijan titled \"Disgraced: Azerbaijan and the end of election monitoring as we know it\". The report revealed the ties between Azerbaijani government and the members of certain observation missions who praised the elections. Azerbaijan's \"Caviar diplomacy\" at 2013 presidential elections sparked a major international scandal, as the reports of two authoritative organizations Parliamentary Assembly of the Council of Europe/European Parliament and OSCE/ODIHR completely contradicted one another in their assessments of elections. Non-governmental anti-corruption organization Transparency International has regularly judged Azerbaijan to be one of the most corrupt countries in the world and has also criticized Azerbaijan for the \"Caviar diplomacy\". At June 2016 the public prosecutor of Milan has accused the former leader of the (Christian) Union of the center and of the European People's Party of the Parliamentary Assembly of the Council of Europe Luca Volonte of accepting large bribes from representatives of the Azerbaijani government. Two people with high-level experience of the Council of Europe's parliamentary assembly (Pace) have told the Guardian they believe its members have been offered bribes for votes by Azerbaijan. Former Azerbaijani diplomat, Arif Mammadov, alleged that a member of Azerbaijan's delegation at the Council of Europe had \u20ac30m (\u00a325m) to spend on lobbying its institutions, including the Council of Europe assembly. PACE ratified the terms of reference of an independent external investigation body to carry out a detailed independent inquiry into the allegations of corruption at the council involving Azerbaijan."
	}, {
		"subtitle": "ESISC report.",
		"level": 4,
		"merged_title": ["Foreign relations of Azerbaijan", "Disputes.", "Caviar diplomacy.", "ESISC report."],
		"text": "On 6 March 2017, ESISC (European Strategic Intelligence and Security Center) published a scandalous report called \"The Armenian Connection\" where it veraciously attacked human rights NGOs and research organisations criticising human rights violations and corruption in Azerbaijan, Turkey, and Russia. ESISC in that report asserted that \"Caviar diplomacy\" report elaborated by ESI aimed to create climate of suspicion based on slander to form a network of MPs that would engage in a political war against Azerbaijan. In the Second Chapter of the report called \"The Armenian Connection: \u00abMr X\u00bb, Nils Mui\u017enieks, Council of Europe Commissioner for Human Rights\" that was published on 18 April 2017 ESISC asserted that the network composed of European PMs, Armenian officials and some NGOs: Human Rights Watch, Amnesty International, \"Human Rights House Foundation\", \"Open Dialog\", European Stability Initiative, and Helsinki Committee for Human Rights, was financed by the Soros Foundation. According to ESISC the key figure of the network since 2012 has been Nils Mui\u017enieks, Commissioner for Human Rights of the Council of Europe and the network has served to the interests of George Soros and the Republic of Armenia. \"The report is written in the worst traditions of authoritarian propaganda, makes absurd claims, and is clearly aimed at deflecting the wave of criticism against cover-up of unethical lobbying and corruption in PACE and demands for change in the Assembly\", said Freedom Files Analytical Centre. According Robert Coalson (Radio Free Europe), ESISC is a part of Baku's lobbying efforts to extend to the use of front think tanks to shift public opinion. European Stability Initiative said that \"ESISC report is full of lies (such as claiming that German PACE member Strasser holds pro-Armenian views and citing as evidence that he went to Yerevan in 2015 to commemorate the Armenian genocide, when Strasser has never in his life been to independent Armenia)\"."
	}],
	"max_level": 4,
	"abstract": ["", "The Republic of Azerbaijan is a member of the United Nations, the Non-Aligned Movement, the Organization for Security and Cooperation in Europe, NATO's Partnership for Peace, the Euro-Atlantic Partnership Council, the World Health Organization, the European Bank for Reconstruction and Development; the Council of Europe, CFE Treaty, the Community of Democracies; the International Monetary Fund; and the World Bank.", "The major trends in the foreign relations of the Republic of Azerbaijan toward both global and regional powers active in Caucasus area. External variables are categorized depending on their original nature into two groups: global and regional. The former category includes global players such as Moscow and Washington, while the latter category rival regional players, namely Ankara and Tehran. Azerbaijan has formal involvement with senior ex-U.S. government officials including James Baker and Henry Kissinger, as they serve on the Honorary Council of Advisors of the U.S.-Azerbaijan Chamber of Commerce (USACC). USACC is co-chaired by Tim Cejka, President of ExxonMobil and Reza Vaziri, President of R.V. Investment Group and Chairman of the Anglo Asian Mining Plc (LSE Ticker: AAZ)."],
	"error": 0
}
```



##### Step2: Contrastive Sampling Strategy

`Wikiformer/code/SRR/contrastive_sampling.py`



#### RWI Task

`wikiformer/code/RWI`

##### Run `gen_data.sh` to reformat the Wikipedia articles:

```
python ./gen_data.py \
--input_folder ../../data/demo_data \
--output_path ./output.json \
--log_path ./log.txt
```



#### ATI Task

`wikiformer/code/ATI`

#### LTM Task

`wikiformer/code/LTM`





## Links to Related Works

**PROP\_MS**  adopts the Representative Words Prediction (ROP) task to learn relevance matching from the pseudo-query-document pairs. It is pre-trained on MS MARCO. [Link to Code](https://github.com/Albert-Ma/PROP)

**PROP\_WIKI** adopts the same pre-training task as PROP\_MS. The only difference is that PROP\_WIKI is pre-trained on Wikipedia. [Link to Code](https://github.com/Albert-Ma/PROP)

**HARP** utilizes hyperlinks and anchor texts to generate pseudo-query-document pairs and achieves state-of-the-art performance on ad-hoc retrieval. [Link to Code](https://github.com/zhengyima/anchors)

**ARES** is a pre-trained language model with Axiomatic Regularization for ad hoc Search. [Link to Code](https://github.com/xuanyuan14/ARES)

**Webformer** is a pre-trained language model based on large-scale web pages and their DOM (Document Object Model) tree structures. [Link to Code](https://github.com/xrr233/Webformer)

