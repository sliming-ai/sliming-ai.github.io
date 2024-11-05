![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Fpvtien96%2FSLIMMING&labelColor=%2337d67a&countColor=%23697689)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

<div class="column centered">
    <h1 class="title is-1 publication-title"
        style="text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; ; font-size: 32px;">
        🇫🇷 Singular values-driven automated filter pruning
    </h1>
<div>
<div align="center">
    <a href='https://github.com/pvti' target='_blank'>Van Tien PHAM<sup>1,&#x2709</sup></a>&emsp;
    <a href='https://yzniyed.blogspot.com/p/about-me.html' target='_blank'>Yassine ZNIYED<sup>1</sup></a>&emsp;
    <a href='https://webusers.i3s.unice.fr/~tpnguyen/' target='_blank'>Thanh Phuong NGUYEN<sup>2</sup></a>&emsp;
</div>

<div align="center">
    <sup>1</sup>Université de Toulon, Aix Marseille Université, CNRS, LIS, UMR 7020, France<br>
    <sup>2</sup>University of Côte d'Azur, CNRS, I3S, UMR 7271, France<br>
    <sup>&#x2709</sup> Corresponding Author
</div>


# 🌀 Abstract
This paper introduces a novel automated filter pruning approach through singular values-driven
optimization. Based on the observation and analysis of the distribution of singular values of the
overparameterized model, we establish a robust connection between weight redundancy and these values,
rendering them potent indicators for automated pruning. The automated structured pruning is formulated as
a constrained combinatorial optimization problem spanning all layers, aiming to maximize the nuclear norm
of the compact model. This problem is decomposed into two sub-problems: determining the pruning
configuration and assessing the filter importance within a layer based on the identified pruning ratio. We
introduce two straightforward algorithms to address these sub-problems, effectively handling the global
relationship between layers and the inter-filter correlation within each layer. Thorough experiments
across 8 architectures, 4 benchmark datasets, and 4 vision tasks underscore the efficacy of our framework.


# 🌟 News
* **1.11.024:** [Baseline and checkpoints are released](https://huggingface.co/sliming/models) 🤗.


# 🕙 ToDo
- [ ] Write detailed documentation.
- [x] Upload compressed models.
- [ ] Clean code.

# 🔖 Citation
If the code and paper help your research, please kindly cite:
```
@misc{pham2024singular,
    title={Singular values-driven automated filter pruning}, 
    author={Pham, Van Tien and Zniyed, Yassine and Nguyen, Thanh Phuong},
    howpublished={\url{https://github.com/sliming-ai/sliming-ai.github.i}},
    year={2024}
    }
```


# 👍 Acknowledgements
This work was granted access to the <a href="http://www.idris.fr/eng/jean-zay/jean-zay-presentation-eng.html">HPC resources of IDRIS</a> under the
allocation 2023-103147 made by <a href="https://genci.fr/">GENCI</a>.  
The work of T.P. Nguyen is partially supported by <a href="https://anr.fr/Projet-ANR-21-ASRO-0003">ANR ASTRID ROV-Chasseur</a>.
