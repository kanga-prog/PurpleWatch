#!/usr/bin/env bash
set -euo pipefail

max_size_bytes=524288
mapfile -t repository_files < <(
  {
    git ls-files
    git ls-files --others --exclude-standard
  } | sort -u
)

for file in "${repository_files[@]}"; do
  [[ "$file" == *.md ]] || continue
  if ! rg -q '^# ' "$file"; then
    echo "Markdown file lacks a level-one heading: $file" >&2
    exit 1
  fi
done

yamllint .github .yamllint.yml

for file in "${repository_files[@]}"; do
  case "$file" in
    .env|*.pem|*.key|*.p12|*.pfx|*.db|*.sqlite|*.sqlite3|*.vmdk|*.vdi|*.vhd|*.vhdx|*.ova|*.ovf|*.iso|*.qcow2|*.vmem|*.pcap|*.pcapng|*.dmp|*.exe|*.dll|*.msi|*.bin|*.elf|*.zip|*.7z|*.rar)
      echo "Forbidden tracked file: $file" >&2
      exit 1
      ;;
  esac
  size=$(wc -c < "$file")
  if (( size > max_size_bytes )); then
    echo "Tracked file exceeds ${max_size_bytes} bytes: $file" >&2
    exit 1
  fi
done
