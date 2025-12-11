

from fastapi_mail import FastMail, MessageSchema
from app.config import EMAIL_CONFIG

# async def send_email(
#     email_to: str,
#     subject: str,
#     client_name: str,
#     order_number: str,
#     order_items: list,
#     order_total: float,
#     shipping_address: str
# ):
#     # Build HTML list of order items
#     items_html = "".join(
#         f"<tr>"
#         f"<td style='padding:8px;border:1px solid #ddd;'>{item['product_name']}</td>"
#         f"<td style='padding:8px;border:1px solid #ddd;text-align:center;'>{item['quantity']}</td>"
#         f"<td style='padding:8px;border:1px solid #ddd;text-align:right;'>${item['price']:.2f}</td>"
#         f"</tr>"
#         for item in order_items
#     )

#     html = f"""
#     <html>
#     <body>
#         <h2>Thank you for your purchase, {client_name}!</h2>
#         <p>Your order <strong>#{order_number}</strong> has been confirmed.</p>
#         <table style="width:100%; border-collapse: collapse;">
#             <thead>
#                 <tr>
#                     <th>Product</th>
#                     <th>Qty</th>
#                     <th>Price</th>
#                 </tr>
#             </thead>
#             <tbody>
#                 {items_html}
#             </tbody>
#         </table>
#         <h3>Total: ${order_total:.2f}</h3>
#         <p>Shipping Address: {shipping_address}</p>
#     </body>
#     </html>
#     """

#     message = MessageSchema(
#         subject=subject,
#         recipients=[email_to],  # ✅ use email_to
#         body=html,
#         subtype="html"
#     )

#     fm = FastMail(EMAIL_CONFIG)
#     await fm.send_message(message)


########################## GENERIC WAY########################

from fastapi_mail import FastMail, MessageSchema
from app.config import EMAIL_CONFIG

async def send_email(email_to: str, subject: str, body: str):
    """
    Generic email sender.
    Only sends what you pass in 'body'.
    Can be used for orders, verification, password reset, etc.
    """
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html"
    )
    fm = FastMail(EMAIL_CONFIG)
    await fm.send_message(message)