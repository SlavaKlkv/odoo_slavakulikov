import random
import string

from odoo import api, fields, models
from odoo.exceptions import ValidationError


def _generate_random_letters(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


class SaleOrder(models.Model):
    _inherit = "sale.order"

    responsible_employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Ответственный за выдачу товара",
        required=True,
    )
    new_field = fields.Char(
        string="New Field",
        default=lambda self: _generate_random_letters(10),
    )

    @api.onchange("order_line", "date_order")
    def _onchange_new_field_from_date_and_total(self):
        for order in self:
            if order.order_line:
                order.new_field = (
                    f"{fields.Datetime.to_string(order.date_order)} + "
                    f"{order.amount_total:.2f}"
                )

    @api.onchange("new_field")
    def _onchange_new_field_length_warning(self):
        if self.new_field and len(self.new_field) > 30:
            return {
                "warning": {
                    "title": "Ошибка",
                    "message": "Длина текста должна быть меньше 30 символов!",
                }
            }
        return None

    @api.constrains("new_field")
    def _check_new_field_length(self):
        for order in self:
            if order.new_field and len(order.new_field) > 30:
                raise ValidationError("Длина текста должна быть меньше 30 символов!")
