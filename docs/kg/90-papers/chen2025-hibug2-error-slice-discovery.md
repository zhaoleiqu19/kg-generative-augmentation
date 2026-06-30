---
title: "HiBug2: Efficient and Interpretable Error Slice Discovery for Comprehensive Model Debugging"
authors: Muxi Chen, Chenchen Zhao, Qiang Xu
year: 2025
venue: arXiv (ICLR 2025)
url: https://arxiv.org/abs/2501.16751
loop-stage: stage1
tags: slice-discovery, model-debugging, object-detection, pose-estimation, tag-then-slice, diagnosis
---

## TL;DR
A tag-then-slice debugging framework that generates task-specific visual attributes, enumerates error slices efficiently, and — crucially — predicts error slices *beyond* the validation set.

## Method
A 4-stage **tag-then-slice** pipeline (paper §; verified against the repo `cure-lab/HiBug2`, steps `step11..step24`):
1. **Attribute & tag generation** — an MLLM (repo default **GPT-4o**, `config.vlm_agent_id='gpt-4o'`) generates task-specific visual attributes per object class + a fine-grained tag set for each.
2. **Validation tagging** — each image is tagged against those attributes (repo uses the same MLLM; CLIP **ViT-B/32** phrase-matcher).
3. **Slice enumeration** — an efficient algorithm enumerates attribute-tag combinations (repo `slice_len=3`) and ranks slices by low accuracy / data proportion.
4. **Model repair** — targeted **retrieval** of real images matching a slice, for fine-tuning (iterable for multi-round repair).

**Attribute taxonomy (verified, paper + repo `prompts/get_base_attrs.py`):** three structured groups — **main-object** (shape, color, size, pose, visibility), **background** (clutter, other objects, lighting, indoor/outdoor), **global** (resolution, noise, brightness, camera angle). Each attribute is typed `single | multi | binary`. This three-way split maps cleanly onto the generator's two-layer input (object attrs → per-instance caption; background+global → global caption).

## Main claim + result
Key novelty: **predicting error slices beyond the validation set** — via (a) **tag substitution** with CLIP-similar tags, and (b) **instruction-based** GPT-generated hypothetical slices with no prior error data. Reported model performance drops **−64.6%** on predicted object-detection slices (paper body, via arXiv HTML 2501.16751v3). Detection experiments use **YOLOv8 / CO-DINO / ViTDet-L / RTMDet-X** on **KITTI** (Car + Pedestrian, 2,481 imgs).

## Recon findings (2026-06-30, cloned to `/home/qushiduo/diag_tools/HiBug2`)
- **Output = image-level slices, NOT per-instance.** Tagging prompt (`prompts/get_labels.py`) says *"If multiple objects appear, only focus on the object closest to the center."* → one main object per image; bounding boxes are **not** linked to slices. Confirms the bridge's §6.1 caveat: HiBug2 supplies the *attributes/why*, but `pycocotools` must still supply *which box*.
- **Runtime dependency = OpenAI GPT-4o** (external API, per-call cost) + CLIP on CUDA — not a self-contained local model. A runnability/cost gate for our pipeline.
- **Native repair = retrieval of real matching images**, not generation. For our loop we consume the *slice attribute description* as a generation spec; HiBug2 does not itself generate.
- **Detection data unit = one instance per image** (`demo.ipynb`): input is `imgs = {class: [image_path...]}` + per-image `correctness ∈ {0,1}`. For detection, each "image" is a **GT-instance crop** with correctness = detected/missed. → It *can* be box-aligned **if we supply per-instance crops** (we already have boxes + missed labels from pycocotools); HiBug2 then only adds the *why* attributes. The crop is the bridge for the "center-object vs box-unit" mismatch.
- **`utils.readImg` only downscales, never upscales** (`max_query_img_size=256`). A tiny (<32px) crop is sent to GPT-4o at native size → attribute tags unreliable **exactly on the smallest objects** (our 542/698 target band). Auth supports a custom `base_url` (mirror/proxy possible), but needs a working GPT-4o key (none in env as of recon).

## Relevance to us
Multi-task (incl. detection) and explicitly links discovery → repair, matching our loop; its attribute taxonomy directly feeds the two-layer caption (bridge §4). The "predict slices beyond validation" idea matters for the anchor: elevator footage will have failure modes not present in any held-out split. **Caveat now verified:** image-level + center-object tagging means dense COCO scenes (many small objects/image) are only partially covered, and box grounding must come from elsewhere — compare against GH-ESD's grounded/relational slicing.

## Links
- [[stage1-state-of-the-art]]
