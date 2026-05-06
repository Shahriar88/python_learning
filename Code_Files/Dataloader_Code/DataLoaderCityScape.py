#!/usr/bin/env python
# coding: utf-8

# In[1]:


# https://www.cityscapes-dataset.com/downloads/


# In[ ]:





# In[ ]:





# # Functions and Variables

# ## Import Libraries  =========

# In[2]:


from pathlib import Path
import json
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw

import torch
from torch.utils.data import Dataset, DataLoader


# ## Cityscapes class definitions  =========

# In[3]:


# ============================================================
# 1. Cityscapes class definitions
# Two versions:
#   1. Semantic segmentation classes for FCN / DeepLabV3 / U-Net
#   2. Instance segmentation classes for Mask R-CNN
# ============================================================

CITYSCAPES_LABEL_IDS = {
    "road": 7,
    "sidewalk": 8,
    "building": 11,
    "wall": 12,
    "fence": 13,
    "pole": 17,
    "traffic light": 19,
    "traffic sign": 20,
    "vegetation": 21,
    "terrain": 22,
    "sky": 23,
    "person": 24,
    "rider": 25,
    "car": 26,
    "truck": 27,
    "bus": 28,
    "train": 31,
    "motorcycle": 32,
    "bicycle": 33,
}


# In[ ]:





# In[ ]:





# ## Common Helper Functions  =========

# In[4]:


# ============================================================
# 2. Required Cityscapes folder structure
# ============================================================

def print_required_cityscapes_structure():
    """
    Print the exact folder structure expected by this DataLoader.
    """

    print(
        r"""
Required Cityscapes folder structure
====================================

You should extract the Cityscapes files like this:

ROOT_FOLDER/
│
├── gtFine_trainvaltest/
│   └── gtFine/
│       ├── train/
│       │   ├── aachen/
│       │   │   ├── *_gtFine_labelIds.png
│       │   │   ├── *_gtFine_instanceIds.png
│       │   │   ├── *_gtFine_polygons.json
│       │   │   └── *_gtFine_color.png
│       │   └── ...
│       ├── val/
│       └── test/
│
└── leftImg8bit_trainvaltest/
    └── leftImg8bit/
        ├── train/
        │   ├── aachen/
        │   │   └── *_leftImg8bit.png
        │   └── ...
        ├── val/
        └── test/
"""
    )


# ============================================================
# 3. Common helper functions
# Used by both semantic segmentation and instance segmentation
# ============================================================

def image_to_tensor(image_pil):
    """
    Convert PIL RGB image to torch Tensor [3, H, W] in [0, 1].
    """
    image_np = np.array(image_pil)
    image_tensor = torch.from_numpy(image_np).permute(2, 0, 1).float() / 255.0
    return image_tensor


def print_dataset_summary(name, dataset):
    """
    Print a short dataset summary.
    """
    print(f"{name}: {len(dataset)} samples")


def mask_to_box(mask):
    """
    Convert a binary mask to a bounding box.

    Returns:
        [x1, y1, x2, y2] or None
    """

    ys, xs = np.where(mask > 0)

    if len(xs) == 0 or len(ys) == 0:
        return None

    x1 = float(xs.min())
    y1 = float(ys.min())
    x2 = float(xs.max())
    y2 = float(ys.max())

    if x2 <= x1 or y2 <= y1:
        return None

    return [x1, y1, x2, y2]


