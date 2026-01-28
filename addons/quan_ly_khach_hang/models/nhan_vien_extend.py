# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NhanVienExtend(models.Model):
    _inherit = 'nhan_vien'
    
    khach_hang_ids = fields.One2many('khach_hang', 'nguoi_phu_trach_id', string="Khách hàng phụ trách")
    so_luong_khach_hang = fields.Integer("Số lượng khách hàng", compute="_compute_so_luong_khach_hang", store=True)
    
    @api.depends('khach_hang_ids')
    def _compute_so_luong_khach_hang(self):
        for record in self:
            record.so_luong_khach_hang = len(record.khach_hang_ids)
