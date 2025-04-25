<div>
  <img class="image" src="static/images/singularity/PPTMooresLawai.png" width="40%" height="100%">
  <img class="image" src="static/images/singularity/Moore&apos;s_Law_over_120_Years.png" width="58%" height="100%">
</div>

<div>
  <img class="image" src="static/images/singularity/PPTExponentialGrowthof_Computing.jpg" width="46%" height="100%">
  <img class="image" src="static/images/singularity/Countdown_to_Singularity_-_Linear.svg" width="52.4%" height="100%">
</div>

> The ever-**accelerating** progress of technology… gives the appearance of approaching some essential **singularity**. — *John von Neumann, 1958*

> **The Singularity Is Nearer: When We Merge with AI.** — *Ray Kurzweil, 2024*


![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Fpvtien96%2FSLIMMING&labelColor=%2337d67a&countColor=%23697689)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![Days since submission](https://img.shields.io/badge/Days_since_submission-177-d22b27?style=flat-square)

<div class="column centered">
    <h1 class="title is-1 publication-title"
        style="text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 32px;">
        🧠 Singular values-driven automated filter pruning
    </h1>
</div>
<div align="center">
    <a href='https://pageperso.lis-lab.fr/van-tien.pham/' target='_blank'>Van Tien PHAM<sup>1,&#x2709</sup></a>&emsp;
    <a href='https://yzniyed.blogspot.com/p/about-me.html' target='_blank'>Yassine ZNIYED<sup>1</sup></a>&emsp;
    <a href='https://webusers.i3s.unice.fr/~tpnguyen/' target='_blank'>Thanh Phuong NGUYEN<sup>2</sup></a>&emsp;
</div>

<div align="center">
    <sup>1</sup>Université de Toulon, Université d'Aix-Marseille, CNRS, LIS, UMR 7020, France<br>
    <sup>2</sup>Université Côte d'Azur, CNRS, I3S, UMR 7271, France<br>
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
* **13.11.024:** 🎬 Lights, Camera, Action! 🔥[Presentation Video Out Now!](https://www.youtube.com/watch?v=P0jVSO9LjPg) 🍿 Kick back and enjoy!
* **1.11.2024:** [Baseline and checkpoints are released](https://huggingface.co/sliming/models) 🤗. Get your 👋 dirty 💻!
* **31.10.024:** The manuscript has been submitted to [Neural Networks](https://www.sciencedirect.com/journal/neural-networks).

# :art: Supplementary materials
## 1. Throughput acceleration <a name="throughput-acceleration"></a>
+ FasterRCNN for object detection
<table style="width: 100%; border: none; border-collapse: collapse;">
  <tr>
    <td style="width: 50%; padding: 10px; border: none;">
      <img src="static/videos/faster-baseline.gif" alt="Baseline" style="width: 100%;">
    </td>
    <td style="width: 50%; padding: 10px; border: none;">
      <img src="static/videos/faster-pruned.gif" alt="Pruned" style="width: 100%;">
    </td>
  </tr>
</table>

+ MaskRCNN for instance segmentation
<table style="width: 100%; border: none; border-collapse: collapse;">
  <tr>
    <td style="width: 50%; padding: 10px; border: none;">
      <img src="static/videos/mask-baseline.gif" alt="Baseline" style="width: 100%;">
    </td>
    <td style="width: 50%; padding: 10px; border: none;">
      <img src="static/videos/mask-pruned.gif" alt="Pruned" style="width: 100%;">
    </td>
  </tr>
</table>

+ KeypointRCNN for human keypoint detection
<table style="width: 100%; border: none; border-collapse: collapse;">
  <tr>
    <td style="width: 50%; padding: 10px; border: none;">
      <img src="static/videos/keypoint-baseline.gif" alt="Baseline" style="width: 100%;">
    </td>
    <td style="width: 50%; padding: 10px; border: none;">
      <img src="static/videos/keypoint-pruned.gif" alt="Pruned" style="width: 100%;">
    </td>
  </tr>
</table>

<div align="center">
    Baseline (<em>left</em>) vs Compressed (<em>right</em>) model inference.
</div>

To underscore the practical advantages of SLIMING, an experiment was meticulously conducted, involving a direct comparison between a baseline model and a compressed model, both tailored for object detection tasks. Leveraging the FasterRCNN_ResNet50_FPN architecture on a RTX 3060 GPU, the experiment robustly highlights the substantial performance enhancement achieved by SLIMING. The accompanying GIFs offer a vivid visual depiction: the baseline model showcases an inference speed of approximately 12 FPS, while the SLIMING-compressed model boasts a remarkable twofold acceleration in throughput. This notable disparity effectively showcases SLIMING's efficacy and scalability, firmly establishing its relevance and applicability across diverse deployment scenarios.

*Note*: For replication of this experiment, please refer to [detection/README.md](detection/README.md).

## 2. Visualizing feature preservation <a name="cam"></a>
|                        Input                        |                           CR=0%                            |                            CR=50%                             |                           CR=64%                            |                            CR=78%                            |
| :-------------------------------------------------: | :--------------------------------------------------------: | :-----------------------------------------------------------: | :---------------------------------------------------------: | :----------------------------------------------------------: |
| ![](static/images/cam/ILSVRC2012_val_00003498.JPEG) | ![](static/images/cam/ILSVRC2012_val_00003498_[0.]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00003498_[0.255]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00003498_[0.4]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00003498_[0.55]*20.jpg) |
| ![](static/images/cam/ILSVRC2012_val_00009497.JPEG) | ![](static/images/cam/ILSVRC2012_val_00009497_[0.]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00009497_[0.255]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00009497_[0.4]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00009497_[0.55]*20.jpg) |
| ![](static/images/cam/ILSVRC2012_val_00049750.JPEG) | ![](static/images/cam/ILSVRC2012_val_00049750_[0.]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00049750_[0.255]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00049750_[0.4]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00049750_[0.55]*20.jpg) |
| ![](static/images/cam/ILSVRC2012_val_00044350.JPEG) | ![](static/images/cam/ILSVRC2012_val_00044350_[0.]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00044350_[0.255]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00044350_[0.4]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00044350_[0.55]*20.jpg) |
| ![](static/images/cam/ILSVRC2012_val_00018573.JPEG) | ![](static/images/cam/ILSVRC2012_val_00018573_[0.]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00018573_[0.255]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00018573_[0.4]*20.jpg) | ![](static/images/cam/ILSVRC2012_val_00018573_[0.55]*20.jpg) |

<div align="center">
    Qualitative assessment of feature preservation in compressed models.
</div>
We present a qualitative evaluation of feature preservation in SLIMING, complementing the established efficiency demonstrated through numerical results. Our analysis involves a random selection of 5 images from the ImageNet validation dataset, examining three compression levels applied to the original ResNet-50 model: 50%, 64%, and 78%. Utilizing GradCAM for interpretation, we visually assess and analyze feature maps in both the original and compressed models.

The visual representation underscores SLIMING's efficacy in retaining crucial features across a diverse range of classes. Noteworthy is its consistent robustness in capturing and preserving essential information at different CRs. This resilience implies sustained effectiveness and reliability across varying scenarios and compression levels, positioning SLIMING as a versatile choice for network compression across diverse applications and datasets.

# 🕙 ToDo
- [x] Write detailed documentation.
- [x] Upload compressed models.
- [ ] Clean code.


# 👪 Équipe


# 🔖 Citation
If the code and paper help your research, please kindly cite:
```
@misc{pham2024singular,
    title={Singular values-driven automated filter pruning}, 
    author={Pham, Van Tien and Zniyed, Yassine and Nguyen, Thanh Phuong},
    howpublished={\url{https://sliming-ai.github.io/}},
    year={2024}
    }
```


# 👍 Acknowledgements
This work was granted access to the <a href="http://www.idris.fr/eng/jean-zay/jean-zay-presentation-eng.html">HPC resources of IDRIS</a> under the
allocation 2023-103147 made by <a href="https://genci.fr/">GENCI</a>.  
The work of T.P. Nguyen is partially supported by <a href="https://anr.fr/Projet-ANR-21-ASRO-0003">ANR ASTRID ROV-Chasseur</a>.
