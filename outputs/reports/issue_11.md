# Bug Report – Payment Gateway Notification Failure  
**Feature Area:** `payment_gateway`  
**Title:** “Sometimes if someone sends money there is no notification”  
**Review Count:** 6  
**Error Correlation:** **122.5×** baseline error rate  
**Priority Score:** **0.57** (Medium‑High)

---

## 1. Summary

When a user receives a money transfer, the app fails to send the expected push/notification/email to the recipient in a significant number of cases. This is causing confusion, missed payments, and user complaints.  

---

## 2. Detailed Description

- **Observed Behavior:**  
  - User A transfers ₹500 to User B.  
  - User B's device shows no notification or in‑app alert.  
  - The transaction still appears in User B's balance after a few minutes.  
- **Reported by:**  
  - “sometimes if someone sending money there is no notification”  