def build_cityscapes_pairs(
    gt_fine_root,
    left_img_root,
    split="train",
    require_instance=False,
    require_polygon=False,
    require_label=True,
    verbose=True,
):
    """
    Build paired Cityscapes samples.

    Parameters
    ----------
    gt_fine_root:
        Path to:
            gtFine_trainvaltest/gtFine

    left_img_root:
        Path to:
            leftImg8bit_trainvaltest/leftImg8bit

    split:
        One of:
            "train", "val", "test"

    require_instance:
        If True, each sample must have:
            *_gtFine_instanceIds.png

    require_polygon:
        If True, each sample must have:
            *_gtFine_polygons.json

    require_label:
        If True, each sample must have:
            *_gtFine_labelIds.png

    Returns
    -------
    pairs:
        List of dictionaries. Each dictionary contains:
            image
            label
            instance
            polygon
            color
            city
            stem
    """

    gt_fine_root = Path(gt_fine_root)
    left_img_root = Path(left_img_root)

    gt_split_dir = gt_fine_root / split
    left_split_dir = left_img_root / split

    if not gt_split_dir.exists():
        raise FileNotFoundError(f"gtFine split folder not found: {gt_split_dir}")

    if not left_split_dir.exists():
        raise FileNotFoundError(f"leftImg8bit split folder not found: {left_split_dir}")

    label_paths = sorted(gt_split_dir.glob("*/*_gtFine_labelIds.png"))

    pairs = []

    missing_image = 0
    missing_label = 0
    missing_instance = 0
    missing_polygon = 0

    for label_path in label_paths:
        city = label_path.parent.name

        stem = label_path.name.replace("_gtFine_labelIds.png", "")

        image_path = left_split_dir / city / f"{stem}_leftImg8bit.png"
        instance_path = label_path.with_name(f"{stem}_gtFine_instanceIds.png")
        polygon_path = label_path.with_name(f"{stem}_gtFine_polygons.json")
        color_path = label_path.with_name(f"{stem}_gtFine_color.png")

        if not image_path.exists():
            missing_image += 1
            if verbose:
                print(f"[SKIP] Missing RGB image: {image_path}")
            continue

        if require_label and not label_path.exists():
            missing_label += 1
            if verbose:
                print(f"[SKIP] Missing labelIds file: {label_path}")
            continue

        if require_instance and not instance_path.exists():
            missing_instance += 1
            if verbose:
                print(f"[SKIP] Missing instance file: {instance_path}")
            continue

        if require_polygon and not polygon_path.exists():
            missing_polygon += 1
            if verbose:
                print(f"[SKIP] Missing polygon file: {polygon_path}")
            continue

        pairs.append(
            {
                "image": image_path,
                "label": label_path if label_path.exists() else None,
                "instance": instance_path if instance_path.exists() else None,
                "polygon": polygon_path if polygon_path.exists() else None,
                "color": color_path if color_path.exists() else None,
                "city": city,
                "stem": stem,
            }
        )

    print(f"[Cityscapes] split={split}, pairs={len(pairs)}")

    if missing_image > 0:
        print(f"[INFO] Missing RGB images: {missing_image}")

    if missing_label > 0:
        print(f"[INFO] Missing labelIds files: {missing_label}")

    if missing_instance > 0:
        print(f"[INFO] Missing instance files: {missing_instance}")

    if missing_polygon > 0:
        print(f"[INFO] Missing polygon files: {missing_polygon}")

    return pairs



# In[ ]:





# In[ ]:





# In[ ]:





# ## Semantic Segmentation ********

# In[5]:


# ============================================================
# 1A. Semantic segmentation classes
# For FCN, DeepLabV3, U-Net, SegFormer, etc.
# ============================================================
# Semantic target:
#   mask: LongTensor [H, W]
#   each pixel contains compact class index:
#       0, 1, 2, ..., C - 1
#
# Here:
#   0 = background / ignored non-selected Cityscapes labels

CITYSCAPES_SEMANTIC_CLASS_NAMES = {
    0: "background",
    1: "road",
    2: "sidewalk",
    3: "building",
    4: "wall",
    5: "fence",
    6: "pole",
    7: "traffic light",
    8: "traffic sign",
    9: "vegetation",
    10: "terrain",
    11: "sky",
    12: "person",
    13: "rider",
    14: "car",
    15: "truck",
    16: "bus",
    17: "train",
    18: "motorcycle",
    19: "bicycle",
}

CITYSCAPES_SEMANTIC_LABELID_TO_TRAIN_ID = {
    CITYSCAPES_LABEL_IDS["road"]: 1,
    CITYSCAPES_LABEL_IDS["sidewalk"]: 2,
    CITYSCAPES_LABEL_IDS["building"]: 3,
    CITYSCAPES_LABEL_IDS["wall"]: 4,
    CITYSCAPES_LABEL_IDS["fence"]: 5,
    CITYSCAPES_LABEL_IDS["pole"]: 6,
    CITYSCAPES_LABEL_IDS["traffic light"]: 7,
    CITYSCAPES_LABEL_IDS["traffic sign"]: 8,
    CITYSCAPES_LABEL_IDS["vegetation"]: 9,
    CITYSCAPES_LABEL_IDS["terrain"]: 10,
    CITYSCAPES_LABEL_IDS["sky"]: 11,
    CITYSCAPES_LABEL_IDS["person"]: 12,
    CITYSCAPES_LABEL_IDS["rider"]: 13,
    CITYSCAPES_LABEL_IDS["car"]: 14,
    CITYSCAPES_LABEL_IDS["truck"]: 15,
    CITYSCAPES_LABEL_IDS["bus"]: 16,
    CITYSCAPES_LABEL_IDS["train"]: 17,
    CITYSCAPES_LABEL_IDS["motorcycle"]: 18,
    CITYSCAPES_LABEL_IDS["bicycle"]: 19,
}

CITYSCAPES_SEMANTIC_JSON_LABEL_TO_TRAIN_ID = {
    "road": 1,
    "sidewalk": 2,
    "building": 3,
    "wall": 4,
    "fence": 5,
    "pole": 6,
    "traffic light": 7,
    "traffic sign": 8,
    "vegetation": 9,
    "terrain": 10,
    "sky": 11,
    "person": 12,
    "rider": 13,
    "car": 14,
    "truck": 15,
    "bus": 16,
    "train": 17,
    "motorcycle": 18,
    "bicycle": 19,
}

CITYSCAPES_SEMANTIC_CLASS_MAP = {
    name: idx for idx, name in CITYSCAPES_SEMANTIC_CLASS_NAMES.items()
}

