# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NhanVienExtend(models.Model):
    _inherit = 'nhan_vien'
    
    cong_viec_ids = fields.One2many('cong_viec', 'nguoi_thuc_hien_id', string="Công việc")
    so_luong_cong_viec = fields.Integer("Số lượng công việc", compute="_compute_so_luong_cong_viec", store=True)
    
    @api.depends('cong_viec_ids')
    def _compute_so_luong_cong_viec(self):
        for record in self:
            record.so_luong_cong_viec = len(record.cong_viec_ids)
