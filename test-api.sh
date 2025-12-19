#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

# Read API_TOKEN from .env (your file uses API_TOKEN=...)
API_TOKEN="$(grep -E '^API_TOKEN=' .env | head -n1 | cut -d= -f2- | tr -d '\r')"

AUTH_HEADER="Authorization: Bearer ${API_TOKEN}"

# Create a tiny valid PDF if it doesn't exist
PDF_FILE="${PDF_FILE:-./sample.pdf}"
if [ ! -f "$PDF_FILE" ]; then
  cat > "$PDF_FILE" <<'PDF'
%PDF-1.4
1 0 obj<<>>endobj
2 0 obj<< /Type /Catalog /Pages 3 0 R >>endobj
3 0 obj<< /Type /Pages /Kids [4 0 R] /Count 1 >>endobj
4 0 obj<< /Type /Page /Parent 3 0 R /MediaBox [0 0 200 200] /Contents 5 0 R >>endobj
5 0 obj<< /Length 44 >>stream
BT /F1 18 Tf 20 100 Td (Hello PDF) Tj ET
endstream endobj
xref
0 6
0000000000 65535 f
trailer<< /Root 2 0 R /Size 6 >>
startxref
0
%%EOF
PDF
fi

echo "== 1) Health check =="
curl -sS -i "${BASE_URL}/healthz" | sed -n '1,12p'
echo

echo "== 2) Create profile (POST /api/v1/profiles) =="
PROFILE_JSON="$(curl -sS -X POST "${BASE_URL}/api/v1/profiles" \
  -H "${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "johnsmith@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "github_url": "https://github.com/example"
  }')"

echo "$PROFILE_JSON" | python3 -m json.tool
PROFILE_ID="$(echo "$PROFILE_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')"
echo "PROFILE_ID=$PROFILE_ID"
echo

echo "== 3) Upload submission (POST /api/v1/submissions?profile_id=...) =="
SUB_JSON="$(curl -sS -X POST "${BASE_URL}/api/v1/submissions?profile_id=${PROFILE_ID}" \
  -H "${AUTH_HEADER}" \
  -F "file=@${PDF_FILE};type=application/pdf")"

echo "$SUB_JSON" | python3 -m json.tool
SUB_ID="$(echo "$SUB_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')"
echo "SUBMISSION_ID=$SUB_ID"
echo

echo "== 4) Submit (POST /api/v1/submissions/{id}/submit) =="
curl -sS -X POST "${BASE_URL}/api/v1/submissions/${SUB_ID}/submit" \
  -H "${AUTH_HEADER}" | python3 -m json.tool
echo

echo "== 5) Poll status (GET /api/v1/submissions/{id}) until COMPLETED =="
for i in {1..10}; do
  STATUS_JSON="$(curl -sS -X GET "${BASE_URL}/api/v1/submissions/${SUB_ID}" -H "${AUTH_HEADER}")"
  STATUS="$(echo "$STATUS_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("status"))')"
  echo "Attempt $i => status=$STATUS"
  if [ "$STATUS" = "COMPLETED" ]; then
    echo "$STATUS_JSON" | python3 -m json.tool
    break
  fi
  sleep 1
done
echo

echo "== 6) Unauthorized test (should be 401) =="
curl -sS -i -X POST "${BASE_URL}/api/v1/profiles" \
  -H "Content-Type: application/json" \
  -d '{"email":"johnsmith2@example.com","first_name":"John","last_name":"Smith"}' | sed -n '1,20p'
echo
