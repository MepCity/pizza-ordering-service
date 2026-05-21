import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
  thresholds: {
    http_req_duration: ["p(95)<500"],
    checks: ["rate>0.95"]
  }
};

const baseUrl = __ENV.BASE_URL || "http://127.0.0.1:8000";

export default function () {
  const menuResponse = http.get(`${baseUrl}/menu`);
  check(menuResponse, {
    "menu status is 200": (response) => response.status === 200
  });

  const payload = JSON.stringify({
    customer_name: "k6 User",
    items: [
      {
        menu_item_id: 1,
        quantity: 1,
        extras: ["olive"]
      }
    ]
  });

  const orderResponse = http.post(`${baseUrl}/orders`, payload, {
    headers: {
      "Content-Type": "application/json"
    }
  });

  check(orderResponse, {
    "order status is 201": (response) => response.status === 201
  });

  const orderBody = orderResponse.json();
  const orderId = orderBody.id;

  const statusResponse = http.patch(
    `${baseUrl}/orders/${orderId}/status`,
    JSON.stringify({ status: "preparing" }),
    {
      headers: {
        "Content-Type": "application/json"
      }
    }
  );

  check(statusResponse, {
    "status update is 200": (response) => response.status === 200
  });

  sleep(1);
}
