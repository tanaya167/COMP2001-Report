from marshmallow import Schema, fields, validate

#POST /login
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))
#POST /admin-login
class AdminLoginSchema(Schema):
    email = fields.Email(data_key="Email_Address", required=True)
    role = fields.Str(required=True, validate=validate.Equal('admin'))
#DELETE /trails/<int:trail_id>/locationpoints/<order_no>
class DeleteLocationPointSchema(Schema):
    trail_id = fields.Int(required=True, validate=validate.Range(min=1))
    order_no = fields.Int(data_key="Order_no", required=True, validate=validate.Range(min=1))
#POST /trails/<int:trail_id>/locationpoints
class AddLocationPointSchema(Schema):
    trail_id = fields.Int(required=True, validate=validate.Range(min=1))
    location_point = fields.Int(data_key="Location_Point", required=True, validate=validate.Range(min=1))
    order_no = fields.Int(data_key="Order_no", required=True, validate=validate.Range(min=1))
    



