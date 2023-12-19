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
	"title": "Amplitude modulation",
	"docid": "1140",
	"section_list": [{
		"subtitle": "Forms.",
		"level": 2,
		"merged_title": ["Amplitude modulation", "Forms."],
		"text": "In electronics and telecommunications, modulation means varying some aspect of a continuous wave carrier signal with an information-bearing modulation waveform, such as an audio signal which represents sound, or a video signal which represents images. In this sense, the carrier wave, which has a much higher frequency than the message signal, \"carries\" the information. At the receiving station, the message signal is extracted from the modulated carrier by demodulation. In amplitude modulation, the amplitude or \"strength\" of the carrier oscillations is varied. For example, in AM radio communication, a continuous wave radio-frequency signal (a sinusoidal carrier wave) has its amplitude modulated by an audio waveform before transmission. The audio waveform modifies the amplitude of the carrier wave and determines the \"envelope\" of the waveform. In the frequency domain, amplitude modulation produces a signal with power concentrated at the carrier frequency and two adjacent sidebands. Each sideband is equal in bandwidth to that of the modulating signal, and is a mirror image of the other. Standard AM is thus sometimes called \"double-sideband amplitude modulation\" (DSBAM). A disadvantage of all amplitude modulation techniques, not only standard AM, is that the receiver amplifies and detects noise and electromagnetic interference in equal proportion to the signal. Increasing the received signal-to-noise ratio, say, by a factor of 10 (a 10 decibel improvement), thus would require increasing the transmitter power by a factor of 10. This is in contrast to frequency modulation (FM) and digital radio where the effect of such noise following demodulation is strongly reduced so long as the received signal is well above the threshold for reception. For this reason AM broadcast is not favored for music and high fidelity broadcasting, but rather for voice communications and broadcasts (sports, news, talk radio etc.). AM is also inefficient in power usage; at least two-thirds of the power is concentrated in the carrier signal. The carrier signal contains none of the original information being transmitted (voice, video, data, etc.). However its presence provides a simple means of demodulation using envelope detection, providing a frequency and phase reference to extract the modulation from the sidebands. In some modulation systems based on AM, a lower transmitter power is required through partial or total elimination of the carrier component, however receivers for these signals are more complex because they must provide a precise carrier frequency reference signal (usually as shifted to the intermediate frequency) from a greatly reduced \"pilot\" carrier (in reduced-carrier transmission or DSB-RC) to use in the demodulation process. Even with the carrier totally eliminated in double-sideband suppressed-carrier transmission, carrier regeneration is possible using a Costas phase-locked loop. This does not work for single-sideband suppressed-carrier transmission (SSB-SC), leading to the characteristic \"Donald Duck\" sound from such receivers when slightly detuned. Single-sideband AM is nevertheless used widely in amateur radio and other voice communications because it has power and bandwidth efficiency (cutting the RF bandwidth in half compared to standard AM). On the other hand, in medium wave and short wave broadcasting, standard AM with the full carrier allows for reception using inexpensive receivers. The broadcaster absorbs the extra power cost to greatly increase potential audience. An additional function provided by the carrier in standard AM, but which is lost in either single or double-sideband suppressed-carrier transmission, is that it provides an amplitude reference. In the receiver, the automatic gain control (AGC) responds to the carrier so that the reproduced audio level stays in a fixed proportion to the original modulation. On the other hand, with suppressed-carrier transmissions there is \"no\" transmitted power during pauses in the modulation, so the AGC must respond to peaks of the transmitted power during peaks in the modulation. This typically involves a so-called \"fast attack, slow decay\" circuit which holds the AGC level for a second or more following such peaks, in between syllables or short pauses in the program. This is very acceptable for communications radios, where compression of the audio aids intelligibility. However it is absolutely undesired for music or normal broadcast programming, where a faithful reproduction of the original program, including its varying modulation levels, is expected. A simple form of amplitude modulation is the transmission of speech signals from the traditional analog telephone set using a common battery local loop. The direct current provided by the central office battery is a carrier with a frequency of 0 Hz, that is modulated by a microphone (\"transmitter\") in the telephone set according to the acoustic signal from the mouth of the speaker. The result is a varying amplitude direct current, whose AC-component is the speech signal extracted at the central office for transmission to another subscriber. A simple form of digital amplitude modulation which can be used for transmitting binary data is on-off keying, the simplest form of \"amplitude-shift keying\", in which ones and zeros are represented by the presence or absence of a carrier. On-off keying is likewise used by radio amateurs to transmit Morse code where it is known as continuous wave (CW) operation, even though the transmission is not strictly \"continuous.\" A more complex form of AM, quadrature amplitude modulation is now more commonly used with digital data, while making more efficient use of the available bandwidth."
	}, {
		"subtitle": "ITU designations.",
		"level": 3,
		"merged_title": ["Amplitude modulation", "Forms.", "ITU designations."],
		"text": "In 1982, the International Telecommunication Union (ITU) designated the types of amplitude modulation:"
	}, {
		"subtitle": "History.",
		"level": 2,
		"merged_title": ["Amplitude modulation", "History."],
		"text": "Although AM was used in a few crude experiments in multiplex telegraph and telephone transmission in the late 1800s, the practical development of amplitude modulation is synonymous with the development between 1900 and 1920 of \"radiotelephone\" transmission, that is, the effort to send sound (audio) by radio waves. The first radio transmitters, called spark gap transmitters, transmitted information by wireless telegraphy, using different length pulses of carrier wave to spell out text messages in Morse code. They couldn't transmit audio because the carrier consisted of strings of damped waves, pulses of radio waves that declined to zero, that sounded like a buzz in receivers. In effect they were already amplitude modulated."
	}, {
		"subtitle": "Continuous waves.",
		"level": 3,
		"merged_title": ["Amplitude modulation", "History.", "Continuous waves."],
		"text": "The first AM transmission was made by Canadian researcher Reginald Fessenden on 23 December 1900 using a spark gap transmitter with a specially designed high frequency 10\u00a0kHz interrupter, over a distance of 1 mile (1.6\u00a0km) at Cobb Island, Maryland, US. His first transmitted words were, \"Hello. One, two, three, four. Is it snowing where you are, Mr. Thiessen?\". The words were barely intelligible above the background buzz of the spark. Fessenden was a significant figure in the development of AM radio. He was one of the first researchers to realize, from experiments like the above, that the existing technology for producing radio waves, the spark transmitter, was not usable for amplitude modulation, and that a new kind of transmitter, one that produced sinusoidal \"continuous waves\", was needed. This was a radical idea at the time, because experts believed the impulsive spark was necessary to produce radio frequency waves, and Fessenden was ridiculed. He invented and helped develop one of the first continuous wave transmitters - the Alexanderson alternator, with which he made what is considered the first AM public entertainment broadcast on Christmas Eve, 1906. He also discovered the principle on which AM is based, heterodyning, and invented one of the first detectors able to rectify and receive AM, the electrolytic detector or \"liquid baretter\", in 1902. Other radio detectors invented for wireless telegraphy, such as the Fleming valve (1904) and the crystal detector (1906) also proved able to rectify AM signals, so the technological hurdle was generating AM waves; receiving them was not a problem."
	}, {
		"subtitle": "Early technologies.",
		"level": 3,
		"merged_title": ["Amplitude modulation", "History.", "Early technologies."],
		"text": "Early experiments in AM radio transmission, conducted by Fessenden, Valdemar Poulsen, Ernst Ruhmer, Quirino Majorana, Charles Herrold, and Lee de Forest, were hampered by the lack of a technology for amplification. The first practical continuous wave AM transmitters were based on either the huge, expensive Alexanderson alternator, developed 1906\u20131910, or versions of the Poulsen arc transmitter (arc converter), invented in 1903. The modifications necessary to transmit AM were clumsy and resulted in very low quality audio. Modulation was usually accomplished by a carbon microphone inserted directly in the antenna or ground wire; its varying resistance varied the current to the antenna. The limited power handling ability of the microphone severely limited the power of the first radiotelephones; many of the microphones were water-cooled."
	}, {
		"subtitle": "Vacuum tubes.",
		"level": 3,
		"merged_title": ["Amplitude modulation", "History.", "Vacuum tubes."],
		"text": "The 1912 discovery of the amplifying ability of the Audion tube, invented in 1906 by Lee de Forest, solved these problems. The vacuum tube feedback oscillator, invented in 1912 by Edwin Armstrong and Alexander Meissner, was a cheap source of continuous waves and could be easily modulated to make an AM transmitter. Modulation did not have to be done at the output but could be applied to the signal before the final amplifier tube, so the microphone or other audio source didn't have to modulate a high-power radio signal. Wartime research greatly advanced the art of AM modulation, and after the war the availability of cheap tubes sparked a great increase in the number of radio stations experimenting with AM transmission of news or music. The vacuum tube was responsible for the rise of AM broadcasting around 1920, the first electronic mass communication medium. Amplitude modulation was virtually the only type used for radio broadcasting until FM broadcasting began after World War II. At the same time as AM radio began, telephone companies such as AT&amp;T were developing the other large application for AM: sending multiple telephone calls through a single wire by modulating them on separate carrier frequencies, called \"frequency division multiplexing\"."
	}, {
		"subtitle": "Single-sideband.",
		"level": 3,
		"merged_title": ["Amplitude modulation", "History.", "Single-sideband."],
		"text": "John Renshaw Carson in 1915 did the first mathematical analysis of amplitude modulation, showing that a signal and carrier frequency combined in a nonlinear device would create two sidebands on either side of the carrier frequency, and passing the modulated signal through another nonlinear device would extract the original baseband signal. His analysis also showed only one sideband was necessary to transmit the audio signal, and Carson patented single-sideband modulation (SSB) on 1 December 1915. This more advanced variant of amplitude modulation was adopted by AT&amp;T for longwave transatlantic telephone service beginning 7 January 1927. After WW2 it was developed by the military for aircraft communication."
	}, {
		"subtitle": "Analysis.",
		"level": 2,
		"merged_title": ["Amplitude modulation", "Analysis."],
		"text": "The carrier wave (sine wave) of frequency \"fc\" and amplitude \"A\" is expressed by The message signal, such as an audio signal that is used for modulating the carrier, is \"m\"(\"t\"), and has a frequency \"fm\", much lower than \"fc\": where \"m\" is the amplitude sensitivity, \"M\" is the amplitude of modulation. If \"m\" &lt; 1, \"(1 + m(t)/A)\" is always positive for undermodulation. If \"m\" &gt; 1 then overmodulation occurs and reconstruction of message signal from the transmitted signal would lead in loss of original signal. Amplitude modulation results when the carrier \"c(t)\" is multiplied by the positive quantity \"(1 + m(t)/A)\": In this simple case \"m\" is identical to the modulation index, discussed below. With \"m\" = 0.5 the amplitude modulated signal \"y\"(\"t\") thus corresponds to the top graph (labelled \"50% Modulation\") in figure 4. Using prosthaphaeresis identities, \"y\"(\"t\") can be shown to be the sum of three sine waves: Therefore, the modulated signal has three components: the carrier wave \"c(t)\" which is unchanged in frequency, and two sidebands with frequencies slightly above and below the carrier frequency \"fc\"."
	}, {
		"subtitle": "Spectrum.",
		"level": 2,
		"merged_title": ["Amplitude modulation", "Spectrum."],
		"text": "A useful modulation signal \"m(t)\" is usually more complex than a single sine wave, as treated above. However, by the principle of Fourier decomposition, \"m(t)\" can be expressed as the sum of a set of sine waves of various frequencies, amplitudes, and phases. Carrying out the multiplication of \"1 + m(t)\" with \"c(t)\" as above, the result consists of a sum of sine waves. Again, the carrier \"c(t)\" is present unchanged, but each frequency component of \"m\" at \"fi\" has two sidebands at frequencies \"fc + fi\" and \"fc - fi\". The collection of the former frequencies above the carrier frequency is known as the upper sideband, and those below constitute the lower sideband. The modulation \"m(t)\" may be considered to consist of an equal mix of positive and negative frequency components, as shown in the top of figure 2. One can view the sidebands as that modulation \"m(t)\" having simply been shifted in frequency by \"fc\" as depicted at the bottom right of figure 2. The short-term spectrum of modulation, changing as it would for a human voice for instance, the frequency content (horizontal axis) may be plotted as a function of time (vertical axis), as in figure 3. It can again be seen that as the modulation frequency content varies, an upper sideband is generated according to those frequencies shifted \"above\" the carrier frequency, and the same content mirror-imaged in the lower sideband below the carrier frequency. At all times, the carrier itself remains constant, and of greater power than the total sideband power."
	}, {
		"subtitle": "Power and spectrum efficiency.",
		"level": 2,
		"merged_title": ["Amplitude modulation", "Power and spectrum efficiency."],
		"text": "The RF bandwidth of an AM transmission (refer to figure 2, but only considering positive frequencies) is twice the bandwidth of the modulating (or \"baseband\") signal, since the upper and lower sidebands around the carrier frequency each have a bandwidth as wide as the highest modulating frequency. Although the bandwidth of an AM signal is narrower than one using frequency modulation (FM), it is twice as wide as single-sideband techniques; it thus may be viewed as spectrally inefficient. Within a frequency band, only half as many transmissions (or \"channels\") can thus be accommodated. For this reason analog television employs a variant of single-sideband (known as vestigial sideband, somewhat of a compromise in terms of bandwidth) in order to reduce the required channel spacing. Another improvement over standard AM is obtained through reduction or suppression of the carrier component of the modulated spectrum. In figure 2 this is the spike in between the sidebands; even with full (100%) sine wave modulation, the power in the carrier component is twice that in the sidebands, yet it carries no unique information. Thus there is a great advantage in efficiency in reducing or totally suppressing the carrier, either in conjunction with elimination of one sideband (single-sideband suppressed-carrier transmission) or with both sidebands remaining (double sideband suppressed carrier). While these suppressed carrier transmissions are efficient in terms of transmitter power, they require more sophisticated receivers employing synchronous detection and regeneration of the carrier frequency. For that reason, standard AM continues to be widely used, especially in broadcast transmission, to allow for the use of inexpensive receivers using envelope detection. Even (analog) television, with a (largely) suppressed lower sideband, includes sufficient carrier power for use of envelope detection. But for communications systems where both transmitters and receivers can be optimized, suppression of both one sideband and the carrier represent a net advantage and are frequently employed. A technique used widely in broadcast AM transmitters is an application of the Hapburg carrier, first proposed in the 1930s but impractical with the technology then available. During periods of low modulation the carrier power would be reduced and would return to full power during periods of high modulation levels. This has the effect of reducing the overall power demand of the transmitter and is most effective on speech type programmes. Various trade names are used for its implementation by the transmitter manufacturers from the late 80's onwards."
	}, {
		"subtitle": "Modulation index.",
		"level": 2,
		"merged_title": ["Amplitude modulation", "Modulation index."],
		"text": "The AM modulation index is a measure based on the ratio of the modulation excursions of the RF signal to the level of the unmodulated carrier. It is thus defined as: where formula_6 and formula_7 are the modulation amplitude and carrier amplitude, respectively; the modulation amplitude is the peak (positive or negative) change in the RF amplitude from its unmodulated value. Modulation index is normally expressed as a percentage, and may be displayed on a meter connected to an AM transmitter. So if formula_8, carrier amplitude varies by 50% above (and below) its unmodulated level, as is shown in the first waveform, below. For formula_9, it varies by 100% as shown in the illustration below it. With 100% modulation the wave amplitude sometimes reaches zero, and this represents full modulation using standard AM and is often a target (in order to obtain the highest possible signal-to-noise ratio) but mustn't be exceeded. Increasing the modulating signal beyond that point, known as overmodulation, causes a standard AM modulator (see below) to fail, as the negative excursions of the wave envelope cannot become less than zero, resulting in distortion (\"clipping\") of the received modulation. Transmitters typically incorporate a limiter circuit to avoid overmodulation, and/or a compressor circuit (especially for voice communications) in order to still approach 100% modulation for maximum intelligibility above the noise. Such circuits are sometimes referred to as a vogad. However it is possible to talk about a modulation index exceeding 100%, without introducing distortion, in the case of double-sideband reduced-carrier transmission. In that case, negative excursions beyond zero entail a reversal of the carrier phase, as shown in the third waveform below. This cannot be produced using the efficient high-level (output stage) modulation techniques (see below) which are widely used especially in high power broadcast transmitters. Rather, a special modulator produces such a waveform at a low level followed by a linear amplifier. What's more, a standard AM receiver using an envelope detector is incapable of properly demodulating such a signal. Rather, synchronous detection is required. Thus double-sideband transmission is generally \"not\" referred to as \"AM\" even though it generates an identical RF waveform as standard AM as long as the modulation index is below 100%. Such systems more often attempt a radical reduction of the carrier level compared to the sidebands (where the useful information is present) to the point of double-sideband suppressed-carrier transmission where the carrier is (ideally) reduced to zero. In all such cases the term \"modulation index\" loses its value as it refers to the ratio of the modulation amplitude to a rather small (or zero) remaining carrier amplitude."
	}, {
		"subtitle": "Modulation methods.",
		"level": 2,
		"merged_title": ["Amplitude modulation", "Modulation methods."],
		"text": "Modulation circuit designs may be classified as low- or high-level (depending on whether they modulate in a low-power domain\u2014followed by amplification for transmission\u2014or in the high-power domain of the transmitted signal)."
	}, {
		"subtitle": "Low-level generation.",
		"level": 3,
		"merged_title": ["Amplitude modulation", "Modulation methods.", "Low-level generation."],
		"text": "In modern radio systems, modulated signals are generated via digital signal processing (DSP). With DSP many types of AM are possible with software control (including DSB with carrier, SSB suppressed-carrier and independent sideband, or ISB). Calculated digital samples are converted to voltages with a digital-to-analog converter, typically at a frequency less than the desired RF-output frequency. The analog signal must then be shifted in frequency and linearly amplified to the desired frequency and power level (linear amplification must be used to prevent modulation distortion). This low-level method for AM is used in many Amateur Radio transceivers. AM may also be generated at a low level, using analog methods described in the next section."
	}, {
		"subtitle": "High-level generation.",
		"level": 3,
		"merged_title": ["Amplitude modulation", "Modulation methods.", "High-level generation."],
		"text": "High-power AM transmitters (such as those used for AM broadcasting) are based on high-efficiency class-D and class-E power amplifier stages, modulated by varying the supply voltage. Older designs (for broadcast and amateur radio) also generate AM by controlling the gain of the transmitter's final amplifier (generally class-C, for efficiency). The following types are for vacuum tube transmitters (but similar options are available with transistors):"
	}, {
		"subtitle": "Demodulation methods.",
		"level": 2,
		"merged_title": ["Amplitude modulation", "Demodulation methods."],
		"text": "The simplest form of AM demodulator consists of a diode which is configured to act as envelope detector. Another type of demodulator, the product detector, can provide better-quality demodulation with additional circuit complexity."
	}],
	"max_level": 3,
	"abstract": ["", "Amplitude modulation (AM) is a modulation technique used in electronic communication, most commonly for transmitting messages with a radio wave. In amplitude modulation, the amplitude (signal strength) of the carrier wave is varied in proportion to that of the message signal, such as an audio signal. This technique contrasts with angle modulation, in which either the frequency of the carrier wave is varied, as in frequency modulation, or its phase, as in phase modulation.", "AM was the earliest modulation method used for transmitting audio in radio broadcasting. It was developed during the first quarter of the 20th century beginning with Roberto Landell de Moura and Reginald Fessenden's radiotelephone experiments in 1900. This original form of AM is sometimes called double-sideband amplitude modulation (DSBAM), because the standard method produces sidebands on either side of the carrier frequency. Single-sideband modulation uses bandpass filters to eliminate one of the sidebands and possibly the carrier signal, which improves the ratio of message power to total transmission power, reduces power handling requirements of line repeaters, and permits better bandwidth utilization of the transmission medium.", "AM remains in use in many forms of communication in addition to AM broadcasting: shortwave radio, amateur radio, two-way radios, VHF aircraft radio, citizens band radio, and in computer modems in the form of QAM."],
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

