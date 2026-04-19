import json
from odoo import http
from odoo.http import request


class PropertyApi(http.Controller):
    @http.route("/v2/property",type="http",auth="none",methods=["POST"],csrf=False)
    def property_post(self):

        print("Inside Method Post")
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get("name"):
            return request.make_json_response({
                "message": "Property Name Required",
            },status=400)
        try:
            res = request.env['property'].sudo().create(vals)
            if res :
                return request.make_json_response({
                    "message": "Property successfully created",
                    "id": res.id,
                    "name": res.name,
                })

        except Exception as error:
            return request.make_json_response({
                "message":error,
            },status=400)



    # update Method API
    @http.route("/v1/property/<int:property_id>",type="http",auth="none",methods=["PUT"],csrf=False)
    def property_put(self,property_id):
        property_id = request.env['property'].sudo().search([('id', '=', property_id)])
        if not property_id:
            return request.make_json_response({
                "message": "Property ID not found",
            })
        try :
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return request.make_json_response({
                "message":"Property successfully updated",
                "id": property_id.id,
                "name": property_id.name,
                "expecting_price": property_id.expecting_price,
            },status=200)
        except Exception as error:
            return request.make_json_response({
                "message":error,
            })


    # Read Method api
    @http.route("/v1/property/<int:property_id>",type="http",auth="none",methods=["GET"],csrf=False)
    def property_get(self,property_id):
        try:
            property_id = request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return request.make_json_response({
                    "error": "Property ID not found",
                })
            return request.make_json_response({
                "id":property_id.id,
                "name":property_id.name,
                "postcode":property_id.postcode,
                "ref":property_id.ref,
                "garage":property_id.garage,
                "garden":property_id.garden,
                "description":property_id.description,

            },status=200)
        except Exception as error:
            return request.make_json_response({
                "message":error,
            })







    @http.route("/v1/property/json",methods="POST",type="json",auth="none",csrf=False)
    def property_json_post(self):
        args = request.httprequest.data.decode()
        vals= json.loads(args)
        res  = request.env['property'].sudo().create(vals)
        if res :
            return [{
                "message": "Property successfully created",
            }]