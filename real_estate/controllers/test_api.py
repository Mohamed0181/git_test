import json
from odoo import http
from odoo.http import request

class TestApi(http.Controller):
    @http.route("/test/api",type="http",methods=["POST"],auth="none",csrf=False)
    def test(self):
        print("Inside Method Test Api")
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return request.make_response(
                json.dumps({"message": "Property successfully created"}),
                headers=[("Content-Type", "application/json")]
            )
