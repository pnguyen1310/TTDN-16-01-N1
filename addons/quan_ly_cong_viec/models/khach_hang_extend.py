# -*- coding: utf-8 -*-
from odoo import models, fields, api


class KhachHangExtend(models.Model):
    _inherit = 'khach_hang'
    
    cong_viec_ids = fields.One2many('cong_viec', 'khach_hang_id', string="Công việc")
    so_luong_cong_viec = fields.Integer("Số lượng công việc", compute="_compute_so_luong_cong_viec", store=True)
    
    @api.depends('cong_viec_ids')
    def _compute_so_luong_cong_viec(self):
        for record in self:
            record.so_luong_cong_viec = len(record.cong_viec_ids)
