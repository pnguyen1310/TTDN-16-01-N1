# -*- coding: utf-8 -*-
import json
import requests

from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource


class ChatbotNoiQuyMessage(models.Model):
    """Model lưu trữ tin nhắn (tương thích dữ liệu cũ)"""
    _name = "chatbot.noiquy.message"
    _description = "Chatbot Nội Quy Message"
    _order = "id desc"

    message = fields.Text(string="Tin nhắn")
    timestamp = fields.Datetime(string="Thời gian")


class ChatbotNoiQuyChat(models.Model):
    _name = "chatbot.noiquy.chat"
    _description = "Chatbot Nội Quy (Groq)"
    _order = "id desc"

    question = fields.Text(string="Câu hỏi", required=True)
    answer = fields.Text(string="Trả lời", readonly=True)
    last_error = fields.Text(string="Lỗi (nếu có)", readonly=True)

    # Model Groq mặc định (llama-3.1-8b-instant - nhanh và nhẹ)
    GROQ_MODEL = "llama-3.1-8b-instant"

    def _get_api_key(self):
        key = self.env["ir.config_parameter"].sudo().get_param("groq.api.key")
        if not key:
            raise UserError(
                _(
                    "Chưa cấu hình Groq API Key.\n"
                    "Vào: Thiết lập → Kỹ thuật → Thông số → Thông số hệ thống\n"
                    "Tạo: Từ khóa = groq.api.key, Giá trị = API key của Groq."
                )
            )
        return key.strip()

    def _load_policy_text(self):
        # File nội quy demo: data/noi_quy.md (bạn sửa nội dung file này theo doanh nghiệp)
        path = get_module_resource("chatbot_noiquy", "data", "noi_quy.md")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def _call_groq(self, prompt_text, system_text=None, model_name=None, timeout=30):
        api_key = self._get_api_key()
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_text:
            messages.append({"role": "system", "content": system_text})
        messages.append({"role": "user", "content": prompt_text})

        payload = {
            "model": model_name or self.GROQ_MODEL,
            "messages": messages,
            "temperature": 0.2,
        }

        try:
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
        except requests.RequestException as e:
            raise UserError(_("Không gọi được Groq API: %s") % str(e))

        if resp.status_code != 200:
            raise UserError(_("Groq API lỗi (%s): %s") % (resp.status_code, resp.text))

        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            return json.dumps(data, ensure_ascii=False, indent=2)

    def _clean_markdown(self, text):
        """Chuyển đổi markdown thành plain text"""
        import re
        # Remove bold/italic markers
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # **text** -> text
        text = re.sub(r'\*(.+?)\*', r'\1', text)      # *text* -> text
        text = re.sub(r'__(.+?)__', r'\1', text)      # __text__ -> text
        # Remove markdown headers
        text = re.sub(r'^#+\s', '', text, flags=re.MULTILINE)  # ### text -> text
        return text

    def action_ask(self):
        for rec in self:
            rec.answer = False
            rec.last_error = False

            prompt = (rec.question or "").strip()
            if not prompt:
                rec.last_error = "Vui lòng nhập câu hỏi."
                continue

            policy = rec._load_policy_text()

            system_text = (
                "Bạn là một trợ lý thông minh. "
                "Nếu có nội quy công ty được cung cấp, hãy ưu tiên trả lời dựa trên nội quy. "
                "Nếu câu hỏi không liên quan đến nội quy, bạn vẫn có thể trả lời những câu hỏi khác một cách hữu ích. "
                "Trả lời ngắn gọn, rõ ràng, tiếng Việt."
            )

            if policy:
                prompt = (
                    f"CÂU HỎI: {prompt}\n\n"
                    f"NỘI QUY CÔNG TY (tham khảo):\n{policy}\n\n"
                    "Hãy trả lời câu hỏi trên. Ưu tiên sử dụng nội quy nếu liên quan."
                )

            try:
                rec.answer = rec._call_groq(prompt_text=prompt, system_text=system_text)
                rec.answer = rec._clean_markdown(rec.answer)
            except Exception as e:
                rec.answer = False
                rec.last_error = str(e)

        return True
