```markdown
# Bug Report – Cluster ID #CR-2026-0418
**Title:**  
Not issuing refund despite wrong order delivery

**Feature Area:**  
Checkout / Refund Processing

**Priority:**  
**Medium‑High** (Priority Score = 0.65)

**Severity:**  
High – multiple users report financial loss and loss of trust

---

## 1. Description

Customers who receive a wrong product or an empty order are not getting a full refund through the app. The refund appears in the order history but is never applied to the user’s wallet or account balance. In several cases, the refund is issued as a coupon that fails to redeem, or the refund is never processed at all, resulting in duplicate charges.  

The issue appears consistently across both Android and iOS clients, and is linked to an elevated error correlation (93 × baseline error rate).

---

## 2. Likely Reproduction Steps

1. **Place an order** for a single item (e.g., a pizza).  
2. **Receive the wrong item** (e.g., a salad) or an empty delivery.  
3. **Open the order details** and tap the **“Request Refund”** button.  
4. **Confirm refund request**.  
5. **Wait for the refund to be processed** (usually 5–15 min).  
6. **Check wallet balance** or attempt to redeem the received refund coupon.

*Observations:*  
- The order status updates to **“Refunded”** in the UI, but the wallet remains unchanged.  
- The