CITYSCAPES_SEMANTIC_N_CLASSES = len(CITYSCAPES_SEMANTIC_CLASS_NAMES)





# ============================================================
# 4. Semantic segmentation functions
# For FCN, DeepLabV3, U-Net, SegFormer, etc.
# ============================================================

def cityscapes_semantic_collate_fn(batch):
    """
    Standard collate function for semantic segmentation.

    Returns:
        images: Tensor [B, 3, H, W]
        masks:  LongTensor [B, H, W]
    """
    images, masks = zip(*batch)
    images = torch.stack(list(images), dim=0)
    masks = torch.stack(list(masks), dim=0)
    return images, masks


class CityscapesSemanticSegmentationDataset(Dataset):
    """
    Cityscapes semantic segmentation dataset using:

        input image:
            leftImg8bit/*/*_leftImg8bit.png

        semantic label:
            gtFine/*/*_gtFine_labelIds.png

    Output:
        image:
            Tensor [3, H, W], float32, values in [0, 1]

        mask:
            LongTensor [H, W], compact class indices

    For semantic models:
        FCN, DeepLabV3, U-Net, SegFormer, etc.
    """

    def __init__(
        self,
        pairs,
        labelid_to_train_id,
        resize=None,
        ignore_index=255,
        background_id=0,
    ):
        self.pairs = list(pairs)
        self.labelid_to_train_id = dict(labelid_to_train_id)
        self.resize = resize
        self.ignore_index = int(ignore_index)
        self.background_id = int(background_id)

    def __len__(self):
        return len(self.pairs)

    def convert_labelids_to_trainids(self, label_np):
        """
        Convert Cityscapes original labelIds into compact semantic class IDs.

        Unknown or unused Cityscapes labels are assigned to background_id.
        If you prefer ignoring unknown labels during loss computation,
        change fill_value from background_id to ignore_index.
        """

        semantic_mask = np.full(
            shape=label_np.shape,
            fill_value=self.background_id,
            dtype=np.int64,
        )

        for city_label_id, train_id in self.labelid_to_train_id.items():
            semantic_mask[label_np == city_label_id] = int(train_id)

        return semantic_mask

    def __getitem__(self, idx):
        item = self.pairs[idx]

        image = Image.open(item["image"]).convert("RGB")
        label_img = Image.open(item["label"])

        if self.resize is not None:
            image = image.resize(
                (self.resize, self.resize),
                resample=Image.BILINEAR,
            )
            label_img = label_img.resize(
                (self.resize, self.resize),
                resample=Image.NEAREST,
            )

        label_np = np.array(label_img)

        if label_np.ndim == 3:
            label_np = label_np[:, :, 0]

        semantic_np = self.convert_labelids_to_trainids(label_np)

        image_tensor = image_to_tensor(image)
        mask_tensor = torch.from_numpy(semantic_np).long()

        return image_tensor, mask_tensor


def make_semantic_dataloader(dataset, batch_size, shuffle, num_workers):
    """
    Build one semantic segmentation DataLoader.
    """

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        collate_fn=cityscapes_semantic_collate_fn,
        pin_memory=torch.cuda.is_available(),
    )

    return loader


def build_cityscapes_semantic_dataloaders(
    gt_fine_root,
    left_img_root,
    batch_size=2,
    num_workers=0,
    resize=None,
    ignore_index=255,
    background_id=0,
    verbose=True,
):
    """
    Build train, val, and test DataLoaders for semantic segmentation.

    Uses:
        *_gtFine_labelIds.png

    Output:
        images: Tensor [B, 3, H, W]
        masks:  LongTensor [B, H, W]
    """

    pairs = {}

    for split in ["train", "val", "test"]:
        pairs[split] = build_cityscapes_pairs(
            gt_fine_root=gt_fine_root,
            left_img_root=left_img_root,
            split=split,
            require_instance=False,
            require_polygon=False,
            require_label=True,
            verbose=verbose,
        )

    datasets = {}

    for split in ["train", "val", "test"]:
        datasets[split] = CityscapesSemanticSegmentationDataset(
            pairs=pairs[split],
            labelid_to_train_id=CITYSCAPES_SEMANTIC_LABELID_TO_TRAIN_ID,
            resize=resize,
            ignore_index=ignore_index,
            background_id=background_id,
        )

    loaders = {
        "train": make_semantic_dataloader(
            dataset=datasets["train"],
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
        ),
        "val": make_semantic_dataloader(
            dataset=datasets["val"],
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
        ),
        "test": make_semantic_dataloader(
            dataset=datasets["test"],
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
        ),
    }

    print("")
    print("Semantic segmentation dataset summary")
    print("=====================================")
    print_dataset_summary("Train", datasets["train"])
    print_dataset_summary("Val", datasets["val"])
    print_dataset_summary("Test", datasets["test"])

    return datasets, loaders


def check_one_semantic_batch(loader, name="Semantic DataLoader"):
    """
    Print one batch shape from a semantic segmentation DataLoader.
    """

    images, masks = next(iter(loader))

    print("")
    print(f"{name} sanity check")
    print("=" * (len(name) + 13))

    print("Images shape:", images.shape)
    print("Images dtype:", images.dtype)
    print("Images min/max:", images.min().item(), images.max().item())

    print("Masks shape:", masks.shape)
    print("Masks dtype:", masks.dtype)
    print("Mask unique values:", torch.unique(masks[0]))


SEMANTIC_COLOR_TABLE = {
    0: (0.00, 0.00, 0.00),  # background
    1: (0.50, 0.50, 0.50),  # road
    2: (0.70, 0.70, 0.70),  # sidewalk
    3: (0.60, 0.30, 0.20),  # building
    4: (0.50, 0.20, 0.20),  # wall
    5: (0.40, 0.20, 0.20),  # fence
    6: (0.70, 0.70, 0.20),  # pole
    7: (1.00, 0.80, 0.00),  # traffic light
    8: (1.00, 1.00, 0.00),  # traffic sign
    9: (0.00, 0.60, 0.00),  # vegetation
    10: (0.30, 0.70, 0.30), # terrain
    11: (0.00, 0.50, 1.00), # sky
    12: (1.00, 0.00, 0.00), # person
    13: (1.00, 0.50, 0.00), # rider
    14: (0.00, 0.00, 1.00), # car
    15: (0.00, 0.50, 1.00), # truck
    16: (0.00, 0.80, 1.00), # bus
    17: (0.30, 0.30, 1.00), # train
    18: (0.00, 1.00, 1.00), # motorcycle
    19: (0.00, 1.00, 0.00), # bicycle
}


def semantic_mask_to_rgb(mask):
    """
    Convert semantic mask [H, W] to RGB visualization [H, W, 3].
    """

    if isinstance(mask, torch.Tensor):
        mask = mask.detach().cpu().numpy()

    height, width = mask.shape[:2]
    rgb = np.zeros((height, width, 3), dtype=np.float32)

    unique_ids = np.unique(mask)

    for class_id in unique_ids:
        class_id = int(class_id)
        color = SEMANTIC_COLOR_TABLE.get(class_id, (1.0, 1.0, 1.0))
        m = mask == class_id

        for c in range(3):
            rgb[:, :, c][m] = color[c]

    return rgb


def plot_semantic_loader_samples(
    loader,
    n_samples=4,
    alpha=0.45,
    title="Cityscapes Semantic Segmentation Samples",
):
    """
    Plot image and semantic mask overlay from a semantic segmentation DataLoader.
    """

    import matplotlib.pyplot as plt

    images, masks = next(iter(loader))

    n_samples = min(n_samples, images.shape[0])

    plt.figure(figsize=(14, 4 * n_samples))

    for i in range(n_samples):
        img = images[i].detach().cpu()
        img_np = img.permute(1, 2, 0).numpy()
        img_np = np.clip(img_np, 0.0, 1.0)

        mask = masks[i].detach().cpu()
        mask_rgb = semantic_mask_to_rgb(mask)

        overlay = np.clip((1.0 - alpha) * img_np + alpha * mask_rgb, 0.0, 1.0)

        unique_labels = torch.unique(mask).detach().cpu().numpy().tolist()
        unique_labels = sorted([int(x) for x in unique_labels])

        label_text = ", ".join(
            [
                CITYSCAPES_SEMANTIC_CLASS_NAMES.get(int(lbl), str(lbl))
                for lbl in unique_labels
            ]
        )

        ax1 = plt.subplot(n_samples, 2, 2 * i + 1)
        ax1.imshow(img_np)
        ax1.set_title(f"Image {i}")
        ax1.axis("off")

        ax2 = plt.subplot(n_samples, 2, 2 * i + 2)
        ax2.imshow(overlay)
        ax2.set_title(f"Image + Semantic Mask | Labels: {label_text}")
        ax2.axis("off")

    plt.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# ## Instance Segmentation @@@@@@

# In[6]:


# ============================================================
# 1B. Instance segmentation classes
# For Mask R-CNN
# ============================================================
# 0 must be background for Mask R-CNN.
# These are countable object classes.

CITYSCAPES_INSTANCE_CLASS_NAMES = {
    0: "background",
    1: "person",
    2: "rider",
    3: "car",
    4: "truck",
    5: "bus",
    6: "train",
    7: "motorcycle",
    8: "bicycle",
    9: "traffic sign",
    10: "traffic light",
}

CITYSCAPES_INSTANCE_LABELID_TO_MODEL_ID = {
    CITYSCAPES_LABEL_IDS["person"]: 1,
    CITYSCAPES_LABEL_IDS["rider"]: 2,
    CITYSCAPES_LABEL_IDS["car"]: 3,
    CITYSCAPES_LABEL_IDS["truck"]: 4,
    CITYSCAPES_LABEL_IDS["bus"]: 5,
    CITYSCAPES_LABEL_IDS["train"]: 6,
    CITYSCAPES_LABEL_IDS["motorcycle"]: 7,
    CITYSCAPES_LABEL_IDS["bicycle"]: 8,
    CITYSCAPES_LABEL_IDS["traffic sign"]: 9,
    CITYSCAPES_LABEL_IDS["traffic light"]: 10,
}

