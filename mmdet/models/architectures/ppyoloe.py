#! /usr/bin/env python
# coding=utf-8
# ================================================================
#
#   Author      : miemie2013
#   Created date:
#   Description :
#
# ================================================================
import torch


class PPYOLOE(torch.nn.Module):
    def __init__(self, backbone, neck, yolo_head):
        super(PPYOLOE, self).__init__()
        self.backbone = backbone
        self.neck = neck
        self.yolo_head = yolo_head

    def forward(self, x, scale_factor=None, targets=None):
        '''
        获得损失（训练）、推理 都要放在forward()中进行，否则DDP会计算错误结果。
        '''
        body_feats = self.backbone(x)
        fpn_feats = self.neck(body_feats)
        out = self.yolo_head(fpn_feats, targets)
        if self.training:
            return out
        else:
            out = self.yolo_head.post_process(out, scale_factor)
            return out

    def add_param_group(self, param_groups, base_lr, base_wd, need_clip, clip_norm):
        self.backbone.add_param_group(param_groups, base_lr, base_wd, need_clip, clip_norm)
        self.neck.add_param_group(param_groups, base_lr, base_wd, need_clip, clip_norm)
        self.yolo_head.add_param_group(param_groups, base_lr, base_wd, need_clip, clip_norm)



