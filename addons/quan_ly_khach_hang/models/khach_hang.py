# -*- coding: utf-8 -*-
from odoo import models, fields, api
import unicodedata


class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Quản lý thông tin khách hàng'
    _rec_name = 'ten_khach_hang'

    ma_khach_hang = fields.Char("Mã khách hàng", readonly=True, copy=False)
    ten_khach_hang = fields.Char("Tên khách hàng", required=True)
    loai_khach_hang = fields.Selection([
        ('ca_nhan', 'Cá nhân'),
        ('doanh_nghiep', 'Doanh nghiệp')
    ], string="Loại khách hàng", default='ca_nhan', required=True)
    
    # Thông tin liên hệ
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại", required=True)
    dia_chi = fields.Text("Địa chỉ")
    ngay_sinh = fields.Date("Ngày sinh")
    
    # Thông tin doanh nghiệp
    ma_so_thue = fields.Char("Mã số thuế")
    website = fields.Char("Website")
    
    trang_thai = fields.Selection([
        ('tiem_nang', 'Tiềm năng'),
        ('da_lien_he', 'Đã liên hệ'),
        ('dang_dam_phan', 'Đang đàm phán'),
        ('thanh_cong', 'Thành công'),
        ('that_bai', 'Thất bại')
    ], string="Trạng thái", default='tiem_nang')
    
    # Người phụ trách
    nguoi_phu_trach_id = fields.Many2one('nhan_vien', string="Người phụ trách")
    
    # Ghi chú
    ghi_chu = fields.Text("Ghi chú")
    
    def _remove_accents(self, text):
        """Bỏ dấu tiếng Việt"""
        text = text.replace('Đ', 'D').replace('đ', 'd')
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore').decode('utf-8')
        return text
    
    @api.onchange('ten_khach_hang')
    def _onchange_ma_khach_hang(self):
        """Hiển thị preview mã khách hàng khi nhập tên"""
        if self.ten_khach_hang:
            ten_khong_dau = self._remove_accents(self.ten_khach_hang)
            ma_co_ban = ''.join([word[0].upper() for word in ten_khong_dau.split()])
            ma_co_ban = 'KH' + ma_co_ban
            
            # Tìm mã duy nhất
            counter = 1
            ma_khach_hang = f"{ma_co_ban}{counter:02d}"
            while self.search([('ma_khach_hang', '=', ma_khach_hang), ('id', '!=', self.id or 0)], limit=1):
                counter += 1
                ma_khach_hang = f"{ma_co_ban}{counter:02d}"
            
            self.ma_khach_hang = ma_khach_hang
    
    @api.model
    def create(self, vals):
        if vals.get('ten_khach_hang'):
            # Tạo mã khách hàng từ tên
            ten_khong_dau = self._remove_accents(vals['ten_khach_hang'])
            ma_co_ban = ''.join([word[0].upper() for word in ten_khong_dau.split()])
            
            # Thêm KH vào đầu
            ma_co_ban = 'KH' + ma_co_ban
            
            # Tìm mã duy nhất
            counter = 1
            ma_khach_hang = f"{ma_co_ban}{counter:02d}"
            while self.search([('ma_khach_hang', '=', ma_khach_hang)], limit=1):
                counter += 1
                ma_khach_hang = f"{ma_co_ban}{counter:02d}"
            
            vals['ma_khach_hang'] = ma_khach_hang
        
        records = super(KhachHang, self).create(vals)
        records._add_birthday_campaign_if_today()
        return records

    def write(self, vals):
        res = super(KhachHang, self).write(vals)
        self._add_birthday_campaign_if_today()
        return res

    def _add_birthday_campaign_if_today(self, today=None):
        """Đưa khách có sinh nhật hôm nay vào chiến dịch sinh nhật (tạo nếu chưa có)."""
        today = today or fields.Date.context_today(self)
        if not today:
            return

        birthday_customers = self.filtered(
            lambda c: c.ngay_sinh and (c.ngay_sinh.month, c.ngay_sinh.day) == (today.month, today.day)
        )
        if not birthday_customers:
            return

        Campaign = self.env['chien_dich'].sudo()
        for customer in birthday_customers:
            campaign_name = f"Mừng sinh nhật {customer.ten_khach_hang}"
            campaign = Campaign.search([('ten_chien_dich', '=', campaign_name)], limit=1)
            if not campaign:
                campaign = Campaign.create({
                    'ten_chien_dich': campaign_name,
                    'loai_chien_dich': 'khac',
                    'ngay_bat_dau': today,
                    'trang_thai': 'dang_chay',
                    'muc_tieu': f'Chăm sóc sinh nhật cho {customer.ten_khach_hang}.',
                    'khach_hang_ids': [(6, 0, [customer.id])],
                })
            else:
                campaign.write({
                    'ten_chien_dich': campaign_name,
                    'khach_hang_ids': [(4, customer.id)],
                })

    @api.model
    @api.model
    def _cron_add_birthdays_to_campaign(self):
        """Cron hằng ngày: gom khách sinh nhật hôm nay vào chiến dịch sinh nhật."""
        today = fields.Date.context_today(self)
        if not today:
            return

        birthday_customers = self.search([('ngay_sinh', '!=', False)])
        birthday_customers._add_birthday_campaign_if_today(today=today)