CITYSCAPES_INSTANCE_JSON_LABEL_TO_MODEL_ID = {
    "person": 1,
    "rider": 2,
    "car": 3,
    "truck": 4,
    "bus": 5,
    "train": 6,
    "motorcycle": 7,
    "bicycle": 8,
    "traffic sign": 9,
    "traffic light": 10,
}

CITYSCAPES_INSTANCE_CLASS_MAP = {
    name: idx for idx, name in CITYSCAPES_INSTANCE_CLASS_NAMES.items()
}

CITYSCAPES_INSTANCE_N_CLASSES = len(CITYSCAPES_INSTANCE_CLASS_NAMES)








# ============================================================
# 5. Instance segmentation functions
# For Mask R-CNN
# ============================================================

def cityscapes_maskrcnn_collate_fn(batch):
    """
    Required collate function for Torchvision Mask R-CNN.

    Mask R-CNN expects:
        images:  list[Tensor]
        targets: list[dict]
    """
    images, targets = zip(*batch)
    return list(images), list(targets)


def empty_maskrcnn_target(height, width, image_id):
    """
    Return an empty Mask R-CNN target when no valid object is found.
    """
    return {
        "boxes": torch.zeros((0, 4), dtype=torch.float32),
        "labels": torch.zeros((0,), dtype=torch.int64),
        "masks": torch.zeros((0, height, width), dtype=torch.uint8),
        "image_id": torch.tensor([image_id], dtype=torch.int64),
        "area": torch.zeros((0,), dtype=torch.float32),
        "iscrowd": torch.zeros((0,), dtype=torch.int64),
    }


def build_maskrcnn_target(masks_np, boxes, labels, height, width, image_id):
    """
    Convert lists of masks, boxes, and labels into a Mask R-CNN target dict.
    """

    if len(masks_np) == 0:
        return empty_maskrcnn_target(
            height=height,
            width=width,
            image_id=image_id,
        )

    masks = torch.stack(
        [torch.from_numpy(mask).to(torch.uint8) for mask in masks_np],
        dim=0,
    )

    boxes = torch.tensor(boxes, dtype=torch.float32)
    labels = torch.tensor(labels, dtype=torch.int64)

    area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    iscrowd = torch.zeros((labels.shape[0],), dtype=torch.int64)

    target = {
        "boxes": boxes,
        "labels": labels,
        "masks": masks,
        "image_id": torch.tensor([image_id], dtype=torch.int64),
        "area": area,
        "iscrowd": iscrowd,
    }

    return target


class CityscapesInstanceMaskRCNNDataset(Dataset):
    """
    Cityscapes Mask R-CNN dataset using:

        input image:
            leftImg8bit/*/*_leftImg8bit.png

        instance mask:
            gtFine/*/*_gtFine_instanceIds.png

    Cityscapes instance ID encoding:

        instance_id = class_label_id * 1000 + instance_number

    Examples:
        26001 = car instance 1
        24002 = person instance 2
    """

    def __init__(
        self,
        pairs,
        labelid_to_model_id,
        min_area=50,
        resize=None,
    ):
        self.pairs = list(pairs)
        self.labelid_to_model_id = dict(labelid_to_model_id)
        self.min_area = int(min_area)
        self.resize = resize

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        item = self.pairs[idx]

        image = Image.open(item["image"]).convert("RGB")
        instance_img = Image.open(item["instance"])

        if self.resize is not None:
            image = image.resize(
                (self.resize, self.resize),
                resample=Image.BILINEAR,
            )
            instance_img = instance_img.resize(
                (self.resize, self.resize),
                resample=Image.NEAREST,
            )

        instance_np = np.array(instance_img)

        if instance_np.ndim == 3:
            instance_np = instance_np[:, :, 0]

        image_tensor = image_to_tensor(image)

        masks_np = []
        boxes = []
        labels = []

        unique_instance_ids = np.unique(instance_np)

        for instance_id in unique_instance_ids:
            instance_id = int(instance_id)

            # True object instances in Cityscapes are usually >= 1000.
            # Stuff classes such as road and sidewalk are usually below 1000.
            if instance_id < 1000:
                continue

            city_label_id = instance_id // 1000

            if city_label_id not in self.labelid_to_model_id:
                continue

            model_class_id = self.labelid_to_model_id[city_label_id]

            mask = (instance_np == instance_id).astype(np.uint8)

            if int(mask.sum()) < self.min_area:
                continue

            box = mask_to_box(mask)

            if box is None:
                continue

            masks_np.append(mask)
            boxes.append(box)
            labels.append(int(model_class_id))

        height, width = instance_np.shape[:2]

        target = build_maskrcnn_target(
            masks_np=masks_np,
            boxes=boxes,
            labels=labels,
            height=height,
            width=width,
            image_id=idx,
        )

        return image_tensor, target


