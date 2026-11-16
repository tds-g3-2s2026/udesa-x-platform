#!/usr/bin/env bash
# Writes the state of the deployed services to $1 as JSON: replicas, pod resources
# and autoscaler state. Run it before and after a load run to see what scaled.
set -euo pipefail

: "${NAMESPACE:?Definí NAMESPACE.}"
salida="${1:?Indicá el archivo de salida.}"

deployments=$(kubectl get deployment users-api posts-api api-gateway -n "$NAMESPACE" -o json |
  jq '[.items[] | {
    name: .metadata.name,
    image: .spec.template.spec.containers[0].image,
    replicas: .status.replicas,
    ready: .status.readyReplicas,
    resources: .spec.template.spec.containers[0].resources
  }]')

autoscalers=$(kubectl get hpa -n "$NAMESPACE" -o json |
  jq '[.items[] | {
    name: .metadata.name,
    min: .spec.minReplicas,
    max: .spec.maxReplicas,
    current: .status.currentReplicas,
    desired: .status.desiredReplicas,
    metrics: .status.currentMetrics
  }]')

jq -n --argjson deployments "$deployments" --argjson autoscalers "$autoscalers" \
  '{recorded_at: (now | todate), deployments: $deployments, autoscalers: $autoscalers}' >"$salida"
