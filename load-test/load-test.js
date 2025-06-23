import http from 'k6/http';
import { check } from 'k6';
import { sleep } from 'k6';

export let options = {
  stages: [
    { duration: '1m', target: 10 },
    { duration: '4m', target: 10 },
  ],
};

export default function () {
  const url = 'http://192.168.49.2:30080/collect';
  const targetIndex = __ENV.INDEX || 'default-logs'; // Get index from env or use default
  
  const payload = JSON.stringify({
    message: `log message ${Math.random()}`,
    timestamp: new Date().toISOString()
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'X-Elastic-Index': targetIndex  // Custom header for index specification
    }
  };

  const res = http.post(url, payload, params);
  
  check(res, {
    'index acknowledgment': (r) => r.json().index === targetIndex
  });
  
  sleep(0.1);
}
