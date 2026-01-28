# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class CongViec(models.Model):
    _name = 'cong_viec'
    _description = 'Quản lý công việc và tương tác khách hàng'
    _rec_name = 'tieu_de'
    _order = 'ngay_bat_dau desc'

    ma_cong_viec = fields.Char("Mã công việc", readonly=True, copy=False)
    tieu_de = fields.Char("Tiêu đề", required=True)
    
    # Loại công việc
    loai_cong_viec = fields.Selection([
        ('goi_dien', 'Gọi điện'),
        ('gui_bao_gia', 'Gửi báo giá'),
        ('lich_hen', 'Lịch hẹn'),
        ('gap_mat', 'Gặp mặt'),
        ('email', 'Email'),
        ('khac', 'Khác')
    ], string="Loại công việc", required=True, default='goi_dien')
    
    # Thông tin khách hàng
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)
    du_an_id = fields.Many2one('du_an', string="Dự án")
    
    # Thời gian
    ngay_bat_dau = fields.Datetime("Ngày bắt đầu", default=fields.Datetime.now)
    ngay_hoan_thanh = fields.Datetime("Ngày hoàn thành")
    thoi_luong = fields.Float("Thời lượng (giờ)")
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy')
    ], string="Trạng thái", default='moi', required=True)
    
    # Mức độ ưu tiên
    muc_do_uu_tien = fields.Selection([
        ('thap', 'Thấp'),
        ('trung_binh', 'Trung bình'),
        ('cao', 'Cao'),
        ('khan_cap', 'Khẩn cấp')
    ], string="Mức độ ưu tiên", default='trung_binh')
    
    # Phòng ban phụ trách & nhân viên được gán tự động
    phong_ban_phu_trach_id = fields.Many2one('phong_ban', string="Phòng ban phụ trách", required=True)
    nguoi_thuc_hien_id = fields.Many2one('nhan_vien', string="Nhân viên được gán", readonly=True)
    
    # Nội dung công việc
    mo_ta = fields.Text("Mô tả")
    ket_qua = fields.Text("Kết quả")
    
    # Thông tin báo giá (nếu là gửi báo giá)
    gia_tri_bao_gia = fields.Float("Giá trị báo giá")
    trang_thai_bao_gia = fields.Selection([
        ('chua_gui', 'Chưa gửi'),
        ('da_gui', 'Đã gửi'),
        ('dong_y', 'Đồng ý'),
        ('tu_choi', 'Từ chối')
    ], string="Trạng thái báo giá")
    
    # Ghi chú
    ghi_chu = fields.Text("Ghi chú")
    
    # Google Calendar Integration
    google_calendar_event_id = fields.Char("Google Calendar Event ID", readonly=True, copy=False)
    sync_to_google_calendar = fields.Boolean("Đồng bộ với Google Calendar", default=True)
    last_sync_date = fields.Datetime("Lần đồng bộ cuối", readonly=True)
    
    @api.onchange('phong_ban_phu_trach_id')
    def _onchange_phong_ban_phu_trach(self):
        """Auto-assign free employee when department is selected."""
        if self.phong_ban_phu_trach_id:
            employee = self._find_free_employee(self.phong_ban_phu_trach_id)
            if employee:
                self.nguoi_thuc_hien_id = employee
    
    @api.model
    def create(self, vals):
        # Tạo mã công việc tự động
        loai_map = {
            'goi_dien': 'GD',
            'gui_bao_gia': 'BG',
            'lich_hen': 'LH',
            'gap_mat': 'GM',
            'email': 'EM',
            'khac': 'KH'
        }
        
        loai = vals.get('loai_cong_viec', 'khac')
        ma_loai = loai_map.get(loai, 'CV')
        
        # Tìm mã duy nhất
        counter = 1
        ma_cong_viec = f"{ma_loai}{counter:04d}"
        while self.search([('ma_cong_viec', '=', ma_cong_viec)], limit=1):
            counter += 1
            ma_cong_viec = f"{ma_loai}{counter:04d}"
        
        vals['ma_cong_viec'] = ma_cong_viec

        # Gán nhân viên rảnh trong phòng ban được chọn
        dept_id = vals.get('phong_ban_phu_trach_id')
        if dept_id and not vals.get('nguoi_thuc_hien_id'):
            employee = self._find_free_employee(self.env['phong_ban'].browse(dept_id))
            if employee:
                vals['nguoi_thuc_hien_id'] = employee.id
        
        record = super(CongViec, self).create(vals)
        
        # Đồng bộ với Google Calendar sau khi tạo
        if record.sync_to_google_calendar and record.ngay_bat_dau:
            record._sync_google_calendar_event()
        
        return record

    def write(self, vals):
        # Nếu đổi phòng ban và chưa có người, tự gán lại
        if 'phong_ban_phu_trach_id' in vals and not vals.get('nguoi_thuc_hien_id'):
            dept_id = vals.get('phong_ban_phu_trach_id') or self.phong_ban_phu_trach_id.id
            if dept_id:
                employee = self._find_free_employee(self.env['phong_ban'].browse(dept_id))
                if employee:
                    vals['nguoi_thuc_hien_id'] = employee.id
        
        result = super().write(vals)
        
        # Đồng bộ với Google Calendar nếu có thay đổi về thời gian hoặc tiêu đề
        sync_fields = ['ngay_bat_dau', 'ngay_hoan_thanh', 'tieu_de', 'mo_ta', 'trang_thai']
        if any(field in vals for field in sync_fields):
            for record in self:
                if record.sync_to_google_calendar and record.ngay_bat_dau:
                    record._sync_google_calendar_event()
        
        return result

    def _find_free_employee(self, department):
        """Tìm nhân viên trong phòng ban chưa phụ trách công việc/dự án đang mở."""
        if not department:
            return False
        employees = self.env['nhan_vien'].search([('phong_ban_id', '=', department.id)])
        for emp in employees:
            active_tasks = self.env['cong_viec'].search_count([
                ('nguoi_thuc_hien_id', '=', emp.id),
                ('trang_thai', 'in', ['moi', 'dang_thuc_hien'])
            ])
            active_projects = self.env['du_an'].search_count([
                ('nguoi_phu_trach_id', '=', emp.id),
                ('trang_thai', 'in', ['ke_hoach', 'dang_tien_hanh', 'tam_dung'])
            ])
            if active_tasks == 0 and active_projects == 0:
                return emp
        return employees[:1] if employees else False
    
    def action_bat_dau(self):
        """Bắt đầu công việc"""
        self.write({'trang_thai': 'dang_thuc_hien'})
    
    def action_hoan_thanh(self):
        """Hoàn thành công việc"""
        self.write({
            'trang_thai': 'hoan_thanh',
            'ngay_hoan_thanh': fields.Datetime.now()
        })
    
    def action_huy(self):
        """Hủy công việc"""
        self.write({'trang_thai': 'huy'})
    
    def _sync_google_calendar_event(self):
        """Đồng bộ công việc với Google Calendar"""
        self.ensure_one()
        
        if not self.sync_to_google_calendar:
            return
        
        try:
            # Sử dụng calendar.event model của Odoo
            if self.google_calendar_event_id:
                # Cập nhật event hiện có
                self._update_google_event()
            else:
                # Tạo event mới
                self._create_google_event()
            
            self.sudo().write({'last_sync_date': fields.Datetime.now()})
            
        except Exception as e:
            _logger.error(f"Lỗi khi đồng bộ với Google Calendar: {str(e)}")
    
    def _prepare_google_event_data(self):
        """Chuẩn bị dữ liệu event cho Google Calendar"""
        self.ensure_one()
        
        # Xác định start và end time
        start_time = self.ngay_bat_dau
        end_time = self.ngay_hoan_thanh or start_time
        
        # Tạo mô tả chi tiết
        description_parts = []
        if self.ma_cong_viec:
            description_parts.append(f"Mã: {self.ma_cong_viec}")
        if self.loai_cong_viec:
            loai_dict = dict(self._fields['loai_cong_viec'].selection)
            description_parts.append(f"Loại: {loai_dict.get(self.loai_cong_viec)}")
        if self.khach_hang_id:
            description_parts.append(f"Khách hàng: {self.khach_hang_id.ten_khach_hang}")
        if self.nguoi_thuc_hien_id:
            description_parts.append(f"Người thực hiện: {self.nguoi_thuc_hien_id.ho_ten_day_du}")
        if self.mo_ta:
            description_parts.append(f"\nMô tả: {self.mo_ta}")
        
        event_data = {
            'summary': f"[{self.ma_cong_viec}] {self.tieu_de}",
            'description': '\n'.join(description_parts),
            'start': {
                'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
            'end': {
                'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 ngày trước
                    {'method': 'popup', 'minutes': 30},  # 30 phút trước
                ],
            },
        }
        
        # Thêm màu sắc theo mức độ ưu tiên
        color_map = {
            'khan_cap': '11',  # Đỏ
            'cao': '9',        # Xanh dương đậm
            'trung_binh': '5', # Vàng
            'thap': '2',       # Xanh lá
        }
        if self.muc_do_uu_tien:
            event_data['colorId'] = color_map.get(self.muc_do_uu_tien, '5')
        
        return event_data
    
    def _create_google_event(self):
        """Tạo event mới trong Google Calendar"""
        self.ensure_one()
        
        try:
            event_data = self._prepare_google_event_data()
            
            # Tạo calendar.event
            calendar_event = self.env['calendar.event'].sudo().create({
                'name': event_data['summary'],
                'description': event_data.get('description', ''),
                'start': self.ngay_bat_dau,
                'stop': self.ngay_hoan_thanh or self.ngay_bat_dau,
                'user_id': self.env.user.id,
                'privacy': 'public',
            })
            
            # Sync với Google Calendar
            if calendar_event:
                calendar_event.write({'need_sync': True})
                
                # Lấy Google event ID sau khi sync (nếu có)
                if hasattr(calendar_event, 'google_id') and calendar_event.google_id:
                    self.sudo().write({'google_calendar_event_id': calendar_event.google_id})
                else:
                    # Lưu calendar event ID tạm thời
                    self.sudo().write({'google_calendar_event_id': f'odoo_{calendar_event.id}'})
            
            _logger.info(f"Đã tạo Google Calendar event cho công việc {self.ma_cong_viec}")
            
        except Exception as e:
            _logger.error(f"Lỗi khi tạo Google Calendar event: {str(e)}")
            raise
    
    def _update_google_event(self):
        """Cập nhật event hiện có trong Google Calendar"""
        self.ensure_one()
        
        try:
            event_data = self._prepare_google_event_data()
            
            # Tìm calendar event
            calendar_event = None
            
            # Thử tìm theo google_id trước
            if self.google_calendar_event_id and not self.google_calendar_event_id.startswith('odoo_'):
                calendar_event = self.env['calendar.event'].sudo().search([
                    ('google_id', '=', self.google_calendar_event_id)
                ], limit=1)
            
            # Nếu không có google_id hoặc không tìm thấy, tìm theo odoo ID
            if not calendar_event and self.google_calendar_event_id and self.google_calendar_event_id.startswith('odoo_'):
                event_id = int(self.google_calendar_event_id.replace('odoo_', ''))
                calendar_event = self.env['calendar.event'].sudo().browse(event_id)
                if not calendar_event.exists():
                    calendar_event = None
            
            if calendar_event:
                calendar_event.sudo().write({
                    'name': event_data['summary'],
                    'description': event_data.get('description', ''),
                    'start': self.ngay_bat_dau,
                    'stop': self.ngay_hoan_thanh or self.ngay_bat_dau,
                    'need_sync': True,
                })
                _logger.info(f"Đã cập nhật Google Calendar event cho công việc {self.ma_cong_viec}")
            else:
                # Nếu không tìm thấy event, tạo mới
                self.sudo().write({'google_calendar_event_id': False})
                self._create_google_event()
                
        except Exception as e:
            _logger.error(f"Lỗi khi cập nhật Google Calendar event: {str(e)}")
            raise
    
    def action_sync_google_calendar(self):
        """Action button để đồng bộ thủ công với Google Calendar"""
        for record in self:
            if not record.ngay_bat_dau:
                raise UserError(_("Vui lòng nhập ngày bắt đầu trước khi đồng bộ với Google Calendar."))
            record._sync_google_calendar_event()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Thành công'),
                'message': _('Đã đồng bộ với Google Calendar'),
                'type': 'success',
                'sticky': False,
            }
        }
    
    def unlink(self):
        """Xóa event khỏi Google Calendar khi xóa công việc"""
        for record in self:
            if record.google_calendar_event_id:
                try:
                    calendar_event = self.env['calendar.event'].sudo().search([
                        ('google_id', '=', record.google_calendar_event_id)
                    ], limit=1)
                    if calendar_event:
                        calendar_event.sudo().unlink()
                except Exception as e:
                    _logger.error(f"Lỗi khi xóa Google Calendar event: {str(e)}")
        
        return super().unlink()
