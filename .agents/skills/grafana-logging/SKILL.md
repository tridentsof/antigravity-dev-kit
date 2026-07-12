---
name: grafana-logging
description: Grafana dashboards and metrics logging
---

# Grafana Logging

> Metrics, dashboards, and alerting with Grafana.

---

## Key Metrics

### Application Metrics
| Metric | Description |
|--------|-------------|
| Request rate | Requests per second |
| Error rate | Errors per second |
| Duration | Response time percentiles |
| Active requests | Concurrent requests |

### Infrastructure Metrics
| Metric | Description |
|--------|-------------|
| CPU usage | Percentage used |
| Memory usage | Bytes used |
| Disk I/O | Read/write operations |
| Network | Bytes in/out |

---

## Prometheus Metrics (ASP.NET)

```csharp
// Install package
// dotnet add package prometheus-net.AspNetCore

// Program.cs
app.UseMetricServer();  // /metrics endpoint
app.UseHttpMetrics();   // HTTP request metrics
```

---

## Custom Metrics

```csharp
using Prometheus;

public class OrderService
{
    private static readonly Counter OrdersCreated = Metrics
        .CreateCounter("orders_created_total", "Total orders created");
    
    private static readonly Histogram OrderDuration = Metrics
        .CreateHistogram("order_duration_seconds", "Order processing time");
    
    public async Task CreateOrder(Order order)
    {
        using (OrderDuration.NewTimer())
        {
            await ProcessOrder(order);
            OrdersCreated.Inc();
        }
    }
}
```

---

## Dashboard Queries

```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

---

## Alerting

```yaml
# Alert rule
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: High error rate detected
```

---

## DO / DON'T

| ✅ Do | ❌ Don't |
|-------|---------|
| RED method (Rate, Error, Duration) | Track everything |
| Set alerting thresholds | Alert fatigue |
| Dashboard per service | One giant dashboard |
