```markdown
# Bug Report – Order Cancellation Failure

**Title**  
worst app ever because you can't even do cancellation of you  

**Feature Area**  
order_tracking  

**Priority**  
0.51 (moderate) – higher than baseline error rate (1.5x) and affecting 25 reviews  

---

## Description  

Users are unable to cancel orders once they have been placed.  
When attempting to cancel, the system returns a bot response saying the cancellation is impossible, or in some cases the order incorrectly shows as *delivered* even after the cancellation request. This leads to high frustration, negative reviews, and a degraded user experience.

---

## Likely Reproduction Steps (inferred)

1. **Login** to the app and navigate to the *Order History* or *Cart* screen.  
2. **Place a new order** for a food item.  
3. **Navigate** to the order details page.  
4. Tap the **“Cancel Order”** button.  
5. Observe the system’s response:
   - Either a bot reply such as “We can’t cancel this” or  
   - The order status changes to *Delivered