class CityscapesPolygonMaskRCNNDataset(Dataset):
    """
    Cityscapes Mask R-CNN dataset using:

        input image:
            leftImg8bit/*/*_leftImg8bit.png

        target masks:
            gtFine/*/*_gtFine_polygons.json

    Each selected polygon object becomes one Mask R-CNN instance.
    """

    def __init__(
        self,
        pairs,
        json_label_to_model_id,
        min_area=50,
        resize=None,
    ):
        self.pairs = list(pairs)
        self.json_label_to_model_id = dict(json_label_to_model_id)
        self.min_area = int(min_area)
        self.resize = resize

    def __len__(self):
        return len(self.pairs)

    @staticmethod
    def polygon_to_mask(polygon, height, width):
        """
        Convert one polygon into a binary mask.
        """

        mask_img = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask_img)

        polygon_tuples = [(int(x), int(y)) for x, y in polygon]

        if len(polygon_tuples) >= 3:
            draw.polygon(polygon_tuples, outline=1, fill=1)

        return np.array(mask_img, dtype=np.uint8)

    def __getitem__(self, idx):
        item = self.pairs[idx]

        image = Image.open(item["image"]).convert("RGB")

        with open(item["polygon"], "r", encoding="utf-8") as f:
            data = json.load(f)

        original_height = int(data.get("imgHeight", image.height))
        original_width = int(data.get("imgWidth", image.width))

        masks_np = []
        boxes = []
        labels = []

        for obj in data.get("objects", []):
            label_name = obj.get("label", "")
            polygon = obj.get("polygon", [])

            if label_name not in self.json_label_to_model_id:
                continue

            if len(polygon) < 3:
                continue

            model_class_id = self.json_label_to_model_id[label_name]

            mask = self.polygon_to_mask(
                polygon=polygon,
                height=original_height,
                width=original_width,
            )

            if int(mask.sum()) < self.min_area:
                continue

            box = mask_to_box(mask)

            if box is None:
                continue

            masks_np.append(mask)
            boxes.append(box)
            labels.append(int(model_class_id))

        if self.resize is not None:
            original_w, original_h = image.size

            image = image.resize(
                (self.resize, self.resize),
                resample=Image.BILINEAR,
            )

            scale_x = self.resize / original_w
            scale_y = self.resize / original_h

            resized_masks = []

            for mask in masks_np:
                mask_img = Image.fromarray(mask)
                mask_img = mask_img.resize(
                    (self.resize, self.resize),
                    resample=Image.NEAREST,
                )
                resized_masks.append(np.array(mask_img, dtype=np.uint8))

            masks_np = resized_masks

            boxes = [
                [
                    x1 * scale_x,
                    y1 * scale_y,
                    x2 * scale_x,
                    y2 * scale_y,
                ]
                for x1, y1, x2, y2 in boxes
            ]

            height = self.resize
            width = self.resize

        else:
            height = original_height
            width = original_width

        image_tensor = image_to_tensor(image)

        target = build_maskrcnn_target(
            masks_np=masks_np,
            boxes=boxes,
            labels=labels,
            height=height,
            width=width,
            image_id=idx,
        )

        return image_tensor, target


def make_maskrcnn_dataloader(dataset, batch_size, shuffle, num_workers):
    """
    Build one Mask R-CNN DataLoader.
    """

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        collate_fn=cityscapes_maskrcnn_collate_fn,
        pin_memory=torch.cuda.is_available(),
    )

    return loader


def build_cityscapes_maskrcnn_dataloaders(
    gt_fine_root,
    left_img_root,
    target_source="instance",
    batch_size=2,
    num_workers=0,
    min_area=50,
    resize=None,
    verbose=True,
):
    """
    Build train, val, and test DataLoaders for Mask R-CNN.

    target_source:
        "instance":
            Uses *_gtFine_instanceIds.png

        "polygon":
            Uses *_gtFine_polygons.json
    """

    if target_source not in {"instance", "polygon"}:
        raise ValueError("target_source must be either 'instance' or 'polygon'.")

    require_instance = target_source == "instance"
    require_polygon = target_source == "polygon"

    pairs = {}

    for split in ["train", "val", "test"]:
        pairs[split] = build_cityscapes_pairs(
            gt_fine_root=gt_fine_root,
            left_img_root=left_img_root,
            split=split,
            require_instance=require_instance,
            require_polygon=require_polygon,
            require_label=True,
            verbose=verbose,
        )

    datasets = {}

    if target_source == "instance":
        for split in ["train", "val", "test"]:
            datasets[split] = CityscapesInstanceMaskRCNNDataset(
                pairs=pairs[split],
                labelid_to_model_id=CITYSCAPES_INSTANCE_LABELID_TO_MODEL_ID,
                min_area=min_area,
                resize=resize,
            )

    elif target_source == "polygon":
        for split in ["train", "val", "test"]:
            datasets[split] = CityscapesPolygonMaskRCNNDataset(
                pairs=pairs[split],
                json_label_to_model_id=CITYSCAPES_INSTANCE_JSON_LABEL_TO_MODEL_ID,
                min_area=min_area,
                resize=resize,
            )

    loaders = {
        "train": make_maskrcnn_dataloader(
            dataset=datasets["train"],
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
        ),
        "val": make_maskrcnn_dataloader(
            dataset=datasets["val"],
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
        ),
        "test": make_maskrcnn_dataloader(
            dataset=datasets["test"],
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
        ),
    }

    print("")
    print("Mask R-CNN dataset summary")
    print("==========================")
    print_dataset_summary("Train", datasets["train"])
    print_dataset_summary("Val", datasets["val"])
    print_dataset_summary("Test", datasets["test"])

    return datasets, loaders


