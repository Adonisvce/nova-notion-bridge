#!/bin/bash
echo "🔍 Validating requirements.txt..."

if ! [ -f requirements.txt ]; then
  echo "❌ requirements.txt not found."
  exit 1
fi

# Check for duplicates
dupes=$(sort requirements.txt | uniq -d)
if [ ! -z "$dupes" ]; then
  echo "❌ Duplicate packages found:"
  echo "$dupes"
  exit 1
fi

# Check for bad formatting (lines that don't match typical package==version or package format)
bad_lines=$(grep -vE '^([a-zA-Z0-9_-]+([<>=!]=[a-zA-Z0-9_.-]+)?)(\s*#.*)?$' requirements.txt)
if [ ! -z "$bad_lines" ]; then
  echo "❌ Invalid lines in requirements.txt:"
  echo "$bad_lines"
  exit 1
fi

echo "✅ requirements.txt is valid."
