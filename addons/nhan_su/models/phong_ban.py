# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PhongBan(models.Model):
    _name: str = 'phong_ban'
    _description: str = 'Bảng chứa thông tin phòng ban'
    _rec_name: str = 'ten_phong_ban'
    _order: str = 'ma_phong_ban'

    ma_phong_ban = fields.Char("Mã phòng ban", readonly=True, copy=False)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    mo_ta = fields.Text("Mô tả")
    so_luong_nhan_vien = fields.Integer("Số lượng nhân viên", compute="_compute_so_luong_nhan_vien", store=True)
    nhan_vien_ids = fields.One2many('nhan_vien', 'phong_ban_id', string="Nhân viên")

    @api.depends('nhan_vien_ids')
    def _compute_so_luong_nhan_vien(self) -> None:
        for record in self:
            record.so_luong_nhan_vien = len(record.nhan_vien_ids)

    @api.model
    def create(self, vals):
        # Tự động tạo mã phòng ban dạng PB0001, PB0002...
        if not vals.get('ma_phong_ban'):
            counter = 1
            code = f"PB{counter:04d}"
            while self.search([('ma_phong_ban', '=', code)], limit=1):
                counter += 1
                code = f"PB{counter:04d}"
            vals['ma_phong_ban'] = code
        return super().create(vals)