def check_one_batch(loader, name="Mask R-CNN DataLoader"):
    """
    Print one batch shape from a Mask R-CNN DataLoader.
    """

    images, targets = next(iter(loader))

    print("")
    print(f"{name} sanity check")
    print("=" * (len(name) + 13))

    print("Number of images in batch:", len(images))
    print("Image shape:", images[0].shape)
    print("Image min/max:", images[0].min().item(), images[0].max().item())

    print("Boxes shape:", targets[0]["boxes"].shape)
    print("Labels:", targets[0]["labels"])
    print("Masks shape:", targets[0]["masks"].shape)
    print("Area shape:", targets[0]["area"].shape)
    print("iscrowd shape:", targets[0]["iscrowd"].shape)


MASK_COLOR_TABLE = {
    1: (1.00, 0.00, 0.00),  # person
    2: (1.00, 0.50, 0.00),  # rider
    3: (0.00, 0.00, 1.00),  # car
    4: (0.00, 0.50, 1.00),  # truck
    5: (0.00, 0.80, 1.00),  # bus
    6: (0.30, 0.30, 1.00),  # train
    7: (0.00, 1.00, 1.00),  # motorcycle
    8: (0.00, 1.00, 0.00),  # bicycle
    9: (1.00, 1.00, 0.00),  # traffic sign
    10: (1.00, 0.70, 0.00), # traffic light
}


def target_masks_to_rgb(target):
    """
    Convert target masks to an RGB mask visualization.
    """

    masks = target["masks"]
    labels = target["labels"]

    if isinstance(masks, torch.Tensor):
        masks = masks.detach().cpu().numpy()

    if isinstance(labels, torch.Tensor):
        labels = labels.detach().cpu().numpy()

    if masks.shape[0] == 0:
        height, width = masks.shape[1], masks.shape[2]
        return np.zeros((height, width, 3), dtype=np.float32)

    height, width = masks.shape[1], masks.shape[2]
    mask_rgb = np.zeros((height, width, 3), dtype=np.float32)

    for mask, label in zip(masks, labels):
        color = MASK_COLOR_TABLE.get(int(label), (1.0, 1.0, 1.0))
        m = mask.astype(bool)

        for c in range(3):
            mask_rgb[:, :, c][m] = color[c]

    return mask_rgb


def plot_loader_samples_with_boxes(
    loader,
    n_samples=4,
    alpha=0.45,
    title="Cityscapes Mask R-CNN DataLoader Samples",
):
    """
    Plot image, mask overlay, and bounding boxes from a Mask R-CNN DataLoader.
    """

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    images, targets = next(iter(loader))

    n_samples = min(n_samples, len(images))

    plt.figure(figsize=(14, 4 * n_samples))

    for i in range(n_samples):
        img = images[i].detach().cpu()
        img_np = img.permute(1, 2, 0).numpy()
        img_np = np.clip(img_np, 0.0, 1.0)

        target = targets[i]

        mask_rgb = target_masks_to_rgb(target)
        overlay = np.clip((1.0 - alpha) * img_np + alpha * mask_rgb, 0.0, 1.0)

        boxes = target["boxes"].detach().cpu().numpy()
        labels = target["labels"].detach().cpu().numpy()

        unique_labels = sorted(set(labels.tolist()))

        label_text = ", ".join(
            [
                CITYSCAPES_INSTANCE_CLASS_NAMES.get(int(lbl), str(lbl))
                for lbl in unique_labels
            ]
        )

        ax1 = plt.subplot(n_samples, 2, 2 * i + 1)
        ax1.imshow(img_np)
        ax1.set_title(f"Image {i}")
        ax1.axis("off")

        ax2 = plt.subplot(n_samples, 2, 2 * i + 2)
        ax2.imshow(overlay)
        ax2.set_title(f"Image + Masks + Boxes | Labels: {label_text}")
        ax2.axis("off")

        for box, label in zip(boxes, labels):
            x1, y1, x2, y2 = box

            width = x2 - x1
            height = y2 - y1

            class_name = CITYSCAPES_INSTANCE_CLASS_NAMES.get(
                int(label),
                str(label),
            )

            rect = patches.Rectangle(
                (x1, y1),
                width,
                height,
                linewidth=2,
                edgecolor="red",
                facecolor="none",
            )

            ax2.add_patch(rect)

            ax2.text(
                x1,
                max(y1 - 5, 0),
                class_name,
                fontsize=8,
                color="yellow",
                bbox=dict(
                    facecolor="black",
                    alpha=0.6,
                    edgecolor="none",
                    pad=1,
                ),
            )

    plt.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# # Example Use

# ## Source =======

# In[7]:


# ============================================================
# 10. Main usage example
# ============================================================

if __name__ == "__main__":

    print_required_cityscapes_structure()


    # Ground-truth annotations: label masks, instance masks, polygon JSON files
    gt_fine_root = r"C:\Users\kec994\Downloads\GT\gtFine_trainvaltest\gtFine"  
    # Original RGB images
    left_img_root = r"C:\Users\kec994\Downloads\GT\leftImg8bit_trainvaltest\leftImg8bit" 


# ## Semantic Segmentation ********

# In[8]:


# ============================================================
# 10. Main usage example
# ============================================================

if __name__ == "__main__":

    # ========================================================
    # VERSION 2: Semantic Segmentation
    # Model examples:
    #   - FCN-ResNet50
    #   - DeepLabV3-ResNet50
    #   - U-Net
    #   - SegFormer
    #
    # Annotation source:
    #   gtFine_labelIds.png
    # ========================================================
    print('='*100)
    print('Semantic Segmentation ===')
    print('='*100)


    semantic_datasets, semantic_loaders = build_cityscapes_semantic_dataloaders(
        gt_fine_root=gt_fine_root,
        left_img_root=left_img_root,
        batch_size=2,
        num_workers=0,
        resize=None,
        ignore_index=255,
        background_id=0,
        verbose=True,
    )

    semantic_train_loader = semantic_loaders["train"]

    check_one_semantic_batch(
        semantic_train_loader,
        name="Semantic train loader",
    )

    plot_semantic_loader_samples(
        semantic_train_loader,
        n_samples=4,
        alpha=0.45,
        title="Cityscapes Semantic Segmentation: Image and Semantic Mask Overlay",
    )


# In[ ]:





# In[ ]:





# ## Instance Segmentation @@@@@@

# In[9]:


# ============================================================
# 10. Main usage example
# ============================================================

if __name__ == "__main__":

    print_required_cityscapes_structure()


    # Ground-truth annotations: label masks, instance masks, polygon JSON files
    gt_fine_root = r"C:\Users\kec994\Downloads\GT\gtFine_trainvaltest\gtFine"  
    # Original RGB images
    left_img_root = r"C:\Users\kec994\Downloads\GT\leftImg8bit_trainvaltest\leftImg8bit"  


    # ========================================================
    # VERSION 1: Instance Segmentation
    # Model examples:
    #   - Mask R-CNN
    #
    # Annotation source:
    #   gtFine_instanceIds.png
    # ========================================================
    print('='*100)
    print('Instance Segmentation ===')
    print('='*100)
    instance_datasets, instance_loaders = build_cityscapes_maskrcnn_dataloaders(
        gt_fine_root=gt_fine_root,
        left_img_root=left_img_root,
        target_source="instance",
        batch_size=2,
        num_workers=0,
        min_area=50,
        resize=None,
        verbose=True,
    )

    instance_train_loader = instance_loaders["train"]

    check_one_batch(
        instance_train_loader,
        name="Instance train loader",
    )

    plot_loader_samples_with_boxes(
        instance_train_loader,
        n_samples=4,
        alpha=0.45,
        title="Cityscapes Instance Segmentation: Masks and Bounding Boxes",
    )

    # ========================================================
    # VERSION 1B: Polygon-based Instance Segmentation
    # Model examples:
    #   - Mask R-CNN
    #
    # Annotation source:
    #   gtFine_polygons.json
    # ========================================================

    polygon_instance_datasets, polygon_instance_loaders = build_cityscapes_maskrcnn_dataloaders(
        gt_fine_root=gt_fine_root,
        left_img_root=left_img_root,
        target_source="polygon",
        batch_size=2,
        num_workers=0,
        min_area=50,
        resize=None,
        verbose=True,
    )

    polygon_instance_train_loader = polygon_instance_loaders["train"]

    check_one_batch(
        polygon_instance_train_loader,
        name="Polygon instance train loader",
    )

    plot_loader_samples_with_boxes(
        polygon_instance_train_loader,
        n_samples=4,
        alpha=0.45,
        title="Cityscapes Polygon Instance Segmentation: Masks and Bounding Boxes",
    )


# In[ ]:





# In[ ]:





# In[10]:


print('='*100)
print('Task Completed')
print('='*100)


# In[ ]